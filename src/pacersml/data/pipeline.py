"""Per-game fetch (with source fallback and caching) and processing (stints → validation → quarantine, D11)."""
from __future__ import annotations

from dataclasses import dataclass, field

import pandas as pd

from pacersml.data import cache, normalize
from pacersml.data.http import Client, EndpointBlocked, EndpointError
from pacersml.data.per100 import player_game
from pacersml.data.sources import cdn_nba, pbpstats, stats_nba
from pacersml.data.stints import compare_sub_timing, from_hybrid, from_pbp, player_stints, usable_rotation
from pacersml.data.validate import check_game, failure_group, hard_failures, lineup_ok

PACERS = 1610612754
SEASON_TYPE_BY_PREFIX = {"002": "regular", "004": "playoffs", "005": "play_in"}
UNAVAILABLE = (EndpointBlocked, EndpointError, FileNotFoundError)
REORDER_SUBS = False  # trial of the same-second sub reorder (D8 amendment under test); refresh --reorder-subs


@dataclass
class GameData:
    box: pd.DataFrame
    events: pd.DataFrame
    rotation: pd.DataFrame | None
    sources: dict = field(default_factory=dict)


# ---------------------------------------------------------------- game lists

def game_list(c: Client, season: str, season_types: list[str], source: str) -> tuple[pd.DataFrame, list[str]]:
    """Final games for a season. stats.nba.com game log first, pbpstats.com as fallback; pbpstats possession
    counts are attached whenever pbpstats answers. Returns (games, notes)."""
    frames, notes = [], []
    for st in season_types:
        g = None
        if source in ("auto", "stats"):
            try:
                g = stats_nba.game_log(c, season, st)
            except UNAVAILABLE as e:
                notes.append(f"game_log {season} {st}: stats.nba.com unavailable ({e})")
        try:
            pb = pbpstats.games(c, season, st)
        except UNAVAILABLE as e:
            pb = None
            notes.append(f"game_list {season} {st}: pbpstats.com unavailable ({e})")
        if g is None:
            if pb is None:
                raise EndpointBlocked(f"no game list source answered for {season} {st}")
            g = pb[["game_id", "game_date", "home_team_id", "away_team_id"]]
        if pb is not None and not pb.empty:
            # keyed by pbpstats' own team ids: its home/away can differ from ours at neutral sites
            pb = pb.rename(columns={"home_team_id": "pbpstats_home_id", "away_team_id": "pbpstats_away_id"})
            g = g.merge(pb[["game_id", "pbpstats_home_id", "pbpstats_away_id", "pbpstats_home_poss",
                            "pbpstats_away_poss"]], on="game_id", how="left")
        frames.append(g.assign(season=season, season_type=st))
    games = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()
    if not games.empty:
        games = games[games.game_id.str[:3].isin(SEASON_TYPE_BY_PREFIX)]  # drops the Cup final (006)
        games["home_team_id"] = games.home_team_id.astype("int64")
        games["away_team_id"] = games.away_team_id.astype("int64")
    return games.reset_index(drop=True), notes


# ---------------------------------------------------------------- per-game fetch

BOX_FETCHERS = [("stats_box", stats_nba.box_v3), ("cdn_box", cdn_nba.box_live)]
# liveData first: it is the only PBP format that records who drew each foul (D6). v3 is the fallback.
PBP_FETCHERS = [("cdn_pbp", cdn_nba.pbp_live), ("stats_pbp", stats_nba.pbp_v3)]
ROTATION_FETCHERS = [("stats_rotation", stats_nba.rotation)]


def _payload(c: Client, season: str, gid: str, source: str, fetchers) -> tuple[str, dict] | None:
    """Cached raw payload if any allowed source has one, else fetch from the first allowed source that answers."""
    allowed = [(k, fn) for k, fn in fetchers if source == "auto" or k.startswith(source)]
    for key, fn in allowed:  # in preference order: a cached preferred source, else fetch it, else the next one
        hit = cache.find_raw(season, [key], gid)
        if hit:
            return hit
        try:
            payload = fn(c, gid)
        except UNAVAILABLE:
            continue
        cache.write_raw(payload, season, key, gid)
        return key, payload
    return None


