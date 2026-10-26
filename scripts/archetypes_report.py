"""Phase 2: cluster-naming packets for candidate k (D25). Numbers only: no cluster names, no interpretation.

    python -u scripts/archetypes_report.py              # the two lowest-BIC covariance types, BIC-best k +- 1 each
    python -u scripts/archetypes_report.py --covs tied

Reads data/processed/archetypes/{features.parquet, sweep.pkl} (from archetypes_fit.py). Writes, per k,
reports/archetypes/k{K}/: profiles_blind.md, profiles_players.md, stability.md and six charts; plus
reports/archetypes/k_transitions.png (first set; k_transitions_{cov}.png after it) and index.md.
"""
from __future__ import annotations

import argparse
import pickle
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from sklearn.decomposition import PCA  # noqa: E402

from pacersml.archetypes import plots  # noqa: E402
from pacersml.archetypes.features import FEATURES, ZONE_LABEL, ZONES  # noqa: E402
from pacersml.data import cache  # noqa: E402

OUT = cache.PROCESSED / "archetypes"
REPORTS = ROOT / "reports" / "archetypes"
IND = 1610612754
TURNER, ZUBAC = 1626167, 1627826
POSITIONS = ["G", "G-F", "F-G", "F", "F-C", "C-F", "C"]
N_TYPICAL, N_NEAREST, N_BORDER, N_LABELS = 10, 8, 5, 30
SPEC = {f[0]: f for f in FEATURES}


def fmt(v: float, unit: str) -> str:
    if unit == "pct":
        return f"{100 * v:.1f}%"
    if unit == "ratio":
        return f"{v:.2f}"
    return f"{v:.1f}"


def mahalanobis(model, X: np.ndarray, c: int) -> np.ndarray:
    d = X - model.means_[c]
    cov = {"full": lambda: model.covariances_[c], "tied": lambda: model.covariances_,
           "diag": lambda: np.diag(model.covariances_[c]),
           "spherical": lambda: np.eye(X.shape[1]) * model.covariances_[c]}[model.covariance_type]()
    return np.sqrt(np.einsum("ij,jk,ik->i", d, np.linalg.inv(cov), d))


class Fit:
    """One candidate model, clusters renumbered C1..Ck by size (largest first)."""

    def __init__(self, result, X: np.ndarray, rows: pd.DataFrame):
        self.result, self.model, self.k = result, result.model, result.k
        raw_p = self.model.predict_proba(X)
        raw_top = raw_p.argmax(1)
        order = np.argsort(-np.bincount(raw_top, minlength=self.k), kind="stable")  # new c -> old c
        self.old = order
        self.p = raw_p[:, order]
        srt = np.argsort(-self.p, axis=1)
        self.top, self.second = srt[:, 0], srt[:, 1]
        self.ptop = self.p[np.arange(len(X)), self.top]
        self.psecond = self.p[np.arange(len(X)), self.second]
        self.names = [f"C{c + 1}" for c in range(self.k)]
        self.dist = np.column_stack([mahalanobis(self.model, X, order[c]) for c in range(self.k)])
        self.retention = result.retention[order] if result.retention is not None else np.full(self.k, np.nan)
        self.rows = rows


def candidate_set(sweep: pd.DataFrame, cov: str) -> tuple[list[int], int]:
    """The covariance type's BIC-best k and one either side (kept inside the range at its edges)."""
    ok = sweep[sweep.ok]
    kb = int(ok[ok["cov"] == cov].sort_values("bic").iloc[0].k)
    lo, hi = int(ok.k.min()), int(ok.k.max())
    centre = min(max(kb, lo + 1), hi - 1)
    return [centre - 1, centre, centre + 1], kb


def default_sets(sweep: pd.DataFrame) -> list[str]:
    """The two covariance types with the lowest BIC, best first."""
    return list(sweep[sweep.ok].groupby("cov").bic.min().sort_values().index[:2])


def player_label(r) -> str:
    return f"{r['name']} ({r['teams']}, {r['season']})"


