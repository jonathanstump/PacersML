# Player reveal: F2, k = 3 (diag covariance)

Same sub-role order as profiles_blind.md. Read that file first.

- **Most typical:** highest sub-role probability; ties broken by smallest Mahalanobis distance to the sub-role center.
- **Borderline:** members with top probability under 0.6, the 5 with the most minutes, with their second-most-likely sub-role.
- **Pacers:** every Pacers player-season (any IND minutes that season) in F2's training set. Pacers player-seasons whose top family is F2 but under 0.6 are projected and listed separately.

## F2-S1 (110 player-seasons)

**10 most typical**

| # | player-season | minutes | prob | distance |
|---|---|---|---|---|
| 1 | Isaiah Joe (OKC, 2024-25) | 1566 | 1.00 | 4.59 |
| 2 | AJ Green (MIL, 2025-26) | 2270 | 1.00 | 4.94 |
| 3 | AJ Green (MIL, 2024-25) | 1638 | 1.00 | 5.17 |
| 4 | Sam Hauser (BOS, 2025-26) | 1927 | 1.00 | 4.92 |
| 5 | Sam Merrill (CLE, 2024-25) | 1401 | 1.00 | 4.48 |
| 6 | Gabe Vincent (LAL/ATL, 2025-26) | 879 | 1.00 | 4.45 |
| 7 | Sam Hauser (BOS, 2024-25) | 1517 | 1.00 | 4.24 |
| 8 | Royce O'Neale (PHX, 2025-26) | 2213 | 1.00 | 3.82 |
| 9 | Garrison Mathews (ATL, 2024-25) | 830 | 1.00 | 5.46 |
| 10 | Gabe Vincent (LAL, 2024-25) | 1503 | 1.00 | 4.11 |

**Borderline** (2 members under 0.6; 5 with the most minutes)

| player-season | minutes | prob | second sub-role | prob |
|---|---|---|---|---|
| Keegan Murray (SAC, 2024-25) | 2541 | 0.55 | F2-S2 | 0.45 |
| Max Christie (LAL/DAL, 2024-25) | 2127 | 0.48 | F2-S2 | 0.46 |

**Pacers player-seasons**

| player-season | minutes | prob | second | prob |
|---|---|---|---|---|
| Ben Sheppard (IND, 2024-25) | 1154 | 0.98 | F2-S2 | 0.02 |
| Jarace Walker (IND, 2024-25) | 1115 | 0.85 | F2-S3 | 0.15 |
| Ben Sheppard (IND, 2025-26) | 1390 | 0.95 | F2-S2 | 0.05 |
| Ethan Thompson (IND, 2025-26) | 653 | 0.93 | F2-S2 | 0.07 |

## F2-S2 (95 player-seasons)

**10 most typical**

| # | player-season | minutes | prob | distance |
|---|---|---|---|---|
| 1 | Jarred Vanderbilt (LAL, 2025-26) | 1128 | 1.00 | 5.89 |
| 2 | Mouhamed Gueye (ATL, 2025-26) | 1179 | 1.00 | 4.06 |
| 3 | Ryan Dunn (PHX, 2025-26) | 1355 | 1.00 | 3.54 |
| 4 | John Konchar (UTA/MEM, 2025-26) | 1115 | 1.00 | 4.57 |
| 5 | Mouhamed Gueye (ATL, 2024-25) | 511 | 1.00 | 6.07 |
| 6 | Jeremiah Robinson-Earl (NOP, 2024-25) | 1239 | 1.00 | 3.60 |
| 7 | Hugo González (BOS, 2025-26) | 1084 | 1.00 | 3.18 |
| 8 | Julian Phillips (CHI, 2024-25) | 1078 | 1.00 | 3.77 |
| 9 | Josh Okogie (HOU, 2025-26) | 1354 | 1.00 | 3.50 |
| 10 | Andre Jackson Jr. (MIL, 2024-25) | 950 | 1.00 | 3.53 |

**Borderline** (2 members under 0.6; 5 with the most minutes)

| player-season | minutes | prob | second sub-role | prob |
|---|---|---|---|---|
| Sion James (CHA, 2025-26) | 1798 | 0.58 | F2-S1 | 0.42 |
| Moses Moody (GSW, 2024-25) | 1577 | 0.50 | F2-S1 | 0.49 |

**Pacers player-seasons**

| player-season | minutes | prob | second | prob |
|---|---|---|---|---|
| Obi Toppin (IND, 2024-25) | 1461 | 0.99 | F2-S3 | 0.00 |
| Aaron Nesmith (IND, 2024-25) | 1099 | 0.90 | F2-S1 | 0.10 |
| Kobe Brown (IND/LAC, 2025-26) | 947 | 0.99 | F2-S3 | 0.01 |
| Micah Potter (IND, 2025-26) | 908 | 1.00 | F2-S1 | 0.00 |

## F2-S3 (76 player-seasons)

**10 most typical**

| # | player-season | minutes | prob | distance |
|---|---|---|---|---|
| 1 | Amen Thompson (HOU, 2025-26) | 2953 | 1.00 | 5.41 |
| 2 | Jordan Miller (LAC, 2025-26) | 1314 | 1.00 | 4.82 |
| 3 | Dyson Daniels (ATL, 2025-26) | 2520 | 1.00 | 5.81 |
| 4 | Jaime Jaquez Jr. (MIA, 2024-25) | 1368 | 1.00 | 4.28 |
| 5 | Naji Marshall (DAL, 2024-25) | 1919 | 1.00 | 4.13 |
| 6 | Ausar Thompson (DET, 2025-26) | 1844 | 1.00 | 6.32 |
| 7 | Dyson Daniels (ATL, 2024-25) | 2538 | 1.00 | 5.68 |
| 8 | Anthony Black (ORL, 2025-26) | 1881 | 1.00 | 3.10 |
| 9 | GG Jackson (MEM, 2025-26) | 1178 | 1.00 | 3.99 |
| 10 | P.J. Washington (DAL, 2024-25) | 1835 | 1.00 | 3.42 |

**Borderline** (2 members under 0.6; 5 with the most minutes)

| player-season | minutes | prob | second sub-role | prob |
|---|---|---|---|---|
| Nikola Jović (MIA, 2024-25) | 1156 | 0.45 | F2-S2 | 0.39 |
| Kenrich Williams (OKC, 2025-26) | 855 | 0.55 | F2-S2 | 0.44 |

**Pacers player-seasons**

| player-season | minutes | prob | second | prob |
|---|---|---|---|---|
| Jarace Walker (IND, 2025-26) | 1953 | 0.99 | F2-S1 | 0.01 |

## Pacers player-seasons with top family F2 under 0.6 (not in training, projected)

None.
