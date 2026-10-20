import pytest
from toy import AWAY, GAME, HOME, box, ev, game_rows, rotation

from pacersml.data.stints import from_pbp, from_rotation, infer_starters, player_stints

EXPECTED = {
    "home_ids": [(11, 12, 13, 14, 15), (11, 12, 13, 15, 16)],
    "away_ids": [(21, 22, 23, 24, 25)] * 2,
    "seconds": [60.0, 660.0],
    "home_pts": [5, 0],
    "away_pts": [2, 2],   # both FTs go to the lineup at the foul (D8), though the sub is logged between them
    "home_poss": [2, 1],
    "away_poss": [2, 1],
}


@pytest.mark.parametrize("builder", ["rotation", "pbp"])
def test_toy_stints(builder):
    if builder == "rotation":
        stints, _, _ = from_rotation(game_rows(), rotation(), HOME, AWAY, GAME)
    else:
        stints, _, _ = from_pbp(game_rows(), box(), HOME, AWAY, GAME)
    for col, want in EXPECTED.items():
        assert stints[col].tolist() == want, col


def test_rotation_change_without_pbp_sub_still_splits_at_rotation_time():
    stints, _, _ = from_rotation(game_rows(with_sub=False), rotation(), HOME, AWAY, GAME)
    assert stints.seconds.tolist() == [60.0, 660.0]
    assert stints.away_pts.tolist() == [2, 2]   # both FTs precede the next event after t=60


def test_silent_starter_filled_from_minutes():
    ev = game_rows()
    starters, note = infer_starters(ev, HOME, box()[box().team_id == HOME], prev_five=set())
    assert starters == {11, 12, 13, 14, 15} and note == "events+minutes_fill"


def test_player_seconds_and_plus_minus():
    stints, _, _ = from_rotation(game_rows(), rotation(), HOME, AWAY, GAME)
    ps = player_stints(stints, HOME, AWAY)
    tot = ps.assign(pm=ps.pts_for - ps.pts_against).groupby("person_id")[["seconds", "pm"]].sum()
    assert tot.loc[14, "seconds"] == 60 and tot.loc[14, "pm"] == 3
    assert tot.loc[16, "seconds"] == 660 and tot.loc[16, "pm"] == -2
    assert tot.loc[21, "pm"] == -1


def test_rebound_ingredients_recorded_per_stint():
    stints, _, _ = from_rotation(game_rows(), rotation(), HOME, AWAY, GAME)
    s0 = stints.iloc[0]
    assert (s0.away_fg_miss, s0.home_dreb, s0.home_oreb) == (1, 1, 0)


def test_technical_ft_goes_to_lineup_at_the_technical_not_the_trip():
    rows = [
        dict(etype="period_start"),
        dict(elapsed=10, team_id=HOME, person_id=11, etype="foul", technical=True),           # tech on IND
        dict(elapsed=10, team_id=HOME, etype="sub", in_id=16, out_id=14),
        dict(elapsed=10, team_id=AWAY, person_id=21, etype="ft", value=1, made=True, points=1, technical=True),
        dict(elapsed=720, etype="period_end"),
    ]
    stints, _, _ = from_pbp(ev(rows), box(), HOME, AWAY, GAME)
    assert stints.away_pts.tolist() == [1, 0]


def test_events_after_last_ft_use_lineup_on_floor():
    rows = [
        dict(etype="period_start"),
        dict(elapsed=10, team_id=HOME, person_id=14, etype="foul"),
        dict(elapsed=10, team_id=AWAY, person_id=21, etype="ft", value=1, made=True, points=1, ft_num=1, ft_of=2),
        dict(elapsed=10, team_id=HOME, etype="sub", in_id=16, out_id=14),
        dict(elapsed=10, team_id=AWAY, person_id=21, etype="ft", value=1, ft_num=2, ft_of=2),   # missed
        dict(elapsed=11, team_id=AWAY, person_id=22, etype="rebound"),                           # live, off.
        dict(elapsed=12, team_id=AWAY, person_id=22, etype="fg", value=2, made=True, points=2),  # putback
        dict(elapsed=720, etype="period_end"),
    ]
    stints, _, _ = from_pbp(ev(rows), box(), HOME, AWAY, GAME)
    assert stints.away_pts.tolist() == [1, 2]
    assert (stints.away_ft_miss_live.tolist(), stints.away_oreb.tolist()) == ([1, 0], [0, 1])