def write_blind(f: Fit, X: np.ndarray, feats_fit: pd.DataFrame, league_seconds: float, path: Path) -> None:
    cols = [c for c, *_ in FEATURES]
    raw = feats_fit[cols]
    league = raw.mean()
    zone_cnt = feats_fit[[f"{z}_share" for z in ZONES]].mul(feats_fit.pbp_fga, axis=0)
    lmix = zone_cnt.sum() / feats_fit.pbp_fga.sum()
    lines = [f"# Blind cluster profiles, k = {f.k} ({f.result.cov} covariance)", "",
             "No player names in this file. Clusters are numbered by size (C1 = largest); the numbers carry no "
             "meaning and are not matched across k.", "",
             f"- Fitted player-seasons: {len(X)} (500+ regular-season minutes, 2024-25 and 2025-26).",
             "- Members = player-seasons whose most likely archetype is this one (hard assignment).",
             "- z-scores: members' mean of the standardized feature (SD units against all fitted player-seasons). "
             "League average = mean over fitted player-seasons.",
             "- Share of league minutes: members' regular-season minutes ÷ all players' regular-season minutes in "
             "the two seasons (players under 500 minutes are in no cluster).",
             "- Shot-location mix: all members' FGA pooled.", ""]
    for c in range(f.k):
        m = f.top == c
        z = pd.Series(X[m].mean(0), index=cols)
        top6 = z.abs().sort_values(ascending=False).index[:6]
        mins = feats_fit.seconds[m].sum()
        mix = zone_cnt[m].sum() / feats_fit.pbp_fga[m].sum()
        lines += [f"## {f.names[c]}", "",
                  f"**Size:** {m.sum()} player-seasons ({m.mean():.1%} of fitted) · **share of league minutes:** "
                  f"{mins / league_seconds:.1%} · median membership probability {np.median(f.ptop[m]):.2f}, "
                  f"{np.mean(f.ptop[m] < 0.6):.0%} of members under 0.6", "",
                  "**Six most distinguishing features** (largest |mean z|):", "",
                  "| feature | group | mean z | cluster | league |", "|---|---|---|---|---|"]
        for col in top6:
            _, grp, label, unit = SPEC[col]
            lines.append(f"| {label} | {grp} | {z[col]:+.2f} | {fmt(raw[col][m].mean(), unit)} | "
                         f"{fmt(league[col], unit)} |")
        lines += ["", "**Shot-location mix** (share of FGA):", "",
                  "| | " + " | ".join(ZONE_LABEL[zn] for zn in ZONES) + " |",
                  "|---|" + "---|" * len(ZONES),
                  "| cluster | " + " | ".join(f"{mix[f'{zn}_share']:.0%}" for zn in ZONES) + " |",
                  "| league | " + " | ".join(f"{lmix[f'{zn}_share']:.0%}" for zn in ZONES) + " |", ""]
    path.write_text("\n".join(lines), encoding="utf-8")


def tracked(r) -> bool:
    return IND in r.team_id_list or (r.person_id == TURNER and r.season == "2024-25") or r.person_id == ZUBAC


