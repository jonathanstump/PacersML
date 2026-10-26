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

> **Amended by D14** (2026-10-22): the 1% alarm applies to hybrid-built games only; rebuild failures are listed
> and counted, no alarm.
> **Amended again by D15** (2026-10-22): no rate alarm. The hybrid alarm fires on any game where the shadow
> rebuild passes the lineup checks and the hybrid fails them; a regression alarm stops the run.

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

> **Amended by D14** (2026-10-22): plus-minus is strict except that a gap of ±2 or less passes, with a note,
> when minutes pass and the game has a substitution in the same second as a technical free throw.

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

---

## D13 — Rotation-only pass (2026-10-21, Phase 1)

**What happened:** during the chunked download, gamerotation's 10-minute cooldown (after 5 failures in a row)
meant cached games went by while it was cooling, with no call. On 2026-10-21 15:18 UTC: 2024-25 had all 1,320 games
downloaded, 115 with a rotation file, 86 with at least one failed call, and ~1,120 never called. 2025-26: 321
downloaded, 5 with rotation, 31 failed at least once.

**Decision (Jonathan, "build the rotation-only pass"):** `scripts/rotation_pass.py` makes the skipped calls after
the download finishes, before processing:
- one request per try, same 3.5–4.0 s pace, same limit of 2 tries per game in total (shared ledger, D12); rounds,
  so a failed game's second try comes at least one round later;
- no cooldown; instead, after 10 failures in a row it checks that game's box score on stats.nba.com. Box fails too
  → host outage: those tries are taken back off the ledger and redone after a pause (5, 15, 30 min, then stop).
  Box answers → they were gamerotation's own failures and count;
- rests 30 min after every 400 requests;
- `refresh.py` does not freeze a training season while any of its games still has rotation tries left.
`scripts/backfill.py` now runs download chunks → rotation pass → processing refresh.
Download chunks no longer call gamerotation at all (2026-10-22); the rotation pass makes every call.

---

## D14 — What the remaining validation failures mean, and which games are kept (2026-10-22, Phase 1)

> **Group A rule amended by D15** (2026-10-22): kept with notes when team points match and possessions are within
> tolerance, not only when every team total matches. The entry below is unchanged, for the record.

**What happened:** after the rebuild fix (between-period subs, commit 010f967), an offline re-run of both
training seasons from the cache had 135 games failing (60 of 1,320 in 2024-25, 75 of 1,321 in 2025-26), in four
groups: A, play-by-play counts vs box off by 1–2 with lineups right (89); B, plus-minus only, off by 1–3 (20);
C, lineup failures (24); D, team points (2).

**Options considered:** for A, strict / report-only for gaps ≤ 2 / report-only at any size; for B, strict /
±2 / test other technical-FT rules; for the alarm, keep 1% / raise to 2% / per builder.

**Decision (Jonathan):**
- **Group A:** a player stat gap of 2 or less passes, with a note, when minutes, plus-minus and the **team total
  for that stat** all match: the stat moved between teammates across NBA's two sources (Murray/Westbrook rebound,
  0022400208), so team-level numbers (H1 corner-3 and rim rates) are unaffected. A team total that doesn't match
  means an event is missing, not misattributed: quarantined. Reason: the lineups in these games are right, and
  quarantining throws away correct stints RAPM needs.
- **Group B:** plus-minus gap ±2 or less passes, with a note, only when minutes pass and the game has a
  substitution in the same second as a technical free throw (NBA's box contradicts itself there: in 0022400827 it
  charges the technical FT to the player going out, in 0022401078 to the player coming in, so no attribution rule
  fits both). Any other plus-minus gap, and the game off by 3, stays quarantined: a gap with no known cause is
  what the check exists to catch. Testing more technical rules (option 3) skipped.
- **Alarm (D3 amended):** 1% alarm on hybrid games only, where a breach means a real bug. Rebuild games (missing
  rotation data) are expected to fail more often: no alarm; each failure listed, games lost per season reported.
  A single 2% threshold was rejected because rebuild failures could hide a hybrid regression.