def game_end_utc(pbp_hit: tuple[str, dict]):
    """When the game ended per the play-by-play: a UTC Timestamp (liveData's game-end action), NaT when the
    payload is complete but carries no end time, None when the game isn't over in this payload."""
    key, payload = pbp_hit
    actions = payload.get("game", {}).get("actions", [])
    if key == "cdn_pbp":
        ends = [a for a in actions if a.get("actionType") == "game" and a.get("subType") == "end"]
        if not ends:
            return None
        t = pd.to_datetime(ends[-1].get("timeActual"), utc=True, errors="coerce")
        return t
    # playbyplayv3 has no game-end action: complete when a period of regulation or later has ended
    done = any(str(a.get("actionType", "")).lower() == "period" and str(a.get("subType", "")).lower() == "end"
               and int(a.get("period") or 0) >= 4 for a in actions)
    return pd.NaT if done else None


def load_game(c: Client, season: str, gid: str, source: str, fetch_rotation: bool = True) -> GameData:
    """Raw payloads (cached or fetched), normalized here. Raises EndpointBlocked if no box or PBP source answers.
    fetch_rotation=False: use a cached rotation file if there is one, never request it."""
    box_hit = _payload(c, season, gid, source, BOX_FETCHERS)
    if box_hit is None:
        raise EndpointBlocked(f"{gid}: no box score source")
    box = normalize.box(box_hit[1], gid)
    if box.empty:  # NBA answered before the box was filled in (2026-27: 7 such games cached); don't keep it
        cache.raw_path(season, box_hit[0], gid).unlink(missing_ok=True)
        raise EndpointError(f"{gid}: empty box score (cached copy removed, fetched again next run)")

    pbp_hit = _payload(c, season, gid, source, PBP_FETCHERS)
    if pbp_hit is None:
        raise EndpointBlocked(f"{gid}: no play-by-play source")
    # Payloads fetched while a game was still on are incomplete and would stay cached forever (2026-27: 6 PBP
    # files cached at 02:11 UTC mid-game, quarantined on team points). Drop them; they're fetched again next run.
    end = game_end_utc(pbp_hit)
    if end is None:  # one fresh fetch now; still no game end -> missing this run
        cache.raw_path(season, pbp_hit[0], gid).unlink(missing_ok=True)
        pbp_hit = _payload(c, season, gid, source, PBP_FETCHERS)
        end = game_end_utc(pbp_hit) if pbp_hit else None
        if end is None:
            if pbp_hit:
                cache.raw_path(season, pbp_hit[0], gid).unlink(missing_ok=True)
            raise EndpointError(f"{gid}: play-by-play has no game end (not cached, fetched again next run)")
    box_file = cache.raw_path(season, box_hit[0], gid)
    if end is not pd.NaT and box_file.exists() and pd.Timestamp(box_file.stat().st_mtime, unit="s", tz="UTC") < end:
        box_file.unlink()
        box_hit = _payload(c, season, gid, source, BOX_FETCHERS)
        if box_hit is None:
            raise EndpointError(f"{gid}: box score cached before the game ended (removed, fetched again next run)")
        box = normalize.box(box_hit[1], gid)
    if pbp_hit[0] == "stats_pbp":
        ev = normalize.events_v3(pbp_hit[1], gid, box)
    else:
        ev = normalize.merge_live_subs(normalize.events_live(pbp_hit[1], gid))

    rot_hit = (_payload(c, season, gid, source, ROTATION_FETCHERS) if fetch_rotation
               else cache.find_raw(season, [k for k, _ in ROTATION_FETCHERS], gid))
    rot = stats_nba.rotation_frame(rot_hit[1], gid) if rot_hit else None
    srcs = {"box": box_hit[0], "events": pbp_hit[0], "rotation": rot_hit[0] if rot_hit else None}
    return GameData(box, ev.assign(pbp_source=pbp_hit[0]), rot, srcs)


# ---------------------------------------------------------------- per-game processing

@dataclass
class GameResult:
    stints: pd.DataFrame
    player_game: pd.DataFrame
    checks: pd.DataFrame
    quarantine: dict | None
    starters_info: dict
    sub_timing: dict
    kept_note: dict | None = None  # passed with noted checks (D14): kept, listed in the report
    outcome: dict | None = None    # one row for the regression baseline and the hybrid-bug alarm (D15)


