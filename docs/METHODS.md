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
  gets at most 2 calls across runs (D12), made by a rotation-only pass after the download (D13); a game without a
  rotation file after that uses the rebuild.
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
- **Most of the frozen data uses the rebuild.** gamerotation throttled us for days, and the pass was stopped (D24).
  Rotation files: 2024-25 886 of 1,320 games, 2025-26 237 of 1,321, so 2025-26 is 82% rebuild. Evidence that the
  rebuild holds up: quarantine rates of 1.8% (2024-25) and 0.55% (2025-26) against 1.4% and 0.8% for the hybrid,
  and the Pacers period-starter spot check (D23: 26 of 26, including a rebuild game). The formal test is the
  Phase 3 RAPM fit on hybrid games only, compared with the full fit.

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
| minutes | each player's stint seconds within ±1 s of box MIN; a gap up to 3 s passes **with a note** when it's unpaired (no teammate off by > 1 s the other way, D17) | yes (lineup) |
| floor_five | every stint has exactly 5 per team | yes (lineup) |
| game_seconds | total stint seconds = 2880 + 300·OT (±1 s) | yes (lineup) |
| plus_minus | each player's stint point differential = box +/- exactly; ±2 passes **with a note** only when minutes pass and a substitution shares a second with a technical FT (D14) | yes (lineup) |
| team_points | PBP points per team = box points | yes |
| pbp_counts | PBP-derived PTS, FGM, FGA, 3PM, 3PA, FTM, FTA, TOV, REB, PF per player = box; a gap passes **with a note** when every team total matches (D14), or when team points match and each team's possessions are within 2% of pbpstats (D15) | yes |
| poss_pbpstats | team possessions vs pbpstats.com | reported only |

If any hard check fails, the game is quarantined (no second builder is tried, D11): kept out of processed tables, listed in
`data/processed/quarantine.parquet` and `site_export/quarantine.json` (game, checks failed, residuals,
`stint_method`, whether rotation data existed, the two sub-timing counts, Pacers flag, period starters).
A game that passes only through a noted exception is kept and listed separately as "kept with notes" (D14).

**Shadow rebuild (D15).** On every game with rotation data, the pure rebuild also runs, and its lineup checks
(minutes, floor_five, game_seconds, plus_minus) are recorded. Its stints are not kept.

Alarms:
- **hybrid alarm** (exit 2): any game where the shadow rebuild passes the lineup checks and the hybrid fails them
  (D3 amended, D15). Processed tables not overwritten;
- **regression alarm** (exit 6): any game that passed or was kept last run and is quarantined now. The run stops,
  nothing is written, the baseline (`game_outcomes.parquet`) is not updated (D15);
- no rate alarm. Games lost are counted per season by builder and group (A counts, B plus-minus, C lineup,
  D team points) on the Methods page.

Season-level:
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
  `pbp_counts` / `team_points` failures that no rebuild can fix. Games where team points and possessions still
  match are kept with a note (D15); their shot- and rebound-level counts can be off by a shot or two.
- The hybrid alarm only sees a hybrid bug when the rebuild gets that game right. A bug that hits both builders
  the same way (e.g. a substitution missing from the PBP) shows up as a lost game, not an alarm.
- The regression alarm compares with the last run, so it can't see a game that has failed since it was first
  processed.
- Plus-minus passing doesn't prove the lineups are right: two errors could cancel within one player's minutes.
  Minutes and plus-minus together make that unlikely, but not impossible.
- NBA's player POSS definition isn't documented. Player gaps are definitional (same games, no sampling), so
  individual gaps of a possession or two are expected; a lopsided over/under split is the signal to look for.
- The pbpstats comparison is reported, not enforced; pbpstats uses its own possession rules.
- The 3 s minutes note assumes our team seconds are exact (five on the floor for the whole game), so any lineup
  error shows as two teammates off in opposite directions. If floor_five or game_seconds also fail, that pairing
  logic doesn't hold, and those checks quarantine the game anyway.
- Log order within one second is NBA's, not the true order. A sub logged before a foul in the same second moves
  that foul's free throws to the wrong lineup. A trial rule that moves such subs after live-play events
  (`refresh.py --reorder-subs`, D17) fixed 1 game and broke 102 in testing, so it is not used.

