import numpy as np
import pandas as pd

from pacersml.archetypes.features import rebound_chances, shot_zone
from pacersml.archetypes.gmm import elbow, match_to


def test_shot_zones():
    assert shot_zone({"actionType": "2pt", "area": "Restricted Area"}) == "rim"
    assert shot_zone({"actionType": "2pt", "area": "In The Paint (Non-RA)"}) == "short_mid"
    assert shot_zone({"actionType": "2pt", "area": "Mid-Range"}) == "long_mid"
    assert shot_zone({"actionType": "3pt", "area": "Left Corner 3"}) == "corner3"
    assert shot_zone({"actionType": "3pt", "area": "Mid-Range"}) == "ab3"  # a 3 logged in a 2-point area


def test_rebound_chances_by_side():
    st = pd.DataFrame({"home_ids": [[1, 2], [1]], "away_ids": [[3], [3, 4]],
                       "home_oreb": [2, 1], "home_dreb": [5, 0], "away_oreb": [1, 3], "away_dreb": [4, 2]})
    r = rebound_chances(st)
    assert r.loc[1].tolist() == [3, 6, 5, 4]   # tm_oreb, op_dreb, tm_dreb, op_oreb over both stints
    assert r.loc[4].tolist() == [3, 0, 2, 1]


def test_match_and_elbow():
    ref = np.array([[0.0, 0], [5, 5], [10, 0]])
    assert match_to(ref, ref[[2, 0, 1]] + 0.1).tolist() == [2, 0, 1]
    ks = np.arange(2, 9)
    assert elbow(ks, np.array([100, 60, 40, 35, 33, 32, 31.0])) == 4
