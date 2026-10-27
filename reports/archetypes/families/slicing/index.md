# D30 slicing diagnostics (pending Jonathan's choice)

Per family: within-family PCA, diag sweep with the D31 features, where the diag cluster centers sit relative to the PCs, and 1 vs 2 component fits on PC1 and PC2. Numbers only; nothing named, chosen or packaged. Method: docs/METHODS.md section 7.

| family | rows | features | PC1 / PC2 variance | diag candidate k | BIC vs tied k = 1 | along PC1 at k−1 / k / k+1 | one-line share at k−1 / k / k+1 | PC1 BIC(2)−BIC(1) | PC2 BIC(2)−BIC(1) | report |
|---|---|---|---|---|---|---|---|---|---|---|
| F1 On-ball Shot Creators | 303 | 16 | 31.0% / 17.9% | 2 | +2,246 | k2 96% / k3 66% | k2 1.00 / k3 0.67 | +18.1 | +16.4 | [diagnostics.md](F1/diagnostics.md) |
| F2 Off-ball Spot Ups | 281 | 16 | 33.5% / 17.7% | 4 | +1,870 | k3 75% / k4 74% / k5 68% | k3 0.76 / k4 0.74 / k5 0.69 | +18.2 | +15.2 | [diagnostics.md](F2/diagnostics.md) |
| F3 Bigs | 152 | 15 | 24.8% / 21.1% | 3 | +463 | k2 86% / k3 55% / k4 54% | k2 1.00 / k3 0.61 / k4 0.58 | +2.7 | -10.3 | [diagnostics.md](F3/diagnostics.md) |

Open per family: diagnostics.md, then pc_scatter.png, centroids.png, pc_hist.png.
