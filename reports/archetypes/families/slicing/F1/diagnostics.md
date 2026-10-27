# Slicing diagnostics: F1 On-ball Shot Creators (D30)

303 level-2 training player-seasons (top family F1, probability >= 0.6), 2024-25 + 2025-26. 16 features (D31: dropped charges drawn per 100), standardized with a scaler fitted on these rows. Nothing named or chosen.

## 1. Within-family PCA

| | PC1 | PC2 | PC3 | PC4 | PC5 |
|---|---|---|---|---|---|
| variance explained | 31.0% | 17.9% | 13.1% | 8.2% | 6.0% |
| cumulative | 31.0% | 48.9% | 62.0% | 70.2% | 76.2% |

For reference, 16 uncorrelated features would give 6.2% per PC.

Top 5 loadings (sign convention: each PC's largest-magnitude loading is positive; a positive score means more of the positive-loading features and less of the negative ones):

| PC | #1 | #2 | #3 | #4 | #5 |
|---|---|---|---|---|---|
| PC1 | fouls drawn per 100 +0.34 | corner-3 share of FGA -0.33 | FTA per FGA +0.33 | above-break-3 share of FGA -0.31 | rim share of FGA +0.30 |
| PC2 | pull-up/step-back 3PA per FGA +0.49 | assisted share of made FG -0.36 | OREB% -0.35 | above-break-3 share of FGA +0.31 | shot attempts + TOV per 100 +0.30 |
| PC3 | driving FGA per FGA +0.38 | defensive fouls per 100 +0.35 | DREB% -0.33 | shot attempts + TOV per 100 -0.32 | fouls drawn per 100 -0.31 |

Full loadings: [loadings.csv](loadings.csv). Scatter: [pc_scatter.png](pc_scatter.png) (Pacers player-seasons ringed and labeled; Turner 2024-25 and Zubac seasons labeled when they are in this family's training rows).

## 2. Slicing test

### Diag sweep with the D31 features (k 1-6)

Same init and checks as D26/D27 (20 starts, 50 bootstrap refits, held-out = fit 2024-25, score 2025-26). Stable = median bootstrap ARI >= 0.60 and no cluster under 70% kept. Diag candidate = lowest-BIC stable diag row. Tied k = 1 (one Gaussian with a full covariance) is shown as a reference row.

| cov | k | BIC | params | held-out | boot ARI | season ARI | kept min | stable | |
|---|---|---|---|---|---|---|---|---|---|
| diag | 1 | 13,941 | 32 | -23.01 | 1.00 | 1.00 | 100% | yes |  |
| diag | 2 | 13,174 | 65 | -21.43 | 0.72 | 0.70 | 89% | yes | diag candidate |
| diag | 3 | 12,776 | 98 | -20.91 | 0.59 | 0.36 | 81% | no |  |
| diag | 4 | 12,583 | 131 | -20.72 | 0.37 | 0.32 | 56% | no |  |
| diag | 5 | 12,508 | 164 | -20.62 | 0.41 | 0.31 | 56% | no |  |
| diag | 6 | 12,468 | 197 | -20.53 | 0.41 | 0.33 | 57% | no |  |
| tied | 1 | 10,928 | 152 | -17.59 | 1.00 | 1.00 | 100% | yes | reference |

Diag candidate: k = 2 (BIC 13,174; +2,246 vs tied k = 1 at 10,928).

Charts: [BIC](bic_by_k.png) · [held-out](heldout_ll_by_k.png) · [bootstrap ARI](bootstrap_ari_by_k.png) · [least stable cluster](retention_min_by_k.png) · [season ARI](season_ari_by_k.png) · [sweep.csv](sweep.csv)

### Where the diag cluster centers sit

Centers are the diag model's cluster means in the within-family standardized space. Between-centroid variance B = sum of weight x (center - weighted mean center)², as a matrix. **Along PCj** = share of B's total lying along PCj. **One-line share** = share of B along the centers' own first direction (1.00 = all centers on one straight line; always 1.00 at k = 2). **Angle** = angle between that line and PC1.

| k | along PC1 | PC2 | PC3 | PC4 | PC5 | PC1 + PC2 | one-line share | angle to PC1 |
|---|---|---|---|---|---|---|---|---|
| 2 | 96% | 3% | 0% | 0% | 0% | 99% | 1.00 | 11° |
| 3 | 66% | 32% | 0% | 0% | 0% | 99% | 0.67 | 6° |

Center positions on PC1 / PC2 (S1 = largest cluster):

| k | cluster | members | weight | PC1 | PC2 |
|---|---|---|---|---|---|
| 2 | F1-S1 | 165 | 0.54 | +1.58 | +0.27 |
| 2 | F1-S2 | 138 | 0.46 | -1.83 | -0.31 |
| 3 | F1-S1 | 114 | 0.38 | -2.11 | -0.33 |
| 3 | F1-S2 | 103 | 0.34 | +0.73 | +1.54 |
| 3 | F1-S3 | 86 | 0.28 | +1.93 | -1.43 |

Chart: [centroids.png](centroids.png)

## 3. Multimodality

1-D Gaussian mixture on each PC's scores (10 starts). BIC(2) − BIC(1) below 0 means 2 components fit better after the parameter penalty; above 0 means 1 component. Skewness of the PC scores is shown because a lopsided single hump can also be fitted better by 2 components.

| PC | BIC 1 comp | BIC 2 comp | BIC(2) − BIC(1) | 2-comp weights | 2-comp means | 2-comp SDs | skewness |
|---|---|---|---|---|---|---|---|
| PC1 | 1,356.6 | 1,374.7 | +18.1 | 0.53 / 0.47 | -1.14 / +1.30 | 1.79 / 1.94 | +0.19 |
| PC2 | 1,190.0 | 1,206.5 | +16.4 | 0.56 / 0.44 | -0.99 / +1.24 | 1.29 / 1.26 | +0.03 |

Chart: [pc_hist.png](pc_hist.png)
