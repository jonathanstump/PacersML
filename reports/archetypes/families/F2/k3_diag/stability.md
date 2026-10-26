# Stability: F2, k = 3 (diag covariance)

- **Starts:** 20 seeds; ARI against the best: median 0.713, min 0.301.
- **Bootstrap:** 50 refits on resampled training player-seasons (281); ARI vs this fit: median 0.622, 10th–90th percentile 0.475–0.810.
- **Season-to-season:** ARI between a 2024-25-only and a 2025-26-only model: 0.280.
- Player-seasons of the same player are resampled independently; bootstrap figures are somewhat optimistic.

## Share of each sub-role's players who keep the same sub-role across bootstrap refits

Flag: under 70%.

| sub-role | members | kept | flag |
|---|---|---|---|
| F2-S1 | 110 | 82% |  |
| F2-S2 | 95 | 81% |  |
| F2-S3 | 76 | 93% |  |

Sub-roles under 70%: 0 of 3. Median bootstrap ARI >= 0.60.
