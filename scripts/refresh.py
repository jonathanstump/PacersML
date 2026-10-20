"""Incremental data refresh: game lists → per-game fetch (cached) → stints → validation → per-100 tables.

    python scripts/refresh.py                                   # all three seasons, all season types
    python scripts/refresh.py --seasons 2025-26 --game-ids 0022500001 --no-write   # one-game smoke test

Every run starts with the access probe (D10) and stops before fetching anything if a required endpoint fails.

A host that stops answering mid-run gets a 5-minute pause and a re-probe (up to 3 times) before the run stops (D11).

Exit codes: 0 ok · 2 quarantine alarm (> 1% of a season's games, D3)
            3 preflight failed, or a host stayed down after pausing (nothing written for that season)
            4 team-season possession cross-check > 2% (D1)
Processed outputs for a season are not overwritten when that season trips 2 or 4.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import pandas as pd  # noqa: E402

from pacersml.data import cache  # noqa: E402
from pacersml.data.http import Client, EndpointBlocked  # noqa: E402
from pacersml.data.per100 import season_per100  # noqa: E402
from pacersml.data.pipeline import PACERS, UNAVAILABLE, game_list, load_game, process_game  # noqa: E402
from pacersml.data.sources import stats_nba  # noqa: E402
from pacersml.data.validate import (QUARANTINE_ALARM, gap_direction, plot_season,  # noqa: E402
                                    player_poss_check, team_poss_check)

SEASONS = ["2024-25", "2025-26", "2026-27"]
TRAINING_SEASONS = {"2024-25", "2025-26"}  # frozen after first complete, clean pull
SEASON_TYPES = ["regular", "play_in", "playoffs"]


def nba_reference(c: Client, season: str, st: str) -> dict:
    """NBA's own season tables for cross-checks; empty dict entries if stats.nba.com is blocked."""
    out = {}
    for key, fn in (("team_adv", lambda: stats_nba.dash_team_advanced(c, season, st)),
                    ("player_adv", lambda: stats_nba.dash_players(c, season, st, "Advanced", "Totals")),
                    ("player_per100", lambda: stats_nba.dash_players(c, season, st, "Base", "Per100Possessions"))):
        try:
            out[key] = fn()
        except UNAVAILABLE:
            out[key] = None
    return out


HOST_PAUSE_S = 300   # D11: a host failing a whole call means pause, re-probe, then continue or stop
MAX_HOST_PAUSES = 3


class RunStopped(RuntimeError):
    """A host stayed down after pausing and re-probing; the run stops instead of cascading through games."""


def fetch_game(c: Client, season: str, gid: str, source: str, status: dict):
    """load_game with recovery. Host down -> wait HOST_PAUSE_S, re-run the preflight probe, clear and retry;
    still down (or too many pauses) -> RunStopped. Hosts up but this game's data unavailable -> None."""
    while True:
        try:
            return load_game(c, season, gid, source)
        except UNAVAILABLE as e:
            if not c.blocked_hosts:
                print(f"  {gid}: unavailable ({e})")
                return None
            status["host_pauses"] = status.get("host_pauses", 0) + 1
            if status["host_pauses"] > MAX_HOST_PAUSES:
                raise RunStopped(f"{sorted(c.blocked_hosts)} down again after {MAX_HOST_PAUSES} pauses ({e})")
            print(f"  {gid}: {sorted(c.blocked_hosts)} not answering ({e}); pausing {HOST_PAUSE_S}s, then re-probing")
            time.sleep(HOST_PAUSE_S)
            if not preflight(status):
                raise RunStopped(f"{sorted(c.blocked_hosts)} still down after a {HOST_PAUSE_S}s pause")
            c.blocked_hosts.clear()


