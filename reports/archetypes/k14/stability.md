# Stability, k = 14 (tied covariance)

- **Starts:** 20 fits from different seeds; ARI of each against the best: median 0.407, min 0.332.
- **Bootstrap:** 50 refits on resampled player-seasons, clusters matched to this fit by center distance; ARI vs this fit: median 0.346, 10th–90th percentile 0.264–0.446.
- **Season-to-season:** ARI between a 2024-25-only and a 2025-26-only model labelling all rows: 0.428.
- The same player appears in both seasons, so resampling player-seasons treats them as independent; the bootstrap figures are somewhat optimistic.

## Share of each cluster's players who keep the same archetype across bootstrap refits

Flag: under 70%.

| cluster | members | kept | flag |
|---|---|---|---|
| C1 | 217 | 36% | **under 70%** |
| C2 | 142 | 29% | **under 70%** |
| C3 | 64 | 50% | **under 70%** |
| C4 | 54 | 54% | **under 70%** |
| C5 | 44 | 17% | **under 70%** |
| C6 | 43 | 58% | **under 70%** |
| C7 | 40 | 28% | **under 70%** |
| C8 | 36 | 65% | **under 70%** |
| C9 | 30 | 36% | **under 70%** |
| C10 | 21 | 69% | **under 70%** |
| C11 | 21 | 72% |  |
| C12 | 19 | 22% | **under 70%** |
| C13 | 13 | 53% | **under 70%** |
| C14 | 6 | 80% |  |

Clusters under 70%: 12 of 14.