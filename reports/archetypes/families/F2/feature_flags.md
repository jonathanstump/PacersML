# Feature flags inside F2 (before fitting)

Flags (prompts for Jonathan, nothing dropped): **near-constant** = SD inside the family under 25% of the league SD, or over half the training rows exactly 0; **extremely skewed** = |skewness| > 2. Within-family standardization stretches every feature to SD 1, so a near-constant feature's noise counts as much as a real difference. All 17 features were kept for the sweep (no fit failed).

| feature | family mean | family SD | league SD | SD ratio | share zero | skewness | flags | proposal |
|---|---|---|---|---|---|---|---|---|
| rim share of FGA | 26.4% | 11.6% | 16.6% | 0.70 | 0% | +0.17 |  |  |
| short-mid share of FGA | 13.5% | 6.3% | 8.5% | 0.75 | 0% | +0.66 |  |  |
| corner-3 share of FGA | 20.1% | 7.8% | 8.9% | 0.88 | 0% | +0.62 |  |  |
| above-break-3 share of FGA | 33.9% | 13.5% | 15.6% | 0.87 | 0% | +0.22 |  |  |
| pull-up/step-back 3PA per FGA | 7.3% | 5.2% | 8.6% | 0.61 | 1% | +0.88 |  |  |
| FTA per FGA | 0.19 | 0.08 | 0.12 | 0.70 | 0% | +0.32 |  |  |
| shot attempts + TOV per 100 | 18.4 | 3.5 | 6.3 | 0.56 | 0% | -0.04 |  |  |
| AST per 100 | 3.9 | 1.5 | 2.6 | 0.57 | 0% | +1.14 |  |  |
| assisted share of made FG | 77.3% | 9.5% | 15.5% | 0.61 | 0% | -0.23 |  |  |
| driving FGA per FGA | 18.1% | 8.4% | 10.4% | 0.81 | 0% | +0.31 |  |  |
| fouls drawn per 100 | 2.3 | 1.0 | 1.8 | 0.52 | 0% | +0.37 |  |  |
| OREB% | 4.1% | 1.9% | 3.3% | 0.57 | 0% | +0.58 |  |  |
| DREB% | 11.8% | 3.7% | 5.1% | 0.72 | 0% | +0.62 |  |  |
| STL per 100 | 1.8 | 0.7 | 0.6 | 1.15 | 0% | +1.02 |  |  |
| BLK per 100 | 0.8 | 0.4 | 0.8 | 0.55 | 0% | +1.06 |  |  |
| defensive fouls per 100 | 3.8 | 1.0 | 1.0 | 0.96 | 0% | -0.04 |  |  |
| charges drawn per 100 | 0.1 | 0.1 | 0.1 | 1.26 | 43% | +2.43 | extremely skewed | option: log-transform (log1p) or drop in this family. Reason: a few extreme rows dominate the SD and can form their own sub-role. Option: keep, if those rows are a real role. |