def run_season(c: Client, season: str, args, status: dict) -> int:
    games, notes = game_list(c, season, args.season_types, args.source)
    status["notes"] += notes
    if args.game_ids:
        games = games[games.game_id.isin(args.game_ids)]
    if args.limit:
        games = games.head(args.limit)
    print(f"\n=== {season}: {len(games)} final games ===")

    results, missing = {}, []
    t0 = time.monotonic()
    for i, g in enumerate(games.itertuples(index=False)):
        g = pd.Series(g._asdict())
        data = fetch_game(c, season, g.game_id, args.source, status)
        if data is None:
            missing.append(g.game_id)
            continue
        results[g.game_id] = (g, data, process_game(g, data))
        if (i + 1) % 50 == 0:
            print(f"  {i + 1}/{len(games)} games ({time.monotonic() - t0:.0f}s)")

    # Second pass (D11): gamerotation fails intermittently per game, so retry it for the games that missed it.
    retry = [gid for gid, (_, data, _) in results.items() if data.rotation is None]
    if retry and args.source in ("auto", "stats"):
        print(f"  second pass: retrying rotation for {len(retry)} games")
        c.cooling_until.clear()
        for gid in retry:
            g = results[gid][0]
            data = fetch_game(c, season, gid, args.source, status)
            if data is not None and data.rotation is not None:
                results[gid] = (g, data, process_game(g, data))

    no_rotation = [{"game_id": gid, "season": season, "season_type": g.season_type,
                    "pacers_game": PACERS in (g.home_team_id, g.away_team_id)}
                   for gid, (g, data, _) in results.items() if data.rotation is None]
    timing = pd.DataFrame([r.sub_timing for _, _, r in results.values()])
    results = [r for _, _, r in results.values()]
    if missing:
        print(f"  {len(missing)} games could not be loaded (hosts up, game data unavailable): {missing[:10]}")

    if not results:
        status["seasons"][season] = {"games": int(len(games)), "processed": 0, "missing": len(missing)}
        return 0

    stints = pd.concat([r.stints for r in results], ignore_index=True)
    pg = pd.concat([r.player_game for r in results], ignore_index=True)
    checks = pd.concat([r.checks for r in results], ignore_index=True)
    quarantine = pd.DataFrame([r.quarantine for r in results if r.quarantine])
    q_ids = set(quarantine.game_id) if not quarantine.empty else set()
    clean_stints = stints[~stints.game_id.isin(q_ids)]
    clean_pg = pg[~pg.game_id.isin(q_ids)]

    per100 = season_per100(clean_pg)
    # season-level checks compare against NBA's full-season totals; only enforce them on full seasons
    partial = bool(args.game_ids or args.limit)
    team_tbls, player_tbls, ref_tables, code = [], [], {}, 0
    for st in sorted(clean_stints.season_type.unique()):
        ref = nba_reference(c, season, st)
        ref_tables[st] = ref
        tt, failed = team_poss_check(clean_stints[clean_stints.season_type == st],
                                     games[games.season_type == st], ref["team_adv"])
        team_tbls.append(tt.assign(season_type=st))
        player_tbls.append(player_poss_check(per100[per100.season_type == st], ref["player_adv"]).assign(season_type=st))
        if failed and partial:
            print("  (partial season: team-season possession check not enforced)")
        elif failed:
            code = 4
            print(f"  !! {st}: team-season possession gap > 2% for "
                  f"{int(tt.over_tol.sum())} team(s) — treated as a parser bug (D1)")
    # every game can be quarantined (e.g. a one-game smoke test): keep the tables, just empty
    team_tbl = (pd.concat(team_tbls, ignore_index=True) if team_tbls
                else pd.DataFrame(columns=["team_id", "poss_ours", "games", "poss_nba", "gap_pct", "over_tol"]))
    player_tbl = (pd.concat(player_tbls, ignore_index=True) if player_tbls
                  else pd.DataFrame(columns=["person_id", "gap_pct_avg", "flag_avg"]))
    direction = pd.concat([gap_direction(t).assign(season_type=t.season_type.iloc[0])
                           for t in player_tbls if not t.empty] or [gap_direction(player_tbl)], ignore_index=True)
    for r in direction[direction.share_over.notna()].itertuples():
        if partial:
            break
        print(f"  player poss gaps {r.season_type} {r.measure}: over {r.over} / under {r.under} / equal {r.equal}"
              f" (share over {r.share_over:.0%}){'  -> outside 40/60, investigate (D7)' if r.investigate else ''}")
    n_flag = int(player_tbl.get("flag_avg", pd.Series(dtype=bool)).fillna(False).sum())

    rate = len(q_ids) / len(results)
    if rate > QUARANTINE_ALARM and not partial:
        code = 2
        print(f"  !! quarantine alarm: {len(q_ids)}/{len(results)} games ({rate:.1%}) > {QUARANTINE_ALARM:.0%} (D3)")

    n_rebuilt = int(checks[checks.method == "pbp_rebuild"].game_id.nunique())
    no_rot = pd.DataFrame(no_rotation, columns=["game_id", "season", "season_type", "pacers_game"])
    n_unmatched = int((timing.rotation_unmatched.fillna(0) > 0).sum()) if not timing.empty else 0
    summary = {"games": int(len(games)), "processed": len(results), "missing": len(missing),
               "quarantined": len(q_ids), "quarantine_rate": round(rate, 4), "pbp_rebuild_used": n_rebuilt,
               "rotation_unavailable": len(no_rot),
               "games_with_rotation_unmatched": n_unmatched,
               "rotation_unmatched_total": int(timing.rotation_unmatched.fillna(0).sum()) if not timing.empty else 0,
               "pbp_subs_off_total": int(timing.pbp_subs_off.fillna(0).sum()) if not timing.empty else 0,
               "player_poss_flagged": n_flag,
               "player_gap_direction": json.loads(direction.to_json(orient="records")),
               "stints": int(len(clean_stints)), "exit_code": code,
               "nba_reference": {st: {k: v is not None for k, v in r.items()} for st, r in ref_tables.items()}}
    status["seasons"][season] = summary
    print(f"  processed {len(results)} · missing {len(missing)} · rotation unavailable {len(no_rot)} · "
          f"PBP rebuild used {n_rebuilt} · quarantined {len(q_ids)} ({rate:.2%})")
    print(f"  sub timing vs rotation file: {n_unmatched} games with unmatched rotation changes "
          f"({summary['rotation_unmatched_total']} changes), {summary['pbp_subs_off_total']} PBP subs off by > 2 s")
    pacers_q = quarantine[quarantine.pacers_game] if not quarantine.empty else quarantine
    if not pacers_q.empty:
        print("\n  *** PACERS GAMES QUARANTINED — manual review needed (D3) ***")
        for r in pacers_q.itertuples():
            print(f"  *** {r.game_id} {r.season_type}: {r.failed_checks} [{r.residuals}]")

    out = cache.PROCESSED / season
    out.mkdir(parents=True, exist_ok=True)
    checks.to_parquet(out / "validation.parquet", index=False)
    quarantine.to_parquet(out / "quarantine.parquet", index=False)
    no_rot.to_parquet(out / "rotation_unavailable.parquet", index=False)
    timing.to_parquet(out / "sub_timing.parquet", index=False)
    plot_season(season, checks, team_tbl, player_tbl, ROOT / "reports" / "validation")
    direction.to_csv(ROOT / "reports" / "validation" / f"{season}_player_poss_gap_direction.csv", index=False)
    if args.no_write or code in (2, 4):
        print("  processed outputs NOT written" + (" (--no-write)" if args.no_write else f" (exit {code})"))
        return code

    clean_stints.to_parquet(out / "stints.parquet", index=False)
    clean_pg.to_parquet(out / "player_game.parquet", index=False)
    per100.to_parquet(out / "player_season_per100.parquet", index=False)
    team_tbl.to_parquet(out / "team_poss_check.parquet", index=False)
    player_tbl.to_parquet(out / "player_poss_check.parquet", index=False)
    for st, ref in ref_tables.items():
        for k, df in ref.items():
            if df is not None:
                df.to_parquet(out / f"nba_{k}_{st}.parquet", index=False)

    if season in TRAINING_SEASONS and not missing and not args.game_ids and not args.limit:
        m = cache.load_manifest()
        m["seasons"][season] = {
            "frozen": True, "frozen_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "games": len(results), "quarantined": len(q_ids),
            "rows": {"stints": len(clean_stints), "player_game": len(clean_pg), "per100": len(per100)},
            "hash": {"stints": cache.frame_hash(clean_stints.drop(columns=["home_ids", "away_ids"])),
                     "player_game": cache.frame_hash(clean_pg)},
        }
        cache.save_manifest(m)
        print(f"  {season} frozen in data/manifest.json")
    return code


