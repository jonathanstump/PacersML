"""Phase 2: build style features and run the Gaussian mixture sweep (D25, METHODS section 5). Does not pick k.

    python -u scripts/archetypes_fit.py            # features + sweep (k 2-15 x full/diag/tied) + diagnostic plots
    python -u scripts/archetypes_fit.py --jobs 4

Writes data/processed/archetypes/{features.parquet, sweep.pkl}, reports/archetypes/sweep.csv and the sweep plots.
Then run scripts/archetypes_report.py for the naming packets.
"""
from __future__ import annotations

import argparse
import pickle
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from joblib import Parallel, delayed  # noqa: E402
from sklearn.preprocessing import StandardScaler  # noqa: E402

from pacersml.archetypes import features as F  # noqa: E402
from pacersml.archetypes.gmm import elbow, sweep_one  # noqa: E402
from pacersml.archetypes.plots import sweep_plots  # noqa: E402
from pacersml.data import cache  # noqa: E402
from pacersml.data.http import Client  # noqa: E402

COVS = ["full", "tied", "diag"]
KS = range(2, 16)
OUT = cache.PROCESSED / "archetypes"
REPORTS = ROOT / "reports" / "archetypes"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--jobs", type=int, default=4)
    args = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    t = time.time()
    c = Client()
    frames = []
    for season in F.TRAINING:
        f, _ = F.season_features(season)
        pos = F.player_positions(c, season)
        frames.append(f.merge(pos, on="person_id", how="left"))
        print(f"{season}: {len(f)} player-seasons · fit {(f.tier == 'fit').sum()} · low-sample "
              f"{(f.tier == 'low_sample').sum()} · unknown {(f.tier == 'unknown').sum()} ({time.time() - t:.0f}s)",
              flush=True)
    feats = pd.concat(frames, ignore_index=True)
    feats.to_parquet(OUT / "features.parquet", index=False)

    fit = feats[feats.tier == "fit"].reset_index(drop=True)
    X_raw = fit[F.FEATURE_COLS].to_numpy(float)
    scaler = StandardScaler().fit(X_raw)
    X = scaler.transform(X_raw)
    season = fit.season.to_numpy()
    print(f"fit rows {len(X)} x {X.shape[1]} features; sweep {len(COVS)} covariance types x k {KS.start}-{KS.stop - 1}",
          flush=True)

    jobs = [(cov, k) for cov in COVS for k in KS]
    results = Parallel(n_jobs=args.jobs, verbose=5)(delayed(sweep_one)(X, season, X_raw, cov, k) for cov, k in jobs)

    rows = []
    for r in results:
        ret = r.retention if r.retention is not None else np.array([np.nan])
        rows.append({"cov": r.cov, "k": r.k, "ok": r.ok, "bic": r.bic, "n_params": r.n_params, "n_rows": len(X),
                     "loglik": r.loglik, "heldout_ll_per_row": r.heldout_ll,
                     "ari_starts_median": np.median(r.ari_starts) if r.ari_starts else np.nan,
                     "ari_starts_min": np.min(r.ari_starts) if r.ari_starts else np.nan,
                     "ari_seasons": r.ari_seasons,
                     "ari_boot_median": np.median(r.ari_boot) if r.ari_boot else np.nan,
                     "n_boot": len(r.ari_boot),
                     "retention_min": np.nanmin(ret) if r.ok else np.nan,
                     "clusters_under_70": int((ret < 0.7).sum()) if r.ok else np.nan,
                     "error": r.error})
    sweep = pd.DataFrame(rows)
    for cov in COVS:
        s = sweep[(sweep["cov"] == cov) & sweep.ok]
        if len(s) > 2:
            sweep.loc[(sweep["cov"] == cov) & (sweep.k == elbow(s.k.to_numpy(), s.bic.to_numpy())), "elbow"] = True
    sweep["elbow"] = sweep.get("elbow", False).fillna(False).astype(bool)
    sweep.to_csv(REPORTS / "sweep.csv", index=False, float_format="%.4f")
    with open(OUT / "sweep.pkl", "wb") as fh:
        pickle.dump({"results": results, "scaler": scaler, "fit_index": fit[["season", "person_id"]],
                     "features": F.FEATURE_COLS}, fh)
    sweep_plots(sweep, REPORTS)
    print(sweep[["cov", "k", "ok", "bic", "n_params", "heldout_ll_per_row", "ari_starts_median", "ari_boot_median",
                 "ari_seasons", "retention_min", "clusters_under_70", "elbow"]].round(3).to_string(index=False))
    print(f"done in {time.time() - t:.0f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
