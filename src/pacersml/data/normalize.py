"""Turn raw stats.nba.com v3 and cdn liveData payloads into one canonical schema.

Canonical play-by-play event (one row per action, in source order):
    game_id, seq, period, elapsed (seconds since tip-off), team_id, person_id,
    etype, made, value, points, ft_num, ft_of, technical, in_id, out_id, desc
etype ∈ {period_start, period_end, fg, ft, rebound, turnover, foul, sub, jumpball, other}.
`value` is the shot value (2/3 for field goals, 1 for free throws) whether or not it went in.
For etype == "sub", in_id / out_id are the players entering / leaving (person_id is unused).

Canonical player box (one row per player who appeared):
    game_id, team_id, person_id, name, seconds, pts, fgm, fga, fg3m, fg3a, ftm, fta,
    oreb, dreb, ast, stl, blk, tov, pf, plus_minus

NOTE: these parsers are written against the documented response shapes and have not yet been run against
live responses (the development network was blocked on 2026-10-19). The first real pull is their test.
"""
from __future__ import annotations

import re

import numpy as np
import pandas as pd

BOX_KEYS = {
    "pts": "points", "fgm": "fieldGoalsMade", "fga": "fieldGoalsAttempted", "fg3m": "threePointersMade",
    "fg3a": "threePointersAttempted", "ftm": "freeThrowsMade", "fta": "freeThrowsAttempted",
    "oreb": "reboundsOffensive", "dreb": "reboundsDefensive", "ast": "assists", "stl": "steals",
    "blk": "blocks", "tov": "turnovers", "pf": "foulsPersonal", "plus_minus": "plusMinusPoints",
}
EVENT_COLS = ["game_id", "seq", "period", "elapsed", "team_id", "person_id", "etype", "made", "value", "points",
              "ft_num", "ft_of", "technical", "in_id", "out_id", "desc"]


def period_start(period: int) -> float:
    return 720.0 * min(period - 1, 4) + 300.0 * max(period - 5, 0)


def period_length(period: int) -> float:
    return 720.0 if period <= 4 else 300.0


def parse_clock(s: str) -> float:
    """'PT11M43.00S' (both APIs' event clocks) or '34:12' / '34:12.00' (v3 box minutes) → seconds."""
    if not s:
        return 0.0
    m = re.fullmatch(r"PT(\d+)M([\d.]+)S", s)
    if m:
        return int(m[1]) * 60 + float(m[2])
    mins, _, secs = s.partition(":")
    return int(float(mins)) * 60 + (float(secs) if secs else 0.0)


def elapsed(period: int, clock: str) -> float:
    return period_start(period) + period_length(period) - parse_clock(clock)


# ---------------------------------------------------------------- box scores

def _box_teams(payload: dict) -> list[dict]:
    root = payload.get("boxScoreTraditional") or payload.get("game")
    return [root["homeTeam"], root["awayTeam"]]


def box(payload: dict, game_id: str) -> pd.DataFrame:
    """Works for both boxscoretraditionalv3 and liveData boxscore payloads."""
    rows = []
    for team in _box_teams(payload):
        for p in team["players"]:
            st = p.get("statistics", {})
            secs = parse_clock(st.get("minutes") or "")
            if secs == 0 and p.get("played", "1") == "0":
                continue
            name = p.get("name") or f"{p.get('firstName', '')} {p.get('familyName', '')}".strip()
            row = {"game_id": game_id, "team_id": int(team["teamId"]), "person_id": int(p["personId"]),
                   "name": name, "family_name": p.get("familyName") or name.split(" ")[-1], "seconds": secs}
            row.update({k: int(st.get(v) or 0) for k, v in BOX_KEYS.items()})
            rows.append(row)
    df = pd.DataFrame(rows)
    return df[df.seconds > 0].reset_index(drop=True) if not df.empty else df


def team_ids(payload: dict) -> tuple[int, int]:
    home, away = _box_teams(payload)
    return int(home["teamId"]), int(away["teamId"])


# ---------------------------------------------------------------- play-by-play

def _ft_parts(sub_type: str) -> tuple[float, float]:
    m = re.search(r"(\d) of (\d)", sub_type or "")
    return (float(m[1]), float(m[2])) if m else (np.nan, np.nan)


def _base(game_id: str, seq: int, a: dict) -> dict:
    period = int(a["period"])
    return {"game_id": game_id, "seq": seq, "period": period, "elapsed": elapsed(period, a.get("clock", "")),
            "team_id": int(a.get("teamId") or 0), "person_id": int(a.get("personId") or 0),
            "etype": "other", "made": False, "value": 0, "points": 0, "ft_num": np.nan, "ft_of": np.nan,
            "technical": False, "in_id": 0, "out_id": 0, "desc": a.get("description", "")}


