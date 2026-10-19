"""Per-game player box joined with on-floor possessions from stints, and season per-100 tables.

Numerators come from the box score; denominators are the possessions the player was on the floor for,
counted from our stints (D1). Offensive stats use offensive possessions, defensive stats defensive ones (D5),
following the SIDE mapping (D6, pending review).
"""
from __future__ import annotations

import numpy as np
import pandas as pd

STATS = ["pts", "fgm", "fga", "fg3m", "fg3a", "ftm", "fta", "ast", "tov", "oreb", "stl", "blk", "dreb", "pf"]
SIDE = {
    **{s: "off" for s in ["pts", "fgm", "fga", "fg3m", "fg3a", "ftm", "fta", "ast", "tov", "oreb"]},
    **{s: "def" for s in ["stl", "blk", "dreb", "pf"]},
}


def player_game(box_df: pd.DataFrame, pstints: pd.DataFrame) -> pd.DataFrame:
    """box_df: canonical box for one game. pstints: stints.player_stints() for the same game."""
    on = pstints.groupby(["person_id"]).agg(
        stint_seconds=("seconds", "sum"), poss_off=("poss_off", "sum"), poss_def=("poss_def", "sum"),
        on_pts_for=("pts_for", "sum"), on_pts_against=("pts_against", "sum"))
    out = box_df.merge(on, left_on="person_id", right_index=True, how="left")
    fill = ["stint_seconds", "poss_off", "poss_def", "on_pts_for", "on_pts_against"]
    out[fill] = out[fill].fillna(0)
    return out


def season_per100(pg: pd.DataFrame) -> pd.DataFrame:
    """pg: player_game rows with `season` and `season_type`. One row per player per season per season_type,
    across all teams he played for. Every rate carries its possession sample size."""
    keys = ["season", "season_type", "person_id"]
    agg = pg.groupby(keys).agg(
        name=("name", "last"), team_ids=("team_id", lambda s: ",".join(map(str, pd.unique(s)))),
        games=("game_id", "nunique"), seconds=("seconds", "sum"),
        poss_off=("poss_off", "sum"), poss_def=("poss_def", "sum"),
        **{s: (s, "sum") for s in STATS}).reset_index()
    for s in STATS:
        denom = agg[f"poss_{SIDE[s]}"]
        agg[f"{s}_per100"] = np.where(denom > 0, agg[s] / denom.where(denom > 0, 1) * 100, np.nan)
    return agg
