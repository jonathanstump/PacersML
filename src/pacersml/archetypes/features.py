"""Style features per player-season for the archetype model (D25).

Shot detail (zone, descriptor, assister) comes from the cached liveData play-by-play, read again here so the
frozen Phase 1 tables stay unchanged. Counting stats and possessions come from the Phase 1 per-100 table and
stints. Only games kept in Phase 1 (not quarantined) are used, so every feature has the same games as the
per-100 table. Regular season only (D2); traded players are one row, teams combined.
"""
from __future__ import annotations

import gzip
import json

import numpy as np
import pandas as pd

from pacersml.data import cache

TRAINING = ["2024-25", "2025-26"]
FIT_MIN_SECONDS = 500 * 60   # D25: fit on 500+ minutes
LOW_MIN_SECONDS = 100 * 60   # D25: 100-499 projected (low-sample), under 100 gets league shares

ZONES = ["rim", "short_mid", "long_mid", "corner3", "ab3"]
ZONE_LABEL = {"rim": "rim (restricted area)", "short_mid": "short mid (paint, non-RA)", "long_mid": "long mid",
              "corner3": "corner 3", "ab3": "above-break 3"}

# (column, group, label, unit) in display order; long_mid is reported but not fitted (the five shares add to 1)
FEATURES = [
    ("rim_share", "shooting", "rim share of FGA", "pct"),
    ("short_mid_share", "shooting", "short-mid share of FGA", "pct"),
    ("corner3_share", "shooting", "corner-3 share of FGA", "pct"),
    ("ab3_share", "shooting", "above-break-3 share of FGA", "pct"),
    ("pullup3_rate", "shooting", "pull-up/step-back 3PA per FGA", "pct"),
    ("fta_rate", "shooting", "FTA per FGA", "ratio"),
    ("usage_per100", "creation", "shot attempts + TOV per 100", "per100"),
    ("ast_per100", "creation", "AST per 100", "per100"),
    ("assisted_share", "creation", "assisted share of made FG", "pct"),
    ("drive_rate", "creation", "driving FGA per FGA", "pct"),
    ("fouls_drawn_per100", "creation", "fouls drawn per 100", "per100"),
    ("oreb_pct", "rebounding", "OREB%", "pct"),
    ("dreb_pct", "rebounding", "DREB%", "pct"),
    ("stl_per100", "defense", "STL per 100", "per100"),
    ("blk_per100", "defense", "BLK per 100", "per100"),
    ("pf_def_per100", "defense", "defensive fouls per 100", "per100"),
    ("charges_drawn_per100", "defense", "charges drawn per 100", "per100"),
]
FEATURE_COLS = [f[0] for f in FEATURES]


def shot_zone(a: dict) -> str:
    area = a.get("area") or ""
    if a["actionType"] == "3pt":
        return "corner3" if "Corner" in area else "ab3"
    if area == "Restricted Area":
        return "rim"
    if area == "In The Paint (Non-RA)":
        return "short_mid"
    return "long_mid"


def shots_from_pbp(season: str, game_ids: list[str]) -> tuple[pd.DataFrame, dict]:
    """One row per field-goal attempt from liveData play-by-play; also team id -> tricode."""
    rows, tricode = [], {}
    for gid in game_ids:
        hit = cache.find_raw(season, ["cdn_pbp"], gid)
        if hit is None:
            continue
        for a in hit[1]["game"]["actions"]:
            if a.get("teamId") and a.get("teamTricode"):
                tricode[int(a["teamId"])] = a["teamTricode"]
            if a.get("actionType") not in ("2pt", "3pt") or not a.get("personId"):
                continue
            desc = (a.get("descriptor") or "").lower()
            made = a.get("shotResult") == "Made"
            rows.append((gid, int(a["personId"]), shot_zone(a), a["actionType"] == "3pt", made,
                         made and bool(a.get("assistPersonId")),
                         a["actionType"] == "3pt" and ("pullup" in desc or "step back" in desc),
                         "driving" in desc))
    cols = ["game_id", "person_id", "zone", "three", "made", "assisted", "pullup3", "drive"]
    return pd.DataFrame(rows, columns=cols), tricode


