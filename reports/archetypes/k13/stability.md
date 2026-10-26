# Stability, k = 13 (tied covariance)

- **Starts:** 20 fits from different seeds; ARI of each against the best: median 0.385, min 0.262.
- **Bootstrap:** 50 refits on resampled player-seasons, clusters matched to this fit by center distance; ARI vs this fit: median 0.340, 10th–90th percentile 0.261–0.500.
- **Season-to-season:** ARI between a 2024-25-only and a 2025-26-only model labelling all rows: 0.390.
- The same player appears in both seasons, so resampling player-seasons treats them as independent; the bootstrap figures are somewhat optimistic.

## Share of each cluster's players who keep the same archetype across bootstrap refits

Flag: under 70%.

| cluster | members | kept | flag |
|---|---|---|---|
| C1 | 246 | 29% | **under 70%** |
| C2 | 145 | 32% | **under 70%** |
| C3 | 55 | 56% | **under 70%** |
| C4 | 53 | 22% | **under 70%** |
| C5 | 41 | 61% | **under 70%** |
| C6 | 36 | 81% |  |
| C7 | 31 | 77% |  |
| C8 | 31 | 39% | **under 70%** |
| C9 | 29 | 43% | **under 70%** |
| C10 | 26 | 64% | **under 70%** |
| C11 | 24 | 55% | **under 70%** |
| C12 | 18 | 64% | **under 70%** |
| C13 | 15 | 71% |  |

Clusters under 70%: 10 of 13.