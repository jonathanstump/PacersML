# Blind sub-role profiles: F2, k = 4 (diag covariance)

No player names in this file. Sub-roles are numbered by size inside the family (S1 = largest); the numbers carry no meaning and are not matched across k.

- Training player-seasons in F2: 281 (top family F2 with probability >= 0.6).
- Members = training player-seasons whose most likely sub-role is this one.
- **within-family z**: members' mean of the feature standardized with F2's own mean and SD.
- Real units: sub-role mean vs F2 average (its training rows) vs league average (all 750 fitted player-seasons).
- Share of league minutes: members' minutes ÷ all players' regular-season minutes in the two seasons.

## F2-S1

**Size:** 89 player-seasons (31.7% of F2 training) · **share of F2 minutes:** 29.3% · **share of league minutes:** 9.7% · median membership probability 1.00, 1% of members under 0.6

**Six most distinguishing features** (largest |within-family z|):

| feature | group | within-family z | sub-role | F2 avg | league avg |
|---|---|---|---|---|---|
| OREB% | rebounding | +0.68 | 5.4% | 4.1% | 4.6% |
| pull-up/step-back 3PA per FGA | shooting | -0.67 | 3.8% | 7.3% | 9.3% |
| rim share of FGA | shooting | +0.61 | 33.5% | 26.4% | 30.6% |
| above-break-3 share of FGA | shooting | -0.59 | 26.0% | 33.9% | 29.6% |
| AST per 100 | creation | -0.48 | 3.2 | 3.9 | 5.2 |
| defensive fouls per 100 | defense | +0.45 | 4.2 | 3.8 | 3.7 |

**Shot-location mix** (share of FGA):

| | rim (restricted area) | short mid (paint, non-RA) | long mid | corner 3 | above-break 3 |
|---|---|---|---|---|---|
| sub-role | 34% | 12% | 6% | 22% | 26% |
| F2 | 27% | 14% | 6% | 19% | 34% |
| league | 29% | 19% | 11% | 11% | 31% |

## F2-S2

**Size:** 67 player-seasons (23.8% of F2 training) · **share of F2 minutes:** 26.2% · **share of league minutes:** 8.7% · median membership probability 1.00, 3% of members under 0.6

**Six most distinguishing features** (largest |within-family z|):

| feature | group | within-family z | sub-role | F2 avg | league avg |
|---|---|---|---|---|---|
| driving FGA per FGA | creation | +1.19 | 28.1% | 18.1% | 20.6% |
| short-mid share of FGA | shooting | +1.14 | 20.7% | 13.5% | 17.6% |
| fouls drawn per 100 | creation | +1.12 | 3.4 | 2.3 | 3.4 |
| assisted share of made FG | creation | -1.07 | 67.1% | 77.3% | 67.1% |
| FTA per FGA | shooting | +0.95 | 0.27 | 0.19 | 0.25 |
| shot attempts + TOV per 100 | creation | +0.79 | 21.2 | 18.4 | 22.0 |

**Shot-location mix** (share of FGA):

| | rim (restricted area) | short mid (paint, non-RA) | long mid | corner 3 | above-break 3 |
|---|---|---|---|---|---|
| sub-role | 34% | 21% | 7% | 13% | 24% |
| F2 | 27% | 14% | 6% | 19% | 34% |
| league | 29% | 19% | 11% | 11% | 31% |

## F2-S3

**Size:** 65 player-seasons (23.1% of F2 training) · **share of F2 minutes:** 23.9% · **share of league minutes:** 8.0% · median membership probability 1.00, 0% of members under 0.6

**Six most distinguishing features** (largest |within-family z|):

| feature | group | within-family z | sub-role | F2 avg | league avg |
|---|---|---|---|---|---|
| OREB% | rebounding | -0.62 | 2.9% | 4.1% | 4.6% |
| pull-up/step-back 3PA per FGA | shooting | +0.56 | 10.2% | 7.3% | 9.3% |
| above-break-3 share of FGA | shooting | +0.51 | 40.9% | 33.9% | 29.6% |
| defensive fouls per 100 | defense | -0.49 | 3.3 | 3.8 | 3.7 |
| rim share of FGA | shooting | -0.46 | 21.1% | 26.4% | 30.6% |
| BLK per 100 | defense | -0.46 | 0.6 | 0.8 | 1.0 |

**Shot-location mix** (share of FGA):

| | rim (restricted area) | short mid (paint, non-RA) | long mid | corner 3 | above-break 3 |
|---|---|---|---|---|---|
| sub-role | 21% | 14% | 7% | 17% | 40% |
| F2 | 27% | 14% | 6% | 19% | 34% |
| league | 29% | 19% | 11% | 11% | 31% |

## F2-S4

**Size:** 60 player-seasons (21.4% of F2 training) · **share of F2 minutes:** 20.6% · **share of league minutes:** 6.8% · median membership probability 1.00, 0% of members under 0.6

**Six most distinguishing features** (largest |within-family z|):

| feature | group | within-family z | sub-role | F2 avg | league avg |
|---|---|---|---|---|---|
| rim share of FGA | shooting | -1.16 | 12.9% | 26.4% | 30.6% |
| above-break-3 share of FGA | shooting | +1.14 | 49.4% | 33.9% | 29.6% |
| driving FGA per FGA | creation | -1.11 | 8.7% | 18.1% | 20.6% |
| assisted share of made FG | creation | +1.11 | 87.8% | 77.3% | 67.1% |
| short-mid share of FGA | shooting | -0.99 | 7.2% | 13.5% | 17.6% |
| FTA per FGA | shooting | -0.81 | 0.13 | 0.19 | 0.25 |

**Shot-location mix** (share of FGA):

| | rim (restricted area) | short mid (paint, non-RA) | long mid | corner 3 | above-break 3 |
|---|---|---|---|---|---|
| sub-role | 13% | 7% | 5% | 23% | 51% |
| F2 | 27% | 14% | 6% | 19% | 34% |
| league | 29% | 19% | 11% | 11% | 31% |
