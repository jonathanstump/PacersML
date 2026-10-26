"""Player box stats for individual tracking (D28), 2026-27 onward.

Quarantined games keep their player box stats here (e.g. for H2 rolling windows) while staying out of everything
built from stints (stints.parquet, player_game.parquet, per-100, RAPM, lineup and on/off outputs). For Group C
quarantines (a lineup check failed: minutes, floor five or game seconds) our stint-based possession count may be
wrong for the players involved, so poss_off and poss_def are replaced by NBA's per-player possession count from
boxscoreadvancedv3 (one number, used for both). NBA's count runs ~2% higher than ours (D23).
"""
from __future__ import annotations

from typing import Callable

import numpy as np
import pandas as pd

LINEUP_GROUP = "C"


def tracking_player_game(pg: pd.DataFrame, quarantine: pd.DataFrame,
                         nba_poss: Callable[[str], pd.Series | None]) -> pd.DataFrame:
    """pg: player_game rows for every processed game (quarantined ones too). nba_poss(game_id) returns
    person_id -> NBA possessions, or None when unavailable (those rows get NaN possessions, poss_source
    'unavailable')."""
    t = pg.copy()
    group = quarantine.set_index("game_id").group if not quarantine.empty else pd.Series(dtype=str)
    t["quarantined"] = t.game_id.isin(group.index)
    t["quarantine_group"] = t.game_id.map(group).fillna("")
    t["poss_source"] = "stints"
    for gid in sorted(group[group == LINEUP_GROUP].index):
        m = t.game_id == gid
        nba = nba_poss(gid)
        if nba is None:
            t.loc[m, ["poss_off", "poss_def"]] = np.nan
            t.loc[m, "poss_source"] = "unavailable"
            continue
        poss = t.loc[m, "person_id"].map(nba)
        t.loc[m, "poss_off"] = poss
        t.loc[m, "poss_def"] = poss
        t.loc[m, "poss_source"] = np.where(poss.notna(), "nba_box_advanced", "unavailable")
    return t
