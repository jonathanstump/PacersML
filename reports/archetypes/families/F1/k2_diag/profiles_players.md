# Player reveal: F1, k = 2 (diag covariance)

Same sub-role order as profiles_blind.md. Read that file first.

- **Most typical:** highest sub-role probability; ties broken by smallest Mahalanobis distance to the sub-role center.
- **Borderline:** members with top probability under 0.6, the 5 with the most minutes, with their second-most-likely sub-role.
- **Pacers:** every Pacers player-season (any IND minutes that season) in F1's training set. Pacers player-seasons whose top family is F1 but under 0.6 are projected and listed separately.

## F1-S1 (165 player-seasons)

**10 most typical**

| # | player-season | minutes | prob | distance |
|---|---|---|---|---|
| 1 | Paolo Banchero (ORL, 2025-26) | 2502 | 1.00 | 3.76 |
| 2 | Deni Avdija (POR, 2025-26) | 2161 | 1.00 | 4.12 |
| 3 | Jimmy Butler III (GSW, 2025-26) | 1182 | 1.00 | 5.55 |
| 4 | Alperen Sengun (HOU, 2025-26) | 2398 | 1.00 | 5.73 |
| 5 | Luka Dončić (LAL, 2025-26) | 2289 | 1.00 | 5.80 |
| 6 | Nikola Jokić (DEN, 2024-25) | 2452 | 1.00 | 5.95 |
| 7 | Jimmy Butler III (GSW/MIA, 2024-25) | 1678 | 1.00 | 5.96 |
| 8 | Joel Embiid (PHI, 2024-25) | 574 | 1.00 | 5.99 |
| 9 | Joel Embiid (PHI, 2025-26) | 1201 | 1.00 | 6.01 |
| 10 | Nikola Jokić (DEN, 2025-26) | 2265 | 1.00 | 6.55 |

**Borderline** (4 members under 0.6; 5 with the most minutes)

| player-season | minutes | prob | second sub-role | prob |
|---|---|---|---|---|
| Jamal Murray (DEN, 2024-25) | 2338 | 0.54 | F1-S2 | 0.46 |
| Desmond Bane (MEM, 2024-25) | 2205 | 0.54 | F1-S2 | 0.46 |
| Dillon Brooks (PHX, 2025-26) | 1702 | 0.60 | F1-S2 | 0.40 |
| KJ Simpson (CHA, 2024-25) | 842 | 0.54 | F1-S2 | 0.46 |

**Pacers player-seasons**

| player-season | minutes | prob | second | prob |
|---|---|---|---|---|
| Pascal Siakam (IND, 2024-25) | 2485 | 1.00 | F1-S2 | 0.00 |
| Bennedict Mathurin (IND, 2024-25) | 2056 | 1.00 | F1-S2 | 0.00 |
| T.J. McConnell (IND, 2024-25) | 1362 | 1.00 | F1-S2 | 0.00 |
| Pascal Siakam (IND, 2025-26) | 2057 | 1.00 | F1-S2 | 0.00 |
| Andrew Nembhard (IND, 2025-26) | 1786 | 0.95 | F1-S2 | 0.05 |
| Bennedict Mathurin (IND/LAC, 2025-26) | 1620 | 1.00 | F1-S2 | 0.00 |
| T.J. McConnell (IND, 2025-26) | 963 | 1.00 | F1-S2 | 0.00 |
| Quenton Jackson (IND, 2025-26) | 897 | 1.00 | F1-S2 | 0.00 |

## F1-S2 (138 player-seasons)

**10 most typical**

| # | player-season | minutes | prob | distance |
|---|---|---|---|---|
| 1 | Mike Conley (MIN, 2025-26) | 991 | 1.00 | 5.16 |
| 2 | Jevon Carter (ORL/CHI, 2025-26) | 867 | 1.00 | 4.79 |
| 3 | Kentavious Caldwell-Pope (ORL, 2024-25) | 2245 | 1.00 | 4.98 |
| 4 | Miles McBride (NYK, 2025-26) | 1080 | 1.00 | 3.90 |
| 5 | Rui Hachimura (LAL, 2025-26) | 1927 | 1.00 | 5.09 |
| 6 | Klay Thompson (DAL, 2025-26) | 1497 | 1.00 | 5.77 |
| 7 | Klay Thompson (DAL, 2024-25) | 1965 | 1.00 | 4.54 |
| 8 | Buddy Hield (GSW, 2024-25) | 1767 | 1.00 | 3.95 |
| 9 | Gary Trent Jr. (MIL, 2024-25) | 1859 | 1.00 | 4.13 |
| 10 | Devin Vassell (SAS, 2025-26) | 2044 | 1.00 | 3.85 |

**Borderline** (5 members under 0.6; 5 with the most minutes)

| player-season | minutes | prob | second sub-role | prob |
|---|---|---|---|---|
| Russell Westbrook (SAC, 2025-26) | 1853 | 0.56 | F1-S1 | 0.44 |
| Craig Porter Jr. (CLE, 2025-26) | 1132 | 0.51 | F1-S1 | 0.49 |
| Rob Dillingham (CHI/MIN, 2025-26) | 970 | 0.53 | F1-S1 | 0.47 |
| Khris Middleton (MIL/WAS, 2024-25) | 843 | 0.52 | F1-S1 | 0.48 |
| Javon Small (MEM, 2025-26) | 830 | 0.55 | F1-S1 | 0.45 |

**Pacers player-seasons**

| player-season | minutes | prob | second | prob |
|---|---|---|---|---|
| Tyrese Haliburton (IND, 2024-25) | 2411 | 0.81 | F1-S1 | 0.19 |
| Andrew Nembhard (IND, 2024-25) | 1840 | 0.97 | F1-S1 | 0.03 |
| Aaron Nesmith (IND, 2025-26) | 1335 | 1.00 | F1-S1 | 0.00 |
| Kam Jones (IND, 2025-26) | 616 | 0.99 | F1-S1 | 0.01 |

## Pacers player-seasons with top family F1 under 0.6 (not in training, projected)

None.
