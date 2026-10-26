# Feature flags inside F1 (before fitting)

Flags (prompts for Jonathan, nothing dropped): **near-constant** = SD inside the family under 25% of the league SD, or over half the training rows exactly 0; **extremely skewed** = |skewness| > 2. Within-family standardization stretches every feature to SD 1, so a near-constant feature's noise counts as much as a real difference. All 17 features were kept for the sweep (no fit failed).

| feature | family mean | family SD | league SD | SD ratio | share zero | skewness | flags | proposal |
|---|---|---|---|---|---|---|---|---|
| rim share of FGA | 24.2% | 10.4% | 16.6% | 0.63 | 0% | +0.93 |  |  |
| short-mid share of FGA | 20.0% | 7.7% | 8.5% | 0.91 | 0% | +1.10 |  |  |
| corner-3 share of FGA | 8.5% | 4.8% | 8.9% | 0.54 | 1% | +0.74 |  |  |
| above-break-3 share of FGA | 33.5% | 12.5% | 15.6% | 0.80 | 0% | -0.13 |  |  |
| pull-up/step-back 3PA per FGA | 15.3% | 9.0% | 8.6% | 1.05 | 0% | +0.36 |  |  |
| FTA per FGA | 0.25 | 0.11 | 0.12 | 0.93 | 0% | +0.64 |  |  |
| shot attempts + TOV per 100 | 26.4 | 6.0 | 6.3 | 0.95 | 0% | +0.11 |  |  |
| AST per 100 | 7.1 | 2.7 | 2.6 | 1.04 | 0% | +0.42 |  |  |
| assisted share of made FG | 54.4% | 13.9% | 15.5% | 0.90 | 0% | +0.25 |  |  |
| driving FGA per FGA | 26.1% | 10.3% | 10.4% | 0.99 | 0% | +0.52 |  |  |
| fouls drawn per 100 | 4.1 | 2.0 | 1.8 | 1.09 | 0% | +0.65 |  |  |
| OREB% | 2.8% | 1.5% | 3.3% | 0.45 | 0% | +1.44 |  |  |
| DREB% | 11.4% | 3.9% | 5.1% | 0.77 | 0% | +1.45 |  |  |
| STL per 100 | 1.7 | 0.5 | 0.6 | 0.89 | 0% | +0.42 |  |  |
| BLK per 100 | 0.6 | 0.4 | 0.8 | 0.50 | 1% | +1.10 |  |  |
| defensive fouls per 100 | 3.2 | 0.8 | 1.0 | 0.84 | 0% | +0.52 |  |  |
| charges drawn per 100 | 0.1 | 0.1 | 0.1 | 0.86 | 44% | +2.39 | extremely skewed | option: log-transform (log1p) or drop in this family. Reason: a few extreme rows dominate the SD and can form their own sub-role. Option: keep, if those rows are a real role. |
