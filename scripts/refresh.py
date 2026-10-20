"""Incremental data refresh: game lists → per-game fetch (cached) → stints → validation → per-100 tables.

    python scripts/refresh.py                                   # all three seasons, all season types
    python scripts/refresh.py --seasons 2025-26 --game-ids 0022500001 --no-write   # one-game smoke test

Exit codes: 0 ok · 2 quarantine alarm (> 1% of a season's games, D3) · 3 every source blocked
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


def run_season(c: Client, season: str, args, status: dict) -> int:
    games, notes = game_list(c, season, args.season_types, args.source)
    status["notes"] += notes
    if args.game_ids:
        games = games[games.game_id.isin(args.game_ids)]
    if args.limit:
        games = games.head(args.limit)
    print(f"\n=== {season}: {len(games)} final games ===")

    results, blocked = [], []
    t0 = time.monotonic()
    for i, g in enumerate(games.itertuples(index=False)):
        g = pd.Series(g._asdict())
        try:
            data = load_game(c, season, g.game_id, args.source)
        except UNAVAILABLE as e:
            blocked.append(g.game_id)
            print(f"  {g.game_id}: blocked ({e})")
            continue
        results.append(process_game(g, data))
        if (i + 1) % 50 == 0:
            print(f"  {i + 1}/{len(games)} games ({time.monotonic() - t0:.0f}s)")

    if not results:
        status["seasons"][season] = {"games": int(len(games)), "processed": 0, "blocked": len(blocked)}
        return 3 if blocked else 0

    stints = pd.concat([r.stints for r in results], ignore_index=True)
    pg = pd.concat([r.player_game for r in results], ignore_index=True)
    checks = pd.concat([r.checks for r in results], ignore_index=True)
    quarantine = pd.DataFrame([r.quarantine for r in results if r.quarantine])
    q_ids = set(quarantine.game_id) if not quarantine.empty else set()
    clean_stints = stints[~stints.game_id.isin(q_ids)]
    clean_pg = pg[~pg.game_id.isin(q_ids)]

    per100 = season_per100(clean_pg)
    team_tbls, player_tbls, ref_tables, code = [], [], {}, 0
    for st in sorted(clean_stints.season_type.unique()):
        ref = nba_reference(c, season, st)
        ref_tables[st] = ref
        tt, failed = team_poss_check(clean_stints[clean_stints.season_type == st],
                                     games[games.season_type == st], ref["team_adv"])
        team_tbls.append(tt.assign(season_type=st))
        player_tbls.append(player_poss_check(per100[per100.season_type == st], ref["player_adv"]).assign(season_type=st))
        if failed:
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
        print(f"  player poss gaps {r.season_type} {r.measure}: over {r.over} / under {r.under} / equal {r.equal}"
              f" (share over {r.share_over:.0%}){'  -> outside 40/60, investigate (D7)' if r.investigate else ''}")
    n_flag = int(player_tbl.get("flag_avg", pd.Series(dtype=bool)).fillna(False).sum())

    rate = len(q_ids) / len(results)
    if rate > QUARANTINE_ALARM:
        code = 2
        print(f"  !! quarantine alarm: {len(q_ids)}/{len(results)} games ({rate:.1%}) > {QUARANTINE_ALARM:.0%} (D3)")

    n_rebuilt = int(checks[checks.method == "pbp_rebuild"].game_id.nunique())
    summary = {"games": int(len(games)), "processed": len(results), "blocked": len(blocked),
               "quarantined": len(q_ids), "quarantine_rate": round(rate, 4), "pbp_rebuild_used": n_rebuilt,
               "player_poss_flagged": n_flag,
               "player_gap_direction": json.loads(direction.to_json(orient="records")),
               "stints": int(len(clean_stints)), "exit_code": code,
               "nba_reference": {st: {k: v is not None for k, v in r.items()} for st, r in ref_tables.items()}}
    status["seasons"][season] = summary
    print(f"  processed {len(results)} · blocked {len(blocked)} · PBP rebuild used {n_rebuilt} · "
          f"quarantined {len(q_ids)} ({rate:.2%})")
    pacers_q = quarantine[quarantine.pacers_game] if not quarantine.empty else quarantine
    if not pacers_q.empty:
        print("\n  *** PACERS GAMES QUARANTINED — manual review needed (D3) ***")
        for r in pacers_q.itertuples():
            print(f"  *** {r.game_id} {r.season_type}: {r.failed_checks} [{r.residuals}]")

    out = cache.PROCESSED / season
    out.mkdir(parents=True, exist_ok=True)
    checks.to_parquet(out / "validation.parquet", index=False)
    quarantine.to_parquet(out / "quarantine.parquet", index=False)
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

    if season in TRAINING_SEASONS and not blocked and not args.game_ids and not args.limit:
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
    parts = [pd.read_parquet(p) for p in sorted(cache.PROCESSED.glob("*/quarantine.parquet"))]
    q = pd.concat([p for p in parts if not p.empty], ignore_index=True) if any(not p.empty for p in parts) else pd.DataFrame()
    cache.PROCESSED.mkdir(parents=True, exist_ok=True)
    q.to_parquet(cache.PROCESSED / "quarantine.parquet", index=False)
    site = ROOT / "site_export"
    site.mkdir(exist_ok=True)
    (site / "quarantine.json").write_text(json.dumps({
        "generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "games": json.loads(q.to_json(orient="records")) if not q.empty else []}, indent=2))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seasons", nargs="+", default=SEASONS)
    ap.add_argument("--season-types", nargs="+", default=SEASON_TYPES, choices=SEASON_TYPES)
    ap.add_argument("--source", default="auto", choices=["auto", "stats", "cdn"])
    ap.add_argument("--game-ids", nargs="*")
    ap.add_argument("--limit", type=int)
    ap.add_argument("--force", action="store_true", help="re-process a frozen training season")
    ap.add_argument("--no-write", action="store_true", help="validate only; don't write processed tables")
    args = ap.parse_args()

    c = Client()
    status = {"started_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"), "seasons": {}, "notes": []}
    codes = []
    for season in args.seasons:
        if cache.is_frozen(season) and not args.force:
            print(f"\n=== {season}: frozen (see data/manifest.json), skipped ===")
            continue
        try:
            codes.append(run_season(c, season, args, status))
        except EndpointBlocked as e:
            print(f"\n=== {season}: every source blocked: {e}")
            status["seasons"][season] = {"error": str(e)}
            codes.append(3)
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
