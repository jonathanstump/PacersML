# Stability, k = 4 (full covariance)

- **Starts:** 20 fits from different seeds; ARI of each against the best: median 0.351, min 0.335.
- **Bootstrap:** 50 refits on resampled player-seasons, clusters matched to this fit by center distance; ARI vs this fit: median 0.449, 10th–90th percentile 0.315–0.659.
- **Season-to-season:** ARI between a 2024-25-only and a 2025-26-only model labelling all rows: 0.355.
- The same player appears in both seasons, so resampling player-seasons treats them as independent; the bootstrap figures are somewhat optimistic.

## Share of each cluster's players who keep the same archetype across bootstrap refits

Flag: under 70%.

| cluster | members | kept | flag |
|---|---|---|---|
| C1 | 264 | 68% | **under 70%** |
| C2 | 259 | 76% |  |
| C3 | 118 | 46% | **under 70%** |
| C4 | 109 | 81% |  |

Clusters under 70%: 2 of 4.