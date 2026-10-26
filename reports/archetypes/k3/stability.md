# Stability, k = 3 (full covariance)

- **Starts:** 20 fits from different seeds; ARI of each against the best: median 0.965, min 0.837.
- **Bootstrap:** 50 refits on resampled player-seasons, clusters matched to this fit by center distance; ARI vs this fit: median 0.660, 10th–90th percentile 0.573–0.730.
- **Season-to-season:** ARI between a 2024-25-only and a 2025-26-only model labelling all rows: 0.542.
- The same player appears in both seasons, so resampling player-seasons treats them as independent; the bootstrap figures are somewhat optimistic.

## Share of each cluster's players who keep the same archetype across bootstrap refits

Flag: under 70%.

| cluster | members | kept | flag |
|---|---|---|---|
| C1 | 306 | 84% |  |
| C2 | 291 | 90% |  |
| C3 | 153 | 92% |  |

Clusters under 70%: 0 of 3.