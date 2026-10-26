"""Phase 2: two-level archetypes (D27, METHODS section 6). Numbers only: no names, no interpretation, nothing picked.

    python -u scripts/archetypes_families.py                 # freeze level 1 (first run only), sub-role sweeps, reports
    python -u scripts/archetypes_families.py --report-only   # reports from the saved sweep

Level 1 is the full-covariance k = 3 model from the D26 sweep (data/processed/archetypes/sweep.pkl). The first run
freezes it to models/archetypes/ and records its hashes in data/manifest.json; later runs load the frozen file and
stop if its hash no longer matches. Level 2 sweeps k 1-6 inside each family. Exit 5: a family excludes more than 15%
of its top-assigned rows at the 0.6 cut (ask Jonathan). Exit 6: a sub-role fit failed (ask Jonathan).

Writes models/archetypes/level1_full_k3.{pkl,json}, data/processed/archetypes/{families_sweep.pkl,
combined_weights_{set}.parquet} and reports/archetypes/families/ (packets per candidate set: rule, within diag).
"""
from __future__ import annotations

import argparse
import json
import pickle
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from joblib import Parallel, delayed  # noqa: E402
from sklearn.decomposition import PCA  # noqa: E402
from sklearn.preprocessing import StandardScaler  # noqa: E402

from archetypes_report import (IND, N_BORDER, N_TYPICAL, POSITIONS, SPEC, TURNER, ZUBAC, Fit, fmt,  # noqa: E402
                               mahalanobis, player_label, write_blind)
from pacersml.archetypes import plots  # noqa: E402
from pacersml.archetypes import twolevel as tl  # noqa: E402
from pacersml.archetypes.features import FEATURE_COLS, FEATURES, TRAINING, ZONE_LABEL, ZONES  # noqa: E402
from pacersml.archetypes.gmm import sweep_one  # noqa: E402
from pacersml.data import cache  # noqa: E402

OUT = cache.PROCESSED / "archetypes"
REPORTS = ROOT / "reports" / "archetypes"
FAM = REPORTS / "families"
MODELS = ROOT / "models" / "archetypes"
L1_PATH = MODELS / "level1_full_k3.pkl"
SIAKAM, HALIBURTON, NEMBHARD, WALKER = 1627783, 1630169, 1629614, 1641716
# D27 hypothesis-check players: (person_id, season or None for every training season)
CHECK_PLAYERS = [(TURNER, "2024-25"), (ZUBAC, None), (HALIBURTON, "2024-25"), (NEMBHARD, None), (WALKER, None),
                 (SIAKAM, None)]
STRADDLE = 0.7
N_PCA_LABELS = 15


def is_check(r) -> bool:
    return any(r.person_id == p and (s is None or r.season == s) for p, s in CHECK_PLAYERS)


def is_pacers(r) -> bool:
    return IND in r.team_id_list


# ---------------------------------------------------------------- level 1

def level1(sw: dict, X: np.ndarray) -> dict:
    """Freeze the D26 full k = 3 fit on first use; afterwards load it and check its hash against the manifest."""
    m = cache.load_manifest()
    if L1_PATH.exists():
        fr = tl.load(L1_PATH)
        want = m.get("archetype_model", {}).get("level1", {}).get("param_sha256")
        got = tl.param_hash(fr["model"], fr["scaler"])
        if want != got:
            raise SystemExit(f"frozen level-1 model hash {got[:12]} doesn't match the manifest ({str(want)[:12]})")
        return fr
    r = next(x for x in sw["results"] if x.cov == "full" and x.k == 3)
    order = np.argsort(-np.bincount(r.model.predict(X), minlength=3), kind="stable")
    meta = {"cov": "full", "k": 3, "decision": "D27", "training_seasons": TRAINING, "fit_rows": int(len(X)),
            "frozen_utc": datetime.now(timezone.utc).isoformat(timespec="seconds")}
    info = tl.freeze(L1_PATH, r.model, sw["scaler"], sw["features"], order, meta)
    params = {**meta, "features": sw["features"], "order": order.tolist(), "weights": r.model.weights_.tolist(),
              "means": r.model.means_.tolist(), "covariances": r.model.covariances_.tolist(),
              "scaler_mean": sw["scaler"].mean_.tolist(), "scaler_scale": sw["scaler"].scale_.tolist(),
              "reg_covar": r.model.reg_covar, "note": "order[F] = component index of family F+1 (families by size)"}
    (MODELS / "level1_full_k3.json").write_text(json.dumps(params, indent=1), encoding="utf-8")
    m["archetype_model"] = {"level1": {**info, **meta, "path": L1_PATH.relative_to(ROOT).as_posix(),
                                       "json": "models/archetypes/level1_full_k3.json"}}
    cache.save_manifest(m)
    print(f"level 1 frozen: {L1_PATH} (param hash {info['param_sha256'][:12]})", flush=True)
    return tl.load(L1_PATH)


# ---------------------------------------------------------------- level 2 sweep

def run_sweep(feats_fit: pd.DataFrame, X_raw: np.ndarray, pf: np.ndarray, jobs: int) -> dict:
    season = feats_fit.season.to_numpy()
    fams, work = {}, []
    for f in range(pf.shape[1]):
        m = tl.training_mask(pf, f)
        sc = StandardScaler().fit(X_raw[m])
        fams[f] = {"mask": m, "scaler": sc, "flags": tl.feature_flags(feats_fit[m], feats_fit, FEATURE_COLS),
                   "grid": tl.sweep_grid(int(m.sum()), X_raw.shape[1])}
        work += [(f, cov, k, sc.transform(X_raw[m]), season[m], X_raw[m]) for cov, k in fams[f]["grid"]]
    print(f"sub-role sweep: {len(work)} fits over {len(fams)} families", flush=True)
    out = Parallel(n_jobs=jobs, verbose=5)(delayed(sweep_one)(Xf, s, raw, cov, k, seed0=100 * (f + 1))
                                           for f, cov, k, Xf, s, raw in work)
    for (f, cov, k, *_), r in zip(work, out):
        fams[f].setdefault("results", {})[(cov, k)] = r
    return fams


def sweep_table(fam: dict) -> pd.DataFrame:
    n = int(fam["mask"].sum())
    rows = []
    for (cov, k), r in sorted(fam["results"].items(), key=lambda t: (t[0][0], t[0][1])):
        ret = r.retention if r.retention is not None else np.array([np.nan])
        rows.append({"cov": cov, "k": k, "ok": r.ok, "bic": r.bic, "n_params": r.n_params, "n_rows": n,
                     "heldout_ll_per_row": r.heldout_ll,
                     "ari_starts_median": np.median(r.ari_starts) if r.ari_starts else np.nan,
                     "ari_boot_median": np.median(r.ari_boot) if r.ari_boot else np.nan, "n_boot": len(r.ari_boot),
                     "ari_seasons": r.ari_seasons, "retention_min": np.nanmin(ret) if r.ok else np.nan,
                     "subroles_under_70": int((ret < 0.7).sum()) if r.ok else np.nan, "error": r.error})
    return tl.mark_candidate(pd.DataFrame(rows))


# ---------------------------------------------------------------- level 2 fit wrapper

class Sub:
    """One family sub-model at one (cov, k); sub-roles numbered by size within the family's training rows."""

    def __init__(self, f: int, result, scaler, Xf: np.ndarray):
        self.f, self.result, self.model, self.k, self.scaler = f, result, result.model, result.k, scaler
        p = self.model.predict_proba(Xf)
        self.order = np.argsort(-np.bincount(p.argmax(1), minlength=self.k), kind="stable")
        self.p = p[:, self.order]
        srt = np.argsort(-self.p, axis=1)
        self.top = srt[:, 0]
        self.second = srt[:, 1] if self.k > 1 else srt[:, 0]
        self.ptop = self.p[np.arange(len(Xf)), self.top]
        self.psecond = self.p[np.arange(len(Xf)), self.second] if self.k > 1 else np.zeros(len(Xf))
        self.names = [f"F{f + 1}-S{c + 1}" for c in range(self.k)]
        self.dist = np.column_stack([mahalanobis(self.model, Xf, self.order[c]) for c in range(self.k)])
        self.retention = result.retention[self.order] if result.retention is not None else np.full(self.k, np.nan)

    def project(self, raw: np.ndarray) -> np.ndarray:
        return self.model.predict_proba(self.scaler.transform(raw))[:, self.order]


# ---------------------------------------------------------------- family-level report

def family_report(f1: Fit, feats_fit: pd.DataFrame, X: np.ndarray, league_seconds: float, pf_all: pd.DataFrame,
                  exc: pd.DataFrame) -> None:
    FAM.mkdir(parents=True, exist_ok=True)
    write_blind(f1, X, feats_fit, league_seconds, FAM / "profiles_blind.md")
    p = FAM / "profiles_blind.md"
    p.write_text(p.read_text(encoding="utf-8").replace(
        "# Blind cluster profiles, k = 3 (full covariance)",
        "# Blind family profiles (level 1: full covariance, k = 3, frozen)").replace(
        "Clusters are numbered by size (C1 = largest); the numbers carry no meaning and are not matched across k.",
        "Families are numbered by size (F1 = largest); F1-F3 are C1-C3 of reports/archetypes/k3/."), encoding="utf-8")

    pos = feats_fit.position.fillna("?").replace("", "?")
    fam_lab = pd.Categorical([f1.names[t] for t in f1.top], f1.names)
    tab = pd.crosstab(fam_lab, pos)
    tab = tab.reindex(columns=[c for c in POSITIONS if c in tab.columns] + [c for c in tab.columns if c not in POSITIONS])
    plots.count_heatmap(tab, "Family x NBA listed position (counts; color = share of family)", "listed position",
                        "top family", FAM / "position_crosstab.png")
    plots.top_prob_hist(f1.top, f1.ptop, f1.names, FAM / "top_prob_hist.png")

    shares = tab.div(tab.sum(axis=1), axis=0)
    lines = ["# Level 1: families (full covariance, k = 3, frozen)", "",
             f"{len(X)} fitted player-seasons (500+ regular-season minutes, 2024-25 + 2025-26). Families F1-F3 are "
             "C1-C3 of the k = 3 packet (numbered by size). No names.", "",
             "Frozen model: `models/archetypes/level1_full_k3.pkl` (+ `.json` with every parameter); hashes in "
             "`data/manifest.json` under `archetype_model.level1`.", "",
             "## Family x listed position", "", "Counts (NBA playerindex position, current listing):", "",
             "| family | " + " | ".join(tab.columns) + " | total |", "|---|" + "---|" * (len(tab.columns) + 1)]
    for fam, r in tab.iterrows():
        lines.append(f"| {fam} | " + " | ".join(str(int(v)) for v in r) + f" | {int(r.sum())} |")
    lines += ["", "Row shares (share of the family in each listed position):", "",
              "| family | " + " | ".join(tab.columns) + " |", "|---|" + "---|" * len(tab.columns)]
    for fam, r in shares.iterrows():
        lines.append(f"| {fam} | " + " | ".join(f"{v:.0%}" for v in r) + " |")
    lines += ["", "Chart: [position_crosstab.png](position_crosstab.png)", "",
              "## Top family probability", "", "Chart: [top_prob_hist.png](top_prob_hist.png)", "",
              "| family | members | median top prob | under 0.9 | under 0.7 | under 0.6 |", "|---|---|---|---|---|---|"]
    for c in range(f1.k):
        q = f1.ptop[f1.top == c]
        lines.append(f"| {f1.names[c]} | {len(q)} | {np.median(q):.3f} | {(q < 0.9).sum()} | {(q < 0.7).sum()} | "
                     f"{(q < 0.6).sum()} |")
    df = feats_fit.assign(top=f1.top, ptop=f1.ptop, second=f1.second, psecond=f1.psecond,
                          minutes=(feats_fit.seconds / 60).round().astype(int))
    st = df[df.ptop < STRADDLE].sort_values("ptop")
    lines += ["", f"## Straddlers: every player-season with top family probability under {STRADDLE} ({len(st)})", "",
              "| player-season | minutes | position | top family | prob | second | prob |",
              "|---|---|---|---|---|---|---|"]
    for _, r in st.iterrows():
        lines.append(f"| {player_label(r)} | {r.minutes} | {r.position or '?'} | {f1.names[r.top]} | {r.ptop:.3f} | "
                     f"{f1.names[r.second]} | {r.psecond:.3f} |")
    lines += ["", "## Family probabilities for the hypothesis-check players", "",
              "| player-season | minutes | tier | " + " | ".join(f"P({n})" for n in f1.names) + " |",
              "|---|---|---|" + "---|" * f1.k]
    ck = pf_all[pf_all.apply(is_check, axis=1)].sort_values(["name", "season"])
    for _, r in ck.iterrows():
        lines.append(f"| {player_label(r)} | {int(r.seconds / 60)} | {r.tier} | "
                     + " | ".join(f"{r[f'P_{n}']:.3f}" for n in f1.names) + " |")
    lines += ["", "## Level-2 training sets (top family with probability >= 0.6)", "",
              "| family | top-assigned | training | excluded | excluded share | over 15%? |", "|---|---|---|---|---|---|"]
    for r in exc.itertuples():
        lines.append(f"| {r.family} | {r.top_assigned} | {r.training} | {r.excluded} | {r.excluded_share:.1%} | "
                     f"{'**yes**' if r.over_limit else 'no'} |")
    lines.append("")
    (FAM / "families.md").write_text("\n".join(lines), encoding="utf-8")


