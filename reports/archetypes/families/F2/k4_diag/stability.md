# Stability: F2, k = 4 (diag covariance)

- **Starts:** 20 seeds; ARI against the best: median 0.741, min 0.434.
- **Bootstrap:** 50 refits on resampled training player-seasons (281); ARI vs this fit: median 0.626, 10th–90th percentile 0.434–0.808.
- **Season-to-season:** ARI between a 2024-25-only and a 2025-26-only model: 0.365.
- Player-seasons of the same player are resampled independently; bootstrap figures are somewhat optimistic.

## Share of each sub-role's players who keep the same sub-role across bootstrap refits

Flag: under 70%.

| sub-role | members | kept | flag |
|---|---|---|---|
| F2-S1 | 89 | 78% |  |
| F2-S2 | 67 | 88% |  |
| F2-S3 | 65 | 84% |  |
| F2-S4 | 60 | 79% |  |

Sub-roles under 70%: 0 of 4. Median bootstrap ARI >= 0.60.
