# Archetype model: sweep and naming packets (Phase 2)

**Two-level archetypes (D27): [families/index.md](families/index.md)** — level-1 families (frozen full k = 3) and sub-role sweeps and packets inside each family.

750 player-seasons (500+ regular-season minutes, 2024-25 + 2025-26), 17 style features (D25), Gaussian mixture, k 2–15 × full / tied / diag covariance. Nothing here picks k.

- Lowest BIC overall: **full, k = 3** (BIC 25,066).
- Packet set 1: **full** covariance, k = 2, 3, 4 (BIC-best k for full is 3).
- Packet set 2: **tied** covariance, k = 12, 13, 14 (BIC-best k for tied is 13).
- Elbow (kneedle on each BIC curve): full k = 6, tied k = 9, diag k = 6.

## Open first

1. Each k's **profiles_blind.md** (no player names): write provisional names before looking at players.
2. Then its **profiles_players.md**, the charts and **stability.md**.

## Packets

| set | covariance | k | blind profiles | player reveal | stability | heatmap | shot mix | PCA map | positions | neighbors | top-prob histogram |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | full | 2 | [profiles_blind.md](k2/profiles_blind.md) | [profiles_players.md](k2/profiles_players.md) | [stability.md](k2/stability.md) | [png](k2/heatmap_features.png) | [png](k2/shot_mix.png) | [png](k2/pca_map.png) | [png](k2/position_crosstab.png) | [png](k2/neighbors.png) | [png](k2/top_prob_hist.png) |
| 1 | full | 3 | [profiles_blind.md](k3/profiles_blind.md) | [profiles_players.md](k3/profiles_players.md) | [stability.md](k3/stability.md) | [png](k3/heatmap_features.png) | [png](k3/shot_mix.png) | [png](k3/pca_map.png) | [png](k3/position_crosstab.png) | [png](k3/neighbors.png) | [png](k3/top_prob_hist.png) |
| 1 | full | 4 | [profiles_blind.md](k4/profiles_blind.md) | [profiles_players.md](k4/profiles_players.md) | [stability.md](k4/stability.md) | [png](k4/heatmap_features.png) | [png](k4/shot_mix.png) | [png](k4/pca_map.png) | [png](k4/position_crosstab.png) | [png](k4/neighbors.png) | [png](k4/top_prob_hist.png) |
| 2 | tied | 12 | [profiles_blind.md](k12/profiles_blind.md) | [profiles_players.md](k12/profiles_players.md) | [stability.md](k12/stability.md) | [png](k12/heatmap_features.png) | [png](k12/shot_mix.png) | [png](k12/pca_map.png) | [png](k12/position_crosstab.png) | [png](k12/neighbors.png) | [png](k12/top_prob_hist.png) |
| 2 | tied | 13 | [profiles_blind.md](k13/profiles_blind.md) | [profiles_players.md](k13/profiles_players.md) | [stability.md](k13/stability.md) | [png](k13/heatmap_features.png) | [png](k13/shot_mix.png) | [png](k13/pca_map.png) | [png](k13/position_crosstab.png) | [png](k13/neighbors.png) | [png](k13/top_prob_hist.png) |
| 2 | tied | 14 | [profiles_blind.md](k14/profiles_blind.md) | [profiles_players.md](k14/profiles_players.md) | [stability.md](k14/stability.md) | [png](k14/heatmap_features.png) | [png](k14/shot_mix.png) | [png](k14/pca_map.png) | [png](k14/position_crosstab.png) | [png](k14/neighbors.png) | [png](k14/top_prob_hist.png) |

Across k, full: [k_transitions.png](k_transitions.png) (k = 2 → 3 → 4).
Across k, tied: [k_transitions_tied.png](k_transitions_tied.png) (k = 12 → 13 → 14).

## Sweep charts

[BIC](bic_by_k.png) · [held-out log-likelihood](heldout_ll_by_k.png) · [bootstrap ARI](bootstrap_ari_by_k.png) · [least stable cluster](retention_min_by_k.png) · [season-to-season ARI](season_ari_by_k.png) · [parameter count](n_params_by_k.png) · full table [sweep.csv](sweep.csv)

## BIC and diagnostics for every k

BIC: lower is better. Held-out: mean log-likelihood per 2025-26 row of a model fitted on 2024-25 (higher is better). Starts ARI: median agreement of 20 seeds with the best. Boot ARI: median over 50 bootstrap refits. Season ARI: 2024-25-only vs 2025-26-only model. Kept min: least stable cluster's share of players kept. < 70%: clusters under 70% kept.

### full

