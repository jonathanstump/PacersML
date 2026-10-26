# Sub-role sweep inside F2

281 training player-seasons (top family F2, probability >= 0.6), features standardized with F2's own scaler. Covariance: tied and diag at k 1-6; full only where its parameter count is under half the training rows (140): none (full k = 1 already has 170 parameters).

Same initialization and checks as D26: 20 starts (k-means init), 50 bootstrap refits, held-out = fit 2024-25, score 2025-26 (own scaler), season ARI = 2024-25-only vs 2025-26-only model. At k = 1 every ARI and retention is 1 by construction.

Selection rule (D27, marked here, not picked): BIC narrows; stable = median bootstrap ARI >= 0.60 and no sub-role under 70% kept; **candidate** = lowest-BIC stable row; naming breaks ties (rows within 10 BIC of the candidate that are also stable are marked *near tie*).

| cov | k | BIC | params | held-out | starts ARI | boot ARI | season ARI | kept min | < 70% | stable | |
|---|---|---|---|---|---|---|---|---|---|---|---|
| diag | 1 | 13,748 | 34 | -24.07 | 1.00 | 1.00 | 1.00 | 100% | 0 | yes |  |
| diag | 2 | 13,010 | 69 | -22.55 | 1.00 | 0.80 | 0.86 | 90% | 0 | yes |  |
| diag | 3 | 12,776 | 104 | -22.30 | 0.71 | 0.62 | 0.28 | 81% | 0 | yes |  |
| diag | 4 | 12,570 | 139 | -21.85 | 0.74 | 0.63 | 0.36 | 78% | 0 | yes | candidate within diag |
| diag | 5 | 12,529 | 174 | -21.67 | 0.50 | 0.47 | 0.41 | 36% | 2 | no |  |
| diag | 6 | 12,487 | 209 | -21.25 | 0.59 | 0.43 | 0.36 | 35% | 5 | no |  |
| tied | 1 | 10,726 | 170 | -17.89 | 1.00 | 1.00 | 1.00 | 100% | 0 | yes | **candidate** |
| tied | 2 | 10,800 | 188 | -18.04 | 0.99 | 0.36 | 0.03 | 76% | 0 | no |  |
| tied | 3 | 10,674 | 206 | -17.95 | 0.14 | 0.12 | 0.02 | 43% | 3 | no | lowest BIC |
| tied | 4 | 10,740 | 224 | -18.11 | 0.22 | 0.20 | 0.22 | 39% | 4 | no |  |
| tied | 5 | 10,737 | 242 | -17.96 | 0.21 | 0.19 | 0.19 | 40% | 5 | no |  |
| tied | 6 | 10,788 | 260 | -18.21 | 0.23 | 0.17 | 0.11 | 24% | 6 | no |  |

Candidate under the rule: **tied, k = 1** (BIC 10,726). k = 1 means no sub-structure inside this family under the rule.
Same rule inside diag only: diag, k = 4 (BIC 12,570, +1,844 vs the candidate).
Tied k = 1 is one Gaussian with a full covariance matrix (170 parameters vs 281 training rows); the D27 limit on full covariance (parameters under half the rows, 140) was written for full only and is not applied to it.
Lowest BIC overall in this family: tied, k = 3 (BIC 10,674; not stable).

Charts: [BIC](bic_by_k.png) · [held-out](heldout_ll_by_k.png) · [bootstrap ARI](bootstrap_ari_by_k.png) · [least stable sub-role](retention_min_by_k.png) · [season ARI](season_ari_by_k.png) · [parameters](n_params_by_k.png) · [sweep.csv](sweep.csv)
