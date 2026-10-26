# Stability: F3, k = 2 (tied covariance)

- **Starts:** 20 seeds; ARI against the best: median 0.922, min 0.154.
- **Bootstrap:** 50 refits on resampled training player-seasons (152); ARI vs this fit: median 0.456, 10th–90th percentile 0.029–0.922.
- **Season-to-season:** ARI between a 2024-25-only and a 2025-26-only model: 0.026.
- Player-seasons of the same player are resampled independently; bootstrap figures are somewhat optimistic.

## Share of each sub-role's players who keep the same sub-role across bootstrap refits

Flag: under 70%.

| sub-role | members | kept | flag |
|---|---|---|---|
| F3-S1 | 95 | 88% |  |
| F3-S2 | 57 | 72% |  |

Sub-roles under 70%: 0 of 2. Median bootstrap ARI < 0.60.
