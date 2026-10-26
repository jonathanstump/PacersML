"""Gaussian mixture sweep and stability checks for the archetype model (METHODS section 5, D25).

For one (covariance type, k):
  starts      20 fits from different seeds (k-means initialization) (one init each); the best lower bound is the main fit,
              ARI of each start's labels against it
  BIC         of the main fit, with its parameter count
  held-out    scaler and model fitted on 2024-25 rows only, mean log-likelihood per 2025-26 row (time split)
  seasons     one model per season, every row labelled by both, ARI between the two labelings
  bootstrap   refits on resampled rows; each labels all rows, clusters matched to the main fit by center
              distance (Hungarian), ARI and per-cluster retention (share of a cluster's players kept)
Nothing here picks k.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
from scipy.optimize import linear_sum_assignment
from sklearn.metrics import adjusted_rand_score
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import StandardScaler

N_STARTS = 20
N_BOOT = 50
BOOT_INIT = 3
REG_COVAR = 1e-4   # added to covariance diagonals (standardized units) so tiny clusters don't become singular
MAX_ITER = 500


@dataclass
class SweepResult:
    cov: str
    k: int
    ok: bool
    bic: float = np.nan
    n_params: int = 0
    loglik: float = np.nan
    heldout_ll: float = np.nan
    ari_starts: list = field(default_factory=list)
    ari_seasons: float = np.nan
    ari_boot: list = field(default_factory=list)
    retention: np.ndarray | None = None   # per main cluster, mean over bootstraps
    model: GaussianMixture | None = None
    error: str = ""


def gmm(cov: str, k: int, seed: int, n_init: int = 1) -> GaussianMixture:
    return GaussianMixture(n_components=k, covariance_type=cov, n_init=n_init, init_params="kmeans",
                           reg_covar=REG_COVAR, max_iter=MAX_ITER, random_state=seed)


def match_to(ref_means: np.ndarray, means: np.ndarray) -> np.ndarray:
    """mapping[j] = reference cluster matched to cluster j (Hungarian on center distance)."""
    d = ((ref_means[:, None, :] - means[None, :, :]) ** 2).sum(-1)
    r, c = linear_sum_assignment(d)
    mapping = np.empty(len(c), dtype=int)
    mapping[c] = r
    return mapping


def sweep_one(X: np.ndarray, season: np.ndarray, X_raw: np.ndarray, cov: str, k: int, seed0: int = 0) -> SweepResult:
    res = SweepResult(cov, k, ok=False)
    try:
        starts = [gmm(cov, k, seed0 + s).fit(X) for s in range(N_STARTS)]
        main = max(starts, key=lambda m: m.lower_bound_)
        lab = main.predict(X)
        res.model, res.bic, res.n_params = main, main.bic(X), main._n_parameters()
        res.loglik = main.score(X) * len(X)
        res.ari_starts = [adjusted_rand_score(lab, m.predict(X)) for m in starts]

        s0, s1 = season == "2024-25", season == "2025-26"
        sc = StandardScaler().fit(X_raw[s0])
        m0 = gmm(cov, k, seed0, n_init=5).fit(sc.transform(X_raw[s0]))
        res.heldout_ll = m0.score(sc.transform(X_raw[s1]))
        a = gmm(cov, k, seed0, n_init=5).fit(X[s0]).predict(X)
        b = gmm(cov, k, seed0, n_init=5).fit(X[s1]).predict(X)
        res.ari_seasons = adjusted_rand_score(a, b)

        rng = np.random.default_rng(seed0 + 1000 * k)
        kept = np.zeros(k)
        n = 0
        for _ in range(N_BOOT):
            idx = rng.integers(0, len(X), len(X))
            try:
                m = gmm(cov, k, int(rng.integers(1 << 30)), n_init=BOOT_INIT).fit(X[idx])
            except (ValueError, np.linalg.LinAlgError):
                continue
            mapped = match_to(main.means_, m.means_)[m.predict(X)]
            res.ari_boot.append(adjusted_rand_score(lab, mapped))
            kept += np.array([(mapped[lab == c] == c).mean() if (lab == c).any() else np.nan for c in range(k)])
            n += 1
        res.retention = kept / max(n, 1)
        res.ok = True
    except (ValueError, np.linalg.LinAlgError) as e:
        res.error = str(e)[:200]
    return res


def elbow(ks: np.ndarray, bic: np.ndarray) -> int:
    """k farthest below the straight line from the first to the last BIC value (kneedle-style)."""
    x = (ks - ks.min()) / (ks.max() - ks.min())
    y = (bic - bic.min()) / (bic.max() - bic.min() or 1)
    line = y[0] + (y[-1] - y[0]) * x
    return int(ks[np.argmax(line - y)])
