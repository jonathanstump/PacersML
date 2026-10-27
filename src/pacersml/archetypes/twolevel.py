"""Two-level archetypes (D27, METHODS section 6): frozen level-1 families, sub-role models inside each family.

Level 1   the full-covariance k = 3 Gaussian mixture from the D26 sweep, frozen. Families F1..F3 are numbered by
          size (F1 = largest), the same order as C1..C3 in reports/archetypes/k3/.
Level 2   per family, a mixture fitted on that family's training rows (top family, probability >= 0.6),
          standardized with the family's own scaler.
Combined  weight on sub-role s of family f = P(f) x P(s | f), with P(s | f) from projecting the player into every
          family's sub-model (with that family's scaler), so weights add to 1 over all sub-roles.
Nothing here picks a sub-role k.
"""
from __future__ import annotations

import hashlib
import pickle
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import skew

TRAIN_MIN_PROB = 0.6      # D27: family training set = top family with probability >= 0.6
MAX_EXCLUDED = 0.15       # D27: stop and ask if a family excludes more than this share of its top-assigned rows
SUB_KS = range(1, 7)      # D27: k = 1 is "no sub-structure"
STABLE_ARI, STABLE_KEPT = 0.6, 0.7
L2_DROP_ALL = ["charges_drawn_per100"]       # D31: out of level 2 in every family (level 1 keeps it)
L2_DROP_FAMILY = {2: ["pullup3_rate"]}       # D31: F3 only (0-based family index)


def l2_features(f: int, cols: list[str]) -> list[str]:
    """D31 level-2 feature list for family f (0-based)."""
    drop = set(L2_DROP_ALL) | set(L2_DROP_FAMILY.get(f, []))
    return [c for c in cols if c not in drop]


# ---------------------------------------------------------------- family names (D29)

def load_names(path: Path, frozen: dict) -> dict:
    """Versioned names file keyed to the frozen model's parameter hash; stops if the hash doesn't match."""
    import json
    names = json.loads(path.read_text(encoding="utf-8"))
    got = param_hash(frozen["model"], frozen["scaler"])
    if names["model_param_sha256"] != got:
        raise SystemExit(f"names file {path.name} is keyed to {names['model_param_sha256'][:12]}, model is {got[:12]}")
    return names


def family_labels(names: dict) -> list[str]:
    """'F1 On-ball Shot Creators', ... in family order."""
    fams = names["families"]
    return [f"{k} {fams[k]['name']}" for k in sorted(fams, key=lambda s: int(s[1:]))]


# ---------------------------------------------------------------- level 1: freeze and project

def param_hash(model, scaler) -> str:
    """Hash of the fitted numbers (weights, means, covariances, scaler), independent of pickle format."""
    h = hashlib.sha256()
    for a in (model.weights_, model.means_, model.covariances_, scaler.mean_, scaler.scale_):
        h.update(np.ascontiguousarray(a, dtype=np.float64).tobytes())
    return h.hexdigest()


