# Stability: F3, k = 3 (diag covariance)

- **Starts:** 20 seeds; ARI against the best: median 0.822, min 0.713.
- **Bootstrap:** 50 refits on resampled training player-seasons (152); ARI vs this fit: median 0.729, 10th–90th percentile 0.431–0.836.
- **Season-to-season:** ARI between a 2024-25-only and a 2025-26-only model: 0.634.
- Player-seasons of the same player are resampled independently; bootstrap figures are somewhat optimistic.

## Share of each sub-role's players who keep the same sub-role across bootstrap refits

Flag: under 70%.

| sub-role | members | kept | flag |
|---|---|---|---|
| F3-S1 | 61 | 84% |  |
| F3-S2 | 61 | 90% |  |
| F3-S3 | 30 | 80% |  |

Sub-roles under 70%: 0 of 3. Median bootstrap ARI >= 0.60.
