"""Phase 2: D30 slicing diagnostics inside each level-1 family (METHODS section 7). Numbers only: nothing named,
chosen or packaged.

    python -u scripts/archetypes_slicing.py                  # diag sweep with the D31 features + diagnostics
    python -u scripts/archetypes_slicing.py --report-only    # diagnostics from the saved sweep

Per family, on its level-2 training rows (top family, probability >= 0.6) with the D31 feature list, standardized
with a scaler fitted on those rows:
  1. within-family PCA: variance explained by PCs 1-5, top 5 loadings of PCs 1-3, PC1 x PC2 scatter;
  2. slicing test: diag sweep k 1-6 (D26 init and checks; tied k = 1 kept as a reference row), and for the diag
     candidate k and k +- 1 the share of between-centroid variance along each PC and how close the centroids are to
     one straight line;
  3. multimodality: PC1 and PC2 histograms, 1-D Gaussian mixture BIC for 1 vs 2 components.

Writes data/processed/archetypes/slicing_sweep.pkl and reports/archetypes/families/slicing/.
"""
from __future__ import annotations

import argparse
import pickle
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from joblib import Parallel, delayed  # noqa: E402
from scipy.stats import skew  # noqa: E402
from sklearn.decomposition import PCA  # noqa: E402
from sklearn.preprocessing import StandardScaler  # noqa: E402

from archetypes_families import FAM, NAMES_PATH, OUT, is_pacers, level1, sweep_table  # noqa: E402
from archetypes_report import SPEC, TURNER, ZUBAC  # noqa: E402
from pacersml.archetypes import plots  # noqa: E402
from pacersml.archetypes import twolevel as tl  # noqa: E402
from pacersml.archetypes.features import FEATURE_COLS  # noqa: E402
from pacersml.archetypes.gmm import sweep_one  # noqa: E402

SLC = FAM / "slicing"
N_PCS, N_LOAD, N_LOAD_PCS = 5, 5, 3


def is_tz(r) -> bool:
    """Turner 2024-25 and every Zubac season (D30 labels)."""
    return (r.person_id == TURNER and r.season == "2024-25") or r.person_id == ZUBAC


def family_data(feats_fit: pd.DataFrame, pf_fit: np.ndarray, f: int) -> dict:
    cols = tl.l2_features(f, FEATURE_COLS)
    m = tl.training_mask(pf_fit, f)
    rows = feats_fit[m].reset_index(drop=True)
    raw = rows[cols].to_numpy(float)
    sc = StandardScaler().fit(raw)
    Xf = sc.transform(raw)
    pca = PCA().fit(Xf)
    comps = pca.components_.copy()
    for j in range(len(comps)):          # sign convention: the largest-|loading| feature of each PC is positive
        if comps[j, np.argmax(np.abs(comps[j]))] < 0:
            comps[j] *= -1
    return {"cols": cols, "mask": m, "rows": rows, "raw": raw, "scaler": sc, "Xf": Xf, "comps": comps,
            "var": pca.explained_variance_ratio_, "scores": (Xf - pca.mean_) @ comps.T, "center": pca.mean_}


def run_sweep(fd: dict, jobs: int) -> dict:
    grid = [("diag", k) for k in tl.SUB_KS] + [("tied", 1)]
    work = [(f, cov, k) for f in fd for cov, k in grid]
    print(f"slicing sweep: {len(work)} fits over {len(fd)} families", flush=True)
    out = Parallel(n_jobs=jobs, verbose=5)(
        delayed(sweep_one)(fd[f]["Xf"], fd[f]["rows"].season.to_numpy(), fd[f]["raw"], cov, k, seed0=100 * (f + 1))
        for f, cov, k in work)
    res = {f: {} for f in fd}
    for (f, cov, k), r in zip(work, out):
        res[f][(cov, k)] = r
    return res


