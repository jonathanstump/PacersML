"""Per-game fetch (with source fallback and caching) and processing (stints → validation → rebuild → quarantine)."""
from __future__ import annotations

from dataclasses import dataclass, field

import pandas as pd

from pacersml.data import cache, normalize
from pacersml.data.http import Client, EndpointBlocked, EndpointError
from pacersml.data.per100 import player_game
from pacersml.data.sources import cdn_nba, pbpstats, stats_nba
from pacersml.data.stints import from_pbp, from_rotation, player_stints
from pacersml.data.validate import LINEUP_CHECKS, check_game, hard_failures

PACERS = 1610612754
SEASON_TYPE_BY_PREFIX = {"002": "regular", "004": "playoffs", "005": "play_in"}
UNAVAILABLE = (EndpointBlocked, EndpointError, FileNotFoundError)


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


def load_game(c: Client, season: str, gid: str, source: str) -> GameData:
    """Raw payloads (cached or fetched), normalized here. Raises EndpointBlocked if no box or PBP source answers."""
    box_hit = _payload(c, season, gid, source, BOX_FETCHERS)
    if box_hit is None:
        raise EndpointBlocked(f"{gid}: no box score source")
    box = normalize.box(box_hit[1], gid)

    pbp_hit = _payload(c, season, gid, source, PBP_FETCHERS)
    if pbp_hit is None:
        raise EndpointBlocked(f"{gid}: no play-by-play source")
    if pbp_hit[0] == "stats_pbp":
        ev = normalize.events_v3(pbp_hit[1], gid, box)
    else:
        ev = normalize.merge_live_subs(normalize.events_live(pbp_hit[1], gid))

    rot_hit = _payload(c, season, gid, source, ROTATION_FETCHERS)
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
    rebuild_info: dict


def process_game(g: pd.Series, data: GameData) -> GameResult:
    gid, home, away = g.game_id, int(g.home_team_id), int(g.away_team_id)
    pb = {}
    if pd.notna(g.get("pbpstats_home_poss")):
        pb = {int(g.pbpstats_home_id): int(g.pbpstats_home_poss), int(g.pbpstats_away_id): int(g.pbpstats_away_poss)}

    rebuild_attempted, info, first_fail = False, {}, set()
    if data.rotation is not None and not data.rotation.empty:
        stints, ev, info = from_rotation(data.events, data.rotation, home, away, gid)
        checks = check_game(stints, ev, data.box, home, away, pb).assign(method="rotation")
        first_fail = hard_failures(checks)
        if first_fail & LINEUP_CHECKS:
            rebuild_attempted = True
            s2, ev2, info = from_pbp(data.events, data.box, home, away, gid)
            c2 = check_game(s2, ev2, data.box, home, away, pb).assign(method="pbp_rebuild")
            checks = pd.concat([checks, c2], ignore_index=True)
            stints, ev = s2, ev2
            final = c2
        else:
            final = checks
    else:
        stints, ev, info = from_pbp(data.events, data.box, home, away, gid)
        final = checks = check_game(stints, ev, data.box, home, away, pb).assign(method="pbp_rebuild")

    failed = hard_failures(final)
    q = None
    if failed:
        worst = final[final.check.isin(failed)]
        q = {"game_id": gid, "season": g.season, "season_type": g.season_type,
             "failed_checks": ",".join(sorted(failed)),
             "residuals": ";".join(f"{r.check}={r.residual:g}" for r in worst.itertuples()),
             "first_method": "rotation" if data.rotation is not None else "pbp_rebuild",
             "first_failed": ",".join(sorted(first_fail)),
             "rebuild_attempted": rebuild_attempted,
             "rebuild_result": ("failed" if rebuild_attempted else "not_attempted"),
             "pacers_game": PACERS in (home, away),
             "inferred_starters": str({f"P{p}:{t}": v for (p, t), v in info.items()}) if info else ""}

    stints = stints.assign(season=g.season, season_type=g.season_type)
    pg = player_game(data.box, player_stints(stints, home, away), ev).assign(season=g.season,
                                                                              season_type=g.season_type)
    checks = checks.assign(season=g.season, season_type=g.season_type)
    return GameResult(stints, pg, checks, q, info)
