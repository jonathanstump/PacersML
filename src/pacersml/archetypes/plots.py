"""Diagnostic charts for the archetype sweep and the naming packets (PNG, one chart per file). Numbers only."""
from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from matplotlib.colors import LinearSegmentedColormap  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.patches import Patch, PathPatch  # noqa: E402
from matplotlib.path import Path as MPath  # noqa: E402

# reference palette (light mode): categorical order, sequential blue, diverging blue <-> gray <-> red, chrome
SERIES = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#6250d6", "#e34948"]
SURFACE, INK, INK2, MUTED, GRID, AXIS = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7"
SEQ = LinearSegmentedColormap.from_list("seq", ["#fcfcfb", "#cde2fb", "#86b6ef", "#3987e5", "#1c5cab", "#0d366b"])
DIV = LinearSegmentedColormap.from_list("div", ["#1c5cab", "#86b6ef", "#f0efec", "#f0a3a2", "#c23534"])
MARKERS = ["o", "s", "^", "D"]   # clusters beyond 8 reuse colors with a second marker shape

plt.rcParams.update({
    "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE,
    "font.family": ["Segoe UI", "DejaVu Sans"], "font.size": 9, "text.color": INK,
    "axes.edgecolor": AXIS, "axes.labelcolor": INK2, "axes.titlesize": 11, "axes.titleweight": "bold",
    "axes.titlelocation": "left", "axes.spines.top": False, "axes.spines.right": False,
    "xtick.color": MUTED, "ytick.color": MUTED, "axes.grid": False, "grid.color": GRID, "grid.linewidth": 0.6,
    "legend.frameon": False,
})


def color(c: int) -> str:
    return SERIES[c % len(SERIES)]


