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


def test_clean_game_passes_on_hybrid():
    r = process_game(game(), GameData(full_box(), game_rows(), rotation()))
    assert r.quarantine is None
    assert set(r.checks.method) == {"hybrid"} and r.checks.passed.all()
    assert r.sub_timing["rotation_usable"] and r.sub_timing["rotation_unmatched"] == 0
    pg = r.player_game.set_index("person_id")
    assert pg.loc[14, "poss_off"] == 2 and pg.loc[16, "poss_def"] == 1


def test_unusable_rotation_falls_back_to_rebuild():
    rot = rotation()
    rot.loc[rot.person_id == 16, "in_sec"] = 0                       # six starters in the rotation file
    r = process_game(game(), GameData(full_box(), game_rows(), rot))
    assert r.quarantine is None and set(r.checks.method) == {"pbp_rebuild"}
    assert r.sub_timing["rotation_available"] and not r.sub_timing["rotation_usable"]


def test_no_rotation_uses_rebuild():
    r = process_game(game(), GameData(full_box(), game_rows(), None))
    assert r.quarantine is None and set(r.checks.method) == {"pbp_rebuild"}
    assert r.sub_timing["rotation_unmatched"] is None


def test_quarantine_when_hybrid_fails_no_second_builder():
    ev = game_rows()
    ev.loc[ev.etype == "sub", ["in_id", "out_id"]] = [16, 13]       # PBP names the wrong player leaving
    r = process_game(game(home=PACERS), GameData(full_box().replace({"team_id": {HOME: PACERS}}),
                                                 ev.replace({"team_id": {HOME: PACERS}}),
                                                 rotation().replace({"team_id": {HOME: PACERS}})))
    q = r.quarantine
    assert q is not None and q["pacers_game"] and q["stint_method"] == "hybrid" and not q["rebuild_attempted"]
    assert "plus_minus" in q["failed_checks"] and q["starters"]
    # rotation says 14 left at 60 s (no PBP match); PBP says 13 left (no rotation match); 16 in agrees
    assert (q["rotation_unmatched"], q["pbp_subs_off"]) == (1, 1)
    assert set(r.checks.method) == {"hybrid"}


def test_player_flag_needs_both_floors_and_direction_split():
    from pacersml.data.validate import gap_direction, player_poss_check
    season = pd.DataFrame({"person_id": [1, 2, 3, 4], "name": list("abcd"), "games": 1,
                           "poss_off": [21, 3070, 1000, 500], "poss_def": [21, 3070, 1000, 500]})
    nba = pd.DataFrame({"PLAYER_ID": [1, 2, 3, 4], "POSS": [20, 3000, 1003, 501]})
    t = player_poss_check(season, nba)
    assert t.flag_avg.tolist() == [False, True, False, False]   # 5% but 1 poss; 2.3% and 70 poss
    d = gap_direction(t).set_index("measure").loc["gap_poss_avg"]
    assert (d.over, d.under, d.investigate) == (2, 2, False)


def test_foul_split_by_side_and_drawn():
    from toy import ev

    from pacersml.data.per100 import foul_counts
    from pacersml.data.possessions import assign_possessions
    rows = [
        dict(etype="period_start"),
        dict(elapsed=1, team_id=AWAY, person_id=21, etype="foul", foul_type="personal"),         # no ball yet
        dict(elapsed=5, team_id=HOME, person_id=11, etype="fg", value=2),                         # IND ball
        dict(elapsed=6, team_id=AWAY, person_id=22, etype="foul", foul_type="shooting", drawn_id=11),
        dict(elapsed=7, team_id=HOME, person_id=12, etype="foul", foul_type="loose_ball", drawn_id=23),
        dict(elapsed=8, team_id=HOME, person_id=13, etype="foul", foul_type="offensive", charge=True, drawn_id=24),
        dict(elapsed=8, team_id=HOME, person_id=13, etype="turnover"),
        dict(elapsed=9, team_id=AWAY, person_id=21, etype="foul", technical=True, foul_type="technical"),
    ]
    fc = foul_counts(assign_possessions(ev(rows)).assign(pbp_source="cdn_pbp"), full_box())
    assert fc.loc[21, "pf_side_unknown"] == 1 and fc.loc[21, "pf_def"] == 0      # technical ignored
    assert fc.loc[22, "pf_def"] == 1 and fc.loc[11, "fouls_drawn"] == 1
    assert fc.loc[12, "pf_off_other"] == 1 and fc.loc[23, "fouls_drawn"] == 0   # drawn on defense: not counted
    assert fc.loc[13, "pf_offensive"] == 1 and fc.loc[13, "pf_def"] == 0
    assert fc.loc[24, "charges_drawn"] == 1 and fc.loc[24, "off_fouls_drawn"] == 1
    v3 = foul_counts(assign_possessions(ev(rows)).assign(pbp_source="stats_pbp"), full_box())
    assert v3.fouls_drawn.isna().all()