def export_quarantine():
    """Quarantine list plus, per season, how many games had no rotation data (fell back to the PBP rebuild) and
    how often PBP substitutions disagreed with the rotation file's timing, for the site's Methods page (D10, D11)."""
    def gather(name):
        parts = [pd.read_parquet(p) for p in sorted(cache.PROCESSED.glob(f"*/{name}.parquet"))]
        parts = [p for p in parts if not p.empty]
        return pd.concat(parts, ignore_index=True) if parts else pd.DataFrame()

    q, no_rot, timing = gather("quarantine"), gather("rotation_unavailable"), gather("sub_timing")
    cache.PROCESSED.mkdir(parents=True, exist_ok=True)
    q.to_parquet(cache.PROCESSED / "quarantine.parquet", index=False)
    site = ROOT / "site_export"
    site.mkdir(exist_ok=True)
    (site / "quarantine.json").write_text(json.dumps({
        "generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "rotation_unavailable_games": (no_rot.groupby("season").size().to_dict() if not no_rot.empty else {}),
        # D11: PBP subs vs the rotation file's timing; unmatched rotation changes usually mean a sub missing from PBP
        "sub_timing_disagreements": ({
            season: {"games_with_unmatched": int((t.rotation_unmatched.fillna(0) > 0).sum()),
                     "rotation_unmatched": int(t.rotation_unmatched.fillna(0).sum()),
                     "pbp_subs_off": int(t.pbp_subs_off.fillna(0).sum())}
            for season, t in timing.groupby("season")} if not timing.empty else {}),
        "games": json.loads(q.to_json(orient="records")) if not q.empty else []}, indent=2))


