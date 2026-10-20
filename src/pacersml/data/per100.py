"""Per-game player box joined with on-floor possessions from stints, and season per-100 tables.

Numerators come from the box score, except the foul split below, which comes from our play-by-play;
denominators are the possessions the player was on the floor for, counted from our stints (D1).
Offensive stats use offensive possessions, defensive stats defensive ones (D5), following SIDE (D6).

Foul split (D6), non-technical fouls only:
    pf_def          fouls committed while his team was defending
    pf_off_other    non-offensive fouls committed while his team had the ball (e.g. loose-ball)
    pf_offensive    offensive fouls; stored for reference only, they are already counted in TOV
    pf_side_unknown fouls before either team had the ball in the period (e.g. on a jump ball)
    fouls_drawn     fouls he drew while his team had the ball (offensive fouls excluded)
    charges_drawn   offensive fouls recorded as charges that he drew
    off_fouls_drawn all offensive fouls he drew (charges included); stored, not mapped
fouls_drawn / charges_drawn / off_fouls_drawn need liveData play-by-play (v3 has no drawn-by field). Games parsed
from v3 have them as NaN, and their per-100 rates use only possessions from liveData games.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

BOX_STATS = ["pts", "fgm", "fga", "fg3m", "fg3a", "ftm", "fta", "ast", "tov", "oreb", "stl", "blk", "dreb", "pf"]
FOUL_STATS = ["pf_def", "pf_off_other", "pf_offensive", "pf_side_unknown"]
DRAWN_STATS = ["fouls_drawn", "charges_drawn", "off_fouls_drawn"]
SIDE = {
    **{s: "off" for s in ["pts", "fgm", "fga", "fg3m", "fg3a", "ftm", "fta", "ast", "tov", "oreb",
                          "fouls_drawn", "pf_off_other"]},
    **{s: "def" for s in ["stl", "blk", "dreb", "pf_def", "charges_drawn"]},
}


def foul_counts(ev: pd.DataFrame, box_df: pd.DataFrame) -> pd.DataFrame:
    """Per-player foul split for one game. Which team had the ball comes from NBA's own `ball_team` (liveData);
    v3 games fall back to our possession tracker (`offense`), which lags right after a made basket."""
    f = ev[(ev.etype == "foul") & ~ev.technical]
    f = f.assign(ball=f.ball_team.where(f.ball_team > 0, f.offense))
    offensive = f.foul_type == "offensive"
    other = f[~offensive]
    on_def = (other.ball > 0) & (other.team_id != other.ball)
    on_off = (other.ball > 0) & (other.team_id == other.ball)
    parts = {
        "pf_def": other[on_def].groupby("person_id").size(),
        "pf_off_other": other[on_off].groupby("person_id").size(),
        "pf_offensive": f[offensive].groupby("person_id").size(),
        "pf_side_unknown": other[other.ball == 0].groupby("person_id").size(),
        "fouls_drawn": other[on_def & (other.drawn_id > 0)].groupby("drawn_id").size(),
        "charges_drawn": f[offensive & f.charge & (f.drawn_id > 0)].groupby("drawn_id").size(),
        "off_fouls_drawn": f[offensive & (f.drawn_id > 0)].groupby("drawn_id").size(),
    }
    out = pd.DataFrame(parts).reindex(box_df.person_id).fillna(0).astype(int)
    if not (ev.get("pbp_source", pd.Series(["cdn_pbp"])) == "cdn_pbp").all():
        out[DRAWN_STATS] = np.nan
    return out.rename_axis("person_id")


def player_game(box_df: pd.DataFrame, pstints: pd.DataFrame, ev: pd.DataFrame | None = None) -> pd.DataFrame:
    """box_df: canonical box for one game. pstints: stints.player_stints() for the same game.
    ev: the game's events with possessions assigned (for the foul split)."""
    on = pstints.groupby(["person_id"]).agg(
        stint_seconds=("seconds", "sum"), poss_off=("poss_off", "sum"), poss_def=("poss_def", "sum"),
        on_pts_for=("pts_for", "sum"), on_pts_against=("pts_against", "sum"))
    out = box_df.merge(on, left_on="person_id", right_index=True, how="left")
    fill = ["stint_seconds", "poss_off", "poss_def", "on_pts_for", "on_pts_against"]
    out[fill] = out[fill].fillna(0)
    if ev is not None:
        out = out.merge(foul_counts(ev, box_df), left_on="person_id", right_index=True, how="left")
    return out


def season_per100(pg: pd.DataFrame) -> pd.DataFrame:
    """pg: player_game rows with `season` and `season_type`. One row per player per season per season_type,
    across all teams he played for. Every rate carries its possession sample size."""
    keys = ["season", "season_type", "person_id"]
    pg = pg.copy()
    for s in FOUL_STATS + DRAWN_STATS:
        if s not in pg:
            pg[s] = np.nan
    has_drawn = pg.fouls_drawn.notna()
    pg["poss_off_drawn"] = pg.poss_off.where(has_drawn, 0)
    pg["poss_def_drawn"] = pg.poss_def.where(has_drawn, 0)
    stats = BOX_STATS + FOUL_STATS + DRAWN_STATS
    agg = pg.groupby(keys).agg(
        name=("name", "last"), team_ids=("team_id", lambda s: ",".join(map(str, pd.unique(s)))),
        games=("game_id", "nunique"), seconds=("seconds", "sum"),
        poss_off=("poss_off", "sum"), poss_def=("poss_def", "sum"),
        poss_off_drawn=("poss_off_drawn", "sum"), poss_def_drawn=("poss_def_drawn", "sum"),
        **{s: (s, lambda x: x.sum(min_count=1)) for s in stats}).reset_index()
    for s, side in SIDE.items():
        denom = agg[f"poss_{side}_drawn" if s in DRAWN_STATS else f"poss_{side}"]
        agg[f"{s}_per100"] = np.where(denom > 0, agg[s] / denom.where(denom > 0, 1) * 100, np.nan)
    return agg
