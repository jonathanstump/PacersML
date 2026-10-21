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

**Measurements so far** (`reports/access_probe/`; numbers only):

| date (UTC) | where | headers | stats.nba.com | cdn.nba.com | pbpstats.com |
|---|---|---|---|---|---|
| 2026-10-19 17:39 | laptop, campus (AS3782) | v1 | timeout ×5 | 403 ×3 | ok |
| 2026-10-20 02:30 | GitHub Actions (AS8075) | v1 | timeout ×5 | 403 ×3 | timeout |
| 2026-10-20 02:47 | laptop, hotspot (AS6167) | v1 | timeout ×5 | 403 ×3 | ok |
| 2026-10-20 03:05 | laptop, hotspot (AS6167) | v2 (sec-* headers) | ok ×4, gamerotation 500 | ok ×3 | ok |
| 2026-10-20 03:09 | GitHub Actions (AS8075) | v2 (sec-* headers) | timeout ×5 | 403 ×3 | ok |
| 2026-10-20 03:45 | laptop, campus (AS3782) | v2 (sec-* headers) | ok ×5 (gamerotation 200) | ok ×3 | ok |
| 2026-10-20 13:46 | GitHub Actions (AS8075), scheduled run 2 | v2 (sec-* headers) | timeout ×5 | 403 ×3 | ok |
| 2026-10-20 19:30 | GitHub Actions (AS8075), scheduled run 3 | v2 (sec-* headers) | timeout ×5 | 403 ×3 | timeout |

Scheduled runs 2 and 3 were set for 08:30 and 15:30 UTC; GitHub started them late (times above). The one-off
schedule was removed from the workflow afterwards; manual runs still work.

**Result (2026-10-20):** v2 headers fix laptop access on both networks (campus and hotspot); GitHub's network
(AS8075, Microsoft cloud) is blocked from both NBA sources whatever the headers. Setup: **laptop refresh, GitHub
deploy** (the "everything blocked" reading, applied to GitHub). Re-run the probe if laptop pulls start failing;
every refresh now runs it first (D10).

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

## D6 — Stat-to-side mapping (2026-10-20, Phase 1)

**Decision:**
- **Offensive** (per 100 offensive possessions): PTS, FGM, FGA, 3PM, 3PA, FTM, FTA, AST, TOV, OREB, fouls drawn.
- **Defensive** (per 100 defensive possessions): STL, BLK, DREB, defensive PF, charges drawn.
- **Offensive fouls are counted only in TOV**, never in PF.
- Loose-ball and other non-offensive fouls go to whichever side the fouling player's team was on at the time.
- Which stats enter the archetype feature set is a Phase 2 decision; all of these are computed and stored now so
  adding one later doesn't mean re-parsing three seasons.

**Reasoning:** Box-score PF mixes defensive fouls with offensive fouls that already count in TOV, so a player who
commits a lot of charges would look like a foul-prone defender and those plays would count twice. Splitting PF by
side fixes both. Fouls drawn is the most direct measure of rim pressure, including non-shooting fouls that FTA
misses (H2, Haliburton). The earlier reason for leaving it out (present in liveData, absent from stats.nba.com
box v3) no longer applies: liveData play-by-play is now the primary PBP source and records who drew every foul.

**Verified on game 0022500005** (liveData PBP): PBP personal fouls = box PF for 23/23 players; offensive fouls =
box `foulsOffensive` 23/23; fouls drawn (incl. offensive fouls drawn) = liveData box `foulsDrawn` 23/23.
liveData marks some offensive fouls as charges, with the drawing player (3 of 19 offensive fouls across 6 games
checked), so charges drawn is available.

**Implementation notes:**
- The side of a foul comes from NBA's own possession field on each liveData action. Our possession tracker
  lags right after a made basket and put 15 of 71 fouls on the wrong side in the test game.
- Games parsed from v3 (fallback only) have no fouls-drawn data: those columns are NaN, and their per-100 rates use
  possessions from liveData games only (`poss_off_drawn` / `poss_def_drawn`). Foul side falls back to our tracker.
- Also stored, not mapped: offensive fouls committed (`pf_offensive`, already in TOV), all offensive fouls drawn
  (`off_fouls_drawn`), non-offensive fouls committed on offense (`pf_off_other`, mapped to offense per the
  loose-ball rule), fouls before either team had the ball (`pf_side_unknown`).

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

---

## D8 — Free-throw attribution in stints (2026-10-20, Phase 1)

**Decision:**
- A free-throw trip (shooting fouls, and-ones, flagrant and clear-path FTs) is credited to the lineup on the floor
  **at the foul**, even when NBA logs substitutions between the free throws.
- Technical free throws are credited to the lineup on the floor **when the technical was called**; they are never
  bundled with a nearby shooting trip.
- The trip ends at the last free throw. Everything after it (rebound of a missed last FT, a putback, the possession
  retained after a flagrant or clear-path foul, the next play) goes to the lineup on the floor at the time.
