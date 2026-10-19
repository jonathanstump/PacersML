"""Per-game fetch (with source fallback and caching) and processing (stints → validation → rebuild → quarantine)."""
from __future__ import annotations

from dataclasses import dataclass, field

import pandas as pd

from pacersml.data import cache, normalize
from pacersml.data.http import Client, EndpointBlocked
from pacersml.data.per100 import player_game
from pacersml.data.sources import cdn_nba, pbpstats, stats_nba
from pacersml.data.stints import from_pbp, from_rotation, player_stints
from pacersml.data.validate import LINEUP_CHECKS, check_game, hard_failures

PACERS = 1610612754
SEASON_TYPE_BY_PREFIX = {"002": "regular", "004": "playoffs", "005": "play_in"}
UNAVAILABLE = (EndpointBlocked, FileNotFoundError)


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
            g = g.merge(pb[["game_id", "pbpstats_home_poss", "pbpstats_away_poss"]], on="game_id", how="left")
        frames.append(g.assign(season=season, season_type=st))
    games = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()
    if not games.empty:
        games = games[games.game_id.str[:3].isin(SEASON_TYPE_BY_PREFIX)]  # drops the Cup final (006)
        games["home_team_id"] = games.home_team_id.astype("int64")
        games["away_team_id"] = games.away_team_id.astype("int64")
    return games.reset_index(drop=True), notes


# ---------------------------------------------------------------- per-game fetch

def load_game(c: Client, season: str, gid: str, source: str) -> GameData:
    """Cached normalized frames if present, else fetch. Raises EndpointBlocked if no source answers."""
    srcs = {}
    if cache.has_raw(season, "box", gid):
        box = cache.read_raw(season, "box", gid)
    else:
        box = None
        if source in ("auto", "stats"):
            try:
                box, srcs["box"] = normalize.box(stats_nba.box_v3(c, gid), gid), "stats"
            except UNAVAILABLE:
                pass
        if box is None and source in ("auto", "cdn"):
            box, srcs["box"] = normalize.box(cdn_nba.box_live(c, gid), gid), "cdn"
        if box is None:
            raise EndpointBlocked(f"{gid}: no box score source")
        cache.write_raw(box, season, "box", gid)

    if cache.has_raw(season, "events", gid):
        ev = cache.read_raw(season, "events", gid)
    else:
        ev = None
        if source in ("auto", "stats"):
            try:
                ev, srcs["events"] = normalize.events_v3(stats_nba.pbp_v3(c, gid), gid, box), "stats"
            except UNAVAILABLE:
                pass
        if ev is None and source in ("auto", "cdn"):
            ev = normalize.merge_live_subs(normalize.events_live(cdn_nba.pbp_live(c, gid), gid))
            srcs["events"] = "cdn"
        if ev is None:
            raise EndpointBlocked(f"{gid}: no play-by-play source")
        cache.write_raw(ev, season, "events", gid)

    rot = None
    if cache.has_raw(season, "rotation", gid):
        rot = cache.read_raw(season, "rotation", gid)
    elif source in ("auto", "stats"):
        try:
            rot = stats_nba.rotation(c, gid)
            cache.write_raw(rot, season, "rotation", gid)
            srcs["rotation"] = "stats"
        except UNAVAILABLE:
            pass  # not cached: tried again next refresh; this run uses the PBP rebuild
    return GameData(box, ev, rot, srcs)


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
        pb = {home: int(g.pbpstats_home_poss), away: int(g.pbpstats_away_poss)}

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
    pg = player_game(data.box, player_stints(stints, home, away)).assign(season=g.season, season_type=g.season_type)
    checks = checks.assign(season=g.season, season_type=g.season_type)
    return GameResult(stints, pg, checks, q, info)
