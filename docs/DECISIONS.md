# Decisions

Each entry: date, the decision, the options that were on the table, and the reasoning (Jonathan's).

---

## D1 — Possession source for per-100 stats (2026-10-19, Phase 1)

**Decision:** Possessions are counted from our own play-by-play stints. NBA's official
`leaguedashplayerstats` Per100 numbers are pulled alongside as a cross-check only.

**Options considered:** (a) compute from stints only, (b) NBA leaguedash Per100 only, (c) both, stints primary.

**Reasoning:** The archetype model is fit on 2024-25 + 2025-26 and frozen; 2026-27 players are projected into
it. If the possession definition differed between fit data and projected data, players could appear to drift
when only the counting method changed — that would corrupt H2 and H3. Counting from stints guarantees one
definition everywhere and keeps working if stats.nba.com blocks requests. The official numbers cost one
request per season and catch stint-parsing bugs. If stats.nba.com is blocked the cross-check is skipped and
nothing else breaks.

**Tolerance:** stint possessions vs NBA possessions, per team-season. A gap **> 2%** is treated as a parser bug
(hard fail). At or below 2% it is treated as a definitional difference and reported.

---

## D2 — Which games are pulled (2026-10-19, Phase 1)

**Decision:** Regular season, play-in, and playoffs, each tagged with
`season_type ∈ {regular, play_in, playoffs}` (from the game-id prefix 002 / 005 / 004).

**Options considered:** (a) regular season only, (b) regular + playoffs flagged, (c) regular + playoffs + NBA Cup.

**Reasoning:** Storing extra games is cheap and filtering later is free; re-pulling a season mid-project is
not. Play-in gets its own value: do-or-die games between non-playoff-level teams shouldn't blend into either
group. No separate Cup type: Cup group games, quarterfinals and semifinals already count as regular season;
only the championship game (prefix 006) doesn't, and it is not pulled.

**Default filter per model (applied in later phases):**
- Archetype model: regular season only. Playoffs are a different setting (tighter rotations, opponent-specific
  game plans, 16 teams) and would bend archetypes toward playoff teams.
- RAPM: regular season for the main fit; playoffs as a sensitivity check.
- Comparison baselines: the 2025 playoff run is kept as a separate comparison (Turner-era spacing against
  prepared defenses for H1; pre-injury Haliburton for H2), not as the main baseline.

---

## D3 — Games that fail stint validation (2026-10-19, Phase 1)

**Decision:** If stints built from `gamerotation` fail a hard check, rebuild that game's stints from
play-by-play substitutions plus period-starter inference and re-run the checks. If it still fails, quarantine it.

**Options considered:** (a) quarantine and exclude, (b) keep with a flag column, (c) rebuild from PBP, then quarantine.

**Additions:**
- Quarantine report, one row per failed game: game_id, season, season_type, failed check(s), residual,
  rebuild attempted, rebuild result, Pacers game. Regenerated on every refresh and exported for the site's
  Methods page.
- **Alarm threshold: more than 1.0% of a season's games quarantined → refresh stops** (non-zero exit, status
  flag, processed outputs not overwritten). A high rate means a parser bug, not bad luck.
- Any quarantined Pacers game gets a manual look from Jonathan.

**Note:** PBP only records substitutions, so a player who plays a full quarter without a sub never appears in
one; the rebuild must infer each period's starting five from other events. That inference is the first thing
to check when a rebuild fails.

---

## D4 — Where to test cloud blocking (2026-10-19, Phase 1)

**Decision:** A manually triggered GitHub Actions workflow runs `scripts/probe_endpoints.py`, 3 times a few
hours apart, during the first week.

**Options considered:** (a) GitHub Actions, (b) laptop only, (c) Claude Code cloud session.

**Reasoning:** The probe only means something if it runs where the weekly job would run. A Claude cloud session
is a different network; laptop-only leaves the hosted question open.

**Probe design:** each source tested separately (stats.nba.com, cdn.nba.com, pbpstats.com), 15 s timeout per
request with timeouts counted as blocked, status code and latency recorded.

