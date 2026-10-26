# Stability: F2, k = 2 (tied covariance)

- **Starts:** 20 seeds; ARI against the best: median 0.986, min 0.958.
- **Bootstrap:** 50 refits on resampled training player-seasons (281); ARI vs this fit: median 0.355, 10th–90th percentile 0.068–0.761.
- **Season-to-season:** ARI between a 2024-25-only and a 2025-26-only model: 0.035.
- Player-seasons of the same player are resampled independently; bootstrap figures are somewhat optimistic.

## Share of each sub-role's players who keep the same sub-role across bootstrap refits

Flag: under 70%.

| sub-role | members | kept | flag |
|---|---|---|---|
| F2-S1 | 146 | 76% |  |
| F2-S2 | 135 | 81% |  |

Sub-roles under 70%: 0 of 2. Median bootstrap ARI < 0.60.
