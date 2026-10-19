from toy import AWAY, HOME, ev, game_rows

from pacersml.data.possessions import assign_possessions, possession_table


def test_toy_game_possessions():
    t = possession_table(assign_possessions(game_rows()))
    # home: make / rebound->make / turnover ; away: miss / two FTs / make
    assert t.offense.tolist() == [HOME, AWAY, HOME, AWAY, HOME, AWAY]
    assert t.points.tolist() == [2, 0, 3, 2, 0, 2]


def test_and_one_and_offensive_rebound_stay_one_possession():
    e = ev([
        dict(etype="period_start"),
        dict(elapsed=5, team_id=HOME, person_id=11, etype="fg"),
        dict(elapsed=6, team_id=HOME, person_id=12, etype="rebound"),
        dict(elapsed=8, team_id=HOME, person_id=12, etype="fg", made=True, points=2),
        dict(elapsed=8, team_id=AWAY, person_id=21, etype="foul"),
        dict(elapsed=8, team_id=HOME, person_id=12, etype="ft", made=True, points=1, ft_num=1, ft_of=1),
    ])
    t = possession_table(assign_possessions(e))
    assert len(t) == 1 and t.points.iloc[0] == 3


def test_technical_free_throw_does_not_change_possession():
    e = ev([
        dict(etype="period_start"),
        dict(elapsed=5, team_id=HOME, person_id=11, etype="fg"),
        dict(elapsed=6, team_id=HOME, person_id=12, etype="rebound"),
        dict(elapsed=7, team_id=AWAY, person_id=21, etype="ft", made=True, points=1, technical=True),
        dict(elapsed=9, team_id=HOME, person_id=12, etype="fg", made=True, points=2),
    ])
    t = possession_table(assign_possessions(e))
    assert t.offense.tolist() == [HOME]


def test_new_period_starts_new_possession():
    e = ev([
        dict(etype="period_start"),
        dict(elapsed=700, team_id=HOME, person_id=11, etype="fg"),
        dict(period=2, elapsed=720, etype="period_start"),
        dict(period=2, elapsed=730, team_id=HOME, person_id=11, etype="fg"),
    ])
    assert len(possession_table(assign_possessions(e))) == 2


def test_dead_ball_rebound_between_free_throws_not_live():
    e = ev([
        dict(etype="period_start"),
        dict(elapsed=5, team_id=HOME, person_id=11, etype="ft", value=1, ft_num=1, ft_of=2),
        dict(elapsed=5, team_id=HOME, etype="rebound"),
        dict(elapsed=5, team_id=HOME, person_id=11, etype="ft", value=1, ft_num=2, ft_of=2),
        dict(elapsed=6, team_id=HOME, person_id=12, etype="rebound"),
    ])
    a = assign_possessions(e)
    assert a.reb_live.tolist() == [False, False, False, False, True]
    assert a.reb_off.tolist()[-1]