**Reading the results (decided in advance):**
- Everything works → fully hosted weekly refresh.
- Only stats.nba.com blocked → laptop pulls stats.nba.com endpoints; GitHub handles the rest and the site deploy.
- Everything blocked → laptop runs the refresh; GitHub only builds and deploys the site from pushed data.

**Outcome:** _pending — fill in with date after the 3 probe runs. Re-run the probe if hosted pulls start
failing later in the season._

---

## D5 — Per-100 denominator and how it is cross-checked (2026-10-19, Phase 1)

**Decision:** Split denominators. Offensive stats are per 100 *offensive* possessions the player was on the
floor for; defensive stats per 100 *defensive* possessions. The stat-to-side mapping is D6.

**Options considered:** (a) split off/def, (b) every stat per 100 of (off + def) / 2 (closest to NBA's own
Per100), (c) every stat per 100 offensive possessions.

**Reasoning:** Each stat is measured against the chances it had to happen (a steal can only happen on
defense). It is the cleaner input for archetypes, which are meant to separate what a player does with the ball
from what he does without it. The difference from (b) is usually under 1–2%, so this is about correctness, not
shifting results.

**Cross-check the pieces, not the rates.** Per-100 rates are *not* compared with NBA's Per100. Instead:
- Counting stats per player-game must match the box score exactly; any gap is a parsing bug.
- Possessions per player-season are compared with NBA's player POSS, tolerance 2% (same number as D1).
If both pieces check out, the rates built from them are right whatever the denominator, and a count error
can't hide behind a possession error that cancels it.

**Phase 2 note:** rebounds should become rebound percentages (share of available rebounds), not per-100.
Stints already record missed FGs, missed last FTs, and offensive/defensive rebounds after live misses for this.

---

## D6 — Stat-to-side mapping (2026-10-19, Phase 1) — PROPOSED, pending Jonathan's review

Full table with reasoning in docs/METHODS.md ("Per-100 computation"). Proposed default as implemented in
`src/pacersml/data/per100.py` (`SIDE`):
- Offensive: PTS, FGM, FGA, 3PM, 3PA, FTM, FTA, AST, TOV, OREB
- Defensive: STL, BLK, DREB, PF
- Not used in Phase 1: fouls drawn (in cdn liveData box, not in stats.nba.com box v3, so it would be
  inconsistent across sources), charges drawn (hustle-stats endpoint, not pulled).

**Jonathan's choice:** _pending_

---

## D7 — Player-season possession flag and gap direction (2026-10-19, Phase 1)

**Decision:**
- **Player-season flag:** gap vs NBA player POSS above **2% and** above **5 possessions** (absolute). Report-only;
  never stops a run.
- **Team-season gap above 2%** is treated as a bug (unchanged from D1; refresh exits 4).
- **Direction of player gaps:** the report shows the share of player-seasons where our count is over vs under
  NBA's. A split outside roughly **40/60** means investigate (reported, not a run stop).

**Options considered:** (a) a minimum possession count before flagging, (b) an absolute possession floor on the
flag, (c) report only with no flag.

**Reasoning:** The gap is not sampling noise: we count the same games NBA does. It comes from definitional
differences (crediting a possession across a mid-trip substitution, at period ends, around technical FTs), each
of which moves a player's count by a possession or two over a season. So the threshold belongs in possessions:
a 20-possession player off by 1 (5%) is harmless; a 3,000-possession player off by 60 (2%) is worth a look. A
minimum count would hide low-minute players, including real bugs that only affect them. The player check doesn't
need to stop runs because two other checks catch real bugs better: the team-season check (sub-boundary
attribution evens out at team level, so a gap there means something is broken) and the direction of player gaps
(definitional gaps should split about evenly; a lopsided split points to a systematic bug such as possessions
dropped at period ends, even when every individual gap is small). Low-possession players never reach the
analysis anyway, since the Phase 2 archetype model applies a minutes cutoff.
