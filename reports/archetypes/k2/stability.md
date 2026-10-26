# Stability, k = 2 (full covariance)

- **Starts:** 20 fits from different seeds; ARI of each against the best: median 0.921, min 0.211.
- **Bootstrap:** 50 refits on resampled player-seasons, clusters matched to this fit by center distance; ARI vs this fit: median 0.830, 10th–90th percentile 0.392–0.883.
- **Season-to-season:** ARI between a 2024-25-only and a 2025-26-only model labelling all rows: 0.470.
- The same player appears in both seasons, so resampling player-seasons treats them as independent; the bootstrap figures are somewhat optimistic.

## Share of each cluster's players who keep the same archetype across bootstrap refits

Flag: under 70%.

| cluster | members | kept | flag |
|---|---|---|---|
| C1 | 533 | 93% |  |
| C2 | 217 | 88% |  |

Clusters under 70%: 0 of 2.