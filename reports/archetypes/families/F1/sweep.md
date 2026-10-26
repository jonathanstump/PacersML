# Sub-role sweep inside F1

303 training player-seasons (top family F1, probability >= 0.6), features standardized with F1's own scaler. Covariance: tied and diag at k 1-6; full only where its parameter count is under half the training rows (152): none (full k = 1 already has 170 parameters).

Same initialization and checks as D26: 20 starts (k-means init), 50 bootstrap refits, held-out = fit 2024-25, score 2025-26 (own scaler), season ARI = 2024-25-only vs 2025-26-only model. At k = 1 every ARI and retention is 1 by construction.

Selection rule (D27, marked here, not picked): BIC narrows; stable = median bootstrap ARI >= 0.60 and no sub-role under 70% kept; **candidate** = lowest-BIC stable row; naming breaks ties (rows within 10 BIC of the candidate that are also stable are marked *near tie*).

| cov | k | BIC | params | held-out | starts ARI | boot ARI | season ARI | kept min | < 70% | stable | |
|---|---|---|---|---|---|---|---|---|---|---|---|
| diag | 1 | 14,812 | 34 | -24.30 | 1.00 | 1.00 | 1.00 | 100% | 0 | yes |  |
| diag | 2 | 14,051 | 69 | -22.73 | 0.95 | 0.65 | 0.59 | 88% | 0 | yes |  |
| diag | 3 | 13,648 | 104 | -22.24 | 0.79 | 0.62 | 0.55 | 83% | 0 | yes | candidate within diag |
| diag | 4 | 13,464 | 139 | -22.12 | 0.37 | 0.37 | 0.27 | 54% | 2 | no |  |
| diag | 5 | 13,388 | 174 | -21.72 | 0.52 | 0.44 | 0.32 | 52% | 5 | no |  |
| diag | 6 | 13,289 | 209 | -21.39 | 0.44 | 0.42 | 0.26 | 50% | 4 | no |  |
| tied | 1 | 11,852 | 170 | -18.90 | 1.00 | 1.00 | 1.00 | 100% | 0 | yes | lowest BIC **candidate** |
| tied | 2 | 11,903 | 188 | -19.00 | 0.21 | 0.12 | 0.07 | 66% | 1 | no |  |
| tied | 3 | 11,866 | 206 | -18.97 | 0.83 | 0.44 | -0.00 | 67% | 2 | no |  |
| tied | 4 | 11,890 | 224 | -18.85 | 0.96 | 0.41 | 0.17 | 56% | 3 | no |  |
| tied | 5 | 11,858 | 242 | -18.87 | 0.49 | 0.36 | 0.21 | 44% | 4 | no |  |
| tied | 6 | 11,903 | 260 | -18.82 | 0.47 | 0.29 | 0.20 | 31% | 6 | no |  |

Candidate under the rule: **tied, k = 1** (BIC 11,852). k = 1 means no sub-structure inside this family under the rule.
Same rule inside diag only: diag, k = 3 (BIC 13,648, +1,795 vs the candidate).
Tied k = 1 is one Gaussian with a full covariance matrix (170 parameters vs 303 training rows); the D27 limit on full covariance (parameters under half the rows, 152) was written for full only and is not applied to it.
Lowest BIC overall in this family: tied, k = 1 (BIC 11,852; stable).

Charts: [BIC](bic_by_k.png) · [held-out](heldout_ll_by_k.png) · [bootstrap ARI](bootstrap_ari_by_k.png) · [least stable sub-role](retention_min_by_k.png) · [season ARI](season_ari_by_k.png) · [parameters](n_params_by_k.png) · [sweep.csv](sweep.csv)
