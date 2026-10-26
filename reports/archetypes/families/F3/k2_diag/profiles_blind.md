# Blind sub-role profiles: F3, k = 2 (diag covariance)

No player names in this file. Sub-roles are numbered by size inside the family (S1 = largest); the numbers carry no meaning and are not matched across k.

- Training player-seasons in F3: 152 (top family F3 with probability >= 0.6).
- Members = training player-seasons whose most likely sub-role is this one.
- **within-family z**: members' mean of the feature standardized with F3's own mean and SD.
- Real units: sub-role mean vs F3 average (its training rows) vs league average (all 750 fitted player-seasons).
- Share of league minutes: members' minutes ÷ all players' regular-season minutes in the two seasons.

## F3-S1

**Size:** 79 player-seasons (52.0% of F3 training) · **share of F3 minutes:** 55.4% · **share of league minutes:** 9.6% · median membership probability 1.00, 0% of members under 0.6

**Six most distinguishing features** (largest |within-family z|):

| feature | group | within-family z | sub-role | F3 avg | league avg |
|---|---|---|---|---|---|
| above-break-3 share of FGA | shooting | +0.72 | 23.4% | 13.2% | 29.6% |
| rim share of FGA | shooting | -0.71 | 38.4% | 51.5% | 30.6% |
| OREB% | rebounding | -0.64 | 7.2% | 9.5% | 4.6% |
| corner-3 share of FGA | shooting | +0.61 | 9.9% | 5.7% | 12.4% |
| pull-up/step-back 3PA per FGA | shooting | +0.49 | 2.0% | 1.1% | 9.3% |
| FTA per FGA | shooting | -0.43 | 0.28 | 0.34 | 0.25 |

**Shot-location mix** (share of FGA):

| | rim (restricted area) | short mid (paint, non-RA) | long mid | corner 3 | above-break 3 |
|---|---|---|---|---|---|
| sub-role | 36% | 21% | 10% | 8% | 25% |
| F3 | 46% | 22% | 9% | 6% | 16% |
| league | 29% | 19% | 11% | 11% | 31% |

## F3-S2

**Size:** 73 player-seasons (48.0% of F3 training) · **share of F3 minutes:** 44.6% · **share of league minutes:** 7.7% · median membership probability 1.00, 0% of members under 0.6

**Six most distinguishing features** (largest |within-family z|):

| feature | group | within-family z | sub-role | F3 avg | league avg |
|---|---|---|---|---|---|
| above-break-3 share of FGA | shooting | -0.78 | 2.1% | 13.2% | 29.6% |
| rim share of FGA | shooting | +0.77 | 65.6% | 51.5% | 30.6% |
| OREB% | rebounding | +0.69 | 11.9% | 9.5% | 4.6% |
| corner-3 share of FGA | shooting | -0.66 | 1.3% | 5.7% | 12.4% |
| pull-up/step-back 3PA per FGA | shooting | -0.53 | 0.2% | 1.1% | 9.3% |
| FTA per FGA | shooting | +0.47 | 0.40 | 0.34 | 0.25 |

**Shot-location mix** (share of FGA):

| | rim (restricted area) | short mid (paint, non-RA) | long mid | corner 3 | above-break 3 |
|---|---|---|---|---|---|
| sub-role | 64% | 24% | 9% | 1% | 2% |
| F3 | 46% | 22% | 9% | 6% | 16% |
| league | 29% | 19% | 11% | 11% | 31% |
