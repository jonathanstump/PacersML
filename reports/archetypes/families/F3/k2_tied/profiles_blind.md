# Blind sub-role profiles: F3, k = 2 (tied covariance)

No player names in this file. Sub-roles are numbered by size inside the family (S1 = largest); the numbers carry no meaning and are not matched across k.

- Training player-seasons in F3: 152 (top family F3 with probability >= 0.6).
- Members = training player-seasons whose most likely sub-role is this one.
- **within-family z**: members' mean of the feature standardized with F3's own mean and SD.
- Real units: sub-role mean vs F3 average (its training rows) vs league average (all 750 fitted player-seasons).
- Share of league minutes: members' minutes ÷ all players' regular-season minutes in the two seasons.

## F3-S1

**Size:** 95 player-seasons (62.5% of F3 training) · **share of F3 minutes:** 61.9% · **share of league minutes:** 10.7% · median membership probability 1.00, 0% of members under 0.6

**Six most distinguishing features** (largest |within-family z|):

| feature | group | within-family z | sub-role | F3 avg | league avg |
|---|---|---|---|---|---|
| corner-3 share of FGA | shooting | -0.58 | 1.8% | 5.7% | 12.4% |
| above-break-3 share of FGA | shooting | -0.57 | 5.1% | 13.2% | 29.6% |
| rim share of FGA | shooting | +0.48 | 60.3% | 51.5% | 30.6% |
| OREB% | rebounding | +0.46 | 11.1% | 9.5% | 4.6% |
| pull-up/step-back 3PA per FGA | shooting | -0.36 | 0.5% | 1.1% | 9.3% |
| short-mid share of FGA | shooting | +0.27 | 23.5% | 20.7% | 17.6% |

**Shot-location mix** (share of FGA):

| | rim (restricted area) | short mid (paint, non-RA) | long mid | corner 3 | above-break 3 |
|---|---|---|---|---|---|
| sub-role | 55% | 25% | 10% | 2% | 7% |
| F3 | 46% | 22% | 9% | 6% | 16% |
| league | 29% | 19% | 11% | 11% | 31% |

## F3-S2

**Size:** 57 player-seasons (37.5% of F3 training) · **share of F3 minutes:** 38.1% · **share of league minutes:** 6.6% · median membership probability 1.00, 0% of members under 0.6

**Six most distinguishing features** (largest |within-family z|):

| feature | group | within-family z | sub-role | F3 avg | league avg |
|---|---|---|---|---|---|
| corner-3 share of FGA | shooting | +0.96 | 12.2% | 5.7% | 12.4% |
| above-break-3 share of FGA | shooting | +0.95 | 26.6% | 13.2% | 29.6% |
| rim share of FGA | shooting | -0.80 | 36.8% | 51.5% | 30.6% |
| OREB% | rebounding | -0.76 | 6.8% | 9.5% | 4.6% |
| pull-up/step-back 3PA per FGA | shooting | +0.60 | 2.2% | 1.1% | 9.3% |
| short-mid share of FGA | shooting | -0.44 | 16.2% | 20.7% | 17.6% |

**Shot-location mix** (share of FGA):

| | rim (restricted area) | short mid (paint, non-RA) | long mid | corner 3 | above-break 3 |
|---|---|---|---|---|---|
| sub-role | 34% | 18% | 9% | 10% | 28% |
| F3 | 46% | 22% | 9% | 6% | 16% |
| league | 29% | 19% | 11% | 11% | 31% |
