"""Divergence timeline for a quarantined game (offline, from the raw cache): where our stints first disagree with
NBA's box, and the play-by-play around that moment. For the manual look at quarantined Pacers games (D3, D15).

    python scripts/divergence.py 2024-25 0042400306 [more game ids ...]

What it prints, per failing check:
  minutes     with a rotation file: the first moment our on-floor set differs from the rotation file's.
              Without one: for each pair of teammates where one is over by ~X s and the other short by ~X s, the
              stretches where we have the over-player on and the short-player off, with lengths. A stretch
              matching X (±2 s) is the likely missing/mislabelled substitution; its start is the divergence.
  plus_minus  the scoring plays credited to a lineup that differs from the one a second earlier or later for the
              players whose +/- is off: points in the same second as a substitution involving them.
  pbp_counts  the mismatched players' events of that stat, with team totals.
Then the play-by-play +-20 s around each candidate moment, with our lineup for the team at that moment.
Numbers only; what they mean is for the reader.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import pandas as pd  # noqa: E402

from pacersml.data import cache, normalize  # noqa: E402
from pacersml.data.http import Client  # noqa: E402
from pacersml.data.normalize import period_start  # noqa: E402
from pacersml.data.pipeline import load_game  # noqa: E402
from pacersml.data.stints import from_hybrid, from_pbp, player_stints, usable_rotation  # noqa: E402
from pacersml.data.validate import COUNT_STATS, check_game, pbp_player_counts  # noqa: E402

WINDOW = 20.0


def clock(t: float) -> str:
    """Elapsed game seconds -> 'Q3 07:12' (game clock remaining)."""
    p = 1
    while period_start(p + 1) <= t and p < 10:
        p += 1
    rem = period_start(p) + normalize.period_length(p) - t
    return f"{'Q' + str(p) if p <= 4 else 'OT' + str(p - 4)} {int(rem // 60):02d}:{rem % 60:04.1f}"


def on_floor(stints, team_side, pid):
    return stints[stints[f"{team_side}_ids"].map(lambda s: pid in s)]


def show_events(ev, t, names, lineups):
    w = ev[(ev.elapsed >= t - WINDOW) & (ev.elapsed <= t + WINDOW)]
    for e in w.itertuples():
        who = names.get(e.person_id, "") if e.person_id else ""
        sub = f"  IN {names.get(e.in_id, e.in_id)} / OUT {names.get(e.out_id, e.out_id)}" if e.etype == "sub" else ""
        mark = ">>" if abs(e.elapsed - t) < 0.5 else "  "
        print(f"    {mark} {clock(e.elapsed)}  seq {e.seq:>4}  {e.etype:<12} {who:<22} {str(e.desc)[:60]}{sub}")
    for side, lu in lineups.items():
        print(f"       our {side} lineup at {clock(t)}: {', '.join(names.get(p, str(p)) for p in lu)}")


def lineup_at(stints, t, side):
    s = stints[(stints.start <= t) & (stints.end > t)]
    return list(s[f"{side}_ids"].iloc[0]) if not s.empty else []


def main(season: str, gids: list[str]) -> None:
    c = Client()
    c.blocked_hosts = {"stats.nba.com", "cdn.nba.com"}  # offline only
    for gid in gids:
        d = load_game(c, season, gid, "auto", fetch_rotation=False)
        home, away = normalize.team_ids(cache.find_raw(season, [d.sources["box"]], gid)[1])
        periods = sorted(d.events.period.unique())
        hybrid = usable_rotation(d.rotation, periods, home, away)
        stints, ev, _ = (from_hybrid(d.events, d.rotation, home, away, gid) if hybrid
                         else from_pbp(d.events, d.box, home, away, gid))
        checks = check_game(stints, ev, d.box, home, away)
        bad = checks[~checks.passed & checks.hard]
        names = dict(zip(d.box.person_id, d.box.name))
        side_of = {t: s for t, s in ((home, "home"), (away, "away"))}
        team_of = dict(zip(d.box.person_id, d.box.team_id))
        print(f"\n=== {gid} ({season}) · builder {'hybrid' if hybrid else 'pbp_rebuild'} · "
              f"failing: {', '.join(bad.check) or 'none'}")
        ps = player_stints(stints, home, away)
        ours = ps.assign(pm=ps.pts_for - ps.pts_against).groupby("person_id")[["seconds", "pm"]].sum()
        b = d.box.set_index("person_id")
        sec_gap = ours.seconds.reindex(b.index, fill_value=0) - b.seconds
        pm_gap = ours.pm.reindex(b.index, fill_value=0) - b.plus_minus

        if "minutes" in set(bad.check):
            big = sec_gap[sec_gap.abs() > 1.0]
            print("  minutes gaps > 1 s (ours - box): " + ", ".join(f"{names.get(p)} {v:+.1f} s" for p, v in big.items()))
            if hybrid or d.rotation is not None:
                print("  (rotation file present: compare on-floor sets with it directly)")
            for t in (home, away):
                g = sec_gap[[team_of.get(p) == t for p in sec_gap.index]]
                over, short = g[g > 1.0], g[g < -1.0]
                for o, x in over.items():
                    for s_, y in short.items():
                        side = side_of[t]
                        runs = stints[stints[f"{side}_ids"].map(lambda lu: o in lu and s_ not in lu)]
                        runs = runs.assign(gap=(runs.start != runs.end.shift()).cumsum())
                        spans = runs.groupby("gap").agg(start=("start", "min"), end=("end", "max"),
                                                        seconds=("seconds", "sum"))
                        print(f"  minutes: {names.get(o)} over {x:+.1f} s, {names.get(s_)} short {y:+.1f} s; "
                              f"stretches with {names.get(o)} on and {names.get(s_)} off:")
                        for r in spans.itertuples():
                            hit = "  <- matches" if abs(r.seconds - x) <= 2 or abs(r.seconds + y) <= 2 else ""
                            print(f"     {clock(r.start)} -> {clock(r.end)}  {r.seconds:6.1f} s{hit}")
                        matched = [r for r in spans.itertuples() if abs(r.seconds - x) <= 2 or abs(r.seconds + y) <= 2]
                        if matched:
                            for r in matched:
                                for edge in (r.start, r.end):
                                    print(f"   timeline around {clock(edge)}:")
                                    show_events(ev, edge, names, {side: lineup_at(stints, edge + 0.01, side)})
                        else:
                            # no whole stretch matches: the true boundary of one stretch is X s off ours.
                            # Candidate points: each stretch's end moved X earlier, or its start X later.
                            gap_s = min(abs(x), abs(y))
                            print(f"   no stretch matches {gap_s:.1f} s; candidate points (stretch end - {gap_s:.0f} s, "
                                  f"start + {gap_s:.0f} s) with a dead ball within 3 s:")
                            for r in spans.itertuples():
                                for pt in (r.end - gap_s, r.start + gap_s):
                                    if not (r.start < pt < r.end):
                                        continue
                                    near = ev[(ev.elapsed - pt).abs() <= 3]
                                    if near.etype.isin(["sub", "foul", "timeout", "ft", "turnover"]).any() or                                             near.desc.astype(str).str.contains("Timeout|Violation|Review", case=False).any():
                                        print(f"   timeline around {clock(pt)}:")
                                        show_events(ev, pt, names, {side: lineup_at(stints, pt, side)})

        if "plus_minus" in set(bad.check):
            off = pm_gap[pm_gap != 0]
            print("  plus_minus gaps (ours - box): " + ", ".join(f"{names.get(p)} {v:+d}" for p, v in off.astype(int).items()))
            subs = ev[(ev.etype == "sub") & (ev.in_id.isin(off.index) | ev.out_id.isin(off.index))]
            keys = set(zip(subs.period, subs.elapsed.round(0)))
            same_sec = pd.Series([(p, round(t)) in keys for p, t in zip(ev.period, ev.elapsed)], index=ev.index)
            pts = ev[(ev.points > 0) & same_sec]
            print(f"  scoring plays in the same second as a sub involving those players: {len(pts)}")
            for t in sorted(set(pts.elapsed)):
                print(f"   timeline around {clock(t)}:")
                show_events(ev, t, names, {s: lineup_at(stints, t + 0.01, s) for s in ("home", "away")})

        if "pbp_counts" in set(bad.check):
            cnt = pbp_player_counts(ev).reindex(b.index, fill_value=0)
            cd = cnt[COUNT_STATS] - b.assign(reb=b.oreb + b.dreb)[COUNT_STATS]
            for p, r in cd[(cd != 0).any(axis=1)].iterrows():
                print(f"  pbp_counts: {names.get(p)} (team {team_of.get(p)}): "
                      + ", ".join(f"{k} {int(v):+d}" for k, v in r.items() if v) + "  (ours - box)")
            print("  team totals (ours - box): " + "; ".join(
                f"{t} " + ", ".join(f"{k} {int(v):+d}" for k, v in r.items() if v)
                for t, r in cd.groupby(pd.Series(team_of)).sum().iterrows() if (r != 0).any()))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2:])