**Questions you should be able to answer.**
1. Why is plus-minus the strongest single check on lineups?
2. A season has 15 of 1,230 games quarantined. What happens, and what is the first thing to look at?
3. Which checks can the PBP rebuild fix, and which can't it?
4. A game's Pacers rebound total matches the box, but one Pacer has 2 rebounds too many and another 2 too few.
   Is it kept, and what does that do to team rebound rate vs player rebound rate?
5. A hybrid game fails the minutes check and its shadow rebuild fails too. Does an alarm fire, and why?
6. One player is 2.5 s over his box minutes and a teammate is 2.5 s under. Is the game kept? What if only the
   first player is off?

---

## 5. Archetype model: Gaussian mixture (Phase 2) — `src/pacersml/archetypes/`

**Status:** written before fitting; Jonathan's setup choices (D25) filled in. k is not chosen yet.

**What it does.** Each player-season becomes one point in a feature space: a handful of numbers describing how
he plays. Rows: player-seasons with 500+ regular-season minutes (D2, D25), teams combined for traded players.
Features (D25): 17 style-only measures in four groups, with no efficiency stats (no FG%, 3P%, TS%):
- *shooting:* share of FGA at the rim, short mid (paint, non-RA), corner 3, above-break 3 (long mid is the
  remainder, so it is left out of the fit and only reported); pull-up/step-back 3PA per FGA; FTA per FGA;
- *creation:* shot attempts + turnovers per 100, AST per 100, share of made FG assisted, driving FGA per FGA,
  fouls drawn per 100;
- *rebounding:* OREB%, DREB% (his rebounds ÷ the team's chances while he was on the floor);
- *defense:* STL, BLK, defensive fouls and charges drawn per 100 defensive possessions.
Shot zone, shot type and assister come from the liveData play-by-play. Each feature is standardized
(minus its mean, divided by its standard deviation over the 2024-25 + 2025-26 training rows), so no feature counts
for more just because of its units. A Gaussian mixture model (GMM) assumes these points come from k overlapping
bell-shaped clouds. Each cloud has a center (the "typical" player of that archetype), a shape (which features vary
together inside it), and a weight (its share of players). The fit (expectation–maximization) alternates two steps
until nothing changes:
1. Given the clouds, give each player a probability of belonging to each one.
2. Given those probabilities, move each cloud's center, shape and weight to fit its players.

Unlike k-means, every player gets a probability for every archetype, not just a label. A player between two
roles shows up as 0.55 / 0.45, not as a confident member of one.

**What gets reported for each k** (k = 2–15, for full, tied and diag covariance, D25; k is not chosen in this step):
- **BIC** (Bayesian information criterion): how well the model fits, minus a penalty for every extra parameter.
  Lower is better. It's shown across k as a curve; with ~1,000 rows it often keeps falling slowly, so it's an
  input to your choice, not the choice.
- **Held-out log-likelihood by time:** fit on 2024-25 rows only, score the 2025-26 rows. Rises when extra
  archetypes describe real structure, flattens or falls when they only fit 2024-25 noise. (Time split, per the
  data rules.)
- **Cluster sizes:** player-seasons per archetype (hard assignment = most likely archetype), plus the sum of
  membership probabilities, and the share of players whose top probability is under 0.6 (the "between roles"
  share).
- **The 8 players nearest each center:** by Mahalanobis distance under that archetype's own shape (distance in
  standard deviations of that cloud), with their membership probability, season, minutes and feature values. The
  center itself is printed in original units (e.g. "38% of shots at the rim") so you can name it.
- **Stability**, three checks:
  1. *Starts:* the same k fitted from 20 random starting points. Do they reach the same solution? Agreement is
     measured with the adjusted Rand index (ARI: 1 = identical groupings, 0 = no better than chance) between each
     fit's labels and the best fit's.
  2. *Bootstrap:* 50 refits on resampled players (drawn with replacement). Each refit labels all original
     players; ARI against the full fit. Also per archetype: the share of its players who keep the same archetype
     across refits (retention), flagged under 70% (D25).
  3. *Season-to-season:* fit on 2024-25 only and on 2025-26 only, assign every row with each model, ARI between
     the two labelings. Archetypes that only exist in one season show up here.
  Archetype numbers change between refits (archetype 3 in one fit may be archetype 5 in another). They are matched
  to the full fit by center distance (Hungarian matching) before anything is compared.

