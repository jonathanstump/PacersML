# Stability: F1, k = 2 (diag covariance)

- **Starts:** 20 seeds; ARI against the best: median 0.955, min 0.823.
- **Bootstrap:** 50 refits on resampled training player-seasons (303); ARI vs this fit: median 0.653, 10th–90th percentile 0.272–0.835.
- **Season-to-season:** ARI between a 2024-25-only and a 2025-26-only model: 0.590.
- Player-seasons of the same player are resampled independently; bootstrap figures are somewhat optimistic.

## Share of each sub-role's players who keep the same sub-role across bootstrap refits

Flag: under 70%.

| sub-role | members | kept | flag |
|---|---|---|---|
| F1-S1 | 165 | 90% |  |
| F1-S2 | 138 | 88% |  |

Sub-roles under 70%: 0 of 2. Median bootstrap ARI >= 0.60.
