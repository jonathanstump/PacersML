# Blind sub-role profiles: F2, k = 3 (diag covariance)

No player names in this file. Sub-roles are numbered by size inside the family (S1 = largest); the numbers carry no meaning and are not matched across k.

- Training player-seasons in F2: 281 (top family F2 with probability >= 0.6).
- Members = training player-seasons whose most likely sub-role is this one.
- **within-family z**: members' mean of the feature standardized with F2's own mean and SD.
- Real units: sub-role mean vs F2 average (its training rows) vs league average (all 750 fitted player-seasons).
- Share of league minutes: members' minutes ÷ all players' regular-season minutes in the two seasons.

## F2-S1

**Size:** 110 player-seasons (39.1% of F2 training) · **share of F2 minutes:** 38.6% · **share of league minutes:** 12.8% · median membership probability 1.00, 2% of members under 0.6

**Six most distinguishing features** (largest |within-family z|):

| feature | group | within-family z | sub-role | F2 avg | league avg |
|---|---|---|---|---|---|
| rim share of FGA | shooting | -0.93 | 15.6% | 26.4% | 30.6% |
| above-break-3 share of FGA | shooting | +0.93 | 46.5% | 33.9% | 29.6% |
| assisted share of made FG | creation | +0.67 | 83.7% | 77.3% | 67.1% |
| driving FGA per FGA | creation | -0.66 | 12.5% | 18.1% | 20.6% |
| pull-up/step-back 3PA per FGA | shooting | +0.61 | 10.5% | 7.3% | 9.3% |
| OREB% | rebounding | -0.60 | 2.9% | 4.1% | 4.6% |

**Shot-location mix** (share of FGA):

| | rim (restricted area) | short mid (paint, non-RA) | long mid | corner 3 | above-break 3 |
|---|---|---|---|---|---|
| sub-role | 16% | 10% | 6% | 20% | 47% |
| F2 | 27% | 14% | 6% | 19% | 34% |
| league | 29% | 19% | 11% | 11% | 31% |

## F2-S2

**Size:** 95 player-seasons (33.8% of F2 training) · **share of F2 minutes:** 31.6% · **share of league minutes:** 10.5% · median membership probability 1.00, 2% of members under 0.6

**Six most distinguishing features** (largest |within-family z|):

| feature | group | within-family z | sub-role | F2 avg | league avg |
|---|---|---|---|---|---|
| pull-up/step-back 3PA per FGA | shooting | -0.63 | 4.0% | 7.3% | 9.3% |
| OREB% | rebounding | +0.62 | 5.3% | 4.1% | 4.6% |
| rim share of FGA | shooting | +0.60 | 33.5% | 26.4% | 30.6% |
| above-break-3 share of FGA | shooting | -0.57 | 26.3% | 33.9% | 29.6% |
| AST per 100 | creation | -0.45 | 3.2 | 3.9 | 5.2 |
| defensive fouls per 100 | defense | +0.41 | 4.2 | 3.8 | 3.7 |

**Shot-location mix** (share of FGA):

| | rim (restricted area) | short mid (paint, non-RA) | long mid | corner 3 | above-break 3 |
|---|---|---|---|---|---|
| sub-role | 33% | 12% | 6% | 22% | 27% |
| F2 | 27% | 14% | 6% | 19% | 34% |
| league | 29% | 19% | 11% | 11% | 31% |

## F2-S3

**Size:** 76 player-seasons (27.0% of F2 training) · **share of F2 minutes:** 29.8% · **share of league minutes:** 9.9% · median membership probability 1.00, 3% of members under 0.6

**Six most distinguishing features** (largest |within-family z|):

| feature | group | within-family z | sub-role | F2 avg | league avg |
|---|---|---|---|---|---|
| driving FGA per FGA | creation | +1.15 | 27.8% | 18.1% | 20.6% |
| short-mid share of FGA | shooting | +1.07 | 20.2% | 13.5% | 17.6% |
| assisted share of made FG | creation | -1.02 | 67.6% | 77.3% | 67.1% |
| fouls drawn per 100 | creation | +1.02 | 3.3 | 2.3 | 3.4 |
| FTA per FGA | shooting | +0.83 | 0.26 | 0.19 | 0.25 |
| shot attempts + TOV per 100 | creation | +0.77 | 21.1 | 18.4 | 22.0 |

**Shot-location mix** (share of FGA):

| | rim (restricted area) | short mid (paint, non-RA) | long mid | corner 3 | above-break 3 |
|---|---|---|---|---|---|
| sub-role | 33% | 21% | 7% | 13% | 26% |
| F2 | 27% | 14% | 6% | 19% | 34% |
| league | 29% | 19% | 11% | 11% | 31% |