def write_players(f: Fit, feats_fit: pd.DataFrame, path: Path) -> None:
    df = feats_fit.assign(top=f.top, ptop=f.ptop, second=f.second, psecond=f.psecond,
                          minutes=(feats_fit.seconds / 60).round().astype(int))
    df["dist"] = f.dist[np.arange(len(df)), f.top]
    lines = [f"# Player reveal, k = {f.k} ({f.result.cov} covariance)", "",
             "Same cluster order as profiles_blind.md. Read that file first.", "",
             "- **Most typical:** highest membership probability; ties (many are 1.00) broken by smallest "
             "Mahalanobis distance to the cluster center (in SDs of that cluster's own shape).",
             "- **8 nearest the center:** smallest Mahalanobis distance to the cluster center, whatever their top "
             "archetype.",
             "- **Borderline:** members whose top probability is under 0.6, the 5 with the most minutes, with their "
             "second-most-likely archetype.",
             "- **Tracked:** every Pacers player-season (any minutes for IND that season) in the cluster, plus Myles "
             "Turner 2024-25 and every Ivica Zubac season. Training seasons only (2026-27 is not projected until "
             "the model is frozen). Players under 500 minutes aren't fitted and don't appear.", "",
             "## Tracked players at a glance", "", "| player-season | minutes | top archetype | prob | second | prob |",
             "|---|---|---|---|---|---|"]
    tr = df[df.apply(tracked, axis=1)].sort_values(["season", "minutes"], ascending=[True, False])
    for _, r in tr.iterrows():
        lines.append(f"| {player_label(r)} | {r.minutes} | {f.names[r.top]} | {r.ptop:.2f} | {f.names[r.second]} | "
                     f"{r.psecond:.2f} |")
    lines.append("")
    for c in range(f.k):
        m = df[df.top == c]
        lines += [f"## {f.names[c]} ({len(m)} player-seasons)", "", "**10 most typical**", "",
                  "| # | player-season | minutes | prob | distance |", "|---|---|---|---|---|"]
        for i, (_, r) in enumerate(m.sort_values(["ptop", "dist"], ascending=[False, True]).head(N_TYPICAL).iterrows()):
            lines.append(f"| {i + 1} | {player_label(r)} | {r.minutes} | {r.ptop:.2f} | {r.dist:.2f} |")
        lines += ["", f"**{N_NEAREST} nearest the center** (Mahalanobis distance under this cluster's shape, members "
                  "and non-members)", "", "| # | player-season | minutes | distance | top archetype | prob |",
                  "|---|---|---|---|---|---|"]
        near = df.assign(dc=f.dist[:, c]).sort_values("dc").head(N_NEAREST)
        for i, (_, r) in enumerate(near.iterrows()):
            lines.append(f"| {i + 1} | {player_label(r)} | {r.minutes} | {r.dc:.2f} | {f.names[r.top]} | {r.ptop:.2f} |")
        b = m[m.ptop < 0.6].sort_values("minutes", ascending=False).head(N_BORDER)
        lines += ["", f"**Borderline** ({int((m.ptop < 0.6).sum())} members under 0.6; 5 with the most minutes)", ""]
        if b.empty:
            lines.append("None.")
        else:
            lines += ["| player-season | minutes | prob | second archetype | prob |", "|---|---|---|---|---|"]
            for _, r in b.iterrows():
                lines.append(f"| {player_label(r)} | {r.minutes} | {r.ptop:.2f} | {f.names[r.second]} | "
                             f"{r.psecond:.2f} |")
        t = tr[tr.top == c]
        lines += ["", "**Tracked players in this cluster**", ""]
        if t.empty:
            lines.append("None.")
        else:
            lines += ["| player-season | minutes | prob | second | prob |", "|---|---|---|---|---|"]
            for _, r in t.iterrows():
                lines.append(f"| {player_label(r)} | {r.minutes} | {r.ptop:.2f} | {f.names[r.second]} | "
                             f"{r.psecond:.2f} |")
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def write_stability(f: Fit, path: Path) -> None:
    r = f.result
    lines = [f"# Stability, k = {f.k} ({r.cov} covariance)", "",
             f"- **Starts:** {len(r.ari_starts)} fits from different seeds; ARI of each against the best: median "
             f"{np.median(r.ari_starts):.3f}, min {np.min(r.ari_starts):.3f}.",
             f"- **Bootstrap:** {len(r.ari_boot)} refits on resampled player-seasons, clusters matched to this fit by "
             f"center distance; ARI vs this fit: median {np.median(r.ari_boot):.3f}, 10th–90th percentile "
             f"{np.percentile(r.ari_boot, 10):.3f}–{np.percentile(r.ari_boot, 90):.3f}.",
             f"- **Season-to-season:** ARI between a 2024-25-only and a 2025-26-only model labelling all rows: "
             f"{r.ari_seasons:.3f}.",
             "- The same player appears in both seasons, so resampling player-seasons treats them as independent; "
             "the bootstrap figures are somewhat optimistic.", "",
             "## Share of each cluster's players who keep the same archetype across bootstrap refits", "",
             "Flag: under 70%.", "", "| cluster | members | kept | flag |", "|---|---|---|---|"]
    for c in range(f.k):
        kept = f.retention[c]
        lines.append(f"| {f.names[c]} | {(f.top == c).sum()} | {kept:.0%} | {'**under 70%**' if kept < 0.7 else ''} |")
    lines += ["", f"Clusters under 70%: {int((f.retention < 0.7).sum())} of {f.k}."]
    path.write_text("\n".join(lines), encoding="utf-8")


