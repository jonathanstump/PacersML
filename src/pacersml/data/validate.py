"""Stint-vs-box validation (per game) and possession cross-checks (per season), plus diagnostic plots.

Per-game checks (hard = a failure quarantines the game, D3/D11):
    minutes       player seconds on the floor from stints vs box MIN, |diff| <= 1 s            hard, lineup
                  exception (D17): a gap up to 3 s passes, noted, when it is unpaired: no teammate is off by
                  more than 1 s the other way. A lineup error always shows as a pair (our team seconds are
                  fixed at 5 x game length), so an unpaired gap is box rounding. Paired gaps always fail
    floor_five    every stint has exactly 5 players per team                                hard, lineup
    game_seconds  sum of stint seconds == 2880 + 300 * OT periods (± 1 s)                   hard, lineup
    plus_minus    player (pts for - pts against) over his stints == box +/-                  hard, lineup
                  exception (D8 amended, D14): |gap| <= 2 passes, noted, when minutes pass and the game has
                  a substitution in the same second as a technical free throw (NBA's box is inconsistent there)
    team_points   PBP points per team == box points per team                                hard
    pbp_counts    PBP-derived player counts (pts, fgm, fga, fg3m, fg3a, ftm, fta, tov, reb, pf) vs box (D5).
                  Passes, noted, when every team total matches (moved between teammates, D14), or when team
                  points match and each team's possessions are within 2% of pbpstats.com: shot- and
                  rebound-level differences don't change what stints and RAPM use (D15). Otherwise  hard
A passing check with `noted` set puts the game in the "kept with notes" list instead of quarantine.
    poss_pbpstats team possessions per game vs pbpstats.com                                   reported only
Season checks:
    team-season possessions vs NBA team POSS: gap > 2% fails the season (D1), for team-seasons with at least
    1,000 NBA possessions; smaller ones are reported only (D19)
    player-season possessions vs NBA player POSS: flagged when > 2% AND > 5 possessions, report-only (D7);
    share of players over vs under NBA reported, outside 40/60 marked "investigate" (D7)
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from pacersml.data.normalize import period_length, period_start
from pacersml.data.stints import player_stints

COUNT_STATS = ["pts", "fgm", "fga", "fg3m", "fg3a", "ftm", "fta", "tov", "reb", "pf"]
POSS_TOL = 0.02            # D1 / D5
TEAM_POSS_MIN = 1000       # D19: the D1 team-season check is enforced only from this many NBA possessions
PLAYER_POSS_FLOOR = 5      # D7: player flag also needs |gap| > 5 possessions
DIRECTION_BAND = (0.40, 0.60)  # D7: share of player gaps that are "over"
LINEUP_CHECKS = ("minutes", "floor_five", "game_seconds", "plus_minus")
MIN_NOTE_MAX = 3.0         # D17: unpaired single-player minutes gap kept with a note
PM_NOTE_MAX = 2            # D14: plus-minus gap kept with a note when a sub shares a second with a technical FT


def _row(game_id, check, passed, residual, detail="", hard=True, noted=False):
    return {"game_id": game_id, "check": check, "hard": hard, "passed": bool(passed),
            "residual": float(residual), "detail": detail, "noted": bool(noted)}


def sub_at_technical_ft(ev: pd.DataFrame) -> bool:
    """A substitution in the same second (same period) as a technical free throw (D14)."""
    tft = ev[(ev.etype == "ft") & ev.technical]
    subs = ev[ev.etype == "sub"]
    keys = set(zip(subs.period, subs.elapsed.round(0)))
    return any((p, t) in keys for p, t in zip(tft.period, tft.elapsed.round(0)))


def paired_minutes_gap(diff: pd.Series, team_of: pd.Series) -> bool:
    """Two teammates off by more than 1 s in opposite directions: the signature of a misplaced sub (D17)."""
    big = diff[diff.abs() > 1.0]
    return any((big[team_of.reindex(big.index) == t] > 0).any() and (big[team_of.reindex(big.index) == t] < 0).any()
               for t in team_of.unique())


def pbp_player_counts(ev: pd.DataFrame) -> pd.DataFrame:
    e = ev[ev.person_id > 0]
    fg, ft = e[e.etype == "fg"], e[e.etype == "ft"]
    parts = {
        "pts": e.groupby("person_id").points.sum(),
        "fgm": fg[fg.made].groupby("person_id").size(), "fga": fg.groupby("person_id").size(),
        "fg3m": fg[fg.made & (fg.value == 3)].groupby("person_id").size(),
        "fg3a": fg[fg.value == 3].groupby("person_id").size(),
        "ftm": ft[ft.made].groupby("person_id").size(), "fta": ft.groupby("person_id").size(),
        "tov": e[e.etype == "turnover"].groupby("person_id").size(),
        "reb": e[e.etype == "rebound"].groupby("person_id").size(),
        "pf": e[(e.etype == "foul") & ~e.technical].groupby("person_id").size(),  # box PF: offensive in, techs out
    }
    return pd.DataFrame(parts).fillna(0).astype(int)


def check_game(stints, ev, box_df, home, away, pbpstats_poss: dict | None = None) -> pd.DataFrame:
    gid = box_df.game_id.iloc[0]
    rows = []
    ps = player_stints(stints, home, away)
    on = ps.assign(pm=ps.pts_for - ps.pts_against).groupby("person_id")[["seconds", "pm"]].sum()
    b = box_df.set_index("person_id")

    diff = (on.seconds.reindex(b.index, fill_value=0) - b.seconds)
    extra = on.index.difference(b.index)  # on the floor per stints but not in the box at all
    resid = max(diff.abs().max(), on.seconds.reindex(extra).max() if len(extra) else 0)
    worst = diff.abs().sort_values(ascending=False).head(3)
    minutes_ok = resid <= 1.0
    min_noted = not minutes_ok and not len(extra) and resid <= MIN_NOTE_MAX and not paired_minutes_gap(diff, b.team_id)
    rows.append(_row(gid, "minutes", minutes_ok or min_noted, resid,
                     ("unpaired gap <= 3 s; " if min_noted else "")
                     + ";".join(f"{p}:{d:+.1f}" for p, d in diff[worst.index].items()), noted=min_noted))

    bad = ((stints.home_ids.map(len) != 5) | (stints.away_ids.map(len) != 5)).sum()
    rows.append(_row(gid, "floor_five", bad == 0, bad, f"{bad} of {len(stints)} stints"))

    n_per = int(ev.period.max())
    length = period_start(n_per) + period_length(n_per)
    rows.append(_row(gid, "game_seconds", abs(stints.seconds.sum() - length) <= 1.0, stints.seconds.sum() - length))

    pm = on.pm.reindex(b.index, fill_value=0) - b.plus_minus
    pm_detail = ";".join(f"{p}:{d:+d}" for p, d in pm[pm != 0].astype(int).items())[:200]
    exact = bool((pm == 0).all())
    pm_noted = (not exact and pm.abs().max() <= PM_NOTE_MAX and minutes_ok and sub_at_technical_ft(ev))
    rows.append(_row(gid, "plus_minus", exact or pm_noted, pm.abs().max(),
                     ("sub at technical FT; " if pm_noted else "") + pm_detail, noted=pm_noted))

    team_pbp = ev.groupby("team_id").points.sum()
    team_box = box_df.groupby("team_id").pts.sum()
    tdiff = (team_pbp.reindex(team_box.index, fill_value=0) - team_box)
    rows.append(_row(gid, "team_points", (tdiff == 0).all(), tdiff.abs().max()))

    cnt = pbp_player_counts(ev).reindex(b.index, fill_value=0)
    boxc = b.assign(reb=b.oreb + b.dreb)[COUNT_STATS]
    cd = (cnt[COUNT_STATS] - boxc)
    team_cd = cd.groupby(b.team_id).sum()
    off = [f"{s}:{int(cd[s].abs().sum())}" for s in COUNT_STATS if cd[s].abs().sum()]
    team_off = [f"team {t} {s}:{int(v):+d}" for t, r in team_cd.iterrows() for s, v in r.items() if v]

    ours = {home: int(stints.home_poss.sum()), away: int(stints.away_poss.sum())}
    poss_ok = bool(pbpstats_poss) and all(
        t in pbpstats_poss and abs(ours[t] - pbpstats_poss[t]) <= POSS_TOL * pbpstats_poss[t] for t in (home, away))
    moved = not team_off  # every team total matches: the stat moved between teammates (D14), possessions unchanged
    counts_noted = bool(off) and (moved or ((tdiff == 0).all() and poss_ok))
    note = ("; moved between teammates" if off and moved
            else "; team points match, possessions within 2% of pbpstats" if counts_noted
            else "; possessions not confirmed (no pbpstats)" if off and not pbpstats_poss else "")
    rows.append(_row(gid, "pbp_counts", not off or counts_noted, cd.abs().to_numpy().max(),
                     ";".join(off + team_off) + note, noted=counts_noted))

    if pbpstats_poss:
        r = max(abs(ours[t] - pbpstats_poss[t]) for t in (home, away) if t in pbpstats_poss)
        rows.append(_row(gid, "poss_pbpstats", True, r, f"ours={ours} pbpstats={pbpstats_poss}", hard=False))
    return pd.DataFrame(rows)


def lineup_ok(checks: pd.DataFrame) -> bool:
    """All lineup checks pass (noted passes count as passes)."""
    return bool(checks[checks.check.isin(LINEUP_CHECKS)].passed.all())


def failure_group(failed: set[str]) -> str:
    """D14 groups: D team points, C lineup (minutes/floor/seconds), B plus-minus, A play-by-play counts."""
    if "team_points" in failed:
        return "D"
    if failed & {"minutes", "floor_five", "game_seconds"}:
        return "C"
    if "plus_minus" in failed:
        return "B"
    return "A"


def hard_failures(checks: pd.DataFrame) -> set[str]:
    return set(checks[checks.hard & ~checks.passed].check)


# ---------------------------------------------------------------- season-level

def team_poss_check(stints_all: pd.DataFrame, games: pd.DataFrame, nba_team_adv: pd.DataFrame | None):
    """Team-season possessions, ours vs NBA's. Returns (table, failed) where failed = any gap > 2%."""
    s = stints_all.merge(games[["game_id", "home_team_id", "away_team_id"]], on="game_id")
    ours = pd.concat([
        s.groupby("home_team_id").home_poss.sum().rename_axis("team_id"),
        s.groupby("away_team_id").away_poss.sum().rename_axis("team_id"),
    ]).groupby(level=0).sum().rename("poss_ours")
    gp = pd.concat([games.home_team_id, games.away_team_id]).value_counts().rename("games")
    t = pd.concat([ours, gp], axis=1).rename_axis("team_id").reset_index()
    if nba_team_adv is None or nba_team_adv.empty:
        t["poss_nba"], t["gap_pct"], t["over_tol"] = np.nan, np.nan, False
        return t, False
    nba = nba_team_adv.set_index("TEAM_ID").POSS.rename("poss_nba")
    t = t.merge(nba, left_on="team_id", right_index=True, how="left")
    t["gap_pct"] = (t.poss_ours - t.poss_nba) / t.poss_nba
    t["enforced"] = t.poss_nba >= TEAM_POSS_MIN  # D19: smaller team-seasons (play-in, early season) reported only
    t["over_tol"] = (t.gap_pct.abs() > POSS_TOL) & t.enforced
    return t, bool(t.over_tol.any())


