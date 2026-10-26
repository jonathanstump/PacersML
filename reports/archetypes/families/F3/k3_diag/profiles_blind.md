# Blind sub-role profiles: F3, k = 3 (diag covariance)

No player names in this file. Sub-roles are numbered by size inside the family (S1 = largest); the numbers carry no meaning and are not matched across k.

- Training player-seasons in F3: 152 (top family F3 with probability >= 0.6).
- Members = training player-seasons whose most likely sub-role is this one.
- **within-family z**: members' mean of the feature standardized with F3's own mean and SD.
- Real units: sub-role mean vs F3 average (its training rows) vs league average (all 750 fitted player-seasons).
- Share of league minutes: members' minutes ÷ all players' regular-season minutes in the two seasons.

## F3-S1

**Size:** 61 player-seasons (40.1% of F3 training) · **share of F3 minutes:** 39.6% · **share of league minutes:** 6.9% · median membership probability 1.00, 0% of members under 0.6

**Six most distinguishing features** (largest |within-family z|):

| feature | group | within-family z | sub-role | F3 avg | league avg |
|---|---|---|---|---|---|
| corner-3 share of FGA | shooting | +0.86 | 11.6% | 5.7% | 12.4% |
| above-break-3 share of FGA | shooting | +0.63 | 22.1% | 13.2% | 29.6% |
| FTA per FGA | shooting | -0.61 | 0.26 | 0.34 | 0.25 |
| fouls drawn per 100 | creation | -0.58 | 3.3 | 4.3 | 3.4 |
| rim share of FGA | shooting | -0.54 | 41.5% | 51.5% | 30.6% |
| DREB% | rebounding | -0.50 | 16.9% | 19.3% | 13.1% |

**Shot-location mix** (share of FGA):

| | rim (restricted area) | short mid (paint, non-RA) | long mid | corner 3 | above-break 3 |
|---|---|---|---|---|---|
| sub-role | 38% | 19% | 8% | 11% | 25% |
| F3 | 46% | 22% | 9% | 6% | 16% |
| league | 29% | 19% | 11% | 11% | 31% |

## F3-S2

**Size:** 61 player-seasons (40.1% of F3 training) · **share of F3 minutes:** 37.9% · **share of league minutes:** 6.6% · median membership probability 1.00, 2% of members under 0.6

**Six most distinguishing features** (largest |within-family z|):

| feature | group | within-family z | sub-role | F3 avg | league avg |
|---|---|---|---|---|---|
| rim share of FGA | shooting | +0.87 | 67.4% | 51.5% | 30.6% |
| above-break-3 share of FGA | shooting | -0.87 | 0.9% | 13.2% | 29.6% |
| corner-3 share of FGA | shooting | -0.70 | 1.0% | 5.7% | 12.4% |
| OREB% | rebounding | +0.65 | 11.7% | 9.5% | 4.6% |
| shot attempts + TOV per 100 | creation | -0.57 | 16.6 | 19.9 | 22.0 |
| FTA per FGA | shooting | +0.57 | 0.41 | 0.34 | 0.25 |

**Shot-location mix** (share of FGA):

| | rim (restricted area) | short mid (paint, non-RA) | long mid | corner 3 | above-break 3 |
|---|---|---|---|---|---|
| sub-role | 66% | 24% | 8% | 1% | 1% |
| F3 | 46% | 22% | 9% | 6% | 16% |
| league | 29% | 19% | 11% | 11% | 31% |

## F3-S3

**Size:** 30 player-seasons (19.7% of F3 training) · **share of F3 minutes:** 22.5% · **share of league minutes:** 3.9% · median membership probability 1.00, 0% of members under 0.6

**Six most distinguishing features** (largest |within-family z|):

| feature | group | within-family z | sub-role | F3 avg | league avg |
|---|---|---|---|---|---|
| shot attempts + TOV per 100 | creation | +1.46 | 28.3 | 19.9 | 22.0 |
| fouls drawn per 100 | creation | +1.31 | 6.5 | 4.3 | 3.4 |
| pull-up/step-back 3PA per FGA | shooting | +1.05 | 3.0% | 1.1% | 9.3% |
| AST per 100 | creation | +0.97 | 5.1 | 3.7 | 5.2 |
| driving FGA per FGA | creation | +0.92 | 21.5% | 13.9% | 20.6% |
| DREB% | rebounding | +0.71 | 22.7% | 19.3% | 13.1% |

**Shot-location mix** (share of FGA):

| | rim (restricted area) | short mid (paint, non-RA) | long mid | corner 3 | above-break 3 |
|---|---|---|---|---|---|
| sub-role | 38% | 25% | 13% | 4% | 21% |
| F3 | 46% | 22% | 9% | 6% | 16% |
| league | 29% | 19% | 11% | 11% | 31% |