def charts(f: Fit, X: np.ndarray, feats_fit: pd.DataFrame, out: Path) -> None:
    cols = [c for c, *_ in FEATURES]
    zmean = pd.DataFrame([X[f.top == c].mean(0) for c in range(f.k)], index=f.names, columns=cols)
    plots.heatmap(zmean, [SPEC[c][1] for c in cols], [SPEC[c][2] for c in cols], out / "heatmap_features.png")

    zone_cnt = feats_fit[[f"{z}_share" for z in ZONES]].mul(feats_fit.pbp_fga, axis=0)
    mix = pd.DataFrame([zone_cnt[f.top == c].sum() / feats_fit.pbp_fga[f.top == c].sum() for c in range(f.k)],
                       index=f.names)
    mix.loc["league"] = zone_cnt.sum() / feats_fit.pbp_fga.sum()
    plots.shot_mix(mix, [ZONE_LABEL[z] for z in ZONES], out / "shot_mix.png")

    pca = PCA(2).fit(X)
    xy = pca.transform(X)
    best = feats_fit.assign(i=np.arange(len(X))).sort_values("pts", ascending=False).drop_duplicates("person_id")
    label_idx = best.head(N_LABELS).i.tolist()
    pacers = feats_fit.team_id_list.apply(lambda t: IND in t).to_numpy()
    label_idx += [i for i in np.flatnonzero(pacers & (feats_fit.seconds.to_numpy() >= 1500 * 60)) if i not in label_idx]
    names = [f"{n} {s[2:4]}-{s[5:]}" for n, s in zip(feats_fit.name, feats_fit.season)]
    plots.pca_map(xy, f.top, f.ptop, names, label_idx, pacers, tuple(pca.explained_variance_ratio_), f.names,
                  out / "pca_map.png")

    pos = feats_fit.position.fillna("?").replace("", "?")
    tab = pd.crosstab(pd.Categorical([f.names[t] for t in f.top], f.names), pos)
    tab = tab.reindex(columns=[p for p in POSITIONS if p in tab.columns] + [p for p in tab.columns if p not in POSITIONS])
    plots.count_heatmap(tab, "Cluster x NBA listed position (counts; color = share of cluster)", "listed position",
                        "top archetype", out / "position_crosstab.png")

    nb = pd.crosstab(pd.Categorical([f.names[t] for t in f.top], f.names),
                     pd.Categorical([f.names[s] for s in f.second], f.names), dropna=False)
    plots.count_heatmap(nb, "Neighbors: top vs second-most-likely archetype (counts; color = share of row)",
                        "second archetype", "top archetype", out / "neighbors.png")
    plots.top_prob_hist(f.top, f.ptop, f.names, out / "top_prob_hist.png")