def player_poss_check(season_tbl: pd.DataFrame, nba_player_adv: pd.DataFrame | None) -> pd.DataFrame:
    """Player-season possessions vs NBA player POSS. Ours is reported as (off + def) / 2 and as off only,
    because NBA's player POSS definition isn't documented; both gaps are kept, with sample sizes."""
    t = season_tbl[["person_id", "name", "games", "poss_off", "poss_def"]].copy()
    if nba_player_adv is None or nba_player_adv.empty:
        return t.assign(poss_nba=np.nan, gap_poss_avg=np.nan, gap_pct_avg=np.nan, gap_poss_off=np.nan,
                        gap_pct_off=np.nan, flag_avg=False, flag_off=False)
    nba = nba_player_adv.groupby("PLAYER_ID").POSS.sum().rename("poss_nba")
    t = t.merge(nba, left_on="person_id", right_index=True, how="left")
    avg = (t.poss_off + t.poss_def) / 2
    t["gap_poss_avg"] = avg - t.poss_nba
    t["gap_pct_avg"] = t.gap_poss_avg / t.poss_nba
    t["gap_poss_off"] = t.poss_off - t.poss_nba
    t["gap_pct_off"] = t.gap_poss_off / t.poss_nba
    # D7: report-only flag, needs both the relative and the absolute gap
    t["flag_avg"] = (t.gap_pct_avg.abs() > POSS_TOL) & (t.gap_poss_avg.abs() > PLAYER_POSS_FLOOR)
    t["flag_off"] = (t.gap_pct_off.abs() > POSS_TOL) & (t.gap_poss_off.abs() > PLAYER_POSS_FLOOR)
    return t