def marker(c: int) -> str:
    return MARKERS[(c // len(SERIES)) % len(MARKERS)]


def _save(fig, path: Path) -> None:
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)


# ---------------------------------------------------------------- sweep

def _by_k(sweep: pd.DataFrame, col: str, title: str, ylabel: str, path: Path, ref: float | None = None,
          mark_elbow: bool = False, ks=range(2, 16)) -> None:
    fig, ax = plt.subplots(figsize=(7.5, 4.2))
    ax.grid(axis="y")
    for i, cov in enumerate(["full", "tied", "diag"]):
        s = sweep[(sweep["cov"] == cov) & sweep.ok].sort_values("k")
        if s.empty:
            continue
        ax.plot(s.k, s[col], color=SERIES[i], lw=2, marker="o", ms=4, label=cov)
        last = s.iloc[-1]
        ax.annotate(cov, (last.k, last[col]), xytext=(6, 0), textcoords="offset points", va="center",
                    color=INK2, fontsize=9)
        if mark_elbow and "elbow" in s and s.elbow.any():
            e = s[s.elbow].iloc[0]
            ax.plot(e.k, e[col], marker="o", ms=10, mfc="none", mec=INK, mew=1.2)
            ax.annotate(f"elbow k={int(e.k)}", (e.k, e[col]), xytext=(0, 10), textcoords="offset points",
                        ha="center", fontsize=8, color=INK2)
    if ref is not None:
        ax.axhline(ref, color=MUTED, lw=1, ls="--")
    ax.set_xticks(list(ks))
    ax.set_xlabel("k (clusters)")
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.legend(loc="best", fontsize=8)
    _save(fig, path)


def sweep_plots(sweep: pd.DataFrame, out: Path, ks=range(2, 16), prefix: str = "") -> None:
    n = int(sweep.n_rows.iloc[0])
    kw = {"ks": ks}
    _by_k(sweep, "bic", f"{prefix}BIC by k (lower is better; {n} player-seasons)", "BIC", out / "bic_by_k.png",
          mark_elbow=True, **kw)
    _by_k(sweep, "heldout_ll_per_row", f"{prefix}Held-out log-likelihood: fit 2024-25, score 2025-26 (higher is "
          "better)", "mean log-likelihood per 2025-26 row", out / "heldout_ll_by_k.png", **kw)
    _by_k(sweep, "ari_boot_median", f"{prefix}Bootstrap stability: median ARI vs main fit (50 resamples)",
          "adjusted Rand index" + (" (dashed = 0.60)" if prefix else ""), out / "bootstrap_ari_by_k.png",
          ref=0.6 if prefix else None, **kw)
    _by_k(sweep, "retention_min", f"{prefix}Least stable cluster: lowest share of players kept across bootstraps",
          "share kept (dashed = 0.70)", out / "retention_min_by_k.png", ref=0.7, **kw)
    _by_k(sweep, "ari_seasons", f"{prefix}Season-to-season: ARI between 2024-25-only and 2025-26-only models",
          "adjusted Rand index", out / "season_ari_by_k.png", **kw)
    _by_k(sweep, "n_params", f"{prefix}Parameters per model (dashed = {n} rows)", "free parameters",
          out / "n_params_by_k.png", ref=n, **kw)


# ---------------------------------------------------------------- packet charts

def heatmap(zmean: pd.DataFrame, groups: list[str], labels: list[str], path: Path,
            title: str = "Clusters x features: mean z-score", cbar: str = "mean z-score vs fitted players") -> None:
    """zmean: clusters x features (mean z-score), columns already in group order."""
    k, p = zmean.shape
    fig, ax = plt.subplots(figsize=(1.0 + 0.55 * p, 1.2 + 0.42 * k))
    lim = max(1.5, np.ceil(np.nanmax(np.abs(zmean.values)) * 2) / 2)
    im = ax.imshow(zmean.values, cmap=DIV, vmin=-lim, vmax=lim, aspect="auto")
    for i in range(k):
        for j in range(p):
            v = zmean.values[i, j]
            ax.text(j, i, f"{v:+.1f}", ha="center", va="center", fontsize=7,
                    color="white" if abs(v) > 0.65 * lim else INK)
    ax.set_xticks(range(p), labels, rotation=55, ha="right")
    ax.set_yticks(range(k), zmean.index)
    for j in range(1, p):
        if groups[j] != groups[j - 1]:
            ax.axvline(j - 0.5, color=SURFACE, lw=3)
    starts = [0] + [j for j in range(1, p) if groups[j] != groups[j - 1]] + [p]
    for a, b in zip(starts[:-1], starts[1:]):
        ax.text((a + b - 1) / 2, -0.8, groups[a], ha="center", va="bottom", fontsize=9, color=INK2, weight="bold")
    ax.tick_params(length=0)
    for s in ax.spines.values():
        s.set_visible(False)
    cb = fig.colorbar(im, ax=ax, fraction=0.025, pad=0.02)
    cb.set_label(cbar, color=INK2)
    cb.outline.set_visible(False)
    ax.set_title(title, pad=26)
    _save(fig, path)


def shot_mix(mix: pd.DataFrame, zone_labels: list[str], path: Path) -> None:
    """mix: clusters x zones, shares of FGA summing to 1; league row last."""
    k = len(mix)
    fig, ax = plt.subplots(figsize=(8, 0.9 + 0.45 * k))
    left = np.zeros(k)
    y = np.arange(k)[::-1]
    for j, z in enumerate(mix.columns):
        w = mix[z].to_numpy()
        ax.barh(y, w, left=left, height=0.7, color=SERIES[j], edgecolor=SURFACE, linewidth=2,
                label=zone_labels[j])
        for yi, l, wi in zip(y, left, w):
            if wi >= 0.07:
                ax.text(l + wi / 2, yi, f"{wi:.0%}", ha="center", va="center", fontsize=7.5, color=INK)
        left += w
    ax.set_yticks(y, mix.index)
    ax.set_xlim(0, 1)
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0%}"))
    ax.tick_params(axis="y", length=0)
    ax.spines["left"].set_visible(False)
    ax.legend(ncol=5, loc="upper left", bbox_to_anchor=(0, -0.08 if k > 6 else -0.15), fontsize=8)
    ax.set_title("Shot-location mix per cluster (share of FGA, all members' shots pooled)")
    _save(fig, path)


