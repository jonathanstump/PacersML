# Blind sub-role profiles: F1, k = 3 (diag covariance)

No player names in this file. Sub-roles are numbered by size inside the family (S1 = largest); the numbers carry no meaning and are not matched across k.

- Training player-seasons in F1: 303 (top family F1 with probability >= 0.6).
- Members = training player-seasons whose most likely sub-role is this one.
- **within-family z**: members' mean of the feature standardized with F1's own mean and SD.
- Real units: sub-role mean vs F1 average (its training rows) vs league average (all 750 fitted player-seasons).
- Share of league minutes: members' minutes ÷ all players' regular-season minutes in the two seasons.

## F1-S1

**Size:** 117 player-seasons (38.6% of F1 training) · **share of F1 minutes:** 42.2% · **share of league minutes:** 17.3% · median membership probability 1.00, 3% of members under 0.6

**Six most distinguishing features** (largest |within-family z|):

| feature | group | within-family z | sub-role | F1 avg | league avg |
|---|---|---|---|---|---|
| assisted share of made FG | creation | -0.69 | 44.7% | 54.4% | 67.1% |
| pull-up/step-back 3PA per FGA | shooting | +0.61 | 20.8% | 15.3% | 9.3% |
| corner-3 share of FGA | shooting | -0.59 | 5.7% | 8.5% | 12.4% |
| shot attempts + TOV per 100 | creation | +0.56 | 29.7 | 26.4 | 22.0 |
| OREB% | rebounding | -0.45 | 2.1% | 2.8% | 4.6% |
| AST per 100 | creation | +0.44 | 8.3 | 7.1 | 5.2 |

**Shot-location mix** (share of FGA):

| | rim (restricted area) | short mid (paint, non-RA) | long mid | corner 3 | above-break 3 |
|---|---|---|---|---|---|
| sub-role | 22% | 21% | 15% | 5% | 37% |
| F1 | 24% | 20% | 15% | 8% | 34% |
| league | 29% | 19% | 11% | 11% | 31% |

## F1-S2

**Size:** 95 player-seasons (31.4% of F1 training) · **share of F1 minutes:** 30.0% · **share of league minutes:** 12.3% · median membership probability 1.00, 1% of members under 0.6

**Six most distinguishing features** (largest |within-family z|):

| feature | group | within-family z | sub-role | F1 avg | league avg |
|---|---|---|---|---|---|
| pull-up/step-back 3PA per FGA | shooting | -0.98 | 6.5% | 15.3% | 9.3% |
| above-break-3 share of FGA | shooting | -0.98 | 21.3% | 33.5% | 29.6% |
| rim share of FGA | shooting | +0.89 | 33.5% | 24.2% | 30.6% |
| OREB% | rebounding | +0.86 | 4.1% | 2.8% | 4.6% |
| DREB% | rebounding | +0.61 | 13.8% | 11.4% | 13.1% |
| short-mid share of FGA | shooting | +0.56 | 24.3% | 20.0% | 17.6% |

**Shot-location mix** (share of FGA):

| | rim (restricted area) | short mid (paint, non-RA) | long mid | corner 3 | above-break 3 |
|---|---|---|---|---|---|
| sub-role | 33% | 24% | 15% | 7% | 22% |
| F1 | 24% | 20% | 15% | 8% | 34% |
| league | 29% | 19% | 11% | 11% | 31% |

## F1-S3

**Size:** 91 player-seasons (30.0% of F1 training) · **share of F1 minutes:** 27.8% · **share of league minutes:** 11.4% · median membership probability 1.00, 1% of members under 0.6

**Six most distinguishing features** (largest |within-family z|):

| feature | group | within-family z | sub-role | F1 avg | league avg |
|---|---|---|---|---|---|
| corner-3 share of FGA | shooting | +0.96 | 13.1% | 8.5% | 12.4% |
| driving FGA per FGA | creation | -0.85 | 17.3% | 26.1% | 20.6% |
| assisted share of made FG | creation | +0.85 | 66.2% | 54.4% | 67.1% |
| fouls drawn per 100 | creation | -0.82 | 2.5 | 4.1 | 3.4 |
| FTA per FGA | shooting | -0.77 | 0.17 | 0.25 | 0.25 |
| short-mid share of FGA | shooting | -0.76 | 14.1% | 20.0% | 17.6% |

**Shot-location mix** (share of FGA):

| | rim (restricted area) | short mid (paint, non-RA) | long mid | corner 3 | above-break 3 |
|---|---|---|---|---|---|
| sub-role | 17% | 14% | 14% | 13% | 43% |
| F1 | 24% | 20% | 15% | 8% | 34% |
| league | 29% | 19% | 11% | 11% | 31% |