**After you pick k:** the model (scaler means and SDs, centers, shapes, weights) is saved and frozen with a hash
in the manifest. 2026-27 player-seasons are standardized with the training means and SDs and *assigned* to the
frozen archetypes, never used to refit (data rules).

**Toy example.** Two features, 3PA share of FGA and AST/100, five players, k = 2. For simplicity both clouds are
round with the same spread (σ = 0.75 in standardized units).

| player | 3PA share | AST/100 | z(3PA) | z(AST) | dist to A | dist to B | P(archetype A) |
|---|---|---|---|---|---|---|---|
| 1 | 0.60 | 4 | 1.20 | 0.39 | 0.50 | 2.76 | 1.00 |
| 2 | 0.55 | 5 | 0.98 | 1.37 | 0.50 | 3.24 | 1.00 |
| 3 | 0.05 | 3 | −1.24 | −0.59 | 2.76 | 0.50 | 0.00 |
| 4 | 0.10 | 2 | −1.02 | −1.57 | 3.24 | 0.50 | 0.00 |
| 5 | 0.35 | 4 | 0.09 | 0.39 | 1.11 | 1.91 | 0.90 |

Center A (players 1–2) sits at z = (1.09, 0.88), center B (3–4) at (−1.13, −1.08). Player 5 is closer to A, so
P(A) = exp(−1.11²/2σ²) / [exp(−1.11²/2σ²) + exp(−1.91²/2σ²)] = 0.90. A real fit also learns each cloud's shape
and weight, and recomputes the centers using these probabilities.

**What could make it wrong.**
- **Features that measure quality, not style.** Efficiency stats (FG%, TS%) or volume stats that rise with
  talent (points/100) produce "good player" clusters. Then a shooting slump looks like a role change (H2), and
  RAPM interactions (H4) count quality twice. This is why the feature set is style only (D25). Usage and the defensive rates still carry some quality.
- **Correlated features double-count.** FGA/100 and points/100 carry nearly the same information; including both
  makes "volume" count twice as much as anything else.
- **Small samples.** A 300-minute player's rates are noisy and land at the edges, where they can create or pull
  a cluster. The 500-minute cutoff (D25) trades sample size against noise. Players under it get projected weights (100–499
  minutes, flagged) or league shares (under 100) for RAPM, never a refit.
- **BIC with many rows** prefers more clusters, some of which split one role into fine shades. The held-out
  likelihood and the stability checks are the counterweight.
- **Local optima and initialization.** EM can stop at a poor solution; the 20 starts show whether that happens.
  How the starts are seeded matters: with k-means++ seeding (centers only, no k-means run) every tied model from
  k = 2 to 12 collapsed onto one center, the log-likelihood of a single Gaussian. Starts now run a full k-means
  first (sklearn's default), D26.
- **Shape assumptions.** Full covariance (each cloud its own tilt and spread) fits better but needs many more
  parameters per cloud; with k = 12 and ~12 features that's ~1,000 parameters on ~1,000 rows, and small clouds can
  collapse onto a few players. Full, tied (one shape shared by all clouds) and diag (no correlations) are all
  fitted, and the parameter count is reported next to each BIC (D25). Every covariance gets 0.0001 added to
  its diagonal (standardized units) so a tiny cloud can't become singular.
- **Player-seasons are not independent.** The same player appears twice (once per season), so bootstrap
  stability is a bit optimistic.
- **Team context.** Rates reflect role on a given team; a traded player's season pools two roles.

**Questions you should be able to answer.**
1. Why standardize the features, and what would happen to the clusters if 3PA share (0–1) and AST/100 (0–15)
   were used raw?
2. BIC keeps falling up to k = 15, but the bootstrap ARI drops below 0.5 after k = 8. What does each tell you?
3. A player is 0.55 archetype 2 and 0.45 archetype 6 in 2025-26 and 0.95 archetype 6 in 2026-27. Did he change
   roles? What else would you check?