def preflight(status: dict) -> bool:
    """Run the access probe; False (with a clear message) if any endpoint the refresh needs is failing."""
    import probe_endpoints  # scripts/ is on sys.path when this file runs
    report = probe_endpoints.run("refresh-preflight")
    status["preflight"] = {"network": report["network"], "failed_required": report["failed_required"]}
    if report["failed_required"]:
        print("\n" + "!" * 78)
        print(f"PREFLIGHT FAILED: {', '.join(report['failed_required'])} not answering from {report['network']}.")
        print("Nothing was fetched or written. If the probe shows 403s or timeouts on every NBA endpoint, NBA has")
        print("probably changed what it checks: compare the headers in src/pacersml/data/http.py with a real")
        print("browser request to nba.com before retrying.")
        print("!" * 78)
        return False
    rot = next(r for r in report["results"] if r["endpoint"] == "gamerotation")
    if rot["result"] != "ok":
        print(f"\n  note: gamerotation not answering ({rot['status'] or rot['error']}); games will use the PBP rebuild")
    return True


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seasons", nargs="+", default=SEASONS)
    ap.add_argument("--season-types", nargs="+", default=SEASON_TYPES, choices=SEASON_TYPES)
    ap.add_argument("--source", default="auto", choices=["auto", "stats", "cdn"])
    ap.add_argument("--game-ids", nargs="*")
    ap.add_argument("--limit", type=int)
    ap.add_argument("--force", action="store_true", help="re-process a frozen training season")
    ap.add_argument("--no-write", action="store_true", help="validate only; don't write processed tables")
    ap.add_argument("--skip-preflight", action="store_true", help="skip the access probe (tests / debugging only)")
    args = ap.parse_args()

    c = Client()
    status = {"started_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"), "seasons": {}, "notes": []}
    codes = []
    if not args.skip_preflight and not preflight(status):
        codes.append(3)
        args.seasons = []
    for season in args.seasons:
        if cache.is_frozen(season) and not args.force:
            print(f"\n=== {season}: frozen (see data/manifest.json), skipped ===")
            continue
        try:
            codes.append(run_season(c, season, args, status))
        except (EndpointBlocked, RunStopped) as e:
            print(f"\n=== {season}: stopped, nothing written for this season: {e}")
            status["seasons"][season] = {"error": str(e)}
            codes.append(3)
            break  # later seasons would hit the same wall
    export_quarantine()
    code = max(codes, default=0)
    status.update(finished_utc=datetime.now(timezone.utc).isoformat(timespec="seconds"), exit_code=code,
                  blocked_hosts=sorted(c.blocked_hosts))
    cache.DATA.mkdir(exist_ok=True)
    (cache.DATA / "status.json").write_text(json.dumps(status, indent=2))
    print(f"\nexit {code} · status in data/status.json")
    return code


if __name__ == "__main__":
    sys.exit(main())
