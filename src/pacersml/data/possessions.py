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
    """Add `poss_id` (game-wide counter, -1 before the first control event of a period) and `offense`."""
    ev = ev.sort_values("seq").reset_index(drop=True)
    ctrl = control_team(ev).to_numpy()
    periods = ev.period.to_numpy()
    poss_id = np.full(len(ev), -1)
    offense = np.zeros(len(ev), dtype="int64")
    cur_team, cur_id, cur_period = 0, -1, None
    for i in range(len(ev)):
        if periods[i] != cur_period:
            cur_period, cur_team = periods[i], 0
        if ctrl[i] and ctrl[i] != cur_team:
            cur_team, cur_id = ctrl[i], cur_id + 1
        if cur_team:
            poss_id[i], offense[i] = cur_id, cur_team
    return ev.assign(poss_id=poss_id, offense=offense)


def possession_table(ev: pd.DataFrame) -> pd.DataFrame:
    """One row per possession: offense team, first event seq, period, points scored by the offense."""
    ev = ev[ev.poss_id >= 0]
    scored = ev.points.where(ev.team_id == ev.offense, 0)
    g = ev.assign(scored=scored).groupby("poss_id")
    return pd.DataFrame({
        "game_id": g.game_id.first(), "period": g.period.first(), "offense": g.offense.first(),
        "first_seq": g.seq.min(), "points": g.scored.sum(),
    }).reset_index()
