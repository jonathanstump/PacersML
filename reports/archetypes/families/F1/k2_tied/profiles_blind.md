# Blind sub-role profiles: F1, k = 2 (tied covariance)

No player names in this file. Sub-roles are numbered by size inside the family (S1 = largest); the numbers carry no meaning and are not matched across k.

- Training player-seasons in F1: 303 (top family F1 with probability >= 0.6).
- Members = training player-seasons whose most likely sub-role is this one.
- **within-family z**: members' mean of the feature standardized with F1's own mean and SD.
- Real units: sub-role mean vs F1 average (its training rows) vs league average (all 750 fitted player-seasons).
- Share of league minutes: members' minutes ÷ all players' regular-season minutes in the two seasons.

## F1-S1

**Size:** 207 player-seasons (68.3% of F1 training) · **share of F1 minutes:** 63.4% · **share of league minutes:** 26.0% · median membership probability 1.00, 1% of members under 0.6

**Six most distinguishing features** (largest |within-family z|):

| feature | group | within-family z | sub-role | F1 avg | league avg |
|---|---|---|---|---|---|
| short-mid share of FGA | shooting | -0.37 | 17.1% | 20.0% | 17.6% |
| fouls drawn per 100 | creation | -0.34 | 3.4 | 4.1 | 3.4 |
| FTA per FGA | shooting | -0.30 | 0.22 | 0.25 | 0.25 |
| corner-3 share of FGA | shooting | +0.28 | 9.9% | 8.5% | 12.4% |
| shot attempts + TOV per 100 | creation | -0.28 | 24.7 | 26.4 | 22.0 |
| above-break-3 share of FGA | shooting | +0.27 | 36.9% | 33.5% | 29.6% |

**Shot-location mix** (share of FGA):

| | rim (restricted area) | short mid (paint, non-RA) | long mid | corner 3 | above-break 3 |
|---|---|---|---|---|---|
| sub-role | 23% | 17% | 13% | 9% | 38% |
| F1 | 24% | 20% | 15% | 8% | 34% |
| league | 29% | 19% | 11% | 11% | 31% |

## F1-S2

**Size:** 96 player-seasons (31.7% of F1 training) · **share of F1 minutes:** 36.6% · **share of league minutes:** 15.0% · median membership probability 0.99, 2% of members under 0.6

**Six most distinguishing features** (largest |within-family z|):

| feature | group | within-family z | sub-role | F1 avg | league avg |
|---|---|---|---|---|---|
| short-mid share of FGA | shooting | +0.81 | 26.2% | 20.0% | 17.6% |
| fouls drawn per 100 | creation | +0.73 | 5.6 | 4.1 | 3.4 |
| FTA per FGA | shooting | +0.64 | 0.32 | 0.25 | 0.25 |
| corner-3 share of FGA | shooting | -0.61 | 5.6% | 8.5% | 12.4% |
| shot attempts + TOV per 100 | creation | +0.61 | 30.0 | 26.4 | 22.0 |
| above-break-3 share of FGA | shooting | -0.59 | 26.2% | 33.5% | 29.6% |

**Shot-location mix** (share of FGA):

| | rim (restricted area) | short mid (paint, non-RA) | long mid | corner 3 | above-break 3 |
|---|---|---|---|---|---|
| sub-role | 25% | 25% | 17% | 5% | 27% |
| F1 | 24% | 20% | 15% | 8% | 34% |
| league | 29% | 19% | 11% | 11% | 31% |
