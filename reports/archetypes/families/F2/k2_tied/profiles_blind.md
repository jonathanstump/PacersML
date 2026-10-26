# Blind sub-role profiles: F2, k = 2 (tied covariance)

No player names in this file. Sub-roles are numbered by size inside the family (S1 = largest); the numbers carry no meaning and are not matched across k.

- Training player-seasons in F2: 281 (top family F2 with probability >= 0.6).
- Members = training player-seasons whose most likely sub-role is this one.
- **within-family z**: members' mean of the feature standardized with F2's own mean and SD.
- Real units: sub-role mean vs F2 average (its training rows) vs league average (all 750 fitted player-seasons).
- Share of league minutes: members' minutes ÷ all players' regular-season minutes in the two seasons.

## F2-S1

**Size:** 146 player-seasons (52.0% of F2 training) · **share of F2 minutes:** 53.0% · **share of league minutes:** 17.6% · median membership probability 0.98, 3% of members under 0.6

**Six most distinguishing features** (largest |within-family z|):

| feature | group | within-family z | sub-role | F2 avg | league avg |
|---|---|---|---|---|---|
| rim share of FGA | shooting | +0.72 | 34.8% | 26.4% | 30.6% |
| above-break-3 share of FGA | shooting | -0.64 | 25.3% | 33.9% | 29.6% |
| assisted share of made FG | creation | -0.55 | 72.0% | 77.3% | 67.1% |
| driving FGA per FGA | creation | +0.47 | 22.0% | 18.1% | 20.6% |
| OREB% | rebounding | +0.44 | 4.9% | 4.1% | 4.6% |
| fouls drawn per 100 | creation | +0.41 | 2.7 | 2.3 | 3.4 |

**Shot-location mix** (share of FGA):

| | rim (restricted area) | short mid (paint, non-RA) | long mid | corner 3 | above-break 3 |
|---|---|---|---|---|---|
| sub-role | 35% | 16% | 7% | 16% | 26% |
| F2 | 27% | 14% | 6% | 19% | 34% |
| league | 29% | 19% | 11% | 11% | 31% |

## F2-S2

**Size:** 135 player-seasons (48.0% of F2 training) · **share of F2 minutes:** 47.0% · **share of league minutes:** 15.6% · median membership probability 0.98, 4% of members under 0.6

**Six most distinguishing features** (largest |within-family z|):

| feature | group | within-family z | sub-role | F2 avg | league avg |
|---|---|---|---|---|---|
| rim share of FGA | shooting | -0.78 | 17.4% | 26.4% | 30.6% |
| above-break-3 share of FGA | shooting | +0.69 | 43.3% | 33.9% | 29.6% |
| assisted share of made FG | creation | +0.60 | 82.9% | 77.3% | 67.1% |
| driving FGA per FGA | creation | -0.51 | 13.8% | 18.1% | 20.6% |
| OREB% | rebounding | -0.48 | 3.2% | 4.1% | 4.6% |
| fouls drawn per 100 | creation | -0.45 | 1.9 | 2.3 | 3.4 |

**Shot-location mix** (share of FGA):

| | rim (restricted area) | short mid (paint, non-RA) | long mid | corner 3 | above-break 3 |
|---|---|---|---|---|---|
| sub-role | 17% | 12% | 6% | 21% | 44% |
| F2 | 27% | 14% | 6% | 19% | 34% |
| league | 29% | 19% | 11% | 11% | 31% |
