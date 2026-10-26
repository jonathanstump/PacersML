# Stability, k = 12 (tied covariance)

- **Starts:** 20 fits from different seeds; ARI of each against the best: median 0.577, min 0.408.
- **Bootstrap:** 50 refits on resampled player-seasons, clusters matched to this fit by center distance; ARI vs this fit: median 0.459, 10th–90th percentile 0.357–0.625.
- **Season-to-season:** ARI between a 2024-25-only and a 2025-26-only model labelling all rows: 0.532.
- The same player appears in both seasons, so resampling player-seasons treats them as independent; the bootstrap figures are somewhat optimistic.

## Share of each cluster's players who keep the same archetype across bootstrap refits

Flag: under 70%.

| cluster | members | kept | flag |
|---|---|---|---|
| C1 | 271 | 54% | **under 70%** |
| C2 | 77 | 40% | **under 70%** |
| C3 | 60 | 64% | **under 70%** |
| C4 | 55 | 62% | **under 70%** |
| C5 | 49 | 28% | **under 70%** |
| C6 | 45 | 56% | **under 70%** |
| C7 | 45 | 81% |  |
| C8 | 40 | 73% |  |
| C9 | 34 | 77% |  |
| C10 | 27 | 63% | **under 70%** |
| C11 | 27 | 53% | **under 70%** |
| C12 | 20 | 87% |  |

Clusters under 70%: 8 of 12.