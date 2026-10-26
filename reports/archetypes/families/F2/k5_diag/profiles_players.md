# Player reveal: F2, k = 5 (diag covariance)

Same sub-role order as profiles_blind.md. Read that file first.

- **Most typical:** highest sub-role probability; ties broken by smallest Mahalanobis distance to the sub-role center.
- **Borderline:** members with top probability under 0.6, the 5 with the most minutes, with their second-most-likely sub-role.
- **Pacers:** every Pacers player-season (any IND minutes that season) in F2's training set. Pacers player-seasons whose top family is F2 but under 0.6 are projected and listed separately.

## F2-S1 (64 player-seasons)

**10 most typical**

| # | player-season | minutes | prob | distance |
|---|---|---|---|---|
| 1 | Bryce McGowens (NOP, 2025-26) | 880 | 1.00 | 4.75 |
| 2 | Dru Smith (MIA, 2025-26) | 1121 | 1.00 | 5.09 |
| 3 | Jae'Sean Tate (HOU, 2024-25) | 573 | 1.00 | 6.44 |
| 4 | Brandin Podziemski (GSW, 2025-26) | 2333 | 1.00 | 5.71 |
| 5 | Draymond Green (GSW, 2024-25) | 1871 | 1.00 | 5.60 |
| 6 | Herbert Jones (NOP, 2024-25) | 648 | 1.00 | 3.15 |
| 7 | Isaac Okoro (CHI, 2025-26) | 1695 | 1.00 | 4.45 |
| 8 | Kenrich Williams (OKC, 2025-26) | 855 | 1.00 | 3.47 |
| 9 | Toumani Camara (POR, 2024-25) | 2518 | 1.00 | 3.51 |
| 10 | Brandin Podziemski (GSW, 2024-25) | 1660 | 1.00 | 5.77 |

**Borderline** (7 members under 0.6; 5 with the most minutes)

| player-season | minutes | prob | second sub-role | prob |
|---|---|---|---|---|
| Harrison Barnes (SAS, 2024-25) | 2208 | 0.59 | F2-S4 | 0.22 |
| Bruce Brown (DEN, 2025-26) | 1972 | 0.52 | F2-S5 | 0.48 |
| Kelly Oubre Jr. (PHI, 2025-26) | 1574 | 0.51 | F2-S5 | 0.48 |
| Julian Strawther (DEN, 2025-26) | 834 | 0.49 | F2-S3 | 0.46 |
| Monté Morris (PHX, 2024-25) | 561 | 0.52 | F2-S3 | 0.44 |

**Pacers player-seasons**

| player-season | minutes | prob | second | prob |
|---|---|---|---|---|
| Aaron Nesmith (IND, 2024-25) | 1099 | 1.00 | F2-S2 | 0.00 |
| Kobe Brown (IND/LAC, 2025-26) | 947 | 0.99 | F2-S4 | 0.01 |
| Ethan Thompson (IND, 2025-26) | 653 | 0.97 | F2-S2 | 0.02 |

## F2-S2 (62 player-seasons)

**10 most typical**

| # | player-season | minutes | prob | distance |
|---|---|---|---|---|
| 1 | Sam Merrill (CLE, 2024-25) | 1401 | 1.00 | 3.84 |
| 2 | Isaiah Joe (OKC, 2024-25) | 1566 | 1.00 | 4.02 |
| 3 | Nicolas Batum (LAC, 2025-26) | 1266 | 1.00 | 5.89 |
| 4 | Garrison Mathews (ATL, 2024-25) | 830 | 1.00 | 4.98 |
| 5 | AJ Green (MIL, 2024-25) | 1638 | 1.00 | 4.52 |
| 6 | Lindy Waters III (GSW/DET, 2024-25) | 753 | 1.00 | 2.16 |
| 7 | Isaiah Joe (OKC, 2025-26) | 1507 | 1.00 | 3.86 |
| 8 | Gabe Vincent (LAL, 2024-25) | 1503 | 1.00 | 4.10 |
| 9 | AJ Green (MIL, 2025-26) | 2270 | 1.00 | 4.26 |
| 10 | Gabe Vincent (LAL/ATL, 2025-26) | 879 | 1.00 | 4.57 |

**Borderline** (0 members under 0.6; 5 with the most minutes)

None.

**Pacers player-seasons**

| player-season | minutes | prob | second | prob |
|---|---|---|---|---|
| Ben Sheppard (IND, 2024-25) | 1154 | 1.00 | F2-S4 | 0.00 |

## F2-S3 (61 player-seasons)

**10 most typical**

