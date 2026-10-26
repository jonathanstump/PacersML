# Stability: F1, k = 4 (diag covariance)

- **Starts:** 20 seeds; ARI against the best: median 0.371, min 0.327.
- **Bootstrap:** 50 refits on resampled training player-seasons (303); ARI vs this fit: median 0.369, 10th–90th percentile 0.305–0.641.
- **Season-to-season:** ARI between a 2024-25-only and a 2025-26-only model: 0.266.
- Player-seasons of the same player are resampled independently; bootstrap figures are somewhat optimistic.

## Share of each sub-role's players who keep the same sub-role across bootstrap refits

Flag: under 70%.

| sub-role | members | kept | flag |
|---|---|---|---|
| F1-S1 | 107 | 54% | **under 70%** |
| F1-S2 | 82 | 65% | **under 70%** |
| F1-S3 | 58 | 91% |  |
| F1-S4 | 56 | 78% |  |

Sub-roles under 70%: 2 of 4. Median bootstrap ARI < 0.60.
