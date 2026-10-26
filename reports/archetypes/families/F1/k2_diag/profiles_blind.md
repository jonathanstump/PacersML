# Blind sub-role profiles: F1, k = 2 (diag covariance)

No player names in this file. Sub-roles are numbered by size inside the family (S1 = largest); the numbers carry no meaning and are not matched across k.

- Training player-seasons in F1: 303 (top family F1 with probability >= 0.6).
- Members = training player-seasons whose most likely sub-role is this one.
- **within-family z**: members' mean of the feature standardized with F1's own mean and SD.
- Real units: sub-role mean vs F1 average (its training rows) vs league average (all 750 fitted player-seasons).
- Share of league minutes: members' minutes ÷ all players' regular-season minutes in the two seasons.

## F1-S1

**Size:** 165 player-seasons (54.5% of F1 training) · **share of F1 minutes:** 58.0% · **share of league minutes:** 23.8% · median membership probability 1.00, 2% of members under 0.6

**Six most distinguishing features** (largest |within-family z|):

| feature | group | within-family z | sub-role | F1 avg | league avg |
|---|---|---|---|---|---|
| fouls drawn per 100 | creation | +0.62 | 5.4 | 4.1 | 3.4 |
| corner-3 share of FGA | shooting | -0.57 | 5.8% | 8.5% | 12.4% |
| FTA per FGA | shooting | +0.54 | 0.31 | 0.25 | 0.25 |
| shot attempts + TOV per 100 | creation | +0.53 | 29.5 | 26.4 | 22.0 |
| assisted share of made FG | creation | -0.49 | 47.6% | 54.4% | 67.1% |
| driving FGA per FGA | creation | +0.46 | 30.9% | 26.1% | 20.6% |

**Shot-location mix** (share of FGA):

| | rim (restricted area) | short mid (paint, non-RA) | long mid | corner 3 | above-break 3 |
|---|---|---|---|---|---|
| sub-role | 27% | 23% | 15% | 5% | 30% |
| F1 | 24% | 20% | 15% | 8% | 34% |
| league | 29% | 19% | 11% | 11% | 31% |

## F1-S2

**Size:** 138 player-seasons (45.5% of F1 training) · **share of F1 minutes:** 42.0% · **share of league minutes:** 17.2% · median membership probability 1.00, 4% of members under 0.6

**Six most distinguishing features** (largest |within-family z|):

| feature | group | within-family z | sub-role | F1 avg | league avg |
|---|---|---|---|---|---|
| fouls drawn per 100 | creation | -0.75 | 2.6 | 4.1 | 3.4 |
| corner-3 share of FGA | shooting | +0.68 | 11.8% | 8.5% | 12.4% |
| FTA per FGA | shooting | -0.65 | 0.18 | 0.25 | 0.25 |
| shot attempts + TOV per 100 | creation | -0.63 | 22.6 | 26.4 | 22.0 |
| assisted share of made FG | creation | +0.58 | 62.5% | 54.4% | 67.1% |
| driving FGA per FGA | creation | -0.55 | 20.5% | 26.1% | 20.6% |

**Shot-location mix** (share of FGA):

| | rim (restricted area) | short mid (paint, non-RA) | long mid | corner 3 | above-break 3 |
|---|---|---|---|---|---|
| sub-role | 19% | 16% | 14% | 11% | 40% |
| F1 | 24% | 20% | 15% | 8% | 34% |
| league | 29% | 19% | 11% | 11% | 31% |
