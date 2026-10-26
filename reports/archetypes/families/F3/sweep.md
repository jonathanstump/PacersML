# Sub-role sweep inside F3

152 training player-seasons (top family F3, probability >= 0.6), features standardized with F3's own scaler. Covariance: tied and diag at k 1-6; full only where its parameter count is under half the training rows (76): none (full k = 1 already has 170 parameters).

Same initialization and checks as D26: 20 starts (k-means init), 50 bootstrap refits, held-out = fit 2024-25, score 2025-26 (own scaler), season ARI = 2024-25-only vs 2025-26-only model. At k = 1 every ARI and retention is 1 by construction.

Selection rule (D27, marked here, not picked): BIC narrows; stable = median bootstrap ARI >= 0.60 and no sub-role under 70% kept; **candidate** = lowest-BIC stable row; naming breaks ties (rows within 10 BIC of the candidate that are also stable are marked *near tie*).

| cov | k | BIC | params | held-out | starts ARI | boot ARI | season ARI | kept min | < 70% | stable | |
|---|---|---|---|---|---|---|---|---|---|---|---|
| diag | 1 | 7,504 | 34 | -25.84 | 1.00 | 1.00 | 1.00 | 100% | 0 | yes |  |
| diag | 2 | 6,847 | 69 | -23.61 | 1.00 | 0.87 | 0.85 | 94% | 0 | yes |  |
| diag | 3 | 6,655 | 104 | -23.16 | 0.82 | 0.73 | 0.63 | 80% | 0 | yes | candidate within diag |
| diag | 4 | 6,478 | 139 | -22.98 | 0.56 | 0.54 | 0.47 | 40% | 1 | no |  |
| diag | 5 | 6,509 | 174 | -23.13 | 0.47 | 0.38 | 0.54 | 42% | 5 | no |  |
| diag | 6 | 6,531 | 209 | -22.64 | 0.44 | 0.41 | 0.51 | 41% | 6 | no |  |
| tied | 1 | 6,358 | 170 | -21.19 | 1.00 | 1.00 | 1.00 | 100% | 0 | yes | **candidate** |
| tied | 2 | 6,359 | 188 | -21.83 | 0.92 | 0.46 | 0.03 | 72% | 0 | no |  |
| tied | 3 | 6,368 | 206 | -21.65 | 0.91 | 0.64 | 0.70 | 66% | 1 | no |  |
| tied | 4 | 6,342 | 224 | -21.46 | 0.52 | 0.50 | 0.30 | 55% | 3 | no | lowest BIC |
| tied | 5 | 6,346 | 242 | -22.81 | 0.67 | 0.50 | 0.53 | 30% | 4 | no |  |
| tied | 6 | 6,342 | 260 | -23.07 | 0.39 | 0.41 | 0.33 | 23% | 5 | no |  |

Candidate under the rule: **tied, k = 1** (BIC 6,358). k = 1 means no sub-structure inside this family under the rule.
Same rule inside diag only: diag, k = 3 (BIC 6,655, +297 vs the candidate).
Tied k = 1 is one Gaussian with a full covariance matrix (170 parameters vs 152 training rows); the D27 limit on full covariance (parameters under half the rows, 76) was written for full only and is not applied to it.
Lowest BIC overall in this family: tied, k = 4 (BIC 6,342; not stable).

Charts: [BIC](bic_by_k.png) · [held-out](heldout_ll_by_k.png) · [bootstrap ARI](bootstrap_ari_by_k.png) · [least stable sub-role](retention_min_by_k.png) · [season ARI](season_ari_by_k.png) · [parameters](n_params_by_k.png) · [sweep.csv](sweep.csv)