| k | BIC | params | held-out | starts ARI | boot ARI | season ARI | kept min | < 70% | |
|---|---|---|---|---|---|---|---|---|---|
| 2 | 25,128 | 341 | -16.01 | 0.92 | 0.83 | 0.47 | 88% | 0 | packet |
| 3 | 25,066 | 512 | -15.56 | 0.97 | 0.66 | 0.54 | 84% | 0 | lowest BIC packet |
| 4 | 25,332 | 683 | -15.84 | 0.35 | 0.45 | 0.36 | 46% | 2 | packet |
| 5 | 25,744 | 854 | -16.03 | 0.52 | 0.46 | 0.36 | 54% | 2 |  |
| 6 | 26,282 | 1025 | -15.99 | 0.42 | 0.34 | 0.42 | 40% | 5 | elbow |
| 7 | 26,831 | 1196 | -16.93 | 0.43 | 0.34 | 0.31 | 37% | 5 |  |
| 8 | 27,483 | 1367 | -18.48 | 0.37 | 0.32 | 0.26 | 30% | 7 |  |
| 9 | 28,154 | 1538 | -18.60 | 0.39 | 0.31 | 0.22 | 32% | 8 |  |
| 10 | 28,967 | 1709 | -18.15 | 0.45 | 0.32 | 0.28 | 34% | 9 |  |
| 11 | 29,689 | 1880 | -19.19 | 0.41 | 0.31 | 0.27 | 31% | 10 |  |
| 12 | 30,519 | 2051 | -20.47 | 0.44 | 0.31 | 0.21 | 29% | 11 |  |
| 13 | 30,662 | 2222 | -22.15 | 0.42 | 0.28 | 0.20 | 18% | 13 |  |
| 14 | 31,425 | 2393 | -23.85 | 0.41 | 0.29 | 0.18 | 20% | 14 |  |
| 15 | 32,229 | 2564 | -24.97 | 0.40 | 0.29 | 0.19 | 22% | 15 |  |

### tied

| k | BIC | params | held-out | starts ARI | boot ARI | season ARI | kept min | < 70% | |
|---|---|---|---|---|---|---|---|---|---|
| 2 | 26,281 | 188 | -17.26 | 1.00 | 0.85 | -0.07 | 87% | 0 |  |
| 3 | 26,071 | 206 | -16.92 | 0.85 | 0.78 | 0.76 | 90% | 0 |  |
| 4 | 25,927 | 224 | -16.75 | 0.50 | 0.61 | 0.75 | 56% | 1 |  |
| 5 | 25,699 | 242 | -16.63 | 0.41 | 0.45 | 0.44 | 46% | 4 |  |
| 6 | 25,620 | 260 | -16.49 | 0.65 | 0.51 | 0.38 | 42% | 3 |  |
| 7 | 25,533 | 278 | -16.41 | 0.64 | 0.45 | 0.36 | 48% | 3 |  |
| 8 | 25,426 | 296 | -16.33 | 0.58 | 0.49 | 0.35 | 47% | 3 |  |
| 9 | 25,344 | 314 | -16.27 | 0.64 | 0.52 | 0.30 | 52% | 7 | elbow |
| 10 | 25,362 | 332 | -16.26 | 0.61 | 0.49 | 0.31 | 34% | 8 |  |
| 11 | 25,296 | 350 | -16.23 | 0.63 | 0.46 | 0.35 | 39% | 8 |  |
| 12 | 25,356 | 368 | -16.24 | 0.58 | 0.46 | 0.53 | 28% | 8 | packet |
| 13 | 25,291 | 386 | -16.13 | 0.39 | 0.34 | 0.39 | 22% | 10 | lowest BIC packet |
| 14 | 25,315 | 404 | -16.16 | 0.41 | 0.35 | 0.43 | 17% | 12 | packet |
| 15 | 25,395 | 422 | -16.17 | 0.50 | 0.45 | 0.28 | 34% | 11 |  |

### diag

| k | BIC | params | held-out | starts ARI | boot ARI | season ARI | kept min | < 70% | |
|---|---|---|---|---|---|---|---|---|---|
| 2 | 32,948 | 69 | -22.01 | 0.56 | 0.90 | 0.03 | 88% | 0 |  |
| 3 | 30,592 | 104 | -20.13 | 1.00 | 0.92 | 0.82 | 94% | 0 |  |
| 4 | 29,668 | 139 | -19.43 | 0.89 | 0.77 | 0.48 | 71% | 0 |  |
| 5 | 29,013 | 174 | -18.92 | 0.90 | 0.74 | 0.77 | 81% | 0 |  |
| 6 | 28,530 | 209 | -18.64 | 0.66 | 0.54 | 0.70 | 49% | 1 | elbow |
| 7 | 28,341 | 244 | -18.39 | 0.51 | 0.49 | 0.42 | 51% | 4 |  |
| 8 | 28,086 | 279 | -18.25 | 0.46 | 0.47 | 0.38 | 46% | 7 |  |
| 9 | 27,972 | 314 | -18.17 | 0.56 | 0.46 | 0.39 | 47% | 7 |  |
| 10 | 27,894 | 349 | -18.07 | 0.57 | 0.46 | 0.34 | 47% | 8 |  |
| 11 | 27,806 | 384 | -18.00 | 0.48 | 0.46 | 0.31 | 47% | 9 |  |
| 12 | 27,860 | 419 | -18.02 | 0.55 | 0.44 | 0.36 | 41% | 11 |  |
| 13 | 27,829 | 454 | -17.90 | 0.44 | 0.41 | 0.31 | 43% | 12 |  |
| 14 | 27,804 | 489 | -17.80 | 0.53 | 0.42 | 0.35 | 42% | 12 |  |
| 15 | 27,763 | 524 | -17.87 | 0.45 | 0.43 | 0.38 | 38% | 14 | lowest BIC |
