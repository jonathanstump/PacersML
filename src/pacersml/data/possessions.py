"""Possession counting from canonical play-by-play.

A possession is a maximal run of events in which the same team has the ball, within one period.
Events that reveal who has the ball:
    field-goal attempt, non-technical free throw, turnover  -> the actor's team has it
    rebound (incl. team rebounds)                             -> the rebounding team has it
Everything else (fouls, subs, timeouts, technical FTs, jump balls) is neutral. A new possession starts
whenever the team in control changes, and at every period start.

So an and-one (made FG + FT by the same team) and an offensive rebound both stay inside one possession,
while a made basket ends it as soon as the other team records anything.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

CONTROL_ETYPES = {"fg", "ft", "turnover", "rebound"}


def control_team(ev: pd.DataFrame) -> pd.Series:
    """Team shown to have the ball by each event; 0 where the event says nothing."""
    informative = ev.etype.isin(CONTROL_ETYPES) & ~ev.technical & (ev.team_id > 0)
    return ev.team_id.where(informative, 0)


def assign_possessions(ev: pd.DataFrame) -> pd.DataFrame:
    """Add `poss_id` (game-wide counter, -1 before the first control event of a period), `offense`, and the
    rebound bookkeeping needed for rebound percentages later:
        live_miss   missed field goal, or missed last free throw of a trip (the ball is live afterwards)
        reb_live    rebound that follows a live miss (excludes dead-ball team rebounds between free throws)
        reb_off     reb_live and the rebounding team is the team that missed
    """
    ev = ev.sort_values("seq").reset_index(drop=True)
    ctrl = control_team(ev).to_numpy()
    periods = ev.period.to_numpy()
    live_miss = (((ev.etype == "fg") & ~ev.made)
                 | ((ev.etype == "ft") & ~ev.made & ~ev.technical & (ev.ft_num == ev.ft_of))).to_numpy()
    is_reb = (ev.etype == "rebound").to_numpy()
    is_shot = ev.etype.isin(["fg", "ft"]).to_numpy() & ~ev.technical.to_numpy()
    team = ev.team_id.to_numpy()
    poss_id = np.full(len(ev), -1)
    offense = np.zeros(len(ev), dtype="int64")
    reb_live = np.zeros(len(ev), dtype=bool)
    reb_off = np.zeros(len(ev), dtype=bool)
    cur_team, cur_id, cur_period, last_shot = 0, -1, None, None
    for i in range(len(ev)):
        if periods[i] != cur_period:
            cur_period, cur_team, last_shot = periods[i], 0, None
        if is_reb[i] and last_shot is not None and live_miss[last_shot]:
            reb_live[i] = True
            reb_off[i] = team[i] == team[last_shot]
            last_shot = None
        if is_shot[i]:
            last_shot = i
        if ctrl[i] and ctrl[i] != cur_team:
            cur_team, cur_id = ctrl[i], cur_id + 1
        if cur_team:
            poss_id[i], offense[i] = cur_id, cur_team
    return ev.assign(poss_id=poss_id, offense=offense, live_miss=live_miss, reb_live=reb_live, reb_off=reb_off)


def possession_table(ev: pd.DataFrame) -> pd.DataFrame:
    """One row per possession: offense team, first event seq, period, points scored by the offense."""
    ev = ev[ev.poss_id >= 0]
    scored = ev.points.where(ev.team_id == ev.offense, 0)
    g = ev.assign(scored=scored).groupby("poss_id")
    return pd.DataFrame({
        "game_id": g.game_id.first(), "period": g.period.first(), "offense": g.offense.first(),
        "first_seq": g.seq.min(), "points": g.scored.sum(),
    }).reset_index()
