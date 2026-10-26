# Stability: F2, k = 5 (diag covariance)

- **Starts:** 20 seeds; ARI against the best: median 0.500, min 0.201.
- **Bootstrap:** 50 refits on resampled training player-seasons (281); ARI vs this fit: median 0.465, 10th–90th percentile 0.359–0.558.
- **Season-to-season:** ARI between a 2024-25-only and a 2025-26-only model: 0.406.
- Player-seasons of the same player are resampled independently; bootstrap figures are somewhat optimistic.

## Share of each sub-role's players who keep the same sub-role across bootstrap refits

Flag: under 70%.

| sub-role | members | kept | flag |
|---|---|---|---|
| F2-S1 | 64 | 36% | **under 70%** |
| F2-S2 | 62 | 67% | **under 70%** |
| F2-S3 | 61 | 71% |  |
| F2-S4 | 58 | 77% |  |
| F2-S5 | 36 | 87% |  |

Sub-roles under 70%: 2 of 5. Median bootstrap ARI < 0.60.