def process_game(g: pd.Series, data: GameData) -> GameResult:
    """Hybrid stints when the rotation file gives five starters per team in every period, otherwise the pure
    PBP rebuild; quarantine if any hard check fails (D11). No second attempt with the other builder."""
    gid, home, away = g.game_id, int(g.home_team_id), int(g.away_team_id)
    pb = {}
    if pd.notna(g.get("pbpstats_home_poss")):
        pb = {int(g.pbpstats_home_id): int(g.pbpstats_home_poss), int(g.pbpstats_away_id): int(g.pbpstats_away_poss)}

    events, n_moved = data.events, 0
    if REORDER_SUBS:
        events, n_moved = normalize.reorder_same_second_subs(events)
    data = GameData(data.box, events, data.rotation, data.sources)
    periods = sorted(data.events.period.unique())
    rotation_ok = usable_rotation(data.rotation, periods, home, away)
    if rotation_ok:
        stints, ev, info = from_hybrid(data.events, data.rotation, home, away, gid)
    else:
        stints, ev, info = from_pbp(data.events, data.box, home, away, gid)
    method = stints.stint_method.iloc[0]
    checks = check_game(stints, ev, data.box, home, away, pb).assign(method=method)
    # Shadow rebuild on every hybrid game (D15): the two builders disagreeing on the lineup checks is the
    # cleanest sign of a bug in the hybrid. Its stints are not kept.
    shadow_ok = None
    if rotation_ok:
        sh_stints, sh_ev, _ = from_pbp(data.events, data.box, home, away, gid)
        shadow_ok = lineup_ok(check_game(sh_stints, sh_ev, data.box, home, away, pb))

    timing = {"pbp_subs": None, "pbp_subs_off": None, "rotation_changes": None, "rotation_unmatched": None,
              "rotation_unmatched_detail": ""}
    if data.rotation is not None and not data.rotation.empty:
        timing = compare_sub_timing(ev, data.rotation)
    timing = {"game_id": gid, "season": g.season, "season_type": g.season_type, "stint_method": method,
              "rotation_available": data.rotation is not None and not data.rotation.empty,
              "rotation_usable": rotation_ok, **timing}

    failed = hard_failures(checks)
    q = None
    if failed:
        worst = checks[checks.check.isin(failed)]
        q = {"game_id": gid, "season": g.season, "season_type": g.season_type,
             "failed_checks": ",".join(sorted(failed)), "group": failure_group(failed),
             "residuals": ";".join(f"{r.check}={r.residual:g}" for r in worst.itertuples()),
             "stint_method": method,
             "rebuild_attempted": method == "pbp_rebuild",
             "rotation_available": timing["rotation_available"],
             "rotation_unmatched": timing["rotation_unmatched"],
             "pbp_subs_off": timing["pbp_subs_off"],
             "pacers_game": PACERS in (home, away),
             "shadow_rebuild_lineup_ok": shadow_ok,
             "starters": str({f"P{p}:{t}": v for (p, t), v in info.items()}) if info else ""}

    kept = None
    noted = checks[checks.noted & checks.passed]
    if q is None and not noted.empty:
        kept = {"game_id": gid, "season": g.season, "season_type": g.season_type, "stint_method": method,
                "pacers_game": PACERS in (home, away), "checks": ",".join(noted.check),
                "detail": " | ".join(f"{r.check}: {r.detail}" for r in noted.itertuples())}

    stints = stints.assign(season=g.season, season_type=g.season_type)
    pg = player_game(data.box, player_stints(stints, home, away), ev).assign(season=g.season,
                                                                              season_type=g.season_type)
    checks = checks.assign(season=g.season, season_type=g.season_type)
    outcome = {"game_id": gid, "season": g.season, "season_type": g.season_type, "stint_method": method,
               "outcome": "quarantined" if q else ("kept_with_notes" if kept else "pass"),
               "group": q["group"] if q else "", "lineup_ok": lineup_ok(checks), "shadow_rebuild_lineup_ok": shadow_ok,
               # D15 hybrid alarm: the rebuild gets the lineups right and the hybrid doesn't
               "hybrid_bug": bool(method == "hybrid" and shadow_ok and not lineup_ok(checks)),
               "subs_reordered": n_moved}
    return GameResult(stints, pg, checks, q, info, timing, kept, outcome)
