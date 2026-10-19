"""Stints: stretches of a game with no change in the ten players on the floor.

Two builders produce the same output:
    from_rotation  - who is on the floor comes from stats.nba.com gamerotation (in/out times per player);
                     play-by-play order only decides which side of a substitution same-second events fall on.
    from_pbp       - the rebuild (D3): PBP substitutions plus inferred period starters.

Output of either builder (via `build`):
    stints:  game_id, stint_id, period, start, end, seconds, home_ids, away_ids (tuples of person ids),
             home_pts, away_pts, home_poss, away_poss, source,
             {home,away}_{fg_miss, ft_miss_live, oreb, dreb}  (rebound-percentage ingredients)
    events:  the input events with `stint_id`, `poss_id`, `offense`
    info:    dict with inferred starters (pbp builder) for debugging failed rebuilds
"""
from __future__ import annotations

import pandas as pd

from pacersml.data.normalize import period_length, period_start
from pacersml.data.possessions import assign_possessions, possession_table

TOL = 0.5  # seconds; rotation times are in tenths, PBP clocks in hundredths


def _segments_to_stints(ev, segments, home, away, game_id, source):
    """segments: list of (first_event_idx, start_time, period, {team: set}) in event order."""
    # A run of substitutions at one moment creates segments with nothing but sub rows: keep only the last.
    cleaned = []
    for seg in segments:
        if cleaned:
            prev = cleaned[-1]
            between = ev.etype.iloc[prev[0]:seg[0]]
            if seg[2] == prev[2] and abs(seg[1] - prev[1]) <= TOL and between.isin(["sub", "period_start"]).all():
                cleaned[-1] = (prev[0], prev[1], seg[2], seg[3])
                continue
        cleaned.append(seg)

    rows, stint_of_event = [], pd.Series(-1, index=ev.index)
    for k, (idx, t0, period, lineup) in enumerate(cleaned):
        nxt = cleaned[k + 1] if k + 1 < len(cleaned) else None
        p_end = period_start(period) + period_length(period)
        t1 = min(nxt[1], p_end) if nxt and nxt[2] == period else p_end
        stint_of_event.iloc[idx:(nxt[0] if nxt else len(ev))] = k
        rows.append({"game_id": game_id, "stint_id": k, "period": period, "start": t0, "end": t1,
                     "seconds": round(t1 - t0, 2), "home_ids": tuple(sorted(lineup[home])),
                     "away_ids": tuple(sorted(lineup[away])), "source": source})
    stints = pd.DataFrame(rows)
    ev = ev.assign(stint_id=stint_of_event.to_numpy())
    return _aggregate(stints, ev, home, away), ev


def _aggregate(stints, ev, home, away):
    pts = ev.groupby(["stint_id", "team_id"]).points.sum().unstack(fill_value=0)
    poss = possession_table(ev)
    poss["stint_id"] = ev.set_index("seq").stint_id.reindex(poss.first_seq).to_numpy()
    pc = poss.groupby(["stint_id", "offense"]).size().unstack(fill_value=0)
    # Raw ingredients for rebound percentages (Phase 2): live misses and rebounds after them, by team.
    ev = ev.assign(fg_miss=(ev.etype == "fg") & ~ev.made, ft_miss_live=ev.live_miss & (ev.etype == "ft"),
                   oreb=ev.reb_off, dreb=ev.reb_live & ~ev.reb_off)
    extra = ev.groupby(["stint_id", "team_id"])[["fg_miss", "ft_miss_live", "oreb", "dreb"]].sum()
    for team, side in ((home, "home"), (away, "away")):
        stints[f"{side}_pts"] = stints.stint_id.map(pts[team] if team in pts else {}).fillna(0).astype(int)
        stints[f"{side}_poss"] = stints.stint_id.map(pc[team] if team in pc else {}).fillna(0).astype(int)
        for col in extra.columns:
            s = extra[col].xs(team, level="team_id") if team in extra.index.get_level_values(1) else {}
            stints[f"{side}_{col}"] = stints.stint_id.map(s).fillna(0).astype(int)
    return stints


def _period_firsts(ev):
    """Index of the first event of each period (the period_start row when present)."""
    return ev.groupby("period").apply(lambda g: g.index[0], include_groups=False).to_dict()


# ---------------------------------------------------------------- rotation builder

