# Blind sub-role profiles: F3, k = 4 (diag covariance)

No player names in this file. Sub-roles are numbered by size inside the family (S1 = largest); the numbers carry no meaning and are not matched across k.

- Training player-seasons in F3: 152 (top family F3 with probability >= 0.6).
- Members = training player-seasons whose most likely sub-role is this one.
- **within-family z**: members' mean of the feature standardized with F3's own mean and SD.
- Real units: sub-role mean vs F3 average (its training rows) vs league average (all 750 fitted player-seasons).
- Share of league minutes: members' minutes ÷ all players' regular-season minutes in the two seasons.

## F3-S1

**Size:** 54 player-seasons (35.5% of F3 training) · **share of F3 minutes:** 35.3% · **share of league minutes:** 6.1% · median membership probability 1.00, 0% of members under 0.6

**Six most distinguishing features** (largest |within-family z|):

| feature | group | within-family z | sub-role | F3 avg | league avg |
|---|---|---|---|---|---|
| corner-3 share of FGA | shooting | +1.03 | 12.7% | 5.7% | 12.4% |
| above-break-3 share of FGA | shooting | +0.75 | 23.8% | 13.2% | 29.6% |
| FTA per FGA | shooting | -0.63 | 0.25 | 0.34 | 0.25 |
| rim share of FGA | shooting | -0.62 | 40.1% | 51.5% | 30.6% |
| OREB% | rebounding | -0.62 | 7.3% | 9.5% | 4.6% |
| fouls drawn per 100 | creation | -0.60 | 3.3 | 4.3 | 3.4 |

**Shot-location mix** (share of FGA):

| | rim (restricted area) | short mid (paint, non-RA) | long mid | corner 3 | above-break 3 |
|---|---|---|---|---|---|
| sub-role | 37% | 18% | 8% | 11% | 26% |
| F3 | 46% | 22% | 9% | 6% | 16% |
| league | 29% | 19% | 11% | 11% | 31% |

## F3-S2

**Size:** 39 player-seasons (25.7% of F3 training) · **share of F3 minutes:** 23.5% · **share of league minutes:** 4.1% · median membership probability 1.00, 0% of members under 0.6

**Six most distinguishing features** (largest |within-family z|):

| feature | group | within-family z | sub-role | F3 avg | league avg |
|---|---|---|---|---|---|
| rim share of FGA | shooting | +0.99 | 69.6% | 51.5% | 30.6% |
| above-break-3 share of FGA | shooting | -0.91 | 0.3% | 13.2% | 29.6% |
| corner-3 share of FGA | shooting | -0.75 | 0.7% | 5.7% | 12.4% |
| FTA per FGA | shooting | +0.68 | 0.43 | 0.34 | 0.25 |
| OREB% | rebounding | +0.67 | 11.8% | 9.5% | 4.6% |
| pull-up/step-back 3PA per FGA | shooting | -0.62 | 0.0% | 1.1% | 9.3% |

**Shot-location mix** (share of FGA):

| | rim (restricted area) | short mid (paint, non-RA) | long mid | corner 3 | above-break 3 |
|---|---|---|---|---|---|
| sub-role | 68% | 25% | 7% | 0% | 0% |
| F3 | 46% | 22% | 9% | 6% | 16% |
| league | 29% | 19% | 11% | 11% | 31% |

## F3-S3

**Size:** 35 player-seasons (23.0% of F3 training) · **share of F3 minutes:** 21.9% · **share of league minutes:** 3.8% · median membership probability 1.00, 0% of members under 0.6

**Six most distinguishing features** (largest |within-family z|):

| feature | group | within-family z | sub-role | F3 avg | league avg |
|---|---|---|---|---|---|
| above-break-3 share of FGA | shooting | -0.65 | 4.0% | 13.2% | 29.6% |
| OREB% | rebounding | +0.64 | 11.7% | 9.5% | 4.6% |
| corner-3 share of FGA | shooting | -0.57 | 1.9% | 5.7% | 12.4% |
| rim share of FGA | shooting | +0.45 | 59.6% | 51.5% | 30.6% |
| pull-up/step-back 3PA per FGA | shooting | -0.41 | 0.4% | 1.1% | 9.3% |
| DREB% | rebounding | +0.38 | 21.1% | 19.3% | 13.1% |

**Shot-location mix** (share of FGA):

| | rim (restricted area) | short mid (paint, non-RA) | long mid | corner 3 | above-break 3 |
|---|---|---|---|---|---|
| sub-role | 58% | 26% | 11% | 2% | 4% |
| F3 | 46% | 22% | 9% | 6% | 16% |
| league | 29% | 19% | 11% | 11% | 31% |

## F3-S4

**Size:** 24 player-seasons (15.8% of F3 training) · **share of F3 minutes:** 19.2% · **share of league minutes:** 3.3% · median membership probability 1.00, 0% of members under 0.6

**Six most distinguishing features** (largest |within-family z|):

| feature | group | within-family z | sub-role | F3 avg | league avg |
|---|---|---|---|---|---|
| shot attempts + TOV per 100 | creation | +1.63 | 29.3 | 19.9 | 22.0 |
| fouls drawn per 100 | creation | +1.41 | 6.7 | 4.3 | 3.4 |
| pull-up/step-back 3PA per FGA | shooting | +1.40 | 3.6% | 1.1% | 9.3% |
| driving FGA per FGA | creation | +0.97 | 21.9% | 13.9% | 20.6% |
| AST per 100 | creation | +0.95 | 5.1 | 3.7 | 5.2 |
| rim share of FGA | shooting | -0.87 | 35.5% | 51.5% | 30.6% |

**Shot-location mix** (share of FGA):

| | rim (restricted area) | short mid (paint, non-RA) | long mid | corner 3 | above-break 3 |
|---|---|---|---|---|---|
| sub-role | 36% | 25% | 12% | 4% | 23% |
| F3 | 46% | 22% | 9% | 6% | 16% |
| league | 29% | 19% | 11% | 11% | 31% |