- The plus-minus check stays strict: exact match per player-game.

**Options considered:** (a) lineup at the foul, (b) play-by-play order (each FT to whoever is on the floor at that
line of the log).

**Reasoning:** It matches NBA's box-score plus-minus: on the first real test game (0022500005) every player
matched exactly, versus 20 players off by up to 4 under PBP order. Free throws come from a foul against the
lineup on the floor, so the trip belongs to that lineup; crediting FT 2 to incoming players would hand them
points for a play they weren't part of. It also keeps points and possessions under one attribution rule
(possessions already go to the lineup that started them); splitting them would corrupt per-100 numbers in a
way no check would catch. With the check passing, any future plus-minus mismatch means a real bug.

---

## D9 — Data access route (2026-10-20, Phase 1)

> **Superseded by D10** (same day). Kept for the record of why the plan changed.

**Context:** With the v1 probe headers, NBA refused every network tested (campus, hotspot, GitHub).

**Options considered:** (1) GitHub archive (shufinskiy/nba_data) for 2024-25 and 2025-26 + pbpstats per-game
stats as the box score + browser route for 2026-27; (2) pbpstats only; (3) find an unblocked network.

**Decision:** Option 1, conditional on first testing whether the block was the request's fingerprint rather than
the network. Option 1 is the only one that keeps stints, which H1 (on/off) and H4 (RAPM) depend on.

**Fingerprint test result (2026-10-20):** adding browser `sec-ch-ua` / `sec-fetch-*` headers made stats.nba.com
and cdn.nba.com answer from the hotspot (see D4 table), so the original sources are back for laptop pulls, with
one exception: `gamerotation` returns HTTP 500 for every game tried, so **every game goes through the PBP
rebuild**. GitHub Actions remains blocked by network. The archive / browser route is on hold, not built.

**Update (2026-10-20 03:45):** on the campus network with v2 headers, `gamerotation` answers (200 for games in
2024-25, 2025-26 and 2025-26 playoffs), so the rotation builder is back as the primary stint path there; the 500s
were specific to the hotspot. On the test game every check passed on the rotation builder with no rebuild.
The two adjustments below still apply to any game that ends up on the rebuild.

**Adjustments that still apply because every game now uses the rebuild:**
- Re-measure the quarantine threshold: run all of 2024-25, check the actual quarantine rate, and re-set the D3
  alarm here from that, not from the earlier guess.
- Spot-check period starters on **3** Pacers games against what Jonathan watched, including at least one overtime game.

**If the laptop route stops working for 2026-27:** fall back to pbpstats for 2026-27 only, and first compute
pbpstats' possession definition on the archive seasons to measure its gap from ours. Under about 1%: projecting
into the frozen model is acceptable. Larger: settle that before any drift analysis (H2/H3).

---

## D10 — Back to the original data plan, run from the laptop (2026-10-20, Phase 1) — supersedes D9

