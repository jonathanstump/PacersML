"""api.pbpstats.com: game list fallback and an independent per-game possession count."""
from __future__ import annotations

import pandas as pd

from pacersml.data.http import Client

SEASON_TYPES = {"regular": "Regular Season", "play_in": "PlayIn", "playoffs": "Playoffs"}


def games(c: Client, season: str, season_type: str) -> pd.DataFrame:
    p = c.get_json("https://api.pbpstats.com/get-games/nba",
                   {"Season": season, "SeasonType": SEASON_TYPES[season_type]},
                   {"User-Agent": "Mozilla/5.0"}, "pbpstats.com")
    df = pd.DataFrame(p.get("results", []))
    if df.empty:
        return pd.DataFrame(columns=["game_id", "game_date", "home_team_id", "away_team_id",
                                     "pbpstats_home_poss", "pbpstats_away_poss"])
    return pd.DataFrame({
        "game_id": df["GameId"], "game_date": df["Date"],
        "home_team_id": df["HomeTeamId"].astype("int64"), "away_team_id": df["AwayTeamId"].astype("int64"),
        "pbpstats_home_poss": df["HomePossessions"], "pbpstats_away_poss": df["AwayPossessions"],
    })