def rebound_chances(stints: pd.DataFrame) -> pd.DataFrame:
    """Per player: team OREB, opponent DREB, team DREB, opponent OREB while he was on the floor."""
    parts = []
    for side, opp in (("home", "away"), ("away", "home")):
        s = stints[[f"{side}_ids", f"{side}_oreb", f"{opp}_dreb", f"{side}_dreb", f"{opp}_oreb"]].explode(f"{side}_ids")
        s.columns = ["person_id", "tm_oreb", "op_dreb", "tm_dreb", "op_oreb"]
        parts.append(s)
    out = pd.concat(parts)
    out["person_id"] = out.person_id.astype(int)
    return out.groupby("person_id").sum()


def season_features(season: str) -> tuple[pd.DataFrame, dict]:
    proc = cache.PROCESSED / season
    p100 = pd.read_parquet(proc / "player_season_per100.parquet")
    p100 = p100[p100.season_type == "regular"].copy()
    pg = pd.read_parquet(proc / "player_game.parquet")
    pg = pg[pg.season_type == "regular"]
    stints = pd.read_parquet(proc / "stints.parquet")
    stints = stints[stints.season_type == "regular"]

    shots, tricode = shots_from_pbp(season, sorted(pg.game_id.unique()))
    fga = shots.groupby("person_id").size()
    zone = shots.groupby(["person_id", "zone"]).size().unstack(fill_value=0).reindex(columns=ZONES, fill_value=0)
    agg = shots.groupby("person_id").agg(fgm=("made", "sum"), assisted=("assisted", "sum"),
                                         pullup3=("pullup3", "sum"), drive=("drive", "sum"))
    reb = rebound_chances(stints)

    f = p100.set_index("person_id")
    pbp_fga = fga.reindex(f.index)
    out = pd.DataFrame(index=f.index)
    for z in ZONES:
        out[f"{z}_share"] = zone[z].reindex(f.index) / pbp_fga
    out["pullup3_rate"] = agg.pullup3.reindex(f.index) / pbp_fga
    out["fta_rate"] = f.fta / f.fga
    out["usage_per100"] = 100 * (f.fga + 0.44 * f.fta + f.tov) / f.poss_off
    out["ast_per100"] = f.ast_per100
    out["assisted_share"] = agg.assisted.reindex(f.index) / agg.fgm.reindex(f.index)
    out["drive_rate"] = agg.drive.reindex(f.index) / pbp_fga
    out["fouls_drawn_per100"] = f.fouls_drawn_per100
    r = reb.reindex(f.index)
    out["oreb_pct"] = f.oreb / (r.tm_oreb + r.op_dreb)
    out["dreb_pct"] = f.dreb / (r.tm_dreb + r.op_oreb)
    out["stl_per100"] = f.stl_per100
    out["blk_per100"] = f.blk_per100
    out["pf_def_per100"] = f.pf_def_per100
    out["charges_drawn_per100"] = f.charges_drawn_per100

    # teams in order of minutes, for display
    tm = pg.groupby(["person_id", "team_id"]).seconds.sum().reset_index().sort_values("seconds", ascending=False)
    teams = tm.groupby("person_id").team_id.apply(lambda s: "/".join(tricode.get(int(t), str(t)) for t in s))
    team_ids = tm.groupby("person_id").team_id.apply(lambda s: [int(t) for t in s])

    meta = f[["name", "games", "seconds", "poss_off", "poss_def", "fga", "fta", "pts"]].copy()
    meta["teams"] = teams.reindex(f.index)
    meta["team_id_list"] = team_ids.reindex(f.index)
    meta["pbp_fga"] = pbp_fga
    out = meta.join(out).reset_index()
    out.insert(0, "season", season)
    out["tier"] = np.select([out.seconds >= FIT_MIN_SECONDS, out.seconds >= LOW_MIN_SECONDS],
                            ["fit", "low_sample"], "unknown")
    return out, tricode


def player_positions(c, season: str) -> pd.DataFrame:
    """NBA's listed position per player (playerindex), cached as parquet."""
    path = cache.PROCESSED / season / "player_index.parquet"
    if path.exists():
        return pd.read_parquet(path)
    d = c.stats("playerindex", {"LeagueID": "00", "Season": season, "Historical": "1"}, timeout=30)
    rs = d["resultSets"][0]
    df = pd.DataFrame(rs["rowSet"], columns=rs["headers"])[["PERSON_ID", "POSITION", "HEIGHT"]]
    df.columns = ["person_id", "position", "height"]
    df.to_parquet(path, index=False)
    return df