**What the probe table (D4) shows:** on the laptop the block was on the request, not the network: same campus and
hotspot networks, v1 headers blocked everywhere, v2 headers got through on everything, including gamerotation on
campus. On GitHub the block is on the network: v2 changed nothing there (AS8075 is Microsoft's cloud range).

**Decision:**
- **Original data plan, run from the laptop.** Rotation-based stints are the main path again; the PBP rebuild is
  the fallback, as originally designed. D9's "archive + pbpstats + browser" route and the weekly browser step are
  dropped.
- **Weekly refresh runs on the laptop; GitHub only builds and deploys the site** (D4 result).
- **Quarantine alarm back to the original 1% (D3).** D9's re-measuring was only needed because every game was going
  through the rebuild. The extra period-starter spot checks stay (3 Pacers games including one overtime game),
  because the rebuild still handles fallback games.
- **gamerotation server errors are a retry case:** retry with backoff (3 tries); if it keeps failing, that game
  goes to the PBP rebuild, and the existing quarantine design covers the rest. The run summary, `status.json`,
  `data/processed/{season}/rotation_unavailable.parquet` and the site's quarantine export all count these games,
  so a pile-up is visible. Implementation detail: after 5 games in a row fail, the endpoint is skipped for the rest
  of that run so an outage can't add hours to an overnight backfill; the skipped games are still counted.

**Risks planned for, now that the laptop is the only working route:**
- **The headers can stop working at any time** (NBA has changed what it checks before). Every refresh starts with
  the access probe and stops with a clear message, before fetching anything, if the game log, box score v3 or
  liveData play-by-play fails. A refresh never runs on partial data.
- **Pull at a polite rate:** 1.5–2.0 s between requests. The backfill is a one-time job and runs slowly overnight;
  firing three seasons as fast as possible is how a working fingerprint gets banned.

---

## D11 — Stints built hybrid: rotation starters, play-by-play substitutions (2026-10-20, Phase 1)

**What happened:** the first full backfill (2026-10-20 04:38–04:59 UTC) processed 298 games of 2024-25 and
quarantined 297; nothing was written or frozen (the 1% alarm worked). Two causes, found offline from the cache:
- **The rotation file's substitution timing glitches.** Test game 0022400064 (ATL–BKN): pure rotation timing put
  **6 players on the floor for the last 2 seconds** of the game, failing minutes and floor-five, so the game fell
  back to the rebuild.
- **The rebuild's starter inference fails.** In the same game it missed a player in period 3: minutes off by 477 s,
  plus-minus by 8. gamerotation also fails intermittently per game (e.g. 0022400061: 200 at 03:45, 500 at 05:00),
  and in the backfill 296 of 298 games ended up on the weak rebuild.

**Options considered:** (1) hybrid primary; (2) pure rotation, then hybrid, then rebuild; (3) keep as designed.

**Decision:**
- **Stints are built hybrid:** the rotation file gives each period's starting five; play-by-play gives every
  substitution after that. Each source is used for what it gets right.
- **Pure play-by-play rebuild only when rotation data is missing** (or doesn't give exactly five starters per team
  in every period).
- **Quarantine if validation still fails.** No second attempt with the other builder: two paths, as in the original
  design. Option 3 would trip the 1% alarm; option 2 adds a third path to keep track of.
- **Exactly five per team at every moment**, enforced by the hard `floor_five` check on every stint, whichever path
  built it. A glitch like the 6-player stint can never pass silently.
- **The rotation file's timing is kept as a comparison.** At every substitution, the hybrid's time is compared with
  the rotation file's (gap > 2 s counted). Rotation changes with no matching PBP sub usually mean a substitution
  missing from the play-by-play, the hybrid's one weak spot. Counts go in the quarantine rows, the run summary,
  `data/processed/{season}/sub_timing.parquet` and the site's quarantine export. Report-only.
- **`stint_method` column** (`hybrid` / `pbp_rebuild`) on every stint.

**Rationale:** the rotation file's substitution timing glitches (the 6-player stint above), and the rebuild's
starter inference fails; the hybrid avoids both whenever rotation data exists. Offline re-run of the cached games
0022400062, 0022400064 and 0022500005: all clean on the hybrid, 0 timing disagreements on 42–72 subs per game.

**Also fixed (engineering):** a short failure patch (~game 250; both hosts at once, NBA answered normally a minute
later) had marked both hosts down for the rest of the run, cascading into ~2,300 "blocked" games. Now a host that
fails a whole call triggers a 5-minute pause and a re-probe (up to 3 times), then the run stops cleanly. Rotation
500s get a longer backoff, a 10-minute cooldown instead of a run-long switch-off, and a second pass at the end of
each season.

---

## D12 — Backfill pace, chunks, and gamerotation timeouts (2026-10-21, Phase 1)

**What happened:** the second backfill (2026-10-20, hybrid stints) was stopped by Claude Code at ~595 of 1,320
2024-25 games because the laptop ran low on memory. Before that:
- **NBA stopped answering after ~260 new games**, like the first run at ~300: both hosts at once, at 1.5–2.0 s per
  request. After a 5-minute pause the preflight probe passed on its fixed test game (0022500005), and the very next
  real game failed again. The same game (0022400562) downloaded normally ~21 hours later.
- **gamerotation mostly fails:** 8 of ~595 cached games had a rotation file. A direct test (2026-10-21 03:00 UTC,
  3.5 s apart, 8 games): 2 × 200 (< 1 s each), 1 × 500, 5 × timeout at 30 s. A timeout marked all of
  stats.nba.com as down in the client, so one slow rotation call could knock out box-score fetches for the next game.
- The run kept every game's raw frames in memory until the season ended.

**Options considered** (Claude's recommendations, accepted as a set by Jonathan: "do everything you recommend"):
slower pace + chunks; re-probe on a real, uncached game; test gamerotation separately before pulling more; less
memory per run.

**Decision:**
- **Pace: 3.5–4.0 s between requests** (replaces D10's 1.5–2.0 s).
- **Chunks:** `scripts/backfill.py` downloads at most **200 games that need the network** per run
  (`refresh.py --max-fetch 200`, download only), rests **30 minutes**, repeats until nothing is left, then runs one
  normal refresh that processes everything from the cache. Each chunk is a separate process.
- **Re-probe on the game that failed** after a mid-run outage, with escalating pauses of **5, 15, 30 minutes**,
  then the run stops. The start-of-run preflight keeps the fixed test game (D10).
- **gamerotation:** 10 s timeout, 2 tries per call; a timeout counts against gamerotation only, never the whole
  host. Each game gets at most **2 gamerotation calls in total, across runs**, recorded in
  `data/raw/{season}/rotation_attempts.json`; after that the game uses the PBP rebuild (D11).
- **Memory:** a run keeps each game's results, not its raw frames.

**Open, for after the download:** if gamerotation coverage stays near the ~25% seen in the test, most games go to
the PBP rebuild, whose starter inference failed on the first backfill, and the D3 1% alarm will likely fire.
Those numbers come back to Jonathan before anything is changed.
