"""Stints: stretches of a game with no change in the ten players on the floor.

Two builders (D11) produce the same output; `stint_method` records which one built each stint:
    from_hybrid  - primary. Each period's starting five from stats.nba.com gamerotation (who is on the floor at
                   the period start), then every play-by-play substitution after that.
    from_pbp     - fallback when a game has no usable rotation data: PBP substitutions plus inferred starters.
Exactly five per team on every stint is enforced afterwards by the `floor_five` validation check, whichever
builder ran. The rotation file's own substitution timing is not used to build stints; `compare_sub_timing`
checks it against the PBP substitutions instead (a large gap usually means a sub missing from the PBP).

Output of either builder:
    stints:  game_id, stint_id, period, start, end, seconds, home_ids, away_ids (tuples of person ids),
             home_pts, away_pts, home_poss, away_poss, stint_method,
             {home,away}_{fg_miss, ft_miss_live, oreb, dreb}  (rebound-percentage ingredients)
    events:  the input events with `stint_id`, `poss_id`, `offense`
    info:    starters per (period, team) and how they were found, for debugging failed games
"""
from __future__ import annotations

import pandas as pd

from pacersml.data.normalize import period_length, period_start
from pacersml.data.possessions import assign_possessions, possession_table

TOL = 0.5      # seconds; rotation times are in tenths, PBP clocks in hundredths
SUB_GAP = 2.0  # seconds; PBP sub vs rotation-file change further apart than this is counted (D11)


def _segments_to_stints(ev, segments, home, away, game_id, method):
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
                     "away_ids": tuple(sorted(lineup[away])), "stint_method": method})
    stints = pd.DataFrame(rows)
    ev = credit_ft_trips(ev.assign(stint_id=stint_of_event.to_numpy()))
    return _aggregate(stints, ev, home, away), ev


def credit_ft_trips(ev: pd.DataFrame) -> pd.DataFrame:
    """Free throws belong to the lineup on the floor when the foul happened (D8), matching NBA's box +/-.

    Shooting trips, and-ones, flagrant and clear-path FTs: anchored to the last real play before the trip
    (normally the foul), skipping subs, timeouts/replays ('other') and dead-ball rebounds between FTs.
    Technical FTs: anchored to the most recent technical foul, never to a nearby shooting trip.
    Everything after the last FT of a trip (rebound of a missed last FT, the retained possession after a
    flagrant, the next play) keeps the stint it happened in.
    """
    stint = ev.stint_id.to_numpy().copy()
    last_play, last_tech = None, None
    period = None
    for i, e in enumerate(ev.itertuples(index=False)):
        if e.period != period:
            period, last_play, last_tech = e.period, None, None
        if e.etype == "ft":
            anchor = last_tech if e.technical else last_play
            if anchor is not None:
                stint[i] = stint[anchor]
        elif e.etype == "foul" and e.technical:
            last_tech = i
        elif e.etype in ("sub", "other", "period_start") or (e.etype == "rebound" and not e.reb_live):
            continue
        else:
            last_play = i
    return ev.assign(stint_id=stint)


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


# ---------------------------------------------------------------- builders

def rotation_starters(rotation: pd.DataFrame, period: int, team: int) -> set:
    """Players the rotation file has on the floor at the start of `period`."""
    t = period_start(period) + TOL
    r = rotation[(rotation.team_id == team) & (rotation.in_sec <= t) & (rotation.out_sec > t)]
    return set(r.person_id)


def usable_rotation(rotation: pd.DataFrame | None, periods, home: int, away: int) -> bool:
    """Rotation data is used only if it gives exactly five starters per team in every period."""
    if rotation is None or rotation.empty:
        return False
    return all(len(rotation_starters(rotation, p, t)) == 5 for p in periods for t in (home, away))


