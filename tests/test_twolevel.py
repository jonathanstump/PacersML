import numpy as np
import pandas as pd
from sklearn.mixture import GaussianMixture

from pacersml.archetypes import twolevel as tl
from pacersml.data.tracking import tracking_player_game


def test_combined_weights_sum_to_one():
    # one guard, one big, one straddler (METHODS section 6 toy example)
    pf = np.array([[0.95, 0.05], [0.02, 0.98], [0.55, 0.45]])
    subs = [np.array([[0.8, 0.2], [0.5, 0.5], [0.3, 0.7]]), np.array([[1.0], [1.0], [1.0]])]
    w = tl.combined(pf, subs)
    assert w.shape == (3, 3)
    assert np.allclose(w.sum(1), 1)
    assert np.allclose(w[2], [0.55 * 0.3, 0.55 * 0.7, 0.45])


def test_n_params_matches_sklearn():
    X = np.random.default_rng(0).normal(size=(200, 5))
    for cov in ("full", "tied", "diag"):
        for k in (1, 3):
            m = GaussianMixture(k, covariance_type=cov, random_state=0).fit(X)
            assert tl.n_params(cov, k, 5) == m._n_parameters()


def test_sweep_grid_full_only_under_half_rows():
    grid = tl.sweep_grid(152, 17)   # full k=1 has 170 parameters > 76
    assert ("full", 1) not in grid and ("tied", 6) in grid and ("diag", 1) in grid
    assert ("full", 1) in tl.sweep_grid(400, 17)


def test_training_mask_and_exclusions():
    pf = np.array([[0.9, 0.1], [0.55, 0.45], [0.2, 0.8], [0.7, 0.3]])
    assert tl.training_mask(pf, 0).tolist() == [True, False, False, True]
    e = tl.exclusions(pf)
    assert e.excluded.tolist() == [1, 0] and bool(e.over_limit.iloc[0])   # 1 of 3 excluded > 15%


def test_mark_candidate_picks_lowest_bic_stable():
    s = pd.DataFrame({"cov": ["tied"] * 3, "k": [1, 2, 3], "ok": True, "bic": [100.0, 90.0, 80.0],
                      "ari_boot_median": [1.0, 0.7, 0.4], "retention_min": [1.0, 0.8, 0.9]})
    m = tl.mark_candidate(s)
    assert m.candidate.tolist() == [False, True, False]   # k=3 has the lowest BIC but isn't stable
    assert m.bic_best.tolist() == [False, False, True]


def test_feature_flags():
    rng = np.random.default_rng(1)
    league = pd.DataFrame({"a": rng.normal(size=500), "b": rng.normal(size=500)})
    fam = pd.DataFrame({"a": rng.normal(scale=0.1, size=100), "b": np.r_[np.zeros(60), rng.exponential(size=40)]})
    f = tl.feature_flags(fam, league, ["a", "b"]).set_index("feature")["flags"]
    assert "near-constant" in f["a"] and "near-constant" in f["b"]


def test_tracking_keeps_quarantined_and_uses_nba_poss_for_group_c():
    pg = pd.DataFrame({"game_id": ["g1", "g1", "g2", "g3"], "person_id": [1, 2, 1, 1],
                       "poss_off": [50.0, 40, 60, 55], "poss_def": [51.0, 41, 61, 54]})
    q = pd.DataFrame({"game_id": ["g2", "g3"], "group": ["B", "C"]})
    t = tracking_player_game(pg, q, lambda gid: pd.Series({1: 57.0}))
    assert len(t) == 4 and t.quarantined.tolist() == [False, False, True, True]
    g3 = t[t.game_id == "g3"].iloc[0]
    assert g3.poss_off == 57 and g3.poss_def == 57 and g3.poss_source == "nba_box_advanced"
    g2 = t[t.game_id == "g2"].iloc[0]   # Group B: lineups fine, our count kept
    assert g2.poss_off == 60 and g2.poss_source == "stints"
    t2 = tracking_player_game(pg, q, lambda gid: None)
    assert np.isnan(t2[t2.game_id == "g3"].poss_off.iloc[0])