def pca_map(xy: np.ndarray, top: np.ndarray, prob: np.ndarray, names: list[str], label_idx: list[int],
            pacers: np.ndarray, var: tuple[float, float], cluster_names: list[str], path: Path,
            title: str = "Player-seasons on the first two principal components of the standardized features") -> None:
    fig, ax = plt.subplots(figsize=(10, 8))
    k = len(cluster_names)
    for c in range(k):
        m = top == c
        cols = np.array([matplotlib.colors.to_rgba(color(c), a) for a in 0.15 + 0.85 * prob[m]]) if m.any() else []
        ax.scatter(xy[m, 0], xy[m, 1], s=26, c=cols, marker=marker(c), linewidths=0)
        if m.any():
            cx, cy = np.median(xy[m, 0]), np.median(xy[m, 1])
            ax.text(cx, cy, cluster_names[c], fontsize=10, weight="bold", ha="center", va="center", color=INK,
                    bbox=dict(boxstyle="round,pad=0.2", fc=SURFACE, ec=color(c), lw=1.5, alpha=0.9))
    ax.scatter(xy[pacers, 0], xy[pacers, 1], s=70, facecolors="none", edgecolors=INK, linewidths=1.3)
    _place_labels(fig, ax, xy, label_idx, names, pacers)
    handles = [Line2D([], [], ls="", marker=marker(c), color=color(c), ms=7, label=cluster_names[c]) for c in range(k)]
    handles.append(Line2D([], [], ls="", marker="o", mfc="none", mec=INK, ms=9, label="Pacers player-season"))
    ax.legend(handles=handles, loc="upper left", bbox_to_anchor=(1.01, 1), fontsize=8,
              title="top archetype\n(opacity = probability)", title_fontsize=8)
    ax.set_xlabel(f"PC1 ({var[0]:.0%} of variance)")
    ax.set_ylabel(f"PC2 ({var[1]:.0%} of variance)")
    ax.grid(True)
    ax.set_title(title)
    _save(fig, path)


def _place_labels(fig, ax, xy, label_idx, names, pacers) -> None:
    """Greedy placement: each label takes the first offset (up to ~40 pt away) that overlaps no earlier label,
    with a leader line when it moved far from its point."""
    offsets = [(4, 4), (4, -10), (-4, 4), (-4, -10)] + [(dx, dy) for r in (14, 24, 36)
                                                       for dx, dy in ((r, 0), (-r, 0), (0, r), (0, -r),
                                                                      (r, r), (-r, r), (r, -r), (-r, -r))]
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    placed = []
    for i in label_idx:
        for dx, dy in offsets:
            t = ax.annotate(names[i], xy[i], xytext=(dx, dy), textcoords="offset points", fontsize=7,
                            ha="left" if dx >= 0 else "right", color=INK if pacers[i] else INK2,
                            weight="bold" if pacers[i] else "normal")
            bb = t.get_window_extent(renderer).expanded(1.05, 1.15)
            if not any(bb.overlaps(p) for p in placed) or (dx, dy) == offsets[-1]:
                if abs(dx) > 10 or abs(dy) > 10:
                    t.remove()
                    t = ax.annotate(names[i], xy[i], xytext=(dx, dy), textcoords="offset points", fontsize=7,
                                    ha="left" if dx >= 0 else "right", color=INK if pacers[i] else INK2,
                                    weight="bold" if pacers[i] else "normal",
                                    arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.6))
                placed.append(bb)
                break
            t.remove()


def count_heatmap(tab: pd.DataFrame, title: str, xlabel: str, ylabel: str, path: Path,
                  share_by_row: bool = True) -> None:
    vals = tab.div(tab.sum(1).replace(0, np.nan), axis=0) if share_by_row else tab
    fig, ax = plt.subplots(figsize=(1.6 + 0.6 * tab.shape[1], 1.0 + 0.42 * tab.shape[0]))
    im = ax.imshow(vals.fillna(0).values, cmap=SEQ, vmin=0, vmax=max(vals.max().max(), 1e-9), aspect="auto")
    vmax = vals.max().max()
    for i in range(tab.shape[0]):
        for j in range(tab.shape[1]):
            n = tab.values[i, j]
            if n:
                ax.text(j, i, f"{int(n)}", ha="center", va="center", fontsize=8,
                        color="white" if vals.values[i, j] > 0.55 * vmax else INK)
    ax.set_xticks(range(tab.shape[1]), tab.columns)
    ax.set_yticks(range(tab.shape[0]), tab.index)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.tick_params(length=0)
    for s in ax.spines.values():
        s.set_visible(False)
    cb = fig.colorbar(im, ax=ax, fraction=0.03, pad=0.02)
    cb.set_label("share of row" if share_by_row else "count", color=INK2)
    cb.outline.set_visible(False)
    ax.set_title(title)
    _save(fig, path)