def _walk_subs(ev, starters, home, away, game_id, method):
    """starters(period, team, ev_period, current_lineup) -> (set, note). Applies every PBP sub after that."""
    ev = assign_possessions(ev)
    firsts = _period_firsts(ev)
    lineup = {home: set(), away: set()}
    segments, info = [], {}
    for i, e in enumerate(ev.itertuples(index=False)):
        if firsts.get(e.period) == i:
            ev_p = ev[ev.period == e.period]
            for t in (home, away):
                lineup[t], note = starters(e.period, t, ev_p, lineup[t])
                info[(e.period, t)] = {"starters": sorted(lineup[t]), "method": note}
            segments.append((i, period_start(e.period), e.period, {k: set(v) for k, v in lineup.items()}))
        # Not elif: between-period subs are logged before the period_start row, so a period's first row is often
        # a sub, and it must still be applied (the rebuild's starters are the lineup before those subs).
        if e.etype == "sub" and e.team_id in lineup:
            lineup[e.team_id].discard(e.out_id)
            if e.in_id:
                lineup[e.team_id].add(e.in_id)
            segments.append((i, e.elapsed, e.period, {k: set(v) for k, v in lineup.items()}))
    stints, ev = _segments_to_stints(ev, segments, home, away, game_id, method)
    return stints, ev, info


def from_hybrid(ev: pd.DataFrame, rotation: pd.DataFrame, home: int, away: int, game_id: str):
    """Primary builder (D11): period starters from the rotation file, substitutions from the play-by-play."""
    return _walk_subs(ev, lambda p, t, ev_p, cur: (rotation_starters(rotation, p, t), "rotation"),
                      home, away, game_id, "hybrid")


def compare_sub_timing(ev: pd.DataFrame, rotation: pd.DataFrame, gap: float = SUB_GAP) -> dict:
    """Compare PBP substitution times with the rotation file's in/out times (D11; report-only).

    pbp_subs_off       PBP subs where the player leaving or entering has no rotation change within `gap` s
    rotation_unmatched rotation changes (not at a period boundary) with no PBP sub for that player within `gap` s;
                       usually a substitution missing from the play-by-play
    """
    n_per = int(ev.period.max())
    bounds = [period_start(p) for p in range(1, n_per + 2)]

    def inside(t):  # changes at period starts/ends are lineup resets, not substitutions
        return min(abs(t - b) for b in bounds) > TOL

    def index(pairs):
        idx = {}
        for pid, t in pairs:
            if pid and inside(t):
                idx.setdefault(pid, []).append(t)
        return idx

    def matched(pid, t, idx):
        return any(abs(t - u) <= gap for u in idx.get(pid, []))

    rot_out = index((r.person_id, r.out_sec) for r in rotation.itertuples())
    rot_in = index((r.person_id, r.in_sec) for r in rotation.itertuples())
    subs = ev[(ev.etype == "sub") & ev.elapsed.map(inside)]
    pbp_out = index((r.out_id, r.elapsed) for r in subs.itertuples())
    pbp_in = index((r.in_id, r.elapsed) for r in subs.itertuples())

    pbp_off = sum(1 for r in subs.itertuples()
                  if (r.out_id and not matched(r.out_id, r.elapsed, rot_out))
                  or (r.in_id and not matched(r.in_id, r.elapsed, rot_in)))
    rot_un = [(pid, t) for idx, other in ((rot_out, pbp_out), (rot_in, pbp_in))
              for pid, ts in idx.items() for t in ts if not matched(pid, t, other)]
    return {"pbp_subs": int(len(subs)), "pbp_subs_off": pbp_off,
            "rotation_changes": sum(len(v) for v in rot_out.values()) + sum(len(v) for v in rot_in.values()),
            "rotation_unmatched": len(rot_un),
            "rotation_unmatched_detail": ";".join(f"{p}@{t:.1f}" for p, t in rot_un)[:200]}


# ---------------------------------------------------------------- PBP rebuild

def infer_starters(ev_period: pd.DataFrame, team: int, roster: pd.DataFrame, prev_five: set) -> tuple[set, str]:
    """Starters for one team in one period.

    1. A player whose first appearance in the period is anything other than being subbed in started it
       (shots, rebounds, fouls, turnovers, or being subbed out). Technical fouls and ejections don't count:
       bench players get them (0022400664: a bench double technical made a sixth "starter"; 0022501127: an
       ejection from the bench).
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
        elif (e.team_id == team and e.person_id and e.person_id not in subbed_in and not e.technical
              and not str(e.desc).startswith("Ejection")):
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
    """Fallback builder: inferred period starters, substitutions from the play-by-play.
    (A box-minutes starter repair was tried and recovered no games, D14; not kept.)"""
    rosters = {t: box_df[box_df.team_id == t] for t in (home, away)}
    return _walk_subs(ev, lambda p, t, ev_p, cur: infer_starters(ev_p, t, rosters[t], cur),
                      home, away, game_id, "pbp_rebuild")


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
