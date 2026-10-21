# Methods

---

## 1. Possession counting (Phase 1) — `src/pacersml/data/possessions.py`

**What it does.** Walks the play-by-play in order and tracks which team has the ball. Only some events tell
us that: a shot attempt, a (non-technical) free throw, or a turnover means the actor's team had it; a rebound
means the rebounding team now has it. Fouls, subs, timeouts, jump balls and technical free throws say nothing.
A possession is a run of events where the same team has the ball; it ends when the other team shows up in
control, or when the period ends. This one definition is used everywhere: per-100 denominators, stint
possessions, RAPM later (D1).

**Toy example.**

| # | event | control after | possession |
|---|---|---|---|
| 1 | IND 11 makes 2 | IND | P0 (IND) |
| 2 | NYK 21 misses | NYK | P1 (NYK) |
| 3 | IND 12 def. rebound | IND | P2 (IND) |
| 4 | IND 12 makes 2, fouled by NYK 22 (foul row is neutral) | IND | P2 |
| 5 | IND 12 FT 1 of 1 (and-one) | IND | P2 |

IND: 2 possessions, 2 + 3 points. NYK: 1 possession, 0 points. The and-one free throw stays in P2 because the
team in control doesn't change; an offensive rebound works the same way.

Also recorded for later rebound percentages: `live_miss` (missed FG or missed *last* FT of a trip),
`reb_live` (a rebound right after a live miss — dead-ball team rebounds between FTs are excluded) and
`reb_off` (that rebound went to the team that missed).

**What could make it wrong.**
- A possession with no recorded event (e.g. a team scores with 1 s left and the period ends before the other
  team touches the ball) is not counted.
- Technical FTs are identified by the word "technical" in the event subtype/description. If a source labels them
  differently, they would split a possession in two.
- Team turnovers or team rebounds with a missing `team_id` are ignored.
- Flagrant-foul FTs followed by the fouled team keeping the ball are handled correctly (same team), but a
  clear-path or away-from-play situation that the source logs oddly might not be.
- Possessions are assigned to the stint in which they *start*. A possession that spans a substitution
  (e.g. between free throws) counts for the lineup that started it, while its points go to whichever lineup was
  on the floor when each point was scored.

**Questions you should be able to answer.**
1. Why does an offensive rebound not create a new possession, and what would happen to a team's per-100
   numbers if it did?
2. Our count and NBA's official POSS differ slightly. Name two concrete event sequences where the definitions
   could disagree.
3. Why is it important for H2/H3 that 2026-27 possessions are counted by exactly this code rather than taken
   from NBA's endpoint?

---

## 2. Stint construction (Phase 1) — `src/pacersml/data/stints.py`

**What it does.** A stint is a stretch of game time with the same ten players on the floor. Two builders
(D11); `stint_method` on every stint records which one ran:

- **Hybrid (primary).** stats.nba.com `gamerotation` gives each period's starting five (who is on the floor at the
  period start); every play-by-play substitution after that swaps one player. Used when the rotation file gives
  exactly five starters per team in every period. gamerotation fails per game (500s and hangs), so each game
  gets at most 2 calls across runs (D12); a game without a rotation file after that uses the rebuild.
- **PBP rebuild (fallback, only when rotation data is missing).** Each period's starting five is inferred, then
  every substitution swaps one player. Starters are inferred as: anyone whose first appearance in the period
  is anything other than being subbed in; if fewer than 5, fill from the previous period's closing five; if still
  short, fill from the rest of the roster by box-score minutes (never anyone subbed in during that period).

If the checks still fail, the game is quarantined; the other builder is not tried.

**Rotation timing as a comparison (report-only).** For every substitution, the PBP time is compared with the
rotation file's in/out time for the same player: PBP subs with no rotation change within 2 s (`pbp_subs_off`) and
rotation changes with no PBP sub within 2 s (`rotation_unmatched`, usually a sub missing from the play-by-play).
Changes at period boundaries are lineup resets and are skipped.

**Free-throw crediting (D8)**, applied after either builder:

| situation | credited to |
|---|---|
| shooting-foul trip (FT 1, sub, FT 2) | lineup on the floor at the foul |
| and-one FT | lineup at the foul (the made shot's lineup) |
| flagrant / clear-path FTs | lineup at the foul; the retained possession after them → lineup on the floor then |
| technical FT | lineup on the floor when the technical was called, never a nearby trip |
| anything after the last FT of a trip (rebound of a missed last FT, putback, next play) | lineup on the floor at the time |

Implementation: each FT is anchored to the last real play before it (subs, timeouts/replays and dead-ball
rebounds between FTs are skipped); technical FTs are anchored to the last technical foul.

Each stint stores both lineups, start/end time, seconds, points and possessions for each team, plus missed FGs,
missed last FTs and offensive/defensive rebounds (rebound-percentage ingredients for Phase 2).

**Toy example** (`tests/toy.py`, period 1 only).

| stint | seconds | IND on floor | NYK on floor | IND pts | NYK pts | IND poss | NYK poss |
|---|---|---|---|---|---|---|---|
| 0 | 0–60 | 11 12 13 14 15 | 21–25 | 5 | 2 | 2 | 2 |
| 1 | 60–720 | 11 12 13 15 16 | 21–25 | 0 | 2 | 1 | 1 |

The sub (16 for 14) is logged between NYK's two free throws; both FTs count in stint 0, the lineup at the foul (D8).
Player 15 never appears in an event and is filled in by the rebuild from box-score minutes.

**What could make it wrong.**
- **Starter inference (rebuild only)** is the weak point: a player who plays an entire quarter without a
  recorded event is invisible to the PBP. If a rebuilt game fails, check the `starters` column in the quarantine
  table first.
- **A substitution missing from the play-by-play** breaks the hybrid from that point in the period (minutes and
  plus-minus fail). The `rotation_unmatched` count usually flags it before the minutes check does.
- The rotation file itself can be wrong at a substitution (0022400064: 6 players for the last 2 s). The hybrid only
  uses it for period starters, which is why it was chosen (D11).
- stats.nba.com v3 substitutions are one row ("SUB: Zubac FOR Turner"); the player without an id is matched by
  family name against that team's box score. Two players with the same family name on one team → unresolved.
- Both PBP normalizers have been run on one real game (0022500005) with every check passing; a full season is the
  real test. liveData is the primary PBP source (it records who drew each foul); v3 is the fallback.

**Questions you should be able to answer.**
1. Which part of a stint does the hybrid take from the rotation file, which part from the play-by-play, and why
   that split?
2. In the toy example the sub is logged between NYK's free throws. Why do both count against the lineup with
   player 14, and what would happen to the plus-minus check if FT 2 went to the lineup with player 16?
3. A rebuild fails on minutes for one player by exactly 12:00. What is the most likely cause?

---

## 3. Per-100 computation (Phase 1) — `src/pacersml/data/per100.py`

**What it does.** Numerators are box-score counts per player-game. Denominators are the possessions the
player was on the floor for, from our stints. Offensive stats are divided by offensive possessions on the floor,
defensive stats by defensive possessions (D5). Season tables are one row per player × season × season type
(regular / play_in / playoffs), summed across teams for traded players, and keep `poss_off`, `poss_def`,
`games` and `seconds` next to every rate so each number carries its sample size.

**Stat-to-side mapping (D6).**

| stat | side | source | note |
|---|---|---|---|
| PTS, FGM, FGA, 3PM, 3PA, FTM, FTA | off | box | |
| AST | off | box | |
| TOV | off | box | includes offensive fouls — the only place they are counted |
| OREB | off | box | Phase 2: replace with OREB% |
| fouls drawn | off | PBP (liveData) | non-offensive fouls drawn while his team had the ball; rim-pressure measure (H2) |
| non-offensive fouls committed on offense (`pf_off_other`) | off | PBP | e.g. loose-ball fouls by the team with the ball |
| STL, BLK | def | box | |
| DREB | def | box | Phase 2: replace with DREB% |
| defensive PF (`pf_def`) | def | PBP | non-technical, non-offensive fouls committed while defending |
| charges drawn | def | PBP (liveData) | offensive fouls recorded as charges, credited to the player who drew them |
| box PF, `pf_offensive`, `off_fouls_drawn`, `pf_side_unknown` | — | box / PBP | stored, no per-100 |

The side of each foul is NBA's own possession field on the liveData action. Fouls drawn and charges drawn exist
only in liveData play-by-play; for a game that fell back to v3 they are NaN, and their per-100 rates use
possessions from liveData games only (`poss_off_drawn`, `poss_def_drawn`). Which of these become archetype
features is a Phase 2 decision.

**Toy example.**

| player | PTS | STL | off poss | def poss | PTS/100 | STL/100 |
|---|---|---|---|---|---|---|
| A | 20 | 1 | 50 | 48 | 40.0 | 2.08 |
| B | 10 | 2 | 25 | 26 | 40.0 | 7.69 |
| C | 0 | 0 | 0 | 2 | NaN | 0.0 |

C has no offensive possessions, so offensive rates are NaN rather than 0.

**What could make it wrong.**
- Possession counting errors propagate directly; the possession cross-check (section 4) is the guard.
- Small samples give extreme rates; the possession counts are stored so later phases can filter. No minimum is
  applied in Phase 1 (that's your call, later).
- Games in quarantine are excluded from both numerator and denominator.

**Questions you should be able to answer.**
1. Why compare counts and possessions against NBA separately, instead of comparing per-100 rates?
2. Why are offensive fouls counted only in TOV, and what would happen to a charge-prone player's defensive profile if box PF were used instead?
3. Player B has the same PTS/100 as A in half the possessions. What does that say about how much to trust each?

---

## 4. Stint-vs-box validation and quarantine (Phase 1) — `src/pacersml/data/validate.py`, `pipeline.py`

**What it does.** Every game is checked against its own box score.

| check | rule | hard? |
|---|---|---|
| minutes | each player's stint seconds within ±1 s of box MIN | yes (lineup) |
| floor_five | every stint has exactly 5 per team | yes (lineup) |
| game_seconds | total stint seconds = 2880 + 300·OT (±1 s) | yes (lineup) |
| plus_minus | each player's stint point differential = box +/- exactly | yes (lineup) |
| team_points | PBP points per team = box points | yes |
| pbp_counts | PBP-derived PTS, FGM, FGA, 3PM, 3PA, FTM, FTA, TOV, REB, PF per player = box exactly | yes |
| poss_pbpstats | team possessions vs pbpstats.com | reported only |

If any hard check fails, the game is quarantined (no second builder is tried, D11): kept out of processed tables, listed in
`data/processed/quarantine.parquet` and `site_export/quarantine.json` (game, checks failed, residuals,
`stint_method`, whether rotation data existed, the two sub-timing counts, Pacers flag, period starters).

Season-level:
- more than **1%** of a season's games quarantined → refresh exits with code 2, processed tables not overwritten (D3);
- team-season possessions vs NBA team POSS, gap **> 2%** → exit code 4 (D1);
- player-season possessions vs NBA player POSS, as (off+def)/2 and off-only: flagged when the gap is > 2% **and**
  > 5 possessions; report-only (D7);
- direction of player gaps: share of player-seasons over vs under NBA; outside 40/60 is marked "investigate" (D7).

Plots and pass-rate tables per season go to `reports/validation/`.

Before any of this, every refresh runs the access probe and stops if the game log, box score v3 or liveData
play-by-play isn't answering (D10). Games with no rotation data (fell back to the rebuild) are counted per season
in the run summary and in `site_export/quarantine.json`.

**Toy example** (one game, three players).

| player | stint sec | box sec | stint +/- | box +/- | result |
|---|---|---|---|---|---|
| 11 | 720.0 | 720 | +1 | +1 | pass |
| 14 | 60.0 | 60 | +4 | +4 | pass |
| 16 | 100.0 | 60 | −3 | +1 | fail → rebuild |

**What could make it wrong.**
- NBA sometimes corrects box scores after the fact without changing the PBP (or vice versa). That shows up as
  `pbp_counts` / `team_points` failures that no rebuild can fix.
- Plus-minus passing doesn't prove the lineups are right: two errors could cancel within one player's minutes.
  Minutes and plus-minus together make that unlikely, but not impossible.
- NBA's player POSS definition isn't documented. Player gaps are definitional (same games, no sampling), so
  individual gaps of a possession or two are expected; a lopsided over/under split is the signal to look for.
- The pbpstats comparison is reported, not enforced; pbpstats uses its own possession rules.

**Questions you should be able to answer.**
1. Why is plus-minus the strongest single check on lineups?
2. A season has 15 of 1,230 games quarantined. What happens, and what is the first thing to look at?
3. Which checks can the PBP rebuild fix, and which can't it?