def gap_direction(player_tbl: pd.DataFrame) -> pd.DataFrame:
    """Share of player-seasons where our count is over vs under NBA's (exact matches counted separately).
    Gaps from definitional differences should split roughly evenly; a split outside 40/60 means investigate (D7)."""
    rows = []
    for col in ("gap_poss_avg", "gap_poss_off"):
        g = player_tbl[col].dropna() if col in player_tbl else pd.Series(dtype=float)
        over, under, equal = int((g > 0).sum()), int((g < 0).sum()), int((g == 0).sum())
        share_over = over / (over + under) if over + under else np.nan
        rows.append({"measure": col, "over": over, "under": under, "equal": equal, "share_over": share_over,
                     "investigate": bool(pd.notna(share_over)
                                         and not DIRECTION_BAND[0] <= share_over <= DIRECTION_BAND[1])})
    return pd.DataFrame(rows)


# ---------------------------------------------------------------- plots

INK, MUTED, GRID, SURFACE, SERIES = "#0b0b0b", "#898781", "#e1e0d9", "#fcfcfb", "#2a78d6"


def _ax(title, xlabel, ylabel):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(7, 4), facecolor=SURFACE)
    ax.set_facecolor(SURFACE)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(MUTED)
    ax.tick_params(colors=MUTED, labelcolor=INK, labelsize=9)
    ax.grid(axis="y", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    ax.set_title(title, color=INK, fontsize=11, loc="left")
    ax.set_xlabel(xlabel, color=INK, fontsize=9)
    ax.set_ylabel(ylabel, color=INK, fontsize=9)
    return fig, ax


def plot_season(season: str, checks: pd.DataFrame, team_tbl: pd.DataFrame, player_tbl: pd.DataFrame,
                out_dir: Path) -> list[Path]:
    import matplotlib.pyplot as plt
    out_dir.mkdir(parents=True, exist_ok=True)
    paths = []

    for check, xlabel in (("minutes", "max |stint seconds - box seconds| per game"),
                          ("plus_minus", "max |stint +/- - box +/-| per game")):
        r = checks[checks.check == check].residual
        if r.empty:
            continue
        fig, ax = _ax(f"{season}: {check} residual (n = {len(r)} games)", xlabel, "games")
        ax.hist(r, bins=40, color=SERIES, edgecolor=SURFACE, linewidth=2)
        if check == "minutes":
            ax.axvline(1.0, color=MUTED, linestyle="--", linewidth=1)
            ax.text(1.0, ax.get_ylim()[1] * 0.95, " tolerance 1 s", color=MUTED, fontsize=8, va="top")
        p = out_dir / f"{season}_{check}_residual.png"
        fig.savefig(p, dpi=130, bbox_inches="tight")
        plt.close(fig)
        paths.append(p)

    if team_tbl.gap_pct.notna().any():
        t = team_tbl.dropna(subset=["gap_pct"]).sort_values("gap_pct")
        fig, ax = _ax(f"{season}: team-season possessions, ours vs NBA (n = {len(t)} teams)",
                      "team id", "gap (ours - NBA) / NBA, %")
        ax.bar(range(len(t)), t.gap_pct * 100, color=SERIES, edgecolor=SURFACE, linewidth=2)
        for y in (-2, 2):
            ax.axhline(y, color=MUTED, linestyle="--", linewidth=1)
        ax.set_xticks(range(len(t)), t.team_id.astype(str).str[-2:], fontsize=7)
        p = out_dir / f"{season}_team_poss_gap.png"
        fig.savefig(p, dpi=130, bbox_inches="tight")
        plt.close(fig)
        paths.append(p)

    if "gap_pct_avg" in player_tbl and player_tbl.gap_pct_avg.notna().any():
        t = player_tbl.dropna(subset=["gap_pct_avg"])
        d = gap_direction(t).set_index("measure").loc["gap_poss_avg"]
        fig, ax = _ax(f"{season}: player-season possessions, ours (off+def)/2 vs NBA (n = {len(t)} players)\n"
                      f"over {d.over} / under {d.under} / equal {d.equal} · flagged (>2% and >5 poss) "
                      f"{int(t.flag_avg.sum())}", "NBA possessions (player-season, log scale)",
                      "gap, possessions (ours - NBA)")
        ax.scatter(t.poss_nba, t.gap_poss_avg, s=10, color=SERIES, alpha=0.6, linewidths=0)
        ax.set_xscale("log")
        for y in (-PLAYER_POSS_FLOOR, PLAYER_POSS_FLOOR):
            ax.axhline(y, color=MUTED, linestyle="--", linewidth=1)
        p = out_dir / f"{season}_player_poss_gap.png"
        fig.savefig(p, dpi=130, bbox_inches="tight")
        plt.close(fig)
        paths.append(p)

    rates = (checks.groupby("check").passed.agg(["sum", "count"])
             .assign(pass_rate=lambda d: d["sum"] / d["count"]))
    rates.to_csv(out_dir / f"{season}_check_pass_rates.csv")
    paths.append(out_dir / f"{season}_check_pass_rates.csv")
    return paths
