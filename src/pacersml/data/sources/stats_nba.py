"""stats.nba.com fetchers. Return raw-ish DataFrames; normalization lives in events.py / box.py."""
from __future__ import annotations

import pandas as pd

from pacersml.data.http import Client

SEASON_TYPES = {"regular": "Regular Season", "play_in": "PlayIn", "playoffs": "Playoffs"}

_DASH_PARAMS = {
    "LeagueID": "00", "PaceAdjust": "N", "PlusMinus": "N", "Rank": "N", "LastNGames": "0", "Month": "0",
    "OpponentTeamID": "0", "Period": "0", "DateFrom": "", "DateTo": "", "GameSegment": "", "Location": "",
    "Outcome": "", "SeasonSegment": "", "VsConference": "", "VsDivision": "", "TeamID": "0",
}


def _result_set(payload: dict, name: str | None = None) -> pd.DataFrame:
    sets = payload.get("resultSets") or [payload["resultSet"]]
    rs = next(s for s in sets if name is None or s["name"] == name)
    return pd.DataFrame(rs["rowSet"], columns=rs["headers"])


def game_log(c: Client, season: str, season_type: str) -> pd.DataFrame:
    p = c.stats("leaguegamelog", {
        "Counter": 1000, "DateFrom": "", "DateTo": "", "Direction": "ASC", "LeagueID": "00",
        "PlayerOrTeam": "T", "Season": season, "SeasonType": SEASON_TYPES[season_type], "Sorter": "DATE"})
    df = _result_set(p)
    if df.empty:
        return pd.DataFrame(columns=["game_id", "game_date", "home_team_id", "away_team_id"])
    df["is_home"] = df["MATCHUP"].str.contains(" vs. ")
    # Neutral-site games (Cup semifinals, international games) list both teams as "@": no home row.
    # Use the first row as the "home" label there; downstream only needs a consistent label per team.
    n_home = df.groupby("GAME_ID").is_home.transform("sum")
    df["neutral_site"] = n_home == 0
    first = ~df.duplicated("GAME_ID")
    df.loc[df.neutral_site, "is_home"] = first[df.neutral_site]
    home = df[df.is_home].set_index("GAME_ID")
    away = df[~df.is_home].set_index("GAME_ID")
    out = pd.DataFrame({"game_date": home["GAME_DATE"], "home_team_id": home["TEAM_ID"],
                        "away_team_id": away["TEAM_ID"].reindex(home.index),
                        "neutral_site": home["neutral_site"]})
    return out.rename_axis("game_id").reset_index()


def box_v3(c: Client, game_id: str) -> dict:
    return c.stats("boxscoretraditionalv3", {"GameID": game_id, "StartPeriod": 0, "EndPeriod": 0,
                                             "StartRange": 0, "EndRange": 0, "RangeType": 0})


def pbp_v3(c: Client, game_id: str) -> dict:
    return c.stats("playbyplayv3", {"GameID": game_id, "StartPeriod": 0, "EndPeriod": 0})


def rotation(c: Client, game_id: str) -> dict:
    # fails intermittently per game (500): longer backoff, 5 s then 10 s, before giving up on this call
    return c.stats("gamerotation", {"GameID": game_id, "LeagueID": "00"}, backoff=5.0)


def rotation_frame(payload: dict, game_id: str) -> pd.DataFrame:
    """One row per player stretch on the floor; IN/OUT_TIME_REAL in tenths of a second from tip-off."""
    df = pd.concat([_result_set(payload, "AwayTeam"), _result_set(payload, "HomeTeam")], ignore_index=True)
    return pd.DataFrame({
        "game_id": game_id,
        "team_id": df["TEAM_ID"].astype("int64"),
        "person_id": df["PERSON_ID"].astype("int64"),
        "in_sec": df["IN_TIME_REAL"].astype(float) / 10,
        "out_sec": df["OUT_TIME_REAL"].astype(float) / 10,
    })


def dash_players(c: Client, season: str, season_type: str, measure: str, per_mode: str) -> pd.DataFrame:
    """measure 'Base' + per_mode 'Per100Possessions' is NBA's per-100 (stored for reference, D1);
    measure 'Advanced' + per_mode 'Totals' carries player POSS for the D5 possession cross-check."""
    p = c.stats("leaguedashplayerstats", {**_DASH_PARAMS, "Season": season,
                                          "SeasonType": SEASON_TYPES[season_type],
                                          "PerMode": per_mode, "MeasureType": measure})
    return _result_set(p)


def dash_team_advanced(c: Client, season: str, season_type: str) -> pd.DataFrame:
    """Team-season totals incl. POSS, for the D1 2% possession cross-check."""
    p = c.stats("leaguedashteamstats", {**_DASH_PARAMS, "Season": season,
                                        "SeasonType": SEASON_TYPES[season_type],
                                        "PerMode": "Totals", "MeasureType": "Advanced"})
    return _result_set(p)