| # | player-season | minutes | prob | distance |
|---|---|---|---|---|
| 1 | Keaton Wallace (ATL, 2025-26) | 536 | 1.00 | 6.56 |
| 2 | Brice Sensabaugh (UTA, 2024-25) | 1432 | 1.00 | 3.43 |
| 3 | Luke Kennard (MEM, 2024-25) | 1472 | 1.00 | 3.80 |
| 4 | Corey Kispert (WAS, 2024-25) | 1572 | 1.00 | 3.55 |
| 5 | Tyus Jones (ORL/DAL/DEN, 2025-26) | 974 | 1.00 | 6.63 |
| 6 | Max Christie (DAL, 2025-26) | 2245 | 1.00 | 3.51 |
| 7 | Patrick Williams (CHI, 2024-25) | 1564 | 1.00 | 2.34 |
| 8 | Trey Murphy III (NOP, 2025-26) | 2341 | 1.00 | 5.33 |
| 9 | Tyrese Martin (BKN/PHI, 2025-26) | 777 | 1.00 | 3.30 |
| 10 | Tyrese Martin (BKN, 2024-25) | 1296 | 1.00 | 2.53 |

**Borderline** (3 members under 0.6; 5 with the most minutes)

| player-season | minutes | prob | second sub-role | prob |
|---|---|---|---|---|
| Caris LeVert (CLE/ATL, 2024-25) | 1596 | 0.60 | F2-S1 | 0.36 |
| Terance Mann (LAC/ATL, 2024-25) | 1381 | 0.54 | F2-S1 | 0.46 |
| Dalton Knecht (LAL, 2025-26) | 553 | 0.58 | F2-S2 | 0.40 |

**Pacers player-seasons**

| player-season | minutes | prob | second | prob |
|---|---|---|---|---|
| Jarace Walker (IND, 2024-25) | 1115 | 0.98 | F2-S1 | 0.02 |
| Jarace Walker (IND, 2025-26) | 1953 | 0.99 | F2-S1 | 0.01 |
| Ben Sheppard (IND, 2025-26) | 1390 | 0.72 | F2-S2 | 0.26 |

## F2-S4 (58 player-seasons)

**10 most typical**

| # | player-season | minutes | prob | distance |
|---|---|---|---|---|
| 1 | Mouhamed Gueye (ATL, 2024-25) | 511 | 1.00 | 5.61 |
| 2 | Jarred Vanderbilt (LAL, 2025-26) | 1128 | 1.00 | 5.44 |
| 3 | Mouhamed Gueye (ATL, 2025-26) | 1179 | 1.00 | 3.75 |
| 4 | Nae'Qwan Tomlin (CLE, 2025-26) | 998 | 1.00 | 4.15 |
| 5 | Rasheer Fleming (PHX, 2025-26) | 673 | 1.00 | 4.87 |
| 6 | Julian Phillips (CHI, 2024-25) | 1078 | 1.00 | 3.47 |
| 7 | Jeremiah Robinson-Earl (NOP, 2024-25) | 1239 | 1.00 | 3.41 |
| 8 | Ryan Dunn (PHX, 2025-26) | 1355 | 1.00 | 3.33 |
| 9 | Josh Okogie (HOU, 2025-26) | 1354 | 1.00 | 3.42 |
| 10 | Spencer Jones (DEN, 2025-26) | 1379 | 1.00 | 4.77 |

**Borderline** (1 members under 0.6; 5 with the most minutes)

| player-season | minutes | prob | second sub-role | prob |
|---|---|---|---|---|
| Alex Caruso (OKC, 2025-26) | 1020 | 0.59 | F2-S1 | 0.40 |

**Pacers player-seasons**

| player-season | minutes | prob | second | prob |
|---|---|---|---|---|
| Obi Toppin (IND, 2024-25) | 1461 | 0.82 | F2-S3 | 0.13 |
| Micah Potter (IND, 2025-26) | 908 | 1.00 | F2-S1 | 0.00 |

## F2-S5 (36 player-seasons)

**10 most typical**

| # | player-season | minutes | prob | distance |
|---|---|---|---|---|
| 1 | Ausar Thompson (DET, 2025-26) | 1844 | 1.00 | 5.77 |
| 2 | Amen Thompson (HOU, 2024-25) | 2177 | 1.00 | 4.54 |
| 3 | Amen Thompson (HOU, 2025-26) | 2953 | 1.00 | 4.90 |
| 4 | Ausar Thompson (DET, 2024-25) | 1294 | 1.00 | 5.29 |
| 5 | Jaime Jaquez Jr. (MIA, 2024-25) | 1368 | 1.00 | 3.70 |
| 6 | Jordan Miller (LAC, 2025-26) | 1314 | 1.00 | 4.57 |
| 7 | GG Jackson (MEM, 2025-26) | 1178 | 1.00 | 4.00 |
| 8 | Jalen Johnson (ATL, 2024-25) | 1284 | 1.00 | 4.17 |
| 9 | P.J. Washington (DAL, 2024-25) | 1835 | 1.00 | 3.18 |
| 10 | Naji Marshall (DAL, 2024-25) | 1919 | 1.00 | 3.93 |

**Borderline** (0 members under 0.6; 5 with the most minutes)

None.

**Pacers player-seasons**

None.

## Pacers player-seasons with top family F2 under 0.6 (not in training, projected)

None.