def from_rotation(ev: pd.DataFrame, rotation: pd.DataFrame, home: int, away: int, game_id: str):
    ev = assign_possessions(ev)
    changes = []  # (time, order, team, pid, +1/-1); outs before ins at the same time
    for r in rotation.itertuples(index=False):
        changes.append((r.in_sec, 1, r.team_id, r.person_id, +1))
        changes.append((r.out_sec, 0, r.team_id, r.person_id, -1))
    changes.sort()
    lineup = {home: set(), away: set()}
    segments, ci = [], 0
    firsts = _period_firsts(ev)
    first_idx = set(firsts.values())

    def apply(limit, inclusive):
        nonlocal ci
        applied_t = None
        while ci < len(changes) and (changes[ci][0] <= limit if inclusive else changes[ci][0] < limit):
            t, _, team, pid, d = changes[ci]
            (lineup[team].add if d > 0 else lineup[team].discard)(pid)
            applied_t, ci = t, ci + 1
        return applied_t

    for i, e in enumerate(ev.itertuples(index=False)):
        if i in first_idx:
            apply(period_start(e.period) + TOL, inclusive=True)
            segments.append((i, period_start(e.period), e.period, {k: set(v) for k, v in lineup.items()}))
            continue
        if e.etype == "sub":
            t = apply(e.elapsed + TOL, inclusive=True)
        else:
            t = apply(e.elapsed - TOL, inclusive=False)
        if t is not None:
            segments.append((i, t, e.period, {k: set(v) for k, v in lineup.items()}))
    stints, ev = _segments_to_stints(ev, segments, home, away, game_id, "rotation")
    return stints, ev, {}


# ---------------------------------------------------------------- PBP rebuild

def infer_starters(ev_period: pd.DataFrame, team: int, roster: pd.DataFrame, prev_five: set) -> tuple[set, str]:
    """Starters for one team in one period.

    1. A player whose first appearance in the period is anything other than being subbed in started it
       (shots, rebounds, fouls, turnovers, or being subbed out).
    2. If fewer than 5 are found, fill from the previous period's closing five (players who weren't subbed in
       during this period), most box-score minutes first.
    3. Still short (e.g. period 1 with a silent player): fill from the rest of the roster by box minutes,
       excluding anyone subbed in during the period.
    Returns (starters, method note).
    """
    starters, subbed_in = set(), set()
    for e in ev_period.itertuples(index=False):
        if e.etype == "sub" and e.team_id == team:
            if e.out_id and e.out_id not in subbed_in:
                starters.add(e.out_id)
            if e.in_id:
                subbed_in.add(e.in_id)
        elif e.team_id == team and e.person_id and e.person_id not in subbed_in:
            if e.person_id in set(roster.person_id):
                starters.add(e.person_id)
    note = "events"
    by_minutes = roster.sort_values("seconds", ascending=False).person_id.tolist()
    if len(starters) < 5:
        for pid in [p for p in by_minutes if p in prev_five]:
            if len(starters) < 5 and pid not in subbed_in:
                starters.add(pid)
                note = "events+prev_period"
    if len(starters) < 5:
        for pid in by_minutes:
            if len(starters) < 5 and pid not in subbed_in:
                starters.add(pid)
                note = "events+minutes_fill"
    return starters, note


def from_pbp(ev: pd.DataFrame, box_df: pd.DataFrame, home: int, away: int, game_id: str):
    ev = assign_possessions(ev)
    rosters = {t: box_df[box_df.team_id == t] for t in (home, away)}
    firsts = _period_firsts(ev)
    lineup = {home: set(), away: set()}
    segments, info = [], {}
    for i, e in enumerate(ev.itertuples(index=False)):
        if firsts.get(e.period) == i:
            ev_p = ev[ev.period == e.period]
            for t in (home, away):
                lineup[t], note = infer_starters(ev_p, t, rosters[t], lineup[t])
                info[(e.period, t)] = {"starters": sorted(lineup[t]), "method": note}
            segments.append((i, period_start(e.period), e.period, {k: set(v) for k, v in lineup.items()}))
        elif e.etype == "sub" and e.team_id in lineup:
            lineup[e.team_id].discard(e.out_id)
            if e.in_id:
                lineup[e.team_id].add(e.in_id)
            segments.append((i, e.elapsed, e.period, {k: set(v) for k, v in lineup.items()}))
    stints, ev = _segments_to_stints(ev, segments, home, away, game_id, "pbp_rebuild")
    return stints, ev, info


def player_stints(stints: pd.DataFrame, home: int, away: int) -> pd.DataFrame:
    """Long form: one row per player per stint, with that player's team for/against points and possessions."""
    parts = []
    for side, team, opp in (("home", home, "away"), ("away", away, "home")):
        s = stints[["game_id", "stint_id", "seconds", f"{side}_ids", f"{side}_pts", f"{opp}_pts",
                    f"{side}_poss", f"{opp}_poss"]].explode(f"{side}_ids")
        s.columns = ["game_id", "stint_id", "seconds", "person_id", "pts_for", "pts_against", "poss_off", "poss_def"]
        parts.append(s.assign(team_id=team).dropna(subset=["person_id"]))
    out = pd.concat(parts, ignore_index=True)
    out["person_id"] = out.person_id.astype("int64")
    return out
