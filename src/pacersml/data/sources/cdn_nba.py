"""cdn.nba.com liveData fetchers (fallback for box score and play-by-play; no rotation or per-100 data)."""
from __future__ import annotations

import pandas as pd

from pacersml.data.http import Client


def box_live(c: Client, game_id: str) -> dict:
    return c.cdn(f"liveData/boxscore/boxscore_{game_id}.json")


def pbp_live(c: Client, game_id: str) -> dict:
    return c.cdn(f"liveData/playbyplay/playbyplay_{game_id}.json")


def schedule(c: Client) -> pd.DataFrame:
    """Current season only. Final games have gameStatus == 3."""
    p = c.cdn("staticData/scheduleLeagueV2.json")
    rows = [
        {"game_id": g["gameId"], "game_date": g["gameDateEst"][:10], "final": g["gameStatus"] == 3,
         "home_team_id": g["homeTeam"]["teamId"], "away_team_id": g["awayTeam"]["teamId"]}
        for d in p["leagueSchedule"]["gameDates"] for g in d["games"]
    ]
    return pd.DataFrame(rows)