- **Group D:** strict (PBP scoring ≠ box means the stints are wrong).
- Games kept with a note go to `kept_with_notes.parquet` and the `kept_with_notes` list in
  `site_export/quarantine.json`.

**Checks Jonathan asked for (numbers, 2026-10-22, cache at that time):**
- The 3 Group A games "off by 4" (0022500109, 0022500188, 0022500788) are 4 summed over two players: one teammate
  +2, another −2 (two free throws, a made 2, a made 2 plus a rebound). Team totals match; kept with notes.
- Group A after the team-total rule: 44 kept with notes, 45 quarantined (team total differs).
- Group B: 14 of the 20 games have a substitution in the same second as a technical FT; 13 of those are kept,
  1 (0022400896, off by 3) quarantined. The other 6 have no such substitution and stay quarantined, unexplained.
- Group C, box-minutes starter repair (tried at Jonathan's request): recovered **0** games beyond the fixes below,
  so it was not kept. The remaining lineup failures are mostly pairs (one player over by X seconds, a teammate
  short by X), i.e. a mid-period substitution missing or logged for the wrong player, not a missing starter.
- Group C, two bug fixes in starter inference (engineering): a technical foul or an ejection no longer counts as
  evidence that a player started a period, since bench players get them (0022400664, a Pacers game: a bench double
  technical made a sixth starter; 0022501127: an ejection from the bench). 7 of the 22 rebuild lineup failures pass
  after these fixes.

---

## D15 — Rotation pass diagnosis; builder-disagreement and regression alarms; Group A revised (2026-10-22, Phase 1)

### Rotation pass: why most pulls failed (diagnosed 2026-10-22, 02:55–03:10 UTC)

The pass was stopped at game 250 of 1,127 (2024-25 round 1): 50 ok, 200 failed, one outage pause (box scores
also unanswered at 02:37 UTC). Sorted by cause:
- **Empty or partial responses / missing data for older games:** not seen. Every failure is an HTTP-level failure;
  failures do not cluster by game date (successes spread across the whole season).
- **Parsing after a successful fetch:** not the cause. All 196 cached 2024-25 rotation files parse with five
  starters per team in every period; 1 of 38 in 2025-26 does not.
- **HTTP errors: the cause.** A slow sample (14 requests, 8 s apart, 20 s timeout): 11 read timeouts, 1 HTTP 500,
  1 success, plus 2 control games that had downloaded fine before, both timed out. In the same minutes,
  `boxscoretraditionalv3` for the same game answered 200 in 0.9 s, and gamerotation with a 60 s timeout returned
  500 in 0.1 s. A few minutes later a box-score request timed out too, and all requests were stopped.
- Success rate by how often gamerotation was being called: ~60% when spread among download requests (chunks,
  2026-10-21), ~20% in the dedicated pass (one call every ~4 s), 1 of 14 in the diagnostic. Most ledger
  "failures" recorded so far say nothing about the game itself.

Not restarted. Restart plan is in the open items below; it needs Jonathan's go-ahead.

### Decision (Jonathan)

- **Hybrid alarm (D3 amended):** option 3. The pure rebuild runs as a **shadow on every game that has rotation
  data**; its stints are not kept. The alarm fires on **any game where the shadow rebuild passes the lineup checks
  (minutes, floor_five, game_seconds, plus_minus) and the hybrid fails them**: the two builders disagreeing on the
  same game is the cleanest sign of a bug in ours. Group A and D failures (NBA's own sources disagreeing)
  quarantine games but are not builder bugs and don't count.
- **Regression alarm (new):** any game that passed or was kept with notes in the previous run and is quarantined
  now **stops the run** (exit 6): nothing written for that season, baseline unchanged. Baseline:
  `data/processed/{season}/game_outcomes.parquet`. `--accept-regressions` accepts an intended change.
- **Games lost per season:** reported by builder and group on the Methods page (`games_lost` in
  `site_export/quarantine.json`), no alarm.
- **Group A revised (D14 amended):** kept with notes when **team points match and our possessions are within
  tolerance**; quarantined otherwise. Reasoning (Jonathan): the team-total rule was meant to separate
  misattribution from missing events, but the 45 "missing events" are single shots and rebounds. They don't change
  team points or possessions, which are what stints and RAPM use, and quarantining ~2% of games for a one-shot
  difference costs more than it protects. Covers all three patterns: extra missed shot + offensive rebound (same
  possession, same points), a 3 re-scored as a 2 (only the shot type changes, which settles that open question),
  a 3-point attempt missing from both totals. Cost: shot-level detail off by one shot in those games, negligible
  for a season's corner-3 rate (H1).
  - Implementation choices (proposed by Claude, **confirmed by Jonathan 2026-10-22**): "within tolerance" = each team's possessions within
    **2% of pbpstats.com** for that game (D1's tolerance; pbpstats has every 2024-25 game, gaps 0–4, median 1).
    No pbpstats number → not confirmed → quarantined, unless every team total matches (the D14 teammate case,
    which can't change possessions). No per-player cap on the count gap.
- **Pacers games:** a divergence timeline for each quarantined Pacers game (`scripts/divergence.py`, output in
  `reports/quarantine_review/`), 0042400306 first.

---

## D16 — Run order: process from the cache now, pull rotation later (2026-10-22, Phase 1)

About 2,400 downloaded games have no rotation file (2024-25: 1,124 of 1,320; 2025-26: 1,283 of 1,321;
2026-27: 8 of 11). At the throttle-safe pace (one gamerotation call per 30 s, D15), pulling them takes about 20 h.

Options given: (1) process now from the cache, then run the rotation pass and re-process; (2) rotation pass first,
then process once; (3) process now and skip the pass.

**Decision (Jonathan): option 1.**
- Process now with `refresh.py --no-rotation-calls`, which never calls gamerotation and uses only cached rotation
  files. Games without one use the pure rebuild. This first run writes the tables and the regression baseline.
- Then run `rotation_pass.py` (after `--reset-throttled`, once), in Jonathan's terminal. It is resumable.
- Then re-process. Training seasons don't freeze while any game still has rotation tries left (D13). Games that
  switch from rebuild to hybrid and now fail trip the regression alarm (exit 6). Jonathan reviews them and
  accepts with `--accept-regressions`.
- Group A tolerance details (D15) confirmed as built: 2% of pbpstats per team; no pbpstats number → quarantined
  unless every team total matches; no per-player cap.

---

## D17 — Pacers divergence review: minutes note, 0022400986 stays quarantined, same-second reorder trial (2026-10-22, Phase 1)

From Jonathan's read of the five Pacers divergence timelines (`reports/quarantine_review/`).

**Decisions (Jonathan):**
- **Minutes tolerance:** a single player's gap of up to **3 s** passes, with a note, when it's unpaired (no
  teammate off by more than 1 s in the other direction). Paired gaps always fail and are investigated, whatever
  their size. Reasoning: every real missing-substitution case so far has been tens of seconds with a matching
  opposite gap on a teammate. Our team seconds are fixed at 5 × game length, so a lineup error always shows as a
  pair; an unpaired gap is box rounding. Case: 0022401055 (LeBron +1.4 s, no matching gap).
- **0022400986 stays quarantined.** Toppin +24.6 s matches the end of Q1 (00:24.6 to 0:00); Freeman −25.0 s,
  not −24.6; and the plus-minus gaps run through the Q3 07:57 ejection sequence (a flagrant 2, two ejections,
  Freeman checking in only to shoot Nembhard's free throws, then leaving). The numbers don't reconcile into one
  fix, and it's one regular-season game.
- **0022400933:** a substitution missing from NBA's play-by-play (Sheppard on for Nesmith from Q2 03:26 to 01:47,
  99 s; plus-minus Nesmith −3 / Sheppard +3). Not a parser bug. Waits for the rotation file (D16 step 2).
- **0022400217** stays quarantined under D15 as confirmed: team points match, but Orlando's possessions are 97
  vs pbpstats' 95 (2.1% > 2%). The D14 Group A rule was amended by D15, and that amendment is what's implemented.
- **Group C repairs:** wait for D16 steps 2–3. For games still failing after that, an inference-based repair is
  accepted only when a single substitution explains the minutes gap **and** plus-minus then passes too.

**Under test (not adopted): same-second reorder, a proposed D8 amendment.** 0042400306, Q2 06:36: the log shows
Hart's foul, Hart subbed out for Towns, then Bridges' away-from-play foul and Haliburton's 1 free throw. Our rule
(credit the lineup at the foul) gives that point to the lineup with Towns; NBA's box gives it to Hart (Towns −1,
Hart +1). Personal fouls only happen in live play and substitutions only at dead balls, so a personal foul logged
after a sub in the same second means the log order is wrong. Trial rule: within a same-second cluster, a sub
moves to just after the last live-play event logged after it (field goal, rebound, turnover, non-technical foul,
jump ball), stopping at any free throw or technical foul (subs between free throws are real; technicals happen
at dead balls). Code: `normalize.reorder_same_second_subs`, `refresh.py --reorder-subs`.
Acceptance test: run it with `--no-write` against the D16 step-1 baseline. Adopt only if it fixes games and
breaks none. If adopted, it's logged as a D8 amendment with this reasoning.

**Trial result (2026-10-22, `data/refresh_reorder_trial.log`, `--no-write` vs the D17 baseline): not adopted.**

| season | games with subs moved | subs moved | fixed | regressed |
|---|---|---|---|---|
| 2024-25 | 336 | 666 | 1 (0042400306) | 49 |
| 2025-26 | 352 | 690 | 0 | 53 |

Under the acceptance rule (fixes games, breaks none), the rule is rejected. D8 is unchanged and 0042400306 stays
quarantined. The code stays behind the off-by-default `--reorder-subs` flag; the 102 regressed games are listed
in the log.

---

## D18 — Possession cross-checks compare the same games as NBA (2026-10-22, Phase 1, bug fix)

The first full-season runs (D16 step 1, 1b) exited 4: 2024-25 had 14 regular-season teams and 2 playoff teams
more than 2% off NBA's team POSS; 2025-26 had 3 regular-season teams and 1 play-in team. Player-season gaps were
almost all under NBA's (2024-25 regular: 2 over, 567 under). Cause: our totals left out quarantined games and
NBA's season totals include them. A team with 2 quarantined games out of 82 is ~2.4% under from that alone.
Fix: the team and player possession cross-checks use every processed game, quarantined ones included.
Possessions come from the play-by-play, not from the lineups. The per-100 tables still use clean games only.
D1's 2% tolerance is unchanged. If a team is still over 2% after the fix, the gap is real and gets investigated.

Also fixed: 7 games of 2026-27 had empty box scores cached (NBA answered before the box was filled in), which
crashed the run. An empty box is now removed from the cache and fetched again on the next run.

---

## D19 — Small samples in the D1 team-season possession check (2026-10-23, Phase 1)

After D18, step A wrote 2024-25. 2025-26 still exited 4 on one team: Phoenix in the play-in, 2 games, ours 183,
pbpstats 184, NBA 188 (−2.7%). In 2024-25 every regular-season team is 0.55–0.92% under NBA (mean −0.71%),
playoffs −0.20% to −1.34%, play-in 0% to −1.52%. On a 2-game sample that offset plus a possession of noise
crosses 2%.

Options given: (1) enforce only for team-seasons with ≥ 1,000 NBA possessions; (2) skip play-in only;
(3) fail only when the gap is > 2% and > 10 possessions.

**Decision (Jonathan): option 1.** The 2% alarm applies to team-seasons with at least **1,000 NBA possessions**
(about 10 games). Smaller ones are reported (`enforced = False` in `team_poss_check.parquet`), not enforced. This
covers play-in, short playoff runs and the first weeks of 2026-27.

Also (bug fix): a season with games that couldn't be loaded counts as partial for the season-level checks, because
NBA's totals include games we don't have. 2026-27 had 7 such games (empty box scores, D18).

Player-season possessions, 2024-25 regular season, for the D7 "investigate" flag (report-only): 569 players, 2 over
/ 567 under. Gap (off+def)/2 vs NBA POSS: median −2.21% (IQR −2.98% to −1.71%), median −0.85 possessions per
game. The team gap over the same games is −0.71%. Not investigated yet.

---

## D20 — Rotation pass: the fixed canary stopped detecting throttling (2026-10-24, Phase 1, bug fix)

Second rotation-pass run (`data/rotation_pass_d15_part2.log`):
- 2024-25 round 1: 844 games, 347 ok, 497 failed. Round 2: 323 games, 48 ok, 275 failed. 871 of 1,320 games have
  rotation now; the other 449 used both tries.
- 2025-26 round 1, stopped at 600 of 1,283: 199 ok. From 02:33 to 05:03 UTC, 1 success in 150 calls.
- "throttled" was 0 for the whole run: the fixed canary (the first cached game) answered every time it was
  asked, probably from a cached response, so every failure counted against its game.

Fix: each canary is a random cached game, and 8 counted failures in a row also count as throttling: those tries
are uncounted, the pass backs off and resumes from the first of them. The ledger was reset again for games without
rotation (backup `rotation_attempts_backup_*.json`), on D15's reasoning: tries made while throttled say nothing
about the game.

---

## D21 — Rotation pass throttled out; process now, retry slower later (2026-10-24, Phase 1)

Third rotation-pass run (`data/rotation_pass_part3.log`, after the D20 fix and ledger reset): 9 new games from
05:09 to 13:54 UTC. It stopped by itself (exit 3) after every backoff (30 min, 1 h, 2 h, 4 h), with random canaries
also failing. No game's try was counted. Coverage: 2024-25 880/1,320, 2025-26 237/1,321, 2026-27 3/7.

Options given: (1) process now, retry the pass slower later, no freeze until it finishes or is stopped;
(2) process now and freeze anyway (amends D13); (3) wait and retry before processing.

**Decision (Jonathan): option 1.** Run the processing refresh now (games without rotation use the rebuild). Retry
the pass in a day or two with `--interval 60`. 2024-25 and 2025-26 stay unfrozen until the pass finishes or
Jonathan decides to stop it.

---

## D22 — Step C results; games cached mid-game are fetched again (2026-10-24, Phase 1, bug fix)

Step C (`data/refresh_d21.log`) exited 0 and wrote all three seasons. No regressions against the baseline, no
hybrid-bug games.

| season | games | hybrid | rebuild | quarantined | kept with notes |
|---|---|---|---|---|---|
| 2024-25 | 1,320 | 880 (12 q) | 440 (8 q) | 20 (1.52%) | 36 |
| 2025-26 | 1,321 | 236 (2 q) | 1,085 (6 q) | 8 (0.61%) | 64 |
| 2026-27 | 28 | 2 (0 q) | 26 (8 q) | 8 | 2 |

2026-27: 6 of the 8 quarantines were play-by-play files cached at 02:11 UTC on 10-22 while the games were still
being played (last action in Q3 or Q4, no game-end action), so they failed team points. Of the 2,669 cached
liveData PBP files, these 6 are the only ones with no game-end action. Fix: a PBP payload without a game end
(liveData's game-end action; for playbyplayv3, a period-4-or-later end) is removed from the cache and fetched
again next run; a box score cached before the game-end time is too. Pacers game 0022600090 is one of the 6.

2026-27 re-run (`data/refresh_2026-27.log`, 36 games): the 5 non-Pacers mid-game games pass now (0 regressions);
Pacers game 0022600090 is down to a plus-minus gap of 1. A new failure, 0022600111 (minutes = 300 s, three Suns
players +300 s), came from NBA tagging the "Game End" action with period 5 in a regulation game (box 14,401 team
seconds, 131-122 at the end of Q4), which created a phantom overtime. Fix: liveData game-end actions are skipped
(they carry no play). Only this game in the 2,669 cached liveData files has a game end in an unplayed period.

---

## D23 — Item 3 review: period starters, 0022600090, player possession gap (2026-10-25, Phase 1)

**Period-starter spot check (D10): passed, 26 of 26.** Every period-start lineup, both teams, in three Pacers
2024-25 games matches Basketball-Reference's Plus/Minus chart (Jonathan, filled in
`reports/spot_checks/pacers_period_starters_2024-25.csv`).

| game | builder | periods | match |
|---|---|---|---|
| 0022400009 vs MIA | hybrid | Q1–Q4 | 8/8 |
| 0022400254 at HOU | rebuild | Q1–Q4 | 8/8 |
| 0022400097 vs PHI | hybrid | Q1–OT1 | 10/10 |

**Player possession gap (D7 flag): accepted as a definition difference (Jonathan, option 1).** Report-only, no
change. Jonathan's fit of regular-season players with 20+ games: the gap splits into a part proportional to
playing time (0.82% of possessions in 2024-25, 0.68% in 2025-26, in line with the −0.71% team gap accepted in D19)
and a fixed part per game (0.53 and 0.56 possessions), spread ~0.2 possessions per game. Counting each possession
once, for one lineup, stays the input for RAPM. Optional later check for METHODS: mid-possession substitutions per
player-game against the fixed part.

**0022600090 (2026-27, Pacers): gap traced to Q4 07:08, a bug (fixed).** At 07:08 NOP subs Fears, Murphy,
Williamson, Missi for Queen, Bey, Mathurin, Jones and IND subs Nembhard for Haliburton; Haliburton then gets a
technical and Murphy makes the free throw — exactly the ten players and one point in the gap (Jonathan's trace).
Cause: in 2026-27 liveData no longer writes "Technical" in a technical free throw's text ("T. Murphy III Free Throw
1 of 1"); only the `descriptor` field says `technical`. All 20 technical FTs in the 2026-27 cache (15 games) have
the new form; none of the 2024-25 / 2025-26 ones do (2,297 with "technical" in the text). So these FTs were
treated as ordinary FTs: credited to the last play before the trip (the pre-sub lineup) instead of the
technical foul (D8), the D14 allowance didn't see a technical FT, and they counted toward possessions.
Fix: the descriptor also marks a free throw technical. Offline re-check of the 15 games:

| game | before | after | possessions |
|---|---|---|---|
| 0022600090 | quarantined (pm 1) | passes, exact | — |
| 0022600101 | quarantined (pm 2) | kept with note (D14, pm 2) | — |
| 0022600003, 0022600004, 0022600092 | clean | clean | −2 each |
| 10 others | clean / noted | unchanged | 0 |

Applied to all seasons on the next refresh (2024-25 / 2025-26 unaffected).

---

## D24 — Rotation pass stopped; training seasons freeze with the PBP rebuild for the rest (2026-10-26, Phase 1)

Rotation pass part 4 (`data/rotation_pass_part4.log`, `--interval 60`, 2026-10-25 20:11 to ~02:21 UTC, stopped during a 2 h backoff): 7 new
files (2024-25), 5 throttle backoffs. Coverage at the stop: 2024-25 886/1,320, 2025-26 237/1,321, 2026-27 3/43.

Options given: (1) stop now and freeze, the rest keeps the PBP rebuild; (2) run one more day, then (1);
(3) run for days, Phase 2 waits.

**Decision (Jonathan): option 1** (stopped the pass and ran the final refresh). Final refresh
(`data/refresh_final.log`): exit 0, no regressions in any season; 2026-27: 0022600090 and 0022600101 fixed (D23).

| season | games | hybrid (q) | rebuild (q) | quarantined | kept with notes |
|---|---|---|---|---|---|
| 2024-25 | 1,320 | 886 (12) | 434 (8) | 20 (1.52%) | 36 |
| 2025-26 | 1,321 | 236 (2) | 1,085 (6) | 8 (0.61%) | 64 |
| 2026-27 | 42 of 43 | 2 (0) | 40 (2) | 2 (4.76%) | 4 |

That run did not freeze (the D13 rule waits for rotation tries). `--rotation-stopped` records this decision:
training seasons freeze with tries left, and the manifest stores `rotation_files` and `rotation_stopped: true`.
2026-27 keeps trying gamerotation on weekly refreshes.
