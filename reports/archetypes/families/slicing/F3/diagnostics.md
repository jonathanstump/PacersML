# Slicing diagnostics: F3 Bigs (D30)

152 level-2 training player-seasons (top family F3, probability >= 0.6), 2024-25 + 2025-26. 15 features (D31: dropped pull-up/step-back 3PA per FGA, charges drawn per 100), standardized with a scaler fitted on these rows. Nothing named or chosen.

## 1. Within-family PCA

| | PC1 | PC2 | PC3 | PC4 | PC5 |
|---|---|---|---|---|---|
| variance explained | 24.8% | 21.1% | 10.2% | 9.7% | 7.6% |
| cumulative | 24.8% | 45.9% | 56.1% | 65.7% | 73.3% |

For reference, 15 uncorrelated features would give 6.7% per PC.

Top 5 loadings (sign convention: each PC's largest-magnitude loading is positive; a positive score means more of the positive-loading features and less of the negative ones):

| PC | #1 | #2 | #3 | #4 | #5 |
|---|---|---|---|---|---|
| PC1 | OREB% +0.44 | rim share of FGA +0.43 | above-break-3 share of FGA -0.42 | corner-3 share of FGA -0.35 | FTA per FGA +0.34 |
| PC2 | shot attempts + TOV per 100 +0.49 | fouls drawn per 100 +0.42 | AST per 100 +0.36 | driving FGA per FGA +0.35 | DREB% +0.27 |
| PC3 | short-mid share of FGA +0.56 | FTA per FGA -0.39 | fouls drawn per 100 -0.33 | corner-3 share of FGA -0.29 | STL per 100 -0.26 |

Full loadings: [loadings.csv](loadings.csv). Scatter: [pc_scatter.png](pc_scatter.png) (Pacers player-seasons ringed and labeled; Turner 2024-25 and Zubac seasons labeled when they are in this family's training rows).

| player-season | PC1 | PC2 |
|---|---|---|
| Myles Turner 24-25 | -3.15 | -0.19 |
| Ivica Zubac 24-25 | +1.04 | +1.56 |
| Ivica Zubac 25-26 | +1.13 | +1.45 |

## 2. Slicing test

### Diag sweep with the D31 features (k 1-6)

Same init and checks as D26/D27 (20 starts, 50 bootstrap refits, held-out = fit 2024-25, score 2025-26). Stable = median bootstrap ARI >= 0.60 and no cluster under 70% kept. Diag candidate = lowest-BIC stable diag row. Tied k = 1 (one Gaussian with a full covariance) is shown as a reference row.

| cov | k | BIC | params | held-out | boot ARI | season ARI | kept min | stable | |
|---|---|---|---|---|---|---|---|---|---|
| diag | 1 | 6,621 | 30 | -23.22 | 1.00 | 1.00 | 100% | yes |  |
| diag | 2 | 6,164 | 61 | -21.58 | 0.78 | 0.75 | 91% | yes |  |
| diag | 3 | 5,963 | 92 | -21.22 | 0.64 | 0.62 | 70% | yes | diag candidate |
| diag | 4 | 5,956 | 123 | -21.33 | 0.59 | 0.38 | 43% | no |  |
| diag | 5 | 5,936 | 154 | -21.19 | 0.53 | 0.41 | 29% | no |  |
| diag | 6 | 5,943 | 185 | -21.21 | 0.55 | 0.54 | 36% | no |  |
| tied | 1 | 5,500 | 135 | -19.03 | 1.00 | 1.00 | 100% | yes | reference |

Diag candidate: k = 3 (BIC 5,963; +463 vs tied k = 1 at 5,500).

Charts: [BIC](bic_by_k.png) · [held-out](heldout_ll_by_k.png) · [bootstrap ARI](bootstrap_ari_by_k.png) · [least stable cluster](retention_min_by_k.png) · [season ARI](season_ari_by_k.png) · [sweep.csv](sweep.csv)

### Where the diag cluster centers sit

Centers are the diag model's cluster means in the within-family standardized space. Between-centroid variance B = sum of weight x (center - weighted mean center)², as a matrix. **Along PCj** = share of B's total lying along PCj. **One-line share** = share of B along the centers' own first direction (1.00 = all centers on one straight line; always 1.00 at k = 2). **Angle** = angle between that line and PC1.

| k | along PC1 | PC2 | PC3 | PC4 | PC5 | PC1 + PC2 | one-line share | angle to PC1 |
|---|---|---|---|---|---|---|---|---|
| 2 | 86% | 9% | 3% | 0% | 1% | 95% | 1.00 | 22° |
| 3 | 55% | 37% | 2% | 1% | 3% | 92% | 0.61 | 20° |
| 4 | 54% | 36% | 2% | 2% | 3% | 90% | 0.58 | 15° |

Center positions on PC1 / PC2 (S1 = largest cluster):

| k | cluster | members | weight | PC1 | PC2 |
|---|---|---|---|---|---|
| 2 | F3-S1 | 81 | 0.54 | -1.35 | +0.44 |
| 2 | F3-S2 | 71 | 0.46 | +1.60 | -0.52 |
| 3 | F3-S1 | 55 | 0.36 | +1.66 | -0.75 |
| 3 | F3-S2 | 49 | 0.32 | -1.89 | -0.91 |
| 3 | F3-S3 | 48 | 0.32 | +0.05 | +1.77 |
| 4 | F3-S1 | 53 | 0.35 | +1.67 | -0.79 |
| 4 | F3-S2 | 50 | 0.33 | -1.76 | -0.95 |
| 4 | F3-S3 | 26 | 0.17 | +1.14 | +1.42 |
| 4 | F3-S4 | 23 | 0.15 | -1.29 | +2.30 |

Chart: [centroids.png](centroids.png)

## 3. Multimodality

1-D Gaussian mixture on each PC's scores (10 starts). BIC(2) − BIC(1) below 0 means 2 components fit better after the parameter penalty; above 0 means 1 component. Skewness of the PC scores is shown because a lopsided single hump can also be fitted better by 2 components.

| PC | BIC 1 comp | BIC 2 comp | BIC(2) − BIC(1) | 2-comp weights | 2-comp means | 2-comp SDs | skewness |
|---|---|---|---|---|---|---|---|
| PC1 | 641.0 | 643.7 | +2.7 | 0.49 / 0.51 | -1.56 / +1.50 | 1.31 / 1.03 | -0.23 |
| PC2 | 616.4 | 606.1 | -10.3 | 0.65 / 0.35 | -0.94 / +1.74 | 0.94 / 1.64 | +0.95 |

Chart: [pc_hist.png](pc_hist.png)
