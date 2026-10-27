# Slicing diagnostics: F2 Off-ball Spot Ups (D30)

281 level-2 training player-seasons (top family F2, probability >= 0.6), 2024-25 + 2025-26. 16 features (D31: dropped charges drawn per 100), standardized with a scaler fitted on these rows. Nothing named or chosen.

## 1. Within-family PCA

| | PC1 | PC2 | PC3 | PC4 | PC5 |
|---|---|---|---|---|---|
| variance explained | 33.5% | 17.7% | 10.6% | 8.1% | 6.3% |
| cumulative | 33.5% | 51.2% | 61.7% | 69.8% | 76.2% |

For reference, 16 uncorrelated features would give 6.2% per PC.

Top 5 loadings (sign convention: each PC's largest-magnitude loading is positive; a positive score means more of the positive-loading features and less of the negative ones):

| PC | #1 | #2 | #3 | #4 | #5 |
|---|---|---|---|---|---|
| PC1 | rim share of FGA +0.34 | driving FGA per FGA +0.33 | assisted share of made FG -0.33 | above-break-3 share of FGA -0.32 | fouls drawn per 100 +0.32 |
| PC2 | pull-up/step-back 3PA per FGA +0.41 | OREB% -0.37 | corner-3 share of FGA -0.33 | defensive fouls per 100 -0.31 | shot attempts + TOV per 100 +0.27 |
| PC3 | DREB% +0.51 | shot attempts + TOV per 100 +0.39 | STL per 100 -0.39 | BLK per 100 +0.28 | fouls drawn per 100 +0.27 |

Full loadings: [loadings.csv](loadings.csv). Scatter: [pc_scatter.png](pc_scatter.png) (Pacers player-seasons ringed and labeled; Turner 2024-25 and Zubac seasons labeled when they are in this family's training rows).

## 2. Slicing test

### Diag sweep with the D31 features (k 1-6)

Same init and checks as D26/D27 (20 starts, 50 bootstrap refits, held-out = fit 2024-25, score 2025-26). Stable = median bootstrap ARI >= 0.60 and no cluster under 70% kept. Diag candidate = lowest-BIC stable diag row. Tied k = 1 (one Gaussian with a full covariance) is shown as a reference row.

| cov | k | BIC | params | held-out | boot ARI | season ARI | kept min | stable | |
|---|---|---|---|---|---|---|---|---|---|
| diag | 1 | 12,940 | 32 | -22.86 | 1.00 | 1.00 | 100% | yes |  |
| diag | 2 | 12,206 | 65 | -21.38 | 0.82 | 0.75 | 92% | yes |  |
| diag | 3 | 11,960 | 98 | -21.11 | 0.61 | 0.26 | 80% | yes |  |
| diag | 4 | 11,780 | 131 | -20.71 | 0.67 | 0.63 | 77% | yes | diag candidate |
| diag | 5 | 11,774 | 164 | -20.78 | 0.59 | 0.46 | 42% | no |  |
| diag | 6 | 11,776 | 197 | -20.74 | 0.54 | 0.38 | 55% | no |  |
| tied | 1 | 9,910 | 152 | -16.77 | 1.00 | 1.00 | 100% | yes | reference |

Diag candidate: k = 4 (BIC 11,780; +1,870 vs tied k = 1 at 9,910).

Charts: [BIC](bic_by_k.png) · [held-out](heldout_ll_by_k.png) · [bootstrap ARI](bootstrap_ari_by_k.png) · [least stable cluster](retention_min_by_k.png) · [season ARI](season_ari_by_k.png) · [sweep.csv](sweep.csv)

### Where the diag cluster centers sit

Centers are the diag model's cluster means in the within-family standardized space. Between-centroid variance B = sum of weight x (center - weighted mean center)², as a matrix. **Along PCj** = share of B's total lying along PCj. **One-line share** = share of B along the centers' own first direction (1.00 = all centers on one straight line; always 1.00 at k = 2). **Angle** = angle between that line and PC1.

| k | along PC1 | PC2 | PC3 | PC4 | PC5 | PC1 + PC2 | one-line share | angle to PC1 |
|---|---|---|---|---|---|---|---|---|
| 3 | 75% | 23% | 1% | 0% | 0% | 98% | 0.76 | 5° |
| 4 | 74% | 24% | 1% | 0% | 0% | 98% | 0.74 | 5° |
| 5 | 68% | 28% | 1% | 1% | 0% | 96% | 0.69 | 5° |

Center positions on PC1 / PC2 (S1 = largest cluster):

| k | cluster | members | weight | PC1 | PC2 |
|---|---|---|---|---|---|
| 3 | F2-S1 | 110 | 0.39 | -2.14 | +0.54 |
| 3 | F2-S2 | 94 | 0.34 | +0.38 | -1.44 |
| 3 | F2-S3 | 77 | 0.28 | +2.51 | +0.98 |
| 4 | F2-S1 | 86 | 0.30 | +0.43 | -1.61 |
| 4 | F2-S2 | 68 | 0.24 | -2.91 | +0.03 |
| 4 | F2-S3 | 65 | 0.24 | -0.41 | +1.37 |
| 4 | F2-S4 | 62 | 0.22 | +3.02 | +0.70 |
| 5 | F2-S1 | 83 | 0.29 | +0.54 | -1.61 |
| 5 | F2-S2 | 62 | 0.22 | +3.00 | +0.77 |
| 5 | F2-S3 | 56 | 0.21 | -0.29 | +1.17 |
| 5 | F2-S4 | 41 | 0.14 | -2.32 | -1.17 |
| 5 | F2-S5 | 39 | 0.14 | -3.07 | +1.60 |

Chart: [centroids.png](centroids.png)

## 3. Multimodality

1-D Gaussian mixture on each PC's scores (10 starts). BIC(2) − BIC(1) below 0 means 2 components fit better after the parameter penalty; above 0 means 1 component. Skewness of the PC scores is shown because a lopsided single hump can also be fitted better by 2 components.

| PC | BIC 1 comp | BIC 2 comp | BIC(2) − BIC(1) | 2-comp weights | 2-comp means | 2-comp SDs | skewness |
|---|---|---|---|---|---|---|---|
| PC1 | 1,280.4 | 1,298.6 | +18.2 | 0.46 / 0.54 | -1.47 / +1.26 | 1.82 / 1.91 | +0.09 |
| PC2 | 1,101.0 | 1,116.3 | +15.2 | 0.47 / 0.53 | -1.24 / +1.10 | 1.25 / 1.17 | -0.12 |

Chart: [pc_hist.png](pc_hist.png)
