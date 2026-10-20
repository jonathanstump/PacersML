"""Hand-built toy game shared by the tests. Home team 1 (players 11-16), away team 2 (players 21-25).

 idx  t    event
  0    0   period start
  1   10   home 11 makes 2
  2   30   away 21 misses
  3   31   home 12 rebound
  4   45   home 13 makes 3
  5   60   home 14 shooting foul
  6   60   away 22 FT 1 of 2 made
  7   60   SUB home: 16 in for 14
  8   60   away 22 FT 2 of 2 made
  9   80   home 11 turnover
 10   90   away 23 makes 2
 11  720   period end
"""
import numpy as np
import pandas as pd

from pacersml.data.normalize import EVENT_COLS

HOME, AWAY, GAME = 1, 2, "0029900001"


def ev(rows):
    out = []
    for seq, r in enumerate(rows):
        base = {"game_id": GAME, "seq": seq, "period": 1, "elapsed": 0.0, "team_id": 0, "person_id": 0,
                "etype": "other", "made": False, "value": 0, "points": 0, "ft_num": np.nan, "ft_of": np.nan,
                "technical": False, "in_id": 0, "out_id": 0, "foul_type": "", "drawn_id": 0, "charge": False,
                "ball_team": 0, "desc": ""}
        base.update(r)
        out.append(base)
    return pd.DataFrame(out, columns=EVENT_COLS)


def game_rows(with_sub=True):
    rows = [
        dict(etype="period_start"),
        dict(elapsed=10, team_id=HOME, person_id=11, etype="fg", value=2, made=True, points=2),
        dict(elapsed=30, team_id=AWAY, person_id=21, etype="fg", value=2),
        dict(elapsed=31, team_id=HOME, person_id=12, etype="rebound"),
        dict(elapsed=45, team_id=HOME, person_id=13, etype="fg", value=3, made=True, points=3),
        dict(elapsed=60, team_id=HOME, person_id=14, etype="foul"),
        dict(elapsed=60, team_id=AWAY, person_id=22, etype="ft", value=1, made=True, points=1, ft_num=1, ft_of=2),
        dict(elapsed=60, team_id=HOME, etype="sub", in_id=16, out_id=14),
        dict(elapsed=60, team_id=AWAY, person_id=22, etype="ft", value=1, made=True, points=1, ft_num=2, ft_of=2),
        dict(elapsed=80, team_id=HOME, person_id=11, etype="turnover"),
        dict(elapsed=90, team_id=AWAY, person_id=23, etype="fg", value=2, made=True, points=2),
        dict(elapsed=720, etype="period_end"),
    ]
    if not with_sub:
        rows.pop(7)
    return ev(rows)


def box():
    rows = [(HOME, 11, 720), (HOME, 12, 720), (HOME, 13, 720), (HOME, 14, 60), (HOME, 15, 720), (HOME, 16, 660),
            (AWAY, 21, 720), (AWAY, 22, 720), (AWAY, 23, 720), (AWAY, 24, 720), (AWAY, 25, 720)]
    return pd.DataFrame(rows, columns=["team_id", "person_id", "seconds"]).assign(game_id=GAME)


def rotation():
    rows = [(HOME, p, 0, 720) for p in (11, 12, 13, 15)] + [(HOME, 14, 0, 60), (HOME, 16, 60, 720)]
    rows += [(AWAY, p, 0, 720) for p in (21, 22, 23, 24, 25)]
    return pd.DataFrame(rows, columns=["team_id", "person_id", "in_sec", "out_sec"]).assign(game_id=GAME)
