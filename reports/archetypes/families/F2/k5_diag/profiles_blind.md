# Blind sub-role profiles: F2, k = 5 (diag covariance)

No player names in this file. Sub-roles are numbered by size inside the family (S1 = largest); the numbers carry no meaning and are not matched across k.

- Training player-seasons in F2: 281 (top family F2 with probability >= 0.6).
- Members = training player-seasons whose most likely sub-role is this one.
- **within-family z**: members' mean of the feature standardized with F2's own mean and SD.
- Real units: sub-role mean vs F2 average (its training rows) vs league average (all 750 fitted player-seasons).
- Share of league minutes: members' minutes ÷ all players' regular-season minutes in the two seasons.

## F2-S1

**Size:** 64 player-seasons (22.8% of F2 training) · **share of F2 minutes:** 21.7% · **share of league minutes:** 7.2% · median membership probability 0.99, 11% of members under 0.6

**Six most distinguishing features** (largest |within-family z|):

| feature | group | within-family z | sub-role | F2 avg | league avg |
|---|---|---|---|---|---|
| driving FGA per FGA | creation | +0.66 | 23.6% | 18.1% | 20.6% |
| assisted share of made FG | creation | -0.58 | 71.7% | 77.3% | 67.1% |
| charges drawn per 100 | defense | +0.57 | 0.2 | 0.1 | 0.1 |
| short-mid share of FGA | shooting | +0.49 | 16.6% | 13.5% | 17.6% |
| STL per 100 | defense | +0.45 | 2.1 | 1.8 | 1.7 |
| FTA per FGA | shooting | +0.41 | 0.23 | 0.19 | 0.25 |

**Shot-location mix** (share of FGA):

| | rim (restricted area) | short mid (paint, non-RA) | long mid | corner 3 | above-break 3 |
|---|---|---|---|---|---|
| sub-role | 29% | 17% | 7% | 17% | 30% |
| F2 | 27% | 14% | 6% | 19% | 34% |
| league | 29% | 19% | 11% | 11% | 31% |

## F2-S2

**Size:** 62 player-seasons (22.1% of F2 training) · **share of F2 minutes:** 21.3% · **share of league minutes:** 7.1% · median membership probability 1.00, 0% of members under 0.6

**Six most distinguishing features** (largest |within-family z|):

| feature | group | within-family z | sub-role | F2 avg | league avg |
|---|---|---|---|---|---|
| rim share of FGA | shooting | -1.13 | 13.3% | 26.4% | 30.6% |
| driving FGA per FGA | creation | -1.12 | 8.6% | 18.1% | 20.6% |
| above-break-3 share of FGA | shooting | +1.11 | 48.9% | 33.9% | 29.6% |
| assisted share of made FG | creation | +1.10 | 87.7% | 77.3% | 67.1% |
| short-mid share of FGA | shooting | -0.99 | 7.2% | 13.5% | 17.6% |
| fouls drawn per 100 | creation | -0.79 | 1.5 | 2.3 | 3.4 |

**Shot-location mix** (share of FGA):

| | rim (restricted area) | short mid (paint, non-RA) | long mid | corner 3 | above-break 3 |
|---|---|---|---|---|---|
| sub-role | 13% | 7% | 5% | 23% | 51% |
| F2 | 27% | 14% | 6% | 19% | 34% |
| league | 29% | 19% | 11% | 11% | 31% |

## F2-S3

**Size:** 61 player-seasons (21.7% of F2 training) · **share of F2 minutes:** 22.8% · **share of league minutes:** 7.6% · median membership probability 0.99, 5% of members under 0.6

**Six most distinguishing features** (largest |within-family z|):

| feature | group | within-family z | sub-role | F2 avg | league avg |
|---|---|---|---|---|---|
| OREB% | rebounding | -0.68 | 2.8% | 4.1% | 4.6% |
| pull-up/step-back 3PA per FGA | shooting | +0.54 | 10.1% | 7.3% | 9.3% |
| defensive fouls per 100 | defense | -0.53 | 3.3 | 3.8 | 3.7 |
| above-break-3 share of FGA | shooting | +0.52 | 40.9% | 33.9% | 29.6% |
| rim share of FGA | shooting | -0.52 | 20.5% | 26.4% | 30.6% |
| BLK per 100 | defense | -0.47 | 0.6 | 0.8 | 1.0 |

**Shot-location mix** (share of FGA):

| | rim (restricted area) | short mid (paint, non-RA) | long mid | corner 3 | above-break 3 |
|---|---|---|---|---|---|
| sub-role | 21% | 14% | 7% | 17% | 40% |
| F2 | 27% | 14% | 6% | 19% | 34% |
| league | 29% | 19% | 11% | 11% | 31% |

## F2-S4

**Size:** 58 player-seasons (20.6% of F2 training) · **share of F2 minutes:** 18.5% · **share of league minutes:** 6.2% · median membership probability 1.00, 2% of members under 0.6

**Six most distinguishing features** (largest |within-family z|):

| feature | group | within-family z | sub-role | F2 avg | league avg |
|---|---|---|---|---|---|
| OREB% | rebounding | +0.88 | 5.8% | 4.1% | 4.6% |
| pull-up/step-back 3PA per FGA | shooting | -0.82 | 3.0% | 7.3% | 9.3% |
| rim share of FGA | shooting | +0.75 | 35.2% | 26.4% | 30.6% |
| above-break-3 share of FGA | shooting | -0.66 | 25.0% | 33.9% | 29.6% |
| AST per 100 | creation | -0.63 | 3.0 | 3.9 | 5.2 |
| BLK per 100 | defense | +0.57 | 1.0 | 0.8 | 1.0 |

**Shot-location mix** (share of FGA):

| | rim (restricted area) | short mid (paint, non-RA) | long mid | corner 3 | above-break 3 |
|---|---|---|---|---|---|
| sub-role | 35% | 11% | 5% | 23% | 25% |
| F2 | 27% | 14% | 6% | 19% | 34% |
| league | 29% | 19% | 11% | 11% | 31% |

## F2-S5

**Size:** 36 player-seasons (12.8% of F2 training) · **share of F2 minutes:** 15.7% · **share of league minutes:** 5.2% · median membership probability 1.00, 0% of members under 0.6

**Six most distinguishing features** (largest |within-family z|):

| feature | group | within-family z | sub-role | F2 avg | league avg |
|---|---|---|---|---|---|
| driving FGA per FGA | creation | +1.37 | 29.7% | 18.1% | 20.6% |
| assisted share of made FG | creation | -1.34 | 64.6% | 77.3% | 67.1% |
| fouls drawn per 100 | creation | +1.33 | 3.6 | 2.3 | 3.4 |
| short-mid share of FGA | shooting | +1.30 | 21.7% | 13.5% | 17.6% |
| shot attempts + TOV per 100 | creation | +1.12 | 22.3 | 18.4 | 22.0 |
| rim share of FGA | shooting | +1.10 | 39.3% | 26.4% | 30.6% |

**Shot-location mix** (share of FGA):

| | rim (restricted area) | short mid (paint, non-RA) | long mid | corner 3 | above-break 3 |
|---|---|---|---|---|---|
| sub-role | 39% | 22% | 7% | 12% | 20% |
| F2 | 27% | 14% | 6% | 19% | 34% |
| league | 29% | 19% | 11% | 11% | 31% |
