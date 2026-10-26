import pandas as pd

from pacersml.data.normalize import elapsed, events_live, events_v3, merge_live_subs, parse_clock


def test_clock_formats():
    assert parse_clock("PT11M43.00S") == 703
    assert parse_clock("34:12") == 2052
    assert parse_clock("") == 0
    assert elapsed(1, "PT12M00.00S") == 0
    assert elapsed(4, "PT00M00.00S") == 2880
    assert elapsed(5, "PT05M00.00S") == 2880 and elapsed(6, "PT04M00.00S") == 3240


def _action(**kw):
    return {"period": 1, "clock": "PT10M00.00S", "teamId": 1, "personId": 0, "description": "", **kw}


def test_live_subs_are_paired():
    payload = {"game": {"actions": [
        _action(actionType="period", subType="start", teamId=0, clock="PT12M00.00S"),
        _action(actionType="substitution", subType="out", personId=14),
        _action(actionType="substitution", subType="in", personId=16),
    ]}}
    ev = merge_live_subs(events_live(payload, "g"))
    sub = ev[ev.etype == "sub"]
    assert len(sub) == 1 and (sub.in_id.iloc[0], sub.out_id.iloc[0]) == (16, 14)


def test_v3_sub_resolved_from_roster_either_direction():
    box = pd.DataFrame({"team_id": [1, 1], "person_id": [14, 16], "family_name": ["Turner", "Zubac"]})
    payload = {"game": {"actions": [
        _action(actionType="Substitution", personId=14, description="SUB: Zubac FOR Turner"),
        _action(actionType="Substitution", personId=16, description="SUB: Zubac FOR Turner"),
    ]}}
    ev = events_v3(payload, "g", box)
    assert ev[["in_id", "out_id"]].values.tolist() == [[16, 14], [16, 14]]


def test_live_technical_ft_from_descriptor():
    # 2026-27 (0022600090 Q4 07:08): the text no longer says "Technical"; the descriptor does
    payload = {"game": {"actions": [
        _action(actionType="freethrow", subType="1 of 1", descriptor="technical", shotResult="Made", personId=7,
                description="T. Murphy III Free Throw 1 of 1 (9 PTS)"),
        _action(actionType="freethrow", subType="1 of 2", shotResult="Made", personId=7,
                description="T. Murphy III Free Throw 1 of 2 (10 PTS)"),
    ]}}
    assert events_live(payload, "g").technical.tolist() == [True, False]
