# Stability: F3, k = 4 (diag covariance)

- **Starts:** 20 seeds; ARI against the best: median 0.565, min 0.436.
- **Bootstrap:** 50 refits on resampled training player-seasons (152); ARI vs this fit: median 0.539, 10th–90th percentile 0.412–0.643.
- **Season-to-season:** ARI between a 2024-25-only and a 2025-26-only model: 0.471.
- Player-seasons of the same player are resampled independently; bootstrap figures are somewhat optimistic.

## Share of each sub-role's players who keep the same sub-role across bootstrap refits

Flag: under 70%.

| sub-role | members | kept | flag |
|---|---|---|---|
| F3-S1 | 54 | 74% |  |
| F3-S2 | 39 | 80% |  |
| F3-S3 | 35 | 40% | **under 70%** |
| F3-S4 | 24 | 71% |  |

Sub-roles under 70%: 1 of 4. Median bootstrap ARI < 0.60.
