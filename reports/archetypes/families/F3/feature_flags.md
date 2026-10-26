# Feature flags inside F3 (before fitting)

Flags (prompts for Jonathan, nothing dropped): **near-constant** = SD inside the family under 25% of the league SD, or over half the training rows exactly 0; **extremely skewed** = |skewness| > 2. Within-family standardization stretches every feature to SD 1, so a near-constant feature's noise counts as much as a real difference. All 17 features were kept for the sweep (no fit failed).

| feature | family mean | family SD | league SD | SD ratio | share zero | skewness | flags | proposal |
|---|---|---|---|---|---|---|---|---|
| rim share of FGA | 51.5% | 18.3% | 16.6% | 1.10 | 0% | +0.05 |  |  |
| short-mid share of FGA | 20.7% | 10.2% | 8.5% | 1.21 | 0% | +0.67 |  |  |
| corner-3 share of FGA | 5.7% | 6.7% | 8.9% | 0.76 | 16% | +1.31 |  |  |
| above-break-3 share of FGA | 13.2% | 14.2% | 15.6% | 0.91 | 14% | +0.97 |  |  |
| pull-up/step-back 3PA per FGA | 1.1% | 1.8% | 8.6% | 0.21 | 37% | +3.60 | near-constant, extremely skewed | option: drop in this family. Reason: little spread here, so within-family z-scores mostly measure noise. Option: keep, if the small differences are meaningful. |
| FTA per FGA | 0.34 | 0.13 | 0.12 | 1.12 | 0% | +1.60 |  |  |
| shot attempts + TOV per 100 | 19.9 | 5.8 | 6.3 | 0.92 | 0% | +0.83 |  |  |
| AST per 100 | 3.7 | 1.5 | 2.6 | 0.56 | 0% | +0.97 |  |  |
| assisted share of made FG | 72.9% | 9.1% | 15.5% | 0.58 | 0% | -0.45 |  |  |
| driving FGA per FGA | 13.9% | 8.2% | 10.4% | 0.78 | 0% | +1.08 |  |  |
| fouls drawn per 100 | 4.3 | 1.7 | 1.8 | 0.94 | 0% | +1.50 |  |  |
| OREB% | 9.5% | 3.5% | 3.3% | 1.06 | 0% | +0.20 |  |  |
| DREB% | 19.3% | 4.8% | 5.1% | 0.94 | 0% | -0.05 |  |  |
| STL per 100 | 1.5 | 0.5 | 0.6 | 0.79 | 0% | +0.83 |  |  |
| BLK per 100 | 2.1 | 1.0 | 0.8 | 1.18 | 0% | +0.71 |  |  |
| defensive fouls per 100 | 4.3 | 1.0 | 1.0 | 1.02 | 0% | +0.36 |  |  |
| charges drawn per 100 | 0.0 | 0.1 | 0.1 | 0.59 | 59% | +2.57 | near-constant, extremely skewed | option: drop in this family. Reason: little spread here, so within-family z-scores mostly measure noise. Option: keep, if the small differences are meaningful. |
