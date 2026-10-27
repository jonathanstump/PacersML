# Two-level archetypes (D27)

Level 1 frozen (full covariance, k = 3); family names D29: F1 On-ball Shot Creators; F2 Off-ball Spot Ups; F3 Bigs. Level 2 swept inside each family; nothing picked, sub-roles unnamed.

**D30 slicing diagnostics (D31 feature drops applied): [slicing/index.md](slicing/index.md).** The sweeps and packets below are the D27 run with all 17 features, before the D31 drops.

## Open first

1. [families.md](families.md) and [profiles_blind.md](profiles_blind.md): level-1 families, position crosstab, straddlers, check players.
2. Each family's sweep.md (candidates marked) and feature_flags.md.
3. Each family's packets: profiles_blind.md first, then profiles_players.md, charts, stability.md.
4. [hypothesis_check.md](hypothesis_check.md) last (reported only, not used to select).

## Candidate sets

- **rule**: lowest-BIC stable row across covariance types (D27 rule as written).
- **within diag**: the same rule inside diag covariance only.

## Families

| family | training rows | excluded (< 0.6) | lowest BIC | rule | within diag | sweep | flags | packets |
|---|---|---|---|---|---|---|---|---|
| F1 | 303 | 3 (1.0%) | tied, k = 1 | tied, k = 1 | diag, k = 3 | [sweep.md](F1/sweep.md) | [feature_flags.md](F1/feature_flags.md) | [diag k2](F1/k2_diag/profiles_blind.md) · [diag k3](F1/k3_diag/profiles_blind.md) · [diag k4](F1/k4_diag/profiles_blind.md) · [tied k2](F1/k2_tied/profiles_blind.md) · [transitions diag](F1/k_transitions_diag.png) · [transitions tied](F1/k_transitions_tied.png) |
| F2 | 281 | 10 (3.4%) | tied, k = 3 | tied, k = 1 | diag, k = 4 | [sweep.md](F2/sweep.md) | [feature_flags.md](F2/feature_flags.md) | [diag k3](F2/k3_diag/profiles_blind.md) · [diag k4](F2/k4_diag/profiles_blind.md) · [diag k5](F2/k5_diag/profiles_blind.md) · [tied k2](F2/k2_tied/profiles_blind.md) · [transitions diag](F2/k_transitions_diag.png) · [transitions tied](F2/k_transitions_tied.png) |
| F3 | 152 | 1 (0.7%) | tied, k = 4 | tied, k = 1 | diag, k = 3 | [sweep.md](F3/sweep.md) | [feature_flags.md](F3/feature_flags.md) | [diag k2](F3/k2_diag/profiles_blind.md) · [diag k3](F3/k3_diag/profiles_blind.md) · [diag k4](F3/k4_diag/profiles_blind.md) · [tied k2](F3/k2_tied/profiles_blind.md) · [transitions diag](F3/k_transitions_diag.png) · [transitions tied](F3/k_transitions_tied.png) |

Combined weights for every training-season player-season (all tiers), one file per candidate set: `data/processed/archetypes/combined_weights_{set}.parquet` (not committed; regenerate with this script).