def freeze(path: Path, model, scaler, features: list[str], order: np.ndarray, meta: dict) -> dict:
    """Save a frozen model; order[new] = the model's own component index for family new (sorted by size)."""
    obj = {"model": model, "scaler": scaler, "features": list(features), "order": np.asarray(order), **meta}
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "wb") as fh:
        pickle.dump(obj, fh)
    return {"path": str(path.as_posix()), "file_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "param_sha256": param_hash(model, scaler), "features": list(features)}


def load(path: Path) -> dict:
    with open(path, "rb") as fh:
        return pickle.load(fh)


def project(frozen: dict, raw: np.ndarray) -> np.ndarray:
    """Membership probabilities in the frozen model's own order (F1..Fk / S1..Sk)."""
    return frozen["model"].predict_proba(frozen["scaler"].transform(raw))[:, frozen["order"]]


# ---------------------------------------------------------------- level 2: training sets and feature flags

def training_mask(pf: np.ndarray, f: int) -> np.ndarray:
    return (pf.argmax(1) == f) & (pf[:, f] >= TRAIN_MIN_PROB)


def exclusions(pf: np.ndarray) -> pd.DataFrame:
    top, ptop = pf.argmax(1), pf.max(1)
    rows = []
    for f in range(pf.shape[1]):
        m = top == f
        rows.append({"family": f"F{f + 1}", "top_assigned": int(m.sum()), "training": int((m & (ptop >= TRAIN_MIN_PROB)).sum()),
                     "excluded": int((m & (ptop < TRAIN_MIN_PROB)).sum())})
    df = pd.DataFrame(rows)
    df["excluded_share"] = df.excluded / df.top_assigned
    df["over_limit"] = df.excluded_share > MAX_EXCLUDED
    return df


def feature_flags(fam: pd.DataFrame, league: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    """Per feature inside one family: spread relative to the league, zeros, skew. A flag is a prompt for Jonathan,
    not a drop: near-constant = family SD under 25% of league SD or over half the rows exactly 0; extremely skewed =
    |skewness| > 2. Within-family standardization stretches a near-constant feature to SD 1, so its noise gets
    the same weight as a real difference."""
    rows = []
    for c in cols:
        x, lx = fam[c].to_numpy(float), league[c].to_numpy(float)
        sd_ratio = x.std() / lx.std() if lx.std() > 0 else np.nan
        zeros = float(np.mean(x == 0))
        sk = float(skew(x)) if x.std() > 0 else np.nan
        flags = []
        if sd_ratio < 0.25 or zeros > 0.5:
            flags.append("near-constant")
        if abs(sk) > 2:
            flags.append("extremely skewed")
        rows.append({"feature": c, "family_mean": x.mean(), "family_sd": x.std(), "league_sd": lx.std(),
                     "sd_ratio": sd_ratio, "zero_share": zeros, "skewness": sk, "flags": ", ".join(flags)})
    return pd.DataFrame(rows)


def n_params(cov: str, k: int, d: int) -> int:
    """sklearn GaussianMixture free-parameter count."""
    cov_p = {"full": k * d * (d + 1) / 2, "tied": d * (d + 1) / 2, "diag": k * d, "spherical": k}[cov]
    return int(cov_p + k * d + k - 1)


def sweep_grid(n_rows: int, d: int) -> list[tuple[str, int]]:
    """D27: tied and diag at every k; full only where its parameter count is under half the family's training rows."""
    return [(cov, k) for cov in ("tied", "diag") for k in SUB_KS] + \
           [("full", k) for k in SUB_KS if n_params("full", k, d) < n_rows / 2]


# ---------------------------------------------------------------- selection rule (marks a candidate, doesn't pick)

def mark_candidate(sweep: pd.DataFrame) -> pd.DataFrame:
    """D25 order: BIC narrows, stability decides. Stable = median bootstrap ARI >= 0.6 and no sub-role under 70%
    kept (k = 1 is trivially stable). Candidate = the lowest-BIC stable (covariance, k). Naming breaks ties: left
    to Jonathan, so a second row within 10 BIC of the candidate is marked as a near tie. cov_candidate applies the
    rule inside each covariance type separately."""
    s = sweep.copy()
    s["stable"] = s.ok & ((s.k == 1) | ((s.ari_boot_median >= STABLE_ARI) & (s.retention_min >= STABLE_KEPT)))
    s["bic_best"] = s.ok & (s.bic == s[s.ok].bic.min())
    st = s[s.stable]
    s["candidate"] = False
    s["near_tie"] = False
    s["cov_candidate"] = False   # the same rule inside one covariance type (reported next to the overall one)
    for _, g in st.groupby("cov"):
        s.loc[g.bic.idxmin(), "cov_candidate"] = True
    if not st.empty:
        best = st.bic.min()
        s.loc[st.bic.idxmin(), "candidate"] = True
        s.loc[s.stable & ~s.candidate & (s.bic - best <= 10), "near_tie"] = True
    return s


# ---------------------------------------------------------------- combined membership

def combined(pf: np.ndarray, subs: list[np.ndarray]) -> np.ndarray:
    """pf: n x F family probabilities; subs[f]: n x k_f probabilities within family f. Returns n x sum(k_f)."""
    return np.hstack([pf[:, [f]] * subs[f] for f in range(pf.shape[1])])


def unknown_shares(pf_fit: np.ndarray, subs_train: list[np.ndarray]) -> tuple[np.ndarray, list[np.ndarray]]:
    """D25 tier 3 (under 100 minutes), at both levels: family shares = mean P(f) over fitted player-seasons;
    sub-role shares = mean P(s | f) over that family's training player-seasons."""
    return pf_fit.mean(0), [s.mean(0) for s in subs_train]


# ---------------------------------------------------------------- slicing test (D30, METHODS section 7)

def centroid_spread(means: np.ndarray, weights: np.ndarray, axes: np.ndarray) -> dict:
    """How cluster centers spread, in the standardized space they were fitted in.
    B = sum_c w_c (mu_c - mu_bar)(mu_c - mu_bar)', the weighted between-centroid covariance.
    share_axis[j] = a_j' B a_j / trace(B) for each unit row a_j of `axes` (the within-family PCs).
    line_share = largest eigenvalue of B / trace(B): 1.0 means every centroid sits on one straight line (always
    true at k = 2). line_angle_pc1 = angle in degrees between that line and PC1 (0 = parallel)."""
    w = np.asarray(weights, float) / np.sum(weights)
    mu = np.asarray(means, float)
    dev = mu - w @ mu
    B = (dev * w[:, None]).T @ dev
    tr = np.trace(B)
    vals, vecs = np.linalg.eigh(B)
    top = vecs[:, -1]
    cos = abs(float(top @ axes[0]) / np.linalg.norm(axes[0]))
    return {"share_axis": np.array([a @ B @ a / tr for a in axes]), "line_share": float(vals[-1] / tr),
            "line_angle_pc1": float(np.degrees(np.arccos(min(cos, 1.0))))}


def gmm_1d(x: np.ndarray, ks=(1, 2), seed: int = 0) -> dict[int, dict]:
    """1-D Gaussian mixture per k: BIC (lower is better) and the components (weights, means, SDs; sorted by mean)."""
    from sklearn.mixture import GaussianMixture
    x = np.asarray(x, float).reshape(-1, 1)
    out = {}
    for k in ks:
        g = GaussianMixture(k, n_init=10, random_state=seed).fit(x)
        o = np.argsort(g.means_.ravel())
        out[k] = {"bic": float(g.bic(x)), "weights": g.weights_[o], "means": g.means_.ravel()[o],
                  "sds": np.sqrt(g.covariances_.ravel()[o])}
    return out