def events_live(payload: dict, game_id: str) -> pd.DataFrame:
    """cdn liveData playbyplay. Substitutions arrive as separate 'in' / 'out' actions."""
    rows = []
    for seq, a in enumerate(payload["game"]["actions"]):
        r = _base(game_id, seq, a)
        at, st = a.get("actionType", ""), (a.get("subType") or "").lower()
        made = a.get("shotResult") == "Made"
        if at == "period":
            r["etype"] = "period_start" if st == "start" else "period_end"
        elif at in ("2pt", "3pt"):
            value = 2 if at == "2pt" else 3
            r.update(etype="fg", made=made, value=value, points=value * made)
        elif at == "freethrow":
            n, of = _ft_parts(st)
            r.update(etype="ft", made=made, value=1, points=int(made), ft_num=n, ft_of=of,
                     technical="technical" in st or "technical" in r["desc"].lower())
        elif at == "substitution":
            r.update(etype="sub", in_id=r["person_id"] if st == "in" else 0,
                     out_id=r["person_id"] if st == "out" else 0)
        elif at in ("rebound", "turnover", "foul", "jumpball"):
            r["etype"] = at
        rows.append(r)
    return pd.DataFrame(rows, columns=EVENT_COLS)


_SUB_RE = re.compile(r"SUB:\s*(.+?)\s+FOR\s+(.+?)\s*$", re.I)


def events_v3(payload: dict, game_id: str, box_df: pd.DataFrame) -> pd.DataFrame:
    """stats.nba.com playbyplayv3. A substitution is one action, 'SUB: <in> FOR <out>'; the player named
    without a personId is resolved by family name against that team's box-score roster."""
    names = {(t, n.lower()): pid for t, n, pid in box_df[["team_id", "family_name", "person_id"]].itertuples(index=False)}
    dup = box_df.groupby(["team_id", box_df.family_name.str.lower()]).size()
    rows = []
    for seq, a in enumerate(payload["game"]["actions"]):
        r = _base(game_id, seq, a)
        at, st = a.get("actionType", ""), a.get("subType") or ""
        if at == "period":
            r["etype"] = "period_start" if st.lower() == "start" else "period_end"
        elif at in ("Made Shot", "Missed Shot"):
            made = at == "Made Shot"
            value = int(a.get("shotValue") or (3 if "3PT" in r["desc"].upper() else 2))
            r.update(etype="fg", made=made, value=value, points=value * made)
        elif at == "Free Throw":
            made = a.get("shotResult") == "Made" or ("MISS" not in r["desc"].upper() and not a.get("shotResult"))
            n, of = _ft_parts(st)
            r.update(etype="ft", made=made, value=1, points=int(made), ft_num=n, ft_of=of,
                     technical="technical" in st.lower())
        elif at == "Substitution":
            r["etype"] = "sub"
            m = _SUB_RE.search(r["desc"])
            if m:
                in_name, out_name = m[1].lower(), m[2].lower()

                def lookup(n):
                    return 0 if dup.get((r["team_id"], n), 0) != 1 else names.get((r["team_id"], n), 0)

                actor = box_df.loc[box_df.person_id == r["person_id"], "family_name"].str.lower()
                actor = actor.iloc[0] if len(actor) else ""
                if actor == in_name:
                    r.update(in_id=r["person_id"], out_id=lookup(out_name))
                else:
                    r.update(out_id=r["person_id"], in_id=lookup(in_name))
        elif at in ("Rebound", "Turnover", "Foul", "Jump Ball"):
            r["etype"] = at.lower().replace(" ", "")
        rows.append(r)
    return pd.DataFrame(rows, columns=EVENT_COLS)


def merge_live_subs(ev: pd.DataFrame) -> pd.DataFrame:
    """Pair liveData's separate in/out actions (same team, same clock) into one sub row each, so both
    sources share the one-row-per-substitution form."""
    subs = ev[ev.etype == "sub"]
    if subs.empty or (subs.in_id.gt(0) & subs.out_id.gt(0)).all():
        return ev
    drop = set()
    for _, g in subs.groupby(["period", "elapsed", "team_id"], sort=False):
        ins = g[g.in_id > 0].index.tolist()
        outs = g[g.out_id > 0].index.tolist()
        for i, o in zip(ins, outs):
            first = min(i, o)
            ev.loc[first, ["in_id", "out_id"]] = [ev.at[i, "in_id"], ev.at[o, "out_id"]]
            drop.add(max(i, o))
        # unpaired halves stay as-is (in_id or out_id == 0) and surface in validation
    return ev.drop(index=list(drop)).reset_index(drop=True)