def test_count_moved_between_teammates_is_kept_with_note_but_missing_event_is_not():
    b = full_box()
    b.loc[b.person_id == 12, "dreb"] = 0
    b.loc[b.person_id == 13, "dreb"] = 1                             # rebound credited to a teammate in the box
    r = process_game(game(), GameData(b, game_rows(), rotation()))
    assert r.quarantine is None and r.kept_note["checks"] == "pbp_counts"
    b.loc[b.person_id == 13, "dreb"] = 0                             # team total now differs: an event is missing
    r = process_game(game(), GameData(b, game_rows(), rotation()))
    assert r.quarantine is not None and "pbp_counts" in r.quarantine["failed_checks"]


def test_plus_minus_note_needs_a_sub_at_a_technical_ft():
    from toy import ev

    from pacersml.data.validate import sub_at_technical_ft
    rows = [dict(etype="period_start"),
            dict(elapsed=30, team_id=AWAY, person_id=21, etype="foul", technical=True, foul_type="technical"),
            dict(elapsed=30, team_id=HOME, etype="sub", in_id=16, out_id=14),
            dict(elapsed=30, team_id=HOME, person_id=11, etype="ft", technical=True, value=1, made=True, points=1)]
    assert sub_at_technical_ft(ev(rows))
    rows[2]["elapsed"] = 40
    assert not sub_at_technical_ft(ev(rows))
    b = full_box()
    b.loc[b.person_id == 14, "plus_minus"] += 1                      # off by 1, but no technical FT in the game
    r = process_game(game(), GameData(b, game_rows(), rotation()))
    assert r.quarantine is not None and "plus_minus" in r.quarantine["failed_checks"]


def test_count_gap_kept_when_points_match_and_possessions_within_tolerance():
    b = full_box()
    b.loc[b.person_id == 12, "dreb"] = 0                             # team rebound total differs by one
    g = game().copy()
    g["pbpstats_home_id"], g["pbpstats_away_id"] = HOME, AWAY
    g["pbpstats_home_poss"], g["pbpstats_away_poss"] = 3, 3          # our toy stints: 3 and 3
    r = process_game(g, GameData(b, game_rows(), rotation()))
    assert r.quarantine is None and "possessions within 2%" in r.kept_note["detail"]
    g["pbpstats_home_poss"] = 10                                     # possessions far off: quarantined
    r = process_game(g, GameData(b, game_rows(), rotation()))
    assert r.quarantine is not None and r.quarantine["group"] == "A"


def test_shadow_rebuild_flags_hybrid_bug():
    rot = rotation()
    rot.loc[rot.person_id == 16, "in_sec"] = 0                       # rotation: 16 starts instead of 15
    rot.loc[rot.person_id == 15, "in_sec"] = 30
    r = process_game(game(), GameData(full_box(), game_rows(), rot))
    assert r.outcome["stint_method"] == "hybrid" and r.outcome["shadow_rebuild_lineup_ok"]
    assert not r.outcome["lineup_ok"] and r.outcome["hybrid_bug"]
    clean = process_game(game(), GameData(full_box(), game_rows(), rotation()))
    assert clean.outcome["outcome"] == "pass" and not clean.outcome["hybrid_bug"]


def test_regression_is_a_pass_or_kept_game_now_quarantined():
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
    from refresh import find_regressions
    base = pd.DataFrame({"game_id": ["a", "b", "c", "d"], "outcome": ["pass", "kept_with_notes", "quarantined", "pass"]})
    now = pd.DataFrame({"game_id": ["a", "b", "c", "e"], "outcome": ["quarantined", "quarantined", "quarantined", "quarantined"]})
    assert find_regressions(base, now) == ["a", "b"]


def test_unpaired_minutes_gap_up_to_3s_kept_with_note_paired_gap_fails():
    b = full_box()
    b.loc[b.person_id == 15, "seconds"] = 722                        # one player off by 2 s, nobody the other way
    r = process_game(game(), GameData(b, game_rows(), rotation()))
    assert r.quarantine is None and r.kept_note["checks"] == "minutes"
    b.loc[b.person_id == 15, "seconds"] = 724                        # 4 s: over the 3 s note limit
    assert "minutes" in process_game(game(), GameData(b, game_rows(), rotation())).quarantine["failed_checks"]
    b = full_box()
    b.loc[b.person_id == 14, "seconds"] = 62                         # the sub 2 s later: a teammate pair
    b.loc[b.person_id == 16, "seconds"] = 658
    assert "minutes" in process_game(game(), GameData(b, game_rows(), rotation())).quarantine["failed_checks"]