# ---------------------------------------------------------------- per-family reports

def write_flags(fname: str, flags: pd.DataFrame, path: Path) -> None:
    lines = [f"# Feature flags inside {fname} (before fitting)", "",
             "Flags (prompts for Jonathan, nothing dropped): **near-constant** = SD inside the family under 25% of the "
             "league SD, or over half the training rows exactly 0; **extremely skewed** = |skewness| > 2. Within-family "
             "standardization stretches every feature to SD 1, so a near-constant feature's noise counts as much as a "
             "real difference. All 17 features were kept for the sweep (no fit failed).", "",
             "| feature | family mean | family SD | league SD | SD ratio | share zero | skewness | flags | proposal |",
             "|---|---|---|---|---|---|---|---|---|"]
    for r in flags.itertuples():
        unit = SPEC[r.feature][3]
        prop = ""
        if "near-constant" in r.flags:
            prop = ("option: drop in this family. Reason: little spread here, so within-family z-scores mostly "
                    "measure noise. Option: keep, if the small differences are meaningful.")
        elif r.flags:
            prop = ("option: log-transform (log1p) or drop in this family. Reason: a few extreme rows dominate the "
                    "SD and can form their own sub-role. Option: keep, if those rows are a real role.")
        lines.append(f"| {SPEC[r.feature][2]} | {fmt(r.family_mean, unit)} | {fmt(r.family_sd, unit)} | "
                     f"{fmt(r.league_sd, unit)} | {r.sd_ratio:.2f} | {r.zero_share:.0%} | {r.skewness:+.2f} | "
                     f"{r.flags} | {prop} |")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_sweep_md(fname: str, s: pd.DataFrame, n: int, d: int, path: Path) -> None:
    full_max = [k for k in tl.SUB_KS if tl.n_params("full", k, d) < n / 2]
    lines = [f"# Sub-role sweep inside {fname}", "",
             f"{n} training player-seasons (top family {fname}, probability >= 0.6), features standardized with "
             f"{fname}'s own scaler. Covariance: tied and diag at k 1-6; full only where its parameter count is under "
             f"half the training rows ({n / 2:.0f}): "
             + (f"k = {', '.join(map(str, full_max))}." if full_max else
                f"none (full k = 1 already has {tl.n_params('full', 1, d)} parameters)."), "",
             "Same initialization and checks as D26: 20 starts (k-means init), 50 bootstrap refits, held-out = fit "
             "2024-25, score 2025-26 (own scaler), season ARI = 2024-25-only vs 2025-26-only model. At k = 1 every "
             "ARI and retention is 1 by construction.", "",
             "Selection rule (D27, marked here, not picked): BIC narrows; stable = median bootstrap ARI >= 0.60 and no "
             "sub-role under 70% kept; **candidate** = lowest-BIC stable row; naming breaks ties (rows within 10 BIC "
             "of the candidate that are also stable are marked *near tie*).", "",
             "| cov | k | BIC | params | held-out | starts ARI | boot ARI | season ARI | kept min | < 70% | stable | |",
             "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for _, r in s.sort_values(["cov", "k"]).iterrows():
        if not r.ok:
            lines.append(f"| {r['cov']} | {int(r.k)} | failed | | | | | | | | | {r.error[:60]} |")
            continue
        tag = " ".join(t for t, on in [("lowest BIC", r.bic_best), ("**candidate**", r.candidate),
                                       ("*near tie*", r.near_tie),
                                       (f"candidate within {r['cov']}", r.cov_candidate and not r.candidate)] if on)
        lines.append(f"| {r['cov']} | {int(r.k)} | {r.bic:,.0f} | {int(r.n_params)} | {r.heldout_ll_per_row:.2f} | "
                     f"{r.ari_starts_median:.2f} | {r.ari_boot_median:.2f} | {r.ari_seasons:.2f} | "
                     f"{r.retention_min:.0%} | {int(r.subroles_under_70)} | {'yes' if r.stable else 'no'} | {tag} |")
    c = s[s.candidate]
    lines += [""]
    if c.empty:
        lines.append("No stable row: no candidate.")
    else:
        c = c.iloc[0]
        lines.append(f"Candidate under the rule: **{c['cov']}, k = {int(c.k)}** (BIC {c.bic:,.0f})."
                     + (" k = 1 means no sub-structure inside this family under the rule." if c.k == 1 else ""))
        for _, w in s[s.cov_candidate & ~s.candidate].iterrows():
            lines.append(f"Same rule inside {w['cov']} only: {w['cov']}, k = {int(w.k)} (BIC {w.bic:,.0f}, "
                         f"{w.bic - c.bic:+,.0f} vs the candidate).")
        if c.k == 1 and c["cov"] == "tied":
            lines.append(f"Tied k = 1 is one Gaussian with a full covariance matrix ({int(c.n_params)} parameters vs "
                         f"{n} training rows); the D27 limit on full covariance (parameters under half the rows, "
                         f"{n / 2:.0f}) was written for full only and is not applied to it.")
    b = s[s.bic_best].iloc[0]
    lines.append(f"Lowest BIC overall in this family: {b['cov']}, k = {int(b.k)} (BIC {b.bic:,.0f}; "
                 f"{'stable' if b.stable else 'not stable'}).")
    lines += ["", "Charts: [BIC](bic_by_k.png) · [held-out](heldout_ll_by_k.png) · [bootstrap ARI](bootstrap_ari_by_k.png)"
              " · [least stable sub-role](retention_min_by_k.png) · [season ARI](season_ari_by_k.png) · "
              "[parameters](n_params_by_k.png) · [sweep.csv](sweep.csv)"]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_sub_blind(sub: Sub, Xf: np.ndarray, rows: pd.DataFrame, feats_fit: pd.DataFrame, league_seconds: float,
                    path: Path) -> None:
    cols = FEATURE_COLS
    fam_mean, league_mean = rows[cols].mean(), feats_fit[cols].mean()
    zone_cnt = rows[[f"{z}_share" for z in ZONES]].mul(rows.pbp_fga, axis=0)
    l_cnt = feats_fit[[f"{z}_share" for z in ZONES]].mul(feats_fit.pbp_fga, axis=0)
    fmix, lmix = zone_cnt.sum() / rows.pbp_fga.sum(), l_cnt.sum() / feats_fit.pbp_fga.sum()
    fname = f"F{sub.f + 1}"
    lines = [f"# Blind sub-role profiles: {fname}, k = {sub.k} ({sub.result.cov} covariance)", "",
             "No player names in this file. Sub-roles are numbered by size inside the family (S1 = largest); the "
             "numbers carry no meaning and are not matched across k.", "",
             f"- Training player-seasons in {fname}: {len(rows)} (top family {fname} with probability >= 0.6).",
             "- Members = training player-seasons whose most likely sub-role is this one.",
             f"- **within-family z**: members' mean of the feature standardized with {fname}'s own mean and SD.",
             f"- Real units: sub-role mean vs {fname} average (its training rows) vs league average (all 750 fitted "
             "player-seasons).",
             "- Share of league minutes: members' minutes ÷ all players' regular-season minutes in the two seasons.",
             ""]
    for c in range(sub.k):
        m = sub.top == c
        z = pd.Series(Xf[m].mean(0), index=cols)
        top6 = z.abs().sort_values(ascending=False).index[:6]
        mix = zone_cnt[m].sum() / rows.pbp_fga[m].sum()
        lines += [f"## {sub.names[c]}", "",
                  f"**Size:** {m.sum()} player-seasons ({m.mean():.1%} of {fname} training) · **share of {fname} "
                  f"minutes:** {rows.seconds[m].sum() / rows.seconds.sum():.1%} · **share of league minutes:** "
                  f"{rows.seconds[m].sum() / league_seconds:.1%} · median membership probability "
                  f"{np.median(sub.ptop[m]):.2f}, {np.mean(sub.ptop[m] < 0.6):.0%} of members under 0.6", "",
                  "**Six most distinguishing features** (largest |within-family z|):", "",
                  f"| feature | group | within-family z | sub-role | {fname} avg | league avg |",
                  "|---|---|---|---|---|---|"]
        for col in top6:
            _, grp, label, unit = SPEC[col]
            lines.append(f"| {label} | {grp} | {z[col]:+.2f} | {fmt(rows[col][m].mean(), unit)} | "
                         f"{fmt(fam_mean[col], unit)} | {fmt(league_mean[col], unit)} |")
        lines += ["", "**Shot-location mix** (share of FGA):", "",
                  "| | " + " | ".join(ZONE_LABEL[zn] for zn in ZONES) + " |", "|---|" + "---|" * len(ZONES),
                  "| sub-role | " + " | ".join(f"{mix[f'{zn}_share']:.0%}" for zn in ZONES) + " |",
                  f"| {fname} | " + " | ".join(f"{fmix[f'{zn}_share']:.0%}" for zn in ZONES) + " |",
                  "| league | " + " | ".join(f"{lmix[f'{zn}_share']:.0%}" for zn in ZONES) + " |", ""]
    path.write_text("\n".join(lines), encoding="utf-8")


def write_sub_players(sub: Sub, rows: pd.DataFrame, outside: pd.DataFrame, path: Path) -> None:
    df = rows.assign(top=sub.top, ptop=sub.ptop, second=sub.second, psecond=sub.psecond,
                     minutes=(rows.seconds / 60).round().astype(int))
    df["dist"] = sub.dist[np.arange(len(df)), sub.top]
    fname = f"F{sub.f + 1}"
    lines = [f"# Player reveal: {fname}, k = {sub.k} ({sub.result.cov} covariance)", "",
             "Same sub-role order as profiles_blind.md. Read that file first.", "",
             "- **Most typical:** highest sub-role probability; ties broken by smallest Mahalanobis distance to the "
             "sub-role center.",
             "- **Borderline:** members with top probability under 0.6, the 5 with the most minutes, with their "
             "second-most-likely sub-role.",
             f"- **Pacers:** every Pacers player-season (any IND minutes that season) in {fname}'s training set. "
             f"Pacers player-seasons whose top family is {fname} but under 0.6 are projected and listed separately.",
             ""]
    pac = df[df.apply(is_pacers, axis=1)]
    for c in range(sub.k):
        m = df[df.top == c]
        lines += [f"## {sub.names[c]} ({len(m)} player-seasons)", "", f"**{N_TYPICAL} most typical**", "",
                  "| # | player-season | minutes | prob | distance |", "|---|---|---|---|---|"]
        for i, (_, r) in enumerate(m.sort_values(["ptop", "dist"], ascending=[False, True]).head(N_TYPICAL).iterrows()):
            lines.append(f"| {i + 1} | {player_label(r)} | {r.minutes} | {r.ptop:.2f} | {r.dist:.2f} |")
        b = m[m.ptop < 0.6].sort_values("minutes", ascending=False).head(N_BORDER)
        lines += ["", f"**Borderline** ({int((m.ptop < 0.6).sum())} members under 0.6; {N_BORDER} with the most "
                  "minutes)", ""]
        if b.empty:
            lines.append("None.")
        else:
            lines += ["| player-season | minutes | prob | second sub-role | prob |", "|---|---|---|---|---|"]
            for _, r in b.iterrows():
                lines.append(f"| {player_label(r)} | {r.minutes} | {r.ptop:.2f} | {sub.names[r.second]} | "
                             f"{r.psecond:.2f} |")
        t = pac[pac.top == c].sort_values(["season", "minutes"], ascending=[True, False])
        lines += ["", "**Pacers player-seasons**", ""]
        if t.empty:
            lines.append("None.")
        else:
            lines += ["| player-season | minutes | prob | second | prob |", "|---|---|---|---|---|"]
            for _, r in t.iterrows():
                lines.append(f"| {player_label(r)} | {r.minutes} | {r.ptop:.2f} | {sub.names[r.second]} | "
                             f"{r.psecond:.2f} |")
        lines.append("")
    op = outside[outside.apply(is_pacers, axis=1)]
    lines += [f"## Pacers player-seasons with top family {fname} under 0.6 (not in training, projected)", ""]
    if op.empty:
        lines.append("None.")
    else:
        pp = sub.project(op[FEATURE_COLS].to_numpy(float))
        lines += ["| player-season | minutes | P(family) | top sub-role | prob |", "|---|---|---|---|---|"]
        for (_, r), q in zip(op.iterrows(), pp):
            lines.append(f"| {player_label(r)} | {int(r.seconds / 60)} | {r[f'P_{fname}']:.2f} | "
                         f"{sub.names[q.argmax()]} | {q.max():.2f} |")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_sub_stability(sub: Sub, n: int, path: Path) -> None:
    r = sub.result
    lines = [f"# Stability: F{sub.f + 1}, k = {sub.k} ({r.cov} covariance)", "",
             f"- **Starts:** {len(r.ari_starts)} seeds; ARI against the best: median {np.median(r.ari_starts):.3f}, "
             f"min {np.min(r.ari_starts):.3f}.",
             f"- **Bootstrap:** {len(r.ari_boot)} refits on resampled training player-seasons ({n}); ARI vs this fit: "
             f"median {np.median(r.ari_boot):.3f}, 10th–90th percentile {np.percentile(r.ari_boot, 10):.3f}–"
             f"{np.percentile(r.ari_boot, 90):.3f}.",
             f"- **Season-to-season:** ARI between a 2024-25-only and a 2025-26-only model: {r.ari_seasons:.3f}.",
             "- Player-seasons of the same player are resampled independently; bootstrap figures are somewhat "
             "optimistic.", "",
             "## Share of each sub-role's players who keep the same sub-role across bootstrap refits", "",
             "Flag: under 70%.", "", "| sub-role | members | kept | flag |", "|---|---|---|---|"]
    for c in range(sub.k):
        kept = sub.retention[c]
        lines.append(f"| {sub.names[c]} | {(sub.top == c).sum()} | {kept:.0%} | {'**under 70%**' if kept < 0.7 else ''} |")
    lines += ["", f"Sub-roles under 70%: {int((sub.retention < 0.7).sum())} of {sub.k}. Median bootstrap ARI "
              f"{'>=' if np.median(r.ari_boot) >= 0.6 else '<'} 0.60."]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def sub_charts(sub: Sub, Xf: np.ndarray, rows: pd.DataFrame, feats_fit: pd.DataFrame, out: Path) -> None:
    cols = FEATURE_COLS
    fname = f"F{sub.f + 1}"
    zmean = pd.DataFrame([Xf[sub.top == c].mean(0) for c in range(sub.k)], index=sub.names, columns=cols)
    plots.heatmap(zmean, [SPEC[c][1] for c in cols], [SPEC[c][2] for c in cols], out / "heatmap_features.png",
                  title=f"{fname} sub-roles x features: mean within-family z-score",
                  cbar=f"mean z-score vs {fname} training players")
    zc = rows[[f"{z}_share" for z in ZONES]].mul(rows.pbp_fga, axis=0)
    mix = pd.DataFrame([zc[sub.top == c].sum() / rows.pbp_fga[sub.top == c].sum() for c in range(sub.k)],
                       index=sub.names)
    mix.loc[fname] = zc.sum() / rows.pbp_fga.sum()
    lc = feats_fit[[f"{z}_share" for z in ZONES]].mul(feats_fit.pbp_fga, axis=0)
    mix.loc["league"] = lc.sum() / feats_fit.pbp_fga.sum()
    plots.shot_mix(mix, [ZONE_LABEL[z] for z in ZONES], out / "shot_mix.png")

    pca = PCA(2).fit(Xf)
    xy = pca.transform(Xf)
    best = rows.assign(i=np.arange(len(rows))).sort_values("pts", ascending=False).drop_duplicates("person_id")
    label_idx = best.head(N_PCA_LABELS).i.tolist()
    pacers = rows.apply(is_pacers, axis=1).to_numpy()
    label_idx += [i for i in np.flatnonzero(pacers | rows.apply(is_check, axis=1).to_numpy()) if i not in label_idx]
    names = [f"{n} {s[2:4]}-{s[5:]}" for n, s in zip(rows.name, rows.season)]
    plots.pca_map(xy, sub.top, sub.ptop, names, label_idx, pacers, tuple(pca.explained_variance_ratio_), sub.names,
                  out / "pca_map.png",
                  title=f"{fname} training player-seasons on the first two principal components (within-family z)")
    if sub.k > 1:
        nb = pd.crosstab(pd.Categorical([sub.names[t] for t in sub.top], sub.names),
                         pd.Categorical([sub.names[s] for s in sub.second], sub.names), dropna=False)
        plots.count_heatmap(nb, "Neighbors: top vs second-most-likely sub-role (counts; color = share of row)",
                            "second sub-role", "top sub-role", out / "neighbors.png")
    plots.top_prob_hist(sub.top, sub.ptop, sub.names, out / "top_prob_hist.png")


# ---------------------------------------------------------------- combined membership + hypothesis check

def packet_ks(k: int) -> list[int]:
    return [x for x in (k - 1, k, k + 1) if x in tl.SUB_KS]


def candidate_sets(tables: dict) -> dict[str, dict[int, tuple[str, int]]]:
    """'rule': the overall candidate per family (lowest-BIC stable row across covariance types). 'within {cov}': the
    same rule inside one covariance type, kept when it differs from 'rule' in at least one family."""
    sets = {"rule": {}}
    for f, s in tables.items():
        c = s[s.candidate].iloc[0]
        sets["rule"][f] = (c["cov"], int(c.k))
    for cov in sorted({c for s in tables.values() for c in s["cov"]}):
        within = {}
        for f, s in tables.items():
            c = s[s.cov_candidate & (s["cov"] == cov)]
            if c.empty:
                break
            within[f] = (cov, int(c.iloc[0].k))
        if len(within) == len(tables) and within != sets["rule"]:
            sets[f"within {cov}"] = within
    return sets


def combined_weights(feats: pd.DataFrame, fr: dict, pf_fit: np.ndarray, cand: dict[int, Sub]) -> pd.DataFrame:
    """Every training-season player-season, all tiers (D25 tier rule at both levels), one sub-model per family."""
    proj = feats.tier.isin(["fit", "low_sample"]) & feats[FEATURE_COLS].notna().all(axis=1)
    raw = feats.loc[proj, FEATURE_COLS].to_numpy(float)
    nf = len(cand)
    fam_share, sub_share = tl.unknown_shares(pf_fit, [cand[f].p for f in range(nf)])
    pf = np.tile(fam_share, (len(feats), 1))
    pf[proj.to_numpy()] = tl.project(fr, raw)
    subs = [np.tile(sub_share[f], (len(feats), 1)) for f in range(nf)]
    for f in range(nf):
        subs[f][proj.to_numpy()] = cand[f].project(raw)
    w = tl.combined(pf, subs)
    names = [n for f in range(nf) for n in cand[f].names]
    out = feats[["season", "person_id", "name", "teams", "seconds", "tier"]].copy()
    out["weights_from"] = np.where(proj, "projected", "shares")
    out["low_sample"] = out.tier == "low_sample"
    for f in range(nf):
        out[f"P_F{f + 1}"] = pf[:, f]
    for j, n in enumerate(names):
        out[f"W_{n}"] = w[:, j]
    out["weight_sum"] = w.sum(1)
    return out


def write_hypothesis(feats: pd.DataFrame, fr: dict, subs: dict, sets: dict, cws: dict, path: Path) -> None:
    """Combined weights for the check players under each candidate set; Turner vs Zubac at each packet k."""
    lines = ["# Hypothesis check: combined sub-role weights (reported, not used for selection)", "",
             "D27: this file is for interpretation only and does not override BIC -> stability -> naming. Sub-role k "
             "is not picked.", "",
             "Weight on sub-role s of family f = P(f) × P(s | f); P(s | f) from projecting the player into every "
             "family's sub-model with that family's scaler. Weights add to 1 across all sub-roles. Values under "
             "0.005 shown as ·. With k = 1 in a family, its single sub-role weight equals P(family)."]
    for name, st in sets.items():
        cw = cws[name]
        ck = cw[cw.apply(is_check, axis=1)].sort_values(["name", "season"])
        wcols = [c for c in cw.columns if c.startswith("W_")]
        lines += ["", f"## Candidate set: {name}", "",
                  ", ".join(f"F{f + 1}: {cov} k = {k}" for f, (cov, k) in st.items()), "",
                  "| player-season | minutes | " + " | ".join(c[2:] for c in wcols) + " | sum |",
                  "|---|---|" + "---|" * (len(wcols) + 1)]
        for _, r in ck.iterrows():
            lines.append(f"| {player_label(r)} | {int(r.seconds / 60)} | "
                         + " | ".join(f"{r[c]:.3f}" if r[c] >= 0.005 else "·" for c in wcols)
                         + f" | {r.weight_sum:.3f} |")

    raw = feats.set_index(["person_id", "season"])
    tz = [(p, s) for p, s in [(TURNER, "2024-25")] + [(ZUBAC, s) for s in TRAINING] if (p, s) in raw.index]
    pf = {ps: tl.project(fr, raw.loc[[ps], FEATURE_COLS].to_numpy(float))[0] for ps in tz}
    lines += ["", "## Turner 2024-25 vs Zubac: top sub-role at each packet k", "",
              "Each player projected into the sub-models of his top family at every packet (covariance type, k). "
              "'different' / 'same' = sub-roles of the family that is top for both; 'different families' = their top "
              "families differ; 'neither's top family' = projection into a family that is top for neither.", "",
              "| player-season | top family | P |", "|---|---|---|"]
    for ps in tz:
        q = pf[ps]
        lines.append(f"| {raw.loc[ps, 'name']} {ps[1]} | F{q.argmax() + 1} | {q.max():.3f} |")
    lines += ["", "| family | cov | k | " + " | ".join(f"{raw.loc[ps, 'name'].split()[-1]} {ps[1]}" for ps in tz)
              + " | Turner vs each Zubac season |", "|---|---|---|" + "---|" * (len(tz) + 1)]
    own = {int(q.argmax()) for q in pf.values()}   # only families that are top for Turner or Zubac
    for f in sorted(own):
        for (cov, k), sub in sorted(subs[f].items()):
            cells, tops = [], []
            for ps in tz:
                q = sub.project(raw.loc[[ps], FEATURE_COLS].to_numpy(float))[0]
                tops.append((pf[ps].argmax(), q.argmax()))
                cells.append(f"{sub.names[q.argmax()]} ({q.max():.2f})")
            cmp = []
            for (fz, sz), ps in zip(tops[1:], tz[1:]):
                if tops[0][0] != fz:
                    cmp.append(f"{ps[1]}: different families")
                elif tops[0][0] != f:
                    cmp.append(f"{ps[1]}: neither's top family")
                else:
                    cmp.append(f"{ps[1]}: {'different' if tops[0][1] != sz else 'same'}")
            lines.append(f"| F{f + 1} | {cov} | {k} | " + " | ".join(cells) + " | " + "; ".join(cmp) + " |")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_family_index(tables: dict, sets: dict, packets: dict, exc: pd.DataFrame) -> None:
    lines = ["# Two-level archetypes (D27)", "",
             "Level 1 frozen (full covariance, k = 3). Level 2 swept inside each family; nothing picked, no names.", "",
             "## Open first", "",
             "1. [families.md](families.md) and [profiles_blind.md](profiles_blind.md): level-1 families, position "
             "crosstab, straddlers, check players.",
             "2. Each family's sweep.md (candidates marked) and feature_flags.md.",
             "3. Each family's packets: profiles_blind.md first, then profiles_players.md, charts, stability.md.",
             "4. [hypothesis_check.md](hypothesis_check.md) last (reported only, not used to select).", "",
             "## Candidate sets", "",
             "- **rule**: lowest-BIC stable row across covariance types (D27 rule as written).",
             *[f"- **{n}**: the same rule inside {n.split()[-1]} covariance only." for n in sets if n != "rule"], "",
             "## Families", "",
             "| family | training rows | excluded (< 0.6) | lowest BIC | " + " | ".join(sets)
             + " | sweep | flags | packets |",
             "|---|---|---|---|" + "---|" * len(sets) + "---|---|---|"]
    for f, s in tables.items():
        e = exc.iloc[f]
        b = s[s.bic_best].iloc[0]
        d = f"F{f + 1}"
        pk = " · ".join(f"[{cov} k{k}]({d}/k{k}_{cov}/profiles_blind.md)" for cov, k in packets[f]) or "none"
        tr = " · ".join(f"[transitions {cov}]({d}/k_transitions_{cov}.png)" for cov in sorted({c for c, _ in packets[f]}))
        lines.append(f"| {d} | {e.training} | {e.excluded} ({e.excluded_share:.1%}) | {b['cov']}, k = {int(b.k)} | "
                     + " | ".join(f"{st[f][0]}, k = {st[f][1]}" for st in sets.values())
                     + f" | [sweep.md]({d}/sweep.md) | [feature_flags.md]({d}/feature_flags.md) | {pk} · {tr} |")
    lines += ["", "Combined weights for every training-season player-season (all tiers), one file per candidate set: "
              "`data/processed/archetypes/combined_weights_{set}.parquet` (not committed; regenerate with this "
              "script).", ""]
    (FAM / "index.md").write_text("\n".join(lines), encoding="utf-8")


def link_main_index() -> None:
    p = REPORTS / "index.md"
    s = p.read_text(encoding="utf-8")
    link = ("**Two-level archetypes (D27): [families/index.md](families/index.md)** — level-1 families (frozen full "
            "k = 3) and sub-role sweeps and packets inside each family.")
    if "families/index.md" not in s:
        head, rest = s.split("\n", 1)
        p.write_text(f"{head}\n\n{link}\n{rest}", encoding="utf-8")


# ---------------------------------------------------------------- main

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
    X = sw["scaler"].transform(X_raw)
    league_seconds = feats.seconds.sum()

    fr = level1(sw, X)
    pf_fit = tl.project(fr, X_raw)
    r3 = next(x for x in sw["results"] if x.cov == "full" and x.k == 3)
    f1 = Fit(r3, X, feats_fit)
    assert (f1.old == fr["order"]).all(), "family order differs from the k = 3 packet"
    f1.names = [f"F{c + 1}" for c in range(3)]
    exc = tl.exclusions(pf_fit)
    print(exc.to_string(index=False), flush=True)

    proj = feats.tier.isin(["fit", "low_sample"]) & feats[FEATURE_COLS].notna().all(axis=1)
    pf_all = feats.copy()
    for c in range(3):
        pf_all[f"P_F{c + 1}"] = np.nan
    pf_all.loc[proj, [f"P_F{c + 1}" for c in range(3)]] = tl.project(fr, feats.loc[proj, FEATURE_COLS].to_numpy(float))
    family_report(f1, feats_fit, X, league_seconds, pf_all, exc)
    if exc.over_limit.any():
        print("a family excludes more than 15% of its top-assigned player-seasons: stop and ask (D27)")
        return 5

    spath = OUT / "families_sweep.pkl"
    if args.report_only:
        with open(spath, "rb") as fh:
            fams = pickle.load(fh)
    else:
        fams = run_sweep(feats_fit, X_raw, pf_fit, args.jobs)
        with open(spath, "wb") as fh:
            pickle.dump(fams, fh)
    failed = [(f, ck, r.error) for f, fam in fams.items() for ck, r in fam["results"].items() if not r.ok]
    if failed:
        for f, ck, e in failed:
            print(f"  F{f + 1} {ck}: failed: {e}")
        print("a sub-role fit failed: stop and ask (D27)")
        return 6

    tables, data = {}, {}
    pf_fit_df = feats_fit.assign(**{f"P_F{c + 1}": pf_fit[:, c] for c in range(3)})
    for f, fam in fams.items():
        d = FAM / f"F{f + 1}"
        d.mkdir(parents=True, exist_ok=True)
        m = fam["mask"]
        data[f] = (pf_fit_df[m].reset_index(drop=True), fam["scaler"].transform(X_raw[m]),
                   pf_fit_df[(pf_fit.argmax(1) == f) & ~m])
        s = sweep_table(fam)
        tables[f] = s
        s.to_csv(d / "sweep.csv", index=False, float_format="%.4f")
        plots.sweep_plots(s, d, ks=tl.SUB_KS, prefix=f"F{f + 1}: ")
        write_sweep_md(f"F{f + 1}", s, int(m.sum()), X_raw.shape[1], d / "sweep.md")
        write_flags(f"F{f + 1}", fam["flags"], d / "feature_flags.md")

    sets = candidate_sets(tables)
    subs, packets = {f: {} for f in fams}, {f: [] for f in fams}
    for f, fam in fams.items():
        d = FAM / f"F{f + 1}"
        rows, Xf, outside = data[f]
        n = int(fam["mask"].sum())
        for cov in sorted({st[f][0] for st in sets.values()}):
            ks = sorted({x for st in sets.values() if st[f][0] == cov for x in packet_ks(st[f][1])})
            for kk in ks:
                sub = Sub(f, fam["results"][(cov, kk)], fam["scaler"], Xf)
                subs[f][(cov, kk)] = sub
                if kk == 1:
                    continue
                packets[f].append((cov, kk))
                kd = d / f"k{kk}_{cov}"
                kd.mkdir(parents=True, exist_ok=True)
                write_sub_blind(sub, Xf, rows, feats_fit, league_seconds, kd / "profiles_blind.md")
                write_sub_players(sub, rows, outside, kd / "profiles_players.md")
                write_sub_stability(sub, n, kd / "stability.md")
                sub_charts(sub, Xf, rows, feats_fit, kd)
            if len(ks) > 1:
                lv = [subs[f][(cov, kk)] for kk in ks]
                levels = [(x.k, x.names, np.bincount(x.top, minlength=x.k)) for x in lv]
                flows = [pd.crosstab(a.top, b.top).reindex(index=range(a.k), columns=range(b.k), fill_value=0)
                         .to_numpy() for a, b in zip(lv[:-1], lv[1:])]
                plots.transitions(levels, flows, d / f"k_transitions_{cov}.png")
        print(f"F{f + 1}: " + "; ".join(f"{nm} {st[f][0]} k={st[f][1]}" for nm, st in sets.items())
              + f"; packets {packets[f]}", flush=True)

    cws = {}
    for name, st in sets.items():
        cw = combined_weights(feats, fr, pf_fit, {f: subs[f][st[f]] for f in fams})
        assert np.allclose(cw.weight_sum, 1), "combined weights don't add to 1"
        cw.to_parquet(OUT / f"combined_weights_{name.replace(' ', '_')}.parquet", index=False)
        cws[name] = cw
    write_hypothesis(feats, fr, subs, sets, cws, FAM / "hypothesis_check.md")
    write_family_index(tables, sets, packets, exc)
    link_main_index()
    print(f"index: {FAM / 'index.md'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
