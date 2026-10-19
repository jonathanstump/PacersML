import pytest
from toy import AWAY, GAME, HOME, box, game_rows, rotation

from pacersml.data.stints import from_pbp, from_rotation, infer_starters, player_stints

EXPECTED = {
    "home_ids": [(11, 12, 13, 14, 15), (11, 12, 13, 15, 16)],
    "away_ids": [(21, 22, 23, 24, 25)] * 2,
    "seconds": [60.0, 660.0],
    "home_pts": [5, 0],
    "away_pts": [1, 3],   # FT 2 of 2 comes after the sub in PBP order, so it belongs to the new stint
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
    assert tot.loc[14, "seconds"] == 60 and tot.loc[14, "pm"] == 4
    assert tot.loc[16, "seconds"] == 660 and tot.loc[16, "pm"] == -3
    assert tot.loc[21, "pm"] == -1
