# Stability: F3, k = 2 (diag covariance)

- **Starts:** 20 seeds; ARI against the best: median 1.000, min 1.000.
- **Bootstrap:** 50 refits on resampled training player-seasons (152); ARI vs this fit: median 0.872, 10th–90th percentile 0.730–0.950.
- **Season-to-season:** ARI between a 2024-25-only and a 2025-26-only model: 0.847.
- Player-seasons of the same player are resampled independently; bootstrap figures are somewhat optimistic.

## Share of each sub-role's players who keep the same sub-role across bootstrap refits

Flag: under 70%.

| sub-role | members | kept | flag |
|---|---|---|---|
| F3-S1 | 79 | 98% |  |
| F3-S2 | 73 | 94% |  |

Sub-roles under 70%: 0 of 2. Median bootstrap ARI >= 0.60.
