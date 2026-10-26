# Blind sub-role profiles: F1, k = 4 (diag covariance)

No player names in this file. Sub-roles are numbered by size inside the family (S1 = largest); the numbers carry no meaning and are not matched across k.

- Training player-seasons in F1: 303 (top family F1 with probability >= 0.6).
- Members = training player-seasons whose most likely sub-role is this one.
- **within-family z**: members' mean of the feature standardized with F1's own mean and SD.
- Real units: sub-role mean vs F1 average (its training rows) vs league average (all 750 fitted player-seasons).
- Share of league minutes: members' minutes ÷ all players' regular-season minutes in the two seasons.

## F1-S1

**Size:** 107 player-seasons (35.3% of F1 training) · **share of F1 minutes:** 32.4% · **share of league minutes:** 13.3% · median membership probability 1.00, 2% of members under 0.6

**Six most distinguishing features** (largest |within-family z|):

| feature | group | within-family z | sub-role | F1 avg | league avg |
|---|---|---|---|---|---|
| DREB% | rebounding | -0.43 | 9.7% | 11.4% | 13.1% |
| defensive fouls per 100 | defense | +0.32 | 3.5 | 3.2 | 3.7 |
| OREB% | rebounding | -0.32 | 2.3% | 2.8% | 4.6% |
| FTA per FGA | shooting | -0.31 | 0.22 | 0.25 | 0.25 |
| fouls drawn per 100 | creation | -0.31 | 3.5 | 4.1 | 3.4 |
| pull-up/step-back 3PA per FGA | shooting | +0.23 | 17.3% | 15.3% | 9.3% |

**Shot-location mix** (share of FGA):

| | rim (restricted area) | short mid (paint, non-RA) | long mid | corner 3 | above-break 3 |
|---|---|---|---|---|---|
| sub-role | 23% | 19% | 13% | 8% | 37% |
| F1 | 24% | 20% | 15% | 8% | 34% |
| league | 29% | 19% | 11% | 11% | 31% |

## F1-S2

**Size:** 82 player-seasons (27.1% of F1 training) · **share of F1 minutes:** 27.2% · **share of league minutes:** 11.2% · median membership probability 1.00, 2% of members under 0.6

**Six most distinguishing features** (largest |within-family z|):

| feature | group | within-family z | sub-role | F1 avg | league avg |
|---|---|---|---|---|---|
| above-break-3 share of FGA | shooting | -1.04 | 20.5% | 33.5% | 29.6% |
| pull-up/step-back 3PA per FGA | shooting | -1.04 | 5.9% | 15.3% | 9.3% |
| OREB% | rebounding | +0.99 | 4.3% | 2.8% | 4.6% |
| rim share of FGA | shooting | +0.91 | 33.7% | 24.2% | 30.6% |
| DREB% | rebounding | +0.79 | 14.5% | 11.4% | 13.1% |
| FTA per FGA | shooting | +0.71 | 0.33 | 0.25 | 0.25 |

**Shot-location mix** (share of FGA):

| | rim (restricted area) | short mid (paint, non-RA) | long mid | corner 3 | above-break 3 |
|---|---|---|---|---|---|
| sub-role | 32% | 24% | 16% | 7% | 21% |
| F1 | 24% | 20% | 15% | 8% | 34% |
| league | 29% | 19% | 11% | 11% | 31% |

## F1-S3

**Size:** 58 player-seasons (19.1% of F1 training) · **share of F1 minutes:** 18.0% · **share of league minutes:** 7.4% · median membership probability 1.00, 5% of members under 0.6

**Six most distinguishing features** (largest |within-family z|):

| feature | group | within-family z | sub-role | F1 avg | league avg |
|---|---|---|---|---|---|
| corner-3 share of FGA | shooting | +1.29 | 14.7% | 8.5% | 12.4% |
| fouls drawn per 100 | creation | -1.09 | 1.9 | 4.1 | 3.4 |
| assisted share of made FG | creation | +1.09 | 69.6% | 54.4% | 67.1% |
| driving FGA per FGA | creation | -1.07 | 15.0% | 26.1% | 20.6% |
| FTA per FGA | shooting | -1.01 | 0.14 | 0.25 | 0.25 |
| short-mid share of FGA | shooting | -0.96 | 12.5% | 20.0% | 17.6% |

**Shot-location mix** (share of FGA):

| | rim (restricted area) | short mid (paint, non-RA) | long mid | corner 3 | above-break 3 |
|---|---|---|---|---|---|
| sub-role | 15% | 13% | 14% | 14% | 44% |
| F1 | 24% | 20% | 15% | 8% | 34% |
| league | 29% | 19% | 11% | 11% | 31% |

## F1-S4

**Size:** 56 player-seasons (18.5% of F1 training) · **share of F1 minutes:** 22.3% · **share of league minutes:** 9.2% · median membership probability 1.00, 4% of members under 0.6

**Six most distinguishing features** (largest |within-family z|):

| feature | group | within-family z | sub-role | F1 avg | league avg |
|---|---|---|---|---|---|
| shot attempts + TOV per 100 | creation | +1.27 | 34.0 | 26.4 | 22.0 |
| fouls drawn per 100 | creation | +1.01 | 6.1 | 4.1 | 3.4 |
| assisted share of made FG | creation | -0.99 | 40.6% | 54.4% | 67.1% |
| corner-3 share of FGA | shooting | -0.86 | 4.4% | 8.5% | 12.4% |
| pull-up/step-back 3PA per FGA | shooting | +0.84 | 22.9% | 15.3% | 9.3% |
| AST per 100 | creation | +0.60 | 8.8 | 7.1 | 5.2 |

**Shot-location mix** (share of FGA):

| | rim (restricted area) | short mid (paint, non-RA) | long mid | corner 3 | above-break 3 |
|---|---|---|---|---|---|
| sub-role | 22% | 21% | 16% | 4% | 36% |
| F1 | 24% | 20% | 15% | 8% | 34% |
| league | 29% | 19% | 11% | 11% | 31% |
