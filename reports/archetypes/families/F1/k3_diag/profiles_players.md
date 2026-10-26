# Player reveal: F1, k = 3 (diag covariance)

Same sub-role order as profiles_blind.md. Read that file first.

- **Most typical:** highest sub-role probability; ties broken by smallest Mahalanobis distance to the sub-role center.
- **Borderline:** members with top probability under 0.6, the 5 with the most minutes, with their second-most-likely sub-role.
- **Pacers:** every Pacers player-season (any IND minutes that season) in F1's training set. Pacers player-seasons whose top family is F1 but under 0.6 are projected and listed separately.

## F1-S1 (117 player-seasons)

**10 most typical**

| # | player-season | minutes | prob | distance |
|---|---|---|---|---|
| 1 | James Harden (LAC, 2024-25) | 2789 | 1.00 | 5.48 |
| 2 | Trae Young (ATL, 2024-25) | 2739 | 1.00 | 5.47 |
| 3 | James Harden (LAC/CLE, 2025-26) | 2370 | 1.00 | 4.60 |
| 4 | Luka Dončić (LAL, 2025-26) | 2289 | 1.00 | 6.26 |
| 5 | Jayson Tatum (BOS, 2024-25) | 2562 | 1.00 | 4.73 |
| 6 | LaMelo Ball (CHA, 2024-25) | 1470 | 1.00 | 3.91 |
| 7 | Jayson Tatum (BOS, 2025-26) | 522 | 1.00 | 5.93 |
| 8 | Jalen Brunson (NYK, 2025-26) | 2590 | 1.00 | 5.43 |
| 9 | Damian Lillard (MIL, 2024-25) | 2093 | 1.00 | 4.04 |
| 10 | Luka Dončić (LAL/DAL, 2024-25) | 1725 | 1.00 | 4.97 |

**Borderline** (3 members under 0.6; 5 with the most minutes)

| player-season | minutes | prob | second sub-role | prob |
|---|---|---|---|---|
| Brandon Miller (CHA, 2025-26) | 1902 | 0.59 | F1-S3 | 0.40 |
| Andrew Nembhard (IND, 2024-25) | 1840 | 0.42 | F1-S3 | 0.42 |
| Cole Anthony (ORL, 2024-25) | 1230 | 0.57 | F1-S2 | 0.43 |

**Pacers player-seasons**

| player-season | minutes | prob | second | prob |
|---|---|---|---|---|
| Tyrese Haliburton (IND, 2024-25) | 2411 | 1.00 | F1-S3 | 0.00 |
| Andrew Nembhard (IND, 2024-25) | 1840 | 0.42 | F1-S3 | 0.42 |
| Andrew Nembhard (IND, 2025-26) | 1786 | 1.00 | F1-S3 | 0.00 |
| Bennedict Mathurin (IND/LAC, 2025-26) | 1620 | 0.75 | F1-S2 | 0.25 |

## F1-S2 (95 player-seasons)

**10 most typical**

| # | player-season | minutes | prob | distance |
|---|---|---|---|---|
| 1 | Alperen Sengun (HOU, 2025-26) | 2398 | 1.00 | 4.89 |
| 2 | Nikola Jokić (DEN, 2025-26) | 2265 | 1.00 | 5.84 |
| 3 | Zion Williamson (NOP, 2025-26) | 1841 | 1.00 | 6.09 |
| 4 | Zion Williamson (NOP, 2024-25) | 857 | 1.00 | 6.57 |
| 5 | Giannis Antetokounmpo (MIL, 2024-25) | 2245 | 1.00 | 6.74 |
| 6 | Moritz Wagner (ORL, 2024-25) | 547 | 1.00 | 7.15 |
| 7 | Elfrid Payton (NOP/CHA, 2024-25) | 511 | 1.00 | 8.46 |
| 8 | Derik Queen (NOP, 2025-26) | 2023 | 1.00 | 4.27 |
| 9 | Nikola Jokić (DEN, 2024-25) | 2452 | 1.00 | 5.30 |
| 10 | Jimmy Butler III (GSW/MIA, 2024-25) | 1678 | 1.00 | 5.11 |

**Borderline** (1 members under 0.6; 5 with the most minutes)

| player-season | minutes | prob | second sub-role | prob |
|---|---|---|---|---|
| Devin Carter (SAC, 2025-26) | 700 | 0.54 | F1-S1 | 0.46 |

**Pacers player-seasons**

| player-season | minutes | prob | second | prob |
|---|---|---|---|---|
| Pascal Siakam (IND, 2024-25) | 2485 | 1.00 | F1-S1 | 0.00 |
| Bennedict Mathurin (IND, 2024-25) | 2056 | 0.80 | F1-S1 | 0.20 |
| T.J. McConnell (IND, 2024-25) | 1362 | 1.00 | F1-S1 | 0.00 |
| Pascal Siakam (IND, 2025-26) | 2057 | 0.99 | F1-S1 | 0.01 |
| T.J. McConnell (IND, 2025-26) | 963 | 0.99 | F1-S1 | 0.01 |
| Quenton Jackson (IND, 2025-26) | 897 | 1.00 | F1-S1 | 0.00 |
| Kam Jones (IND, 2025-26) | 616 | 0.86 | F1-S1 | 0.07 |

## F1-S3 (91 player-seasons)

**10 most typical**

| # | player-season | minutes | prob | distance |
|---|---|---|---|---|
| 1 | Mike Conley (MIN, 2025-26) | 991 | 1.00 | 5.02 |
| 2 | Duncan Robinson (MIA, 2024-25) | 1786 | 1.00 | 4.45 |
| 3 | Jevon Carter (ORL/CHI, 2025-26) | 867 | 1.00 | 4.41 |
| 4 | Svi Mykhailiuk (UTA, 2024-25) | 760 | 1.00 | 3.21 |
| 5 | Buddy Hield (GSW, 2024-25) | 1767 | 1.00 | 3.48 |
| 6 | Lonzo Ball (CLE, 2025-26) | 728 | 1.00 | 6.35 |
| 7 | Mike Conley (MIN, 2024-25) | 1724 | 1.00 | 4.28 |
| 8 | Donte DiVincenzo (MIN, 2024-25) | 1574 | 1.00 | 2.92 |
| 9 | Klay Thompson (DAL, 2025-26) | 1497 | 1.00 | 5.53 |
| 10 | Miles McBride (NYK, 2025-26) | 1080 | 1.00 | 3.55 |

**Borderline** (1 members under 0.6; 5 with the most minutes)

| player-season | minutes | prob | second sub-role | prob |
|---|---|---|---|---|
| Paul George (PHI, 2024-25) | 1334 | 0.51 | F1-S1 | 0.49 |

**Pacers player-seasons**

| player-season | minutes | prob | second | prob |
|---|---|---|---|---|
| Aaron Nesmith (IND, 2025-26) | 1335 | 1.00 | F1-S2 | 0.00 |

## Pacers player-seasons with top family F1 under 0.6 (not in training, projected)

None.