def sub_order(model, Xf: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Clusters renumbered by size (S1 = largest), as in the D27 packets. Returns (order, top in new numbering)."""
    k = model.n_components
    lab = model.predict(Xf)
    order = np.argsort(-np.bincount(lab, minlength=k), kind="stable")
    inv = np.empty(k, int)
    inv[order] = np.arange(k)
    return order, inv[lab]


def label(r) -> str:
    return f"{r['name']} {r['season'][2:4]}-{r['season'][5:]}"


def write_family(f: int, flab: str, d: dict, res: dict, out: Path) -> dict:
    out.mkdir(parents=True, exist_ok=True)
    fid = f"F{f + 1}"
    rows, Xf, comps, var, scores = d["rows"], d["Xf"], d["comps"], d["var"], d["scores"]
    n, p = Xf.shape
    dropped = [c for c in FEATURE_COLS if c not in d["cols"]]

    # sweep table (diag k 1-6 + tied k = 1 reference)
    s = sweep_table({"mask": d["mask"], "results": res})
    s.to_csv(out / "sweep.csv", index=False, float_format="%.4f")
    plots.sweep_plots(s, out, ks=tl.SUB_KS, prefix=f"{fid}: ")
    dg = s[s["cov"] == "diag"]
    cand = dg[dg.cov_candidate]
    ck = int(cand.k.iloc[0]) if not cand.empty else None
    tied1 = s[(s["cov"] == "tied") & (s.k == 1)].iloc[0]

    # labels for the scatter: Pacers player-seasons, Turner 2024-25, every Zubac season (training rows only)
    pac = rows.apply(is_pacers, axis=1).to_numpy()
    tz = rows.apply(is_tz, axis=1).to_numpy()
    lab_idx = list(np.flatnonzero(tz)) + [i for i in np.flatnonzero(pac) if not tz[i]]
    names = [label(r) for _, r in rows.iterrows()]
    plots.pc_scatter(scores[:, :2], names, lab_idx, pac, (var[0], var[1]),
                     f"{flab}: training player-seasons on the within-family PC1 x PC2 ({n} rows, {p} features)",
                     out / "pc_scatter.png")

    # slicing test
    ks = [k for k in ((ck - 1, ck, ck + 1) if ck else ()) if 2 <= k <= max(tl.SUB_KS)]
    slice_rows, panels = [], []
    for k in ks:
        model = res[("diag", k)].model
        order, top = sub_order(model, Xf)
        means, w = model.means_[order], model.weights_[order]
        sp = tl.centroid_spread(means, w, comps[:N_PCS])
        centers = (means - d["center"]) @ comps[:2].T
        snames = [f"{fid}-S{c + 1}" for c in range(k)]
        slice_rows.append({"k": k, "spread": sp, "centers": centers, "weights": w, "names": snames,
                           "sizes": np.bincount(top, minlength=k)})
        panels.append({"k": k, "top": top, "centers": centers, "weights": w, "names": snames,
                       "caption": f"between-centroid variance along PC1 {sp['share_axis'][0]:.0%}, PC2 "
                                  f"{sp['share_axis'][1]:.0%}\ncentroids' own first direction "
                                  f"{sp['line_share']:.0%}, {sp['line_angle_pc1']:.0f}° from PC1"})
    if panels:
        plots.centroid_panels(scores[:, :2], panels, (var[0], var[1]),
                              f"{flab}: diag cluster centers on the within-family PC1 x PC2 (X size = weight)",
                              out / "centroids.png")

    # multimodality
    fits = [tl.gmm_1d(scores[:, j], seed=f) for j in range(2)]
    plots.pc_hist(scores[:, :2], fits, var,
                  f"{flab}: PC score distributions with 1- and 2-component Gaussian fits ({n} rows)",
                  out / "pc_hist.png")

    # ---- markdown
    L = [f"# Slicing diagnostics: {flab} (D30)", "",
         f"{n} level-2 training player-seasons (top family {fid}, probability >= 0.6), 2024-25 + 2025-26. "
         f"{p} features (D31: dropped {', '.join(SPEC[c][2] for c in dropped)}), standardized with a scaler fitted "
         f"on these rows. Nothing named or chosen.", "",
         "## 1. Within-family PCA", "",
         "| | " + " | ".join(f"PC{j + 1}" for j in range(N_PCS)) + " |", "|---|" + "---|" * N_PCS,
         "| variance explained | " + " | ".join(f"{v:.1%}" for v in var[:N_PCS]) + " |",
         "| cumulative | " + " | ".join(f"{v:.1%}" for v in np.cumsum(var)[:N_PCS]) + " |", "",
         f"For reference, {p} uncorrelated features would give {1 / p:.1%} per PC.", "",
         f"Top {N_LOAD} loadings (sign convention: each PC's largest-magnitude loading is positive; a positive score "
         "means more of the positive-loading features and less of the negative ones):", "",
         "| PC | " + " | ".join(f"#{i + 1}" for i in range(N_LOAD)) + " |", "|---|" + "---|" * N_LOAD]
    for j in range(N_LOAD_PCS):
        top = np.argsort(-np.abs(comps[j]))[:N_LOAD]
        L.append(f"| PC{j + 1} | " + " | ".join(f"{SPEC[d['cols'][i]][2]} {comps[j, i]:+.2f}" for i in top) + " |")
    L += ["", "Full loadings: [loadings.csv](loadings.csv). Scatter: [pc_scatter.png](pc_scatter.png) (Pacers "
          "player-seasons ringed and labeled; Turner 2024-25 and Zubac seasons labeled when they are in this "
          "family's training rows).", ""]
    tzr = rows[tz]
    if len(tzr):
        L += ["| player-season | PC1 | PC2 |", "|---|---|---|"]
        for i in np.flatnonzero(tz):
            L.append(f"| {names[i]} | {scores[i, 0]:+.2f} | {scores[i, 1]:+.2f} |")
        L.append("")
    pd.DataFrame(comps[:N_PCS].T, index=[SPEC[c][2] for c in d["cols"]],
                 columns=[f"PC{j + 1}" for j in range(N_PCS)]).to_csv(out / "loadings.csv", float_format="%.4f")

    L += ["## 2. Slicing test", "", "### Diag sweep with the D31 features (k 1-6)", "",
          "Same init and checks as D26/D27 (20 starts, 50 bootstrap refits, held-out = fit 2024-25, score 2025-26). "
          "Stable = median bootstrap ARI >= 0.60 and no cluster under 70% kept. Diag candidate = lowest-BIC stable "
          "diag row. Tied k = 1 (one Gaussian with a full covariance) is shown as a reference row.", "",
          "| cov | k | BIC | params | held-out | boot ARI | season ARI | kept min | stable | |",
          "|---|---|---|---|---|---|---|---|---|---|"]
    for _, r in s.sort_values(["cov", "k"]).iterrows():
        tag = "diag candidate" if (r.cov_candidate and r["cov"] == "diag") else ("reference" if r["cov"] == "tied"
                                                                               else "")
        L.append(f"| {r['cov']} | {int(r.k)} | {r.bic:,.0f} | {int(r.n_params)} | {r.heldout_ll_per_row:.2f} | "
                 f"{r.ari_boot_median:.2f} | {r.ari_seasons:.2f} | {r.retention_min:.0%} | "
                 f"{'yes' if r.stable else 'no'} | {tag} |")
    L.append("")
    if ck:
        c = cand.iloc[0]
        L.append(f"Diag candidate: k = {ck} (BIC {c.bic:,.0f}; {c.bic - tied1.bic:+,.0f} vs tied k = 1 at "
                 f"{tied1.bic:,.0f}).")
    else:
        L.append("No stable diag row above k = 1.")
    L += ["", "Charts: [BIC](bic_by_k.png) · [held-out](heldout_ll_by_k.png) · [bootstrap ARI](bootstrap_ari_by_k.png) "
          "· [least stable cluster](retention_min_by_k.png) · [season ARI](season_ari_by_k.png) · [sweep.csv](sweep.csv)",
          "", "### Where the diag cluster centers sit", "",
          "Centers are the diag model's cluster means in the within-family standardized space. Between-centroid "
          "variance B = sum of weight x (center - weighted mean center)², as a matrix. **Along PCj** = share of B's "
          "total lying along PCj. **One-line share** = share of B along the centers' own first direction (1.00 = all "
          "centers on one straight line; always 1.00 at k = 2). **Angle** = angle between that line and PC1.", "",
          "| k | along PC1 | PC2 | PC3 | PC4 | PC5 | PC1 + PC2 | one-line share | angle to PC1 |",
          "|---|---|---|---|---|---|---|---|---|"]
    for sr in slice_rows:
        a = sr["spread"]["share_axis"]
        L.append(f"| {sr['k']} | " + " | ".join(f"{v:.0%}" for v in a) + f" | {a[:2].sum():.0%} | "
                 f"{sr['spread']['line_share']:.2f} | {sr['spread']['line_angle_pc1']:.0f}° |")
    L += ["", "Center positions on PC1 / PC2 (S1 = largest cluster):", "",
          "| k | cluster | members | weight | PC1 | PC2 |", "|---|---|---|---|---|---|"]
    for sr in slice_rows:
        for c in range(sr["k"]):
            L.append(f"| {sr['k']} | {sr['names'][c]} | {sr['sizes'][c]} | {sr['weights'][c]:.2f} | "
                     f"{sr['centers'][c, 0]:+.2f} | {sr['centers'][c, 1]:+.2f} |")
    L += ["", "Chart: [centroids.png](centroids.png)", "",
          "## 3. Multimodality", "",
          "1-D Gaussian mixture on each PC's scores (10 starts). BIC(2) − BIC(1) below 0 means 2 components fit "
          "better after the parameter penalty; above 0 means 1 component. Skewness of the PC scores is shown because a "
          "lopsided single hump can also be fitted better by 2 components.", "",
          "| PC | BIC 1 comp | BIC 2 comp | BIC(2) − BIC(1) | 2-comp weights | 2-comp means | 2-comp SDs | skewness |",
          "|---|---|---|---|---|---|---|---|"]
    for j, ft in enumerate(fits):
        t = ft[2]
        L.append(f"| PC{j + 1} | {ft[1]['bic']:,.1f} | {t['bic']:,.1f} | {t['bic'] - ft[1]['bic']:+.1f} | "
                 f"{t['weights'][0]:.2f} / {t['weights'][1]:.2f} | {t['means'][0]:+.2f} / {t['means'][1]:+.2f} | "
                 f"{t['sds'][0]:.2f} / {t['sds'][1]:.2f} | {skew(scores[:, j]):+.2f} |")
    L += ["", "Chart: [pc_hist.png](pc_hist.png)", ""]
    (out / "diagnostics.md").write_text("\n".join(L), encoding="utf-8")

    return {"fid": fid, "flab": flab, "n": n, "p": p, "var": var, "ck": ck, "cand": cand, "tied1": tied1,
            "slices": slice_rows, "fits": fits}


def write_index(summ: list[dict]) -> None:
    L = ["# D30 slicing diagnostics (pending Jonathan's choice)", "",
         "Per family: within-family PCA, diag sweep with the D31 features, where the diag cluster centers sit relative "
         "to the PCs, and 1 vs 2 component fits on PC1 and PC2. Numbers only; nothing named, chosen or packaged. "
         "Method: docs/METHODS.md section 7.", "",
         "| family | rows | features | PC1 / PC2 variance | diag candidate k | BIC vs tied k = 1 | along PC1 at k−1 / k / "
         "k+1 | one-line share at k−1 / k / k+1 | PC1 BIC(2)−BIC(1) | PC2 BIC(2)−BIC(1) | report |",
         "|---|---|---|---|---|---|---|---|---|---|---|"]
    for s in summ:
        sl = s["slices"]
        gap = f"{s['cand'].bic.iloc[0] - s['tied1'].bic:+,.0f}" if s["ck"] else "—"
        L.append(f"| {s['flab']} | {s['n']} | {s['p']} | {s['var'][0]:.1%} / {s['var'][1]:.1%} | {s['ck'] or '—'} | "
                 f"{gap} | " + " / ".join(f"k{x['k']} {x['spread']['share_axis'][0]:.0%}" for x in sl) + " | "
                 + " / ".join(f"k{x['k']} {x['spread']['line_share']:.2f}" for x in sl) + " | "
                 f"{s['fits'][0][2]['bic'] - s['fits'][0][1]['bic']:+.1f} | "
                 f"{s['fits'][1][2]['bic'] - s['fits'][1][1]['bic']:+.1f} | "
                 f"[diagnostics.md]({s['fid']}/diagnostics.md) |")
    L += ["", "Open per family: diagnostics.md, then pc_scatter.png, centroids.png, pc_hist.png.", ""]
    (SLC / "index.md").write_text("\n".join(L), encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--report-only", action="store_true")
    args = ap.parse_args()

    with open(OUT / "sweep.pkl", "rb") as fh:
        sw = pickle.load(fh)
    feats = pd.read_parquet(OUT / "features.parquet")
    feats_fit = sw["fit_index"].merge(feats, on=["season", "person_id"], how="left")
    X_raw = feats_fit[FEATURE_COLS].to_numpy(float)
    fr = level1(sw, sw["scaler"].transform(X_raw))     # loads the frozen model, stops on a hash mismatch
    labels = tl.family_labels(tl.load_names(NAMES_PATH, fr))
    pf_fit = tl.project(fr, X_raw)
    fd = {f: family_data(feats_fit, pf_fit, f) for f in range(pf_fit.shape[1])}

    spath = OUT / "slicing_sweep.pkl"
    if args.report_only:
        with open(spath, "rb") as fh:
            res = pickle.load(fh)
    else:
        res = run_sweep(fd, args.jobs)
        with open(spath, "wb") as fh:
            pickle.dump(res, fh)
    failed = [(f, ck, r.error) for f in res for ck, r in res[f].items() if not r.ok]
    if failed:
        for f, ck, e in failed:
            print(f"  F{f + 1} {ck}: failed: {e}")
        print("a fit failed: stop and ask")
        return 6

    summ = []
    for f in fd:
        s = write_family(f, labels[f], fd[f], res[f], SLC / f"F{f + 1}")
        summ.append(s)
        print(f"{labels[f]}: diag candidate k={s['ck']}; along PC1 "
              + ", ".join(f"k{x['k']} {x['spread']['share_axis'][0]:.2f}" for x in s["slices"])
              + f"; PC1/PC2 dBIC {s['fits'][0][2]['bic'] - s['fits'][0][1]['bic']:+.1f} / "
              f"{s['fits'][1][2]['bic'] - s['fits'][1][1]['bic']:+.1f}", flush=True)
    write_index(summ)
    print(f"index: {SLC / 'index.md'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