def write_index(sweep: pd.DataFrame, sets: list[tuple[str, list[int], int, str]], best_overall, n_rows: int) -> None:
    lines = ["# Archetype model: sweep and naming packets (Phase 2)", "",
             f"{n_rows} player-seasons (500+ regular-season minutes, 2024-25 + 2025-26), 17 style features (D25), "
             "Gaussian mixture, k 2–15 × full / tied / diag covariance. Nothing here picks k.", "",
             f"- Lowest BIC overall: **{best_overall['cov']}, k = {int(best_overall.k)}** "
             f"(BIC {best_overall.bic:,.0f}).",
             *[f"- Packet set {i + 1}: **{cov}** covariance, k = {', '.join(map(str, ks))} (BIC-best k for {cov} "
               f"is {kb}" + (", at the edge of the range" if kb in (2, 15) else "") + ")."
               for i, (cov, ks, kb, _) in enumerate(sets)],
             "- Elbow (kneedle on each BIC curve): "
             + ", ".join(f"{r['cov']} k = {int(r.k)}" for _, r in sweep[sweep.elbow].iterrows()) + ".", "",
             "## Open first", "",
             "1. Each k's **profiles_blind.md** (no player names): write provisional names before looking at players.",
             "2. Then its **profiles_players.md**, the charts and **stability.md**.", "",
             "## Packets", "",
             "| set | covariance | k | blind profiles | player reveal | stability | heatmap | shot mix | PCA map "
             "| positions | neighbors | top-prob histogram |",
             "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for i, (cov, ks, kb, _) in enumerate(sets):
        for k in ks:
            d = f"k{k}"
            lines.append(f"| {i + 1} | {cov} | {k} | [profiles_blind.md]({d}/profiles_blind.md) | "
                         f"[profiles_players.md]({d}/profiles_players.md) | [stability.md]({d}/stability.md) | "
                         f"[png]({d}/heatmap_features.png) | [png]({d}/shot_mix.png) | [png]({d}/pca_map.png) | "
                         f"[png]({d}/position_crosstab.png) | [png]({d}/neighbors.png) | [png]({d}/top_prob_hist.png) |")
    lines += [""] + [f"Across k, {cov}: [{tf}]({tf}) (k = {' → '.join(map(str, ks))})." for cov, ks, _, tf in sets]
    lines += ["",
              "## Sweep charts", "",
              "[BIC](bic_by_k.png) · [held-out log-likelihood](heldout_ll_by_k.png) · "
              "[bootstrap ARI](bootstrap_ari_by_k.png) · [least stable cluster](retention_min_by_k.png) · "
              "[season-to-season ARI](season_ari_by_k.png) · [parameter count](n_params_by_k.png) · "
              "full table [sweep.csv](sweep.csv)", "",
              "## BIC and diagnostics for every k", "",
              "BIC: lower is better. Held-out: mean log-likelihood per 2025-26 row of a model fitted on 2024-25 "
              "(higher is better). Starts ARI: median agreement of 20 seeds with the best. Boot ARI: median over 50 "
              "bootstrap refits. Season ARI: 2024-25-only vs 2025-26-only model. Kept min: least stable cluster's "
              "share of players kept. < 70%: clusters under 70% kept.", ""]
    for cv in ["full", "tied", "diag"]:
        s = sweep[sweep["cov"] == cv].sort_values("k")
        lines += [f"### {cv}", "", "| k | BIC | params | held-out | starts ARI | boot ARI | season ARI | kept min | < 70% | |",
                  "|---|---|---|---|---|---|---|---|---|---|"]
        for _, r in s.iterrows():
            if not r.ok:
                lines.append(f"| {int(r.k)} | failed | | | | | | | | {r.error[:60]} |")
                continue
            packet = any(cv == c and r.k in ks for c, ks, _, _ in sets)
            tag = " ".join(t for t, on in [("lowest BIC", r.bic == s[s.ok].bic.min()), ("elbow", r.elbow),
                                           ("packet", packet)] if on)
            lines.append(f"| {int(r.k)} | {r.bic:,.0f} | {int(r.n_params)} | {r.heldout_ll_per_row:.2f} | "
                         f"{r.ari_starts_median:.2f} | {r.ari_boot_median:.2f} | {r.ari_seasons:.2f} | "
                         f"{r.retention_min:.0%} | {int(r.clusters_under_70)} | {tag} |")
        lines.append("")
    (REPORTS / "index.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--covs", nargs="+", choices=["full", "tied", "diag"],
                    help="covariance types to make packets for (default: the two with the lowest BIC)")
    args = ap.parse_args()

    with open(OUT / "sweep.pkl", "rb") as fh:
        sw = pickle.load(fh)
    feats = pd.read_parquet(OUT / "features.parquet")
    sweep = pd.read_csv(REPORTS / "sweep.csv")
    feats_fit = sw["fit_index"].merge(feats, on=["season", "person_id"], how="left")
    X = sw["scaler"].transform(feats_fit[sw["features"]].to_numpy(float))
    league_seconds = feats.seconds.sum()
    best_overall = sweep[sweep.ok].loc[sweep[sweep.ok].bic.idxmin()]
    res = {(r.cov, r.k): r for r in sw["results"]}

    sets, used = [], set()
    for i, cov in enumerate(args.covs or default_sets(sweep)):
        ks, kb = candidate_set(sweep, cov)
        if used & set(ks):
            raise SystemExit(f"k {sorted(used & set(ks))} already has a packet from another covariance type")
        used |= set(ks)
        fits = {}
        for k in ks:
            f = Fit(res[(cov, k)], X, feats_fit)
            fits[k] = f
            d = REPORTS / f"k{k}"
            d.mkdir(parents=True, exist_ok=True)
            write_blind(f, X, feats_fit, league_seconds, d / "profiles_blind.md")
            write_players(f, feats_fit, d / "profiles_players.md")
            write_stability(f, d / "stability.md")
            charts(f, X, feats_fit, d)
            print(f"{cov} k{k}: {d}", flush=True)
        levels = [(k, fits[k].names, np.bincount(fits[k].top, minlength=k)) for k in ks]
        flows = [pd.crosstab(fits[a].top, fits[b].top).reindex(index=range(a), columns=range(b), fill_value=0)
                 .to_numpy() for a, b in zip(ks[:-1], ks[1:])]
        tf = "k_transitions.png" if i == 0 else f"k_transitions_{cov}.png"
        plots.transitions(levels, flows, REPORTS / tf)
        sets.append((cov, ks, kb, tf))
    write_index(sweep, sets, best_overall, len(X))
    print(f"index: {REPORTS / 'index.md'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