def top_prob_hist(top: np.ndarray, prob: np.ndarray, cluster_names: list[str], path: Path) -> None:
    k = len(cluster_names)
    ncol = min(4, k)
    nrow = int(np.ceil(k / ncol))
    fig, axes = plt.subplots(nrow, ncol, figsize=(2.6 * ncol, 1.9 * nrow), sharex=True, squeeze=False)
    bins = np.linspace(0.2, 1.0, 17)
    for c in range(nrow * ncol):
        ax = axes[c // ncol][c % ncol]
        if c >= k:
            ax.axis("off")
            continue
        p = prob[top == c]
        ax.hist(p, bins=bins, color=color(c), edgecolor=SURFACE, linewidth=1)
        ax.axvline(0.6, color=MUTED, lw=1, ls="--")
        ax.set_title(f"{cluster_names[c]} (n={len(p)}, {np.mean(p < 0.6):.0%} under 0.6)", fontsize=8.5)
        ax.tick_params(labelsize=7)
    fig.suptitle("Top membership probability per player-season, by top archetype (dashed = 0.6)",
                 x=0.01, ha="left", fontsize=11, weight="bold")
    fig.tight_layout()
    _save(fig, path)


def transitions(levels: list[tuple[int, list[str], np.ndarray]], flows: list[np.ndarray], path: Path) -> None:
    """levels: (k, cluster names, sizes) per column; flows[i]: count matrix level i -> level i+1."""
    fig, ax = plt.subplots(figsize=(10, 7.5))
    total = levels[0][2].sum()
    gap = 0.012 * total
    xs = [0, 1, 2][:len(levels)]
    w = 0.08
    pos = []
    for x, (k, names, sizes) in zip(xs, levels):
        y = 0.0
        p = []
        for c in range(k):
            p.append((y, y + sizes[c]))
            ax.add_patch(plt.Rectangle((x - w / 2, y), w, sizes[c], color=color(c), lw=0))
            last = x == xs[-1]
            ax.text(x + (w / 2 + 0.01 if last else -w / 2 - 0.01), y + sizes[c] / 2, f"{names[c]} ({int(sizes[c])})",
                    ha="left" if last else "right", va="center", fontsize=7.5, color=INK)
            y += sizes[c] + gap
        pos.append(p)
        ax.text(x, -0.03 * total, f"k = {k}", ha="center", va="top", fontsize=10, weight="bold", color=INK2)
    for i, fl in enumerate(flows):
        out_off = [a for a, _ in pos[i]]
        in_off = [a for a, _ in pos[i + 1]]
        for a in range(fl.shape[0]):
            for b in range(fl.shape[1]):
                n = fl[a, b]
                if n < 1:
                    continue
                y0, y1 = out_off[a], in_off[b]
                x0, x1 = xs[i] + w / 2, xs[i + 1] - w / 2
                xm = (x0 + x1) / 2
                verts = [(x0, y0), (xm, y0), (xm, y1), (x1, y1), (x1, y1 + n), (xm, y1 + n), (xm, y0 + n),
                         (x0, y0 + n), (x0, y0)]
                codes = [MPath.MOVETO, MPath.CURVE4, MPath.CURVE4, MPath.CURVE4, MPath.LINETO, MPath.CURVE4,
                         MPath.CURVE4, MPath.CURVE4, MPath.CLOSEPOLY]
                ax.add_patch(PathPatch(MPath(verts, codes), fc=color(a), alpha=0.35, lw=0))
                out_off[a] += n
                in_off[b] += n
    ax.set_xlim(-0.2, xs[-1] + 0.2)
    ax.set_ylim(-0.07 * total, max(p[-1][1] for p in pos) + gap)
    ax.invert_yaxis()
    ax.axis("off")
    ax.set_title("How clusters split and merge across k (band width = player-seasons; color = cluster on the left)")
    _save(fig, path)


# ---------------------------------------------------------------- slicing test (D30)

def pc_scatter(xy: np.ndarray, names: list[str], label_idx: list[int], pacers: np.ndarray, var: tuple[float, float],
               title: str, path: Path) -> None:
    """Training player-seasons of one family on its own PC1 x PC2; Pacers ringed, labeled rows named."""
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.scatter(xy[:, 0], xy[:, 1], s=24, color=SERIES[0], alpha=0.45, linewidths=0)
    ax.scatter(xy[pacers, 0], xy[pacers, 1], s=70, facecolors="none", edgecolors=INK, linewidths=1.3)
    _place_labels(fig, ax, xy, label_idx, names, pacers)
    ax.legend(handles=[Line2D([], [], ls="", marker="o", color=SERIES[0], alpha=0.6, ms=6, label="player-season"),
                       Line2D([], [], ls="", marker="o", mfc="none", mec=INK, ms=9, label="Pacers player-season")],
              loc="upper left", bbox_to_anchor=(1.01, 1), fontsize=8)
    ax.axhline(0, color=AXIS, lw=0.8)
    ax.axvline(0, color=AXIS, lw=0.8)
    ax.set_xlabel(f"PC1 ({var[0]:.0%} of variance)")
    ax.set_ylabel(f"PC2 ({var[1]:.0%} of variance)")
    ax.grid(True)
    ax.set_title(title)
    _save(fig, path)


def centroid_panels(xy: np.ndarray, panels: list[dict], var: tuple[float, float], title: str, path: Path) -> None:
    """One panel per k: points colored by top diag cluster, cluster centers (projected onto PC1/PC2) as large
    markers sized by weight. panels[i]: {k, top, centers (k x 2), weights, names, caption}."""
    n = len(panels)
    fig, axes = plt.subplots(1, n, figsize=(5.2 * n, 5.0), sharex=True, sharey=True, squeeze=False)
    for ax, p in zip(axes[0], panels):
        for c in range(p["k"]):
            m = p["top"] == c
            ax.scatter(xy[m, 0], xy[m, 1], s=12, color=color(c), alpha=0.35, linewidths=0, marker=marker(c))
        for c in range(p["k"]):
            cx, cy = p["centers"][c]
            ax.scatter(cx, cy, s=120 + 900 * p["weights"][c], color=color(c), marker="X", edgecolors=INK,
                       linewidths=1.2, zorder=3)
            ax.annotate(p["names"][c], (cx, cy), xytext=(8, 6), textcoords="offset points", fontsize=8,
                        weight="bold", color=INK, zorder=4)
        ax.axhline(0, color=AXIS, lw=0.8)
        ax.axvline(0, color=AXIS, lw=0.8)
        ax.grid(True)
        ax.set_title(f"diag k = {p['k']}", fontsize=10)
        ax.text(0.01, -0.13, p["caption"], transform=ax.transAxes, fontsize=7.5, color=INK2, va="top")
        ax.set_xlabel(f"PC1 ({var[0]:.0%})")
    axes[0][0].set_ylabel(f"PC2 ({var[1]:.0%})")
    fig.suptitle(title, x=0.01, ha="left", fontsize=11, weight="bold")
    fig.tight_layout()
    _save(fig, path)


def pc_hist(scores: np.ndarray, fits: list[dict], var: np.ndarray, title: str, path: Path) -> None:
    """Histogram of each PC's scores with the fitted 1- and 2-component 1-D Gaussian mixture densities.
    fits[j]: twolevel.gmm_1d output, {k: {bic, weights, means, sds}} for k = 1, 2."""
    from scipy.stats import norm
    n = scores.shape[1]
    fig, axes = plt.subplots(1, n, figsize=(5.2 * n, 3.8), squeeze=False)
    for j, ax in enumerate(axes[0]):
        x = scores[:, j]
        ax.hist(x, bins=30, density=True, color=AXIS, edgecolor=SURFACE, linewidth=1)
        g = np.linspace(x.min() - 0.5, x.max() + 0.5, 400)
        for kk, col, ls in ((1, SERIES[0], "-"), (2, SERIES[1], "--")):
            f = fits[j][kk]
            w, mu, sd = f["weights"], f["means"], f["sds"]
            ax.plot(g, sum(wi * norm.pdf(g, mi, si) for wi, mi, si in zip(w, mu, sd)), color=col, lw=2, ls=ls,
                    label=f"{kk} component{'s' if kk > 1 else ''} (BIC {f['bic']:,.1f})")
        ax.set_title(f"PC{j + 1} ({var[j]:.0%} of variance): BIC(2) - BIC(1) = "
                     f"{fits[j][2]['bic'] - fits[j][1]['bic']:+.1f}", fontsize=9.5)
        ax.set_xlabel(f"PC{j + 1} score")
        ax.set_ylabel("density")
        ax.legend(fontsize=7.5, loc="upper right")
    fig.suptitle(title, x=0.01, ha="left", fontsize=11, weight="bold")
    fig.tight_layout()
    _save(fig, path)
