import pandas as pd
from toy import AWAY, GAME, HOME, box, game_rows, rotation

from pacersml.data.pipeline import PACERS, GameData, process_game

STATS = {  # person_id: (pts, fgm, fga, fg3m, fg3a, ftm, fta, oreb, dreb, tov, pf, plus_minus)
    11: (2, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1), 12: (0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1),
    13: (3, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1), 14: (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 3),
    15: (0,) * 11 + (1,), 16: (0,) * 11 + (-2,),
    21: (0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, -1), 22: (2, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, -1),
    23: (2, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, -1), 24: (0,) * 11 + (-1,), 25: (0,) * 11 + (-1,),
}
COLS = ["pts", "fgm", "fga", "fg3m", "fg3a", "ftm", "fta", "oreb", "dreb", "tov", "pf", "plus_minus"]


def full_box():
    b = box()
    s = pd.DataFrame.from_dict(STATS, orient="index", columns=COLS).rename_axis("person_id").reset_index()
    return b.merge(s, on="person_id").assign(name=lambda d: d.person_id.astype(str), ast=0, stl=0, blk=0)


def game(home=HOME):
    return pd.Series({"game_id": GAME, "home_team_id": home, "away_team_id": AWAY,
                      "season": "1999-00", "season_type": "regular"})


def test_clean_game_passes_on_rotation():
    r = process_game(game(), GameData(full_box(), game_rows(), rotation()))
    assert r.quarantine is None
    assert set(r.checks.method) == {"rotation"} and r.checks.passed.all()
    pg = r.player_game.set_index("person_id")
    assert pg.loc[14, "poss_off"] == 2 and pg.loc[16, "poss_def"] == 1


def test_bad_rotation_recovered_by_pbp_rebuild():
    rot = rotation()
    rot.loc[rot.person_id == 14, "out_sec"] = 100   # rotation says the sub happened at 100 s
    rot.loc[rot.person_id == 16, "in_sec"] = 100
    r = process_game(game(), GameData(full_box(), game_rows(), rot))
    assert r.quarantine is None
    assert set(r.checks.method) == {"rotation", "pbp_rebuild"}
    assert r.checks[r.checks.method == "pbp_rebuild"].passed.all()


def test_quarantine_when_rebuild_also_fails():
    rot = rotation()
    rot.loc[rot.person_id == 14, "out_sec"] = 100
    rot.loc[rot.person_id == 16, "in_sec"] = 100
    ev = game_rows()
    ev.loc[ev.etype == "sub", ["in_id", "out_id"]] = [16, 13]   # PBP names the wrong player leaving
    r = process_game(game(home=PACERS), GameData(full_box().replace({"team_id": {HOME: PACERS}}),
                                                 ev.replace({"team_id": {HOME: PACERS}}),
                                                 rot.replace({"team_id": {HOME: PACERS}})))
    q = r.quarantine
    assert q is not None and q["pacers_game"] and q["rebuild_attempted"]
    assert "plus_minus" in q["failed_checks"] and q["inferred_starters"]


def test_player_flag_needs_both_floors_and_direction_split():
    from pacersml.data.validate import gap_direction, player_poss_check
    season = pd.DataFrame({"person_id": [1, 2, 3, 4], "name": list("abcd"), "games": 1,
                           "poss_off": [21, 3070, 1000, 500], "poss_def": [21, 3070, 1000, 500]})
    nba = pd.DataFrame({"PLAYER_ID": [1, 2, 3, 4], "POSS": [20, 3000, 1003, 501]})
    t = player_poss_check(season, nba)
    assert t.flag_avg.tolist() == [False, True, False, False]   # 5% but 1 poss; 2.3% and 70 poss
    d = gap_direction(t).set_index("measure").loc["gap_poss_avg"]
    assert (d.over, d.under, d.investigate) == (2, 2, False)
