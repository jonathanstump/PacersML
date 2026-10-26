# Stability: F1, k = 3 (diag covariance)

- **Starts:** 20 seeds; ARI against the best: median 0.791, min 0.335.
- **Bootstrap:** 50 refits on resampled training player-seasons (303); ARI vs this fit: median 0.617, 10th–90th percentile 0.499–0.849.
- **Season-to-season:** ARI between a 2024-25-only and a 2025-26-only model: 0.555.
- Player-seasons of the same player are resampled independently; bootstrap figures are somewhat optimistic.

## Share of each sub-role's players who keep the same sub-role across bootstrap refits

Flag: under 70%.

| sub-role | members | kept | flag |
|---|---|---|---|
| F1-S1 | 117 | 83% |  |
| F1-S2 | 95 | 86% |  |
| F1-S3 | 91 | 91% |  |

Sub-roles under 70%: 0 of 3. Median bootstrap ARI >= 0.60.
