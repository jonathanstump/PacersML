# Player reveal, k = 14 (tied covariance)

Same cluster order as profiles_blind.md. Read that file first.

- **Most typical:** highest membership probability; ties (many are 1.00) broken by smallest Mahalanobis distance to the cluster center (in SDs of that cluster's own shape).
- **8 nearest the center:** smallest Mahalanobis distance to the cluster center, whatever their top archetype.
- **Borderline:** members whose top probability is under 0.6, the 5 with the most minutes, with their second-most-likely archetype.
- **Tracked:** every Pacers player-season (any minutes for IND that season) in the cluster, plus Myles Turner 2024-25 and every Ivica Zubac season. Training seasons only (2026-27 is not projected until the model is frozen). Players under 500 minutes aren't fitted and don't appear.

## Tracked players at a glance

| player-season | minutes | top archetype | prob | second | prob |
|---|---|---|---|---|---|
| Ivica Zubac (LAC, 2024-25) | 2624 | C11 | 1.00 | C7 | 0.00 |
| Pascal Siakam (IND, 2024-25) | 2485 | C1 | 0.85 | C9 | 0.11 |
| Tyrese Haliburton (IND, 2024-25) | 2411 | C6 | 1.00 | C2 | 0.00 |
| Myles Turner (IND, 2024-25) | 2117 | C10 | 1.00 | C1 | 0.00 |
| Bennedict Mathurin (IND, 2024-25) | 2056 | C2 | 0.99 | C1 | 0.01 |
| Andrew Nembhard (IND, 2024-25) | 1840 | C4 | 0.75 | C9 | 0.20 |
| Obi Toppin (IND, 2024-25) | 1461 | C1 | 0.98 | C2 | 0.01 |
| T.J. McConnell (IND, 2024-25) | 1362 | C4 | 1.00 | C1 | 0.00 |
| Ben Sheppard (IND, 2024-25) | 1154 | C3 | 1.00 | C1 | 0.00 |
| Jarace Walker (IND, 2024-25) | 1115 | C2 | 0.94 | C1 | 0.06 |
| Aaron Nesmith (IND, 2024-25) | 1099 | C8 | 0.94 | C1 | 0.05 |
| Thomas Bryant (IND/MIA, 2024-25) | 920 | C5 | 1.00 | C1 | 0.00 |
| Pascal Siakam (IND, 2025-26) | 2057 | C9 | 0.67 | C13 | 0.24 |
| Jarace Walker (IND, 2025-26) | 1953 | C2 | 0.58 | C1 | 0.42 |
| Andrew Nembhard (IND, 2025-26) | 1786 | C4 | 0.70 | C2 | 0.18 |
| Jay Huff (IND, 2025-26) | 1719 | C10 | 1.00 | C5 | 0.00 |
| Bennedict Mathurin (IND/LAC, 2025-26) | 1620 | C2 | 0.95 | C1 | 0.03 |
| Ben Sheppard (IND, 2025-26) | 1390 | C1 | 0.98 | C2 | 0.02 |
| Ivica Zubac (LAC/IND, 2025-26) | 1382 | C11 | 1.00 | C7 | 0.00 |
| Aaron Nesmith (IND, 2025-26) | 1335 | C1 | 0.62 | C2 | 0.38 |
| T.J. McConnell (IND, 2025-26) | 963 | C4 | 1.00 | C9 | 0.00 |
| Kobe Brown (IND/LAC, 2025-26) | 947 | C1 | 0.98 | C3 | 0.01 |
| Isaiah Jackson (IND/LAC, 2025-26) | 908 | C7 | 1.00 | C5 | 0.00 |
| Micah Potter (IND, 2025-26) | 908 | C3 | 0.89 | C1 | 0.11 |
| Quenton Jackson (IND, 2025-26) | 897 | C1 | 0.83 | C2 | 0.12 |
| Ethan Thompson (IND, 2025-26) | 653 | C1 | 0.85 | C3 | 0.13 |
| Johnny Furphy (IND, 2025-26) | 643 | C1 | 0.98 | C3 | 0.01 |
| Kam Jones (IND, 2025-26) | 616 | C4 | 0.97 | C1 | 0.03 |

## C1 (217 player-seasons)

**10 most typical**

| # | player-season | minutes | prob | distance |
|---|---|---|---|---|
| 1 | Jalen Wilson (BKN, 2025-26) | 859 | 1.00 | 4.16 |
| 2 | Bruce Brown (NOP/TOR, 2024-25) | 922 | 1.00 | 3.14 |
| 3 | Jalen Wilson (BKN, 2024-25) | 2002 | 1.00 | 2.91 |
| 4 | Jordan Miller (LAC, 2025-26) | 1314 | 1.00 | 3.99 |
| 5 | Naji Marshall (DAL, 2025-26) | 2184 | 1.00 | 4.21 |
| 6 | RJ Barrett (TOR, 2025-26) | 1726 | 1.00 | 3.71 |
| 7 | Quinten Post (GSW, 2024-25) | 648 | 1.00 | 4.32 |
| 8 | Daeqwon Plowden (SAC, 2025-26) | 844 | 1.00 | 3.41 |
| 9 | Tidjane Salaün (CHA, 2025-26) | 558 | 1.00 | 3.86 |
| 10 | Jonathan Kuminga (GSW, 2024-25) | 1125 | 1.00 | 3.87 |

**8 nearest the center** (Mahalanobis distance under this cluster's shape, members and non-members)

| # | player-season | minutes | distance | top archetype | prob |
|---|---|---|---|---|---|
| 1 | Kyle Kuzma (MIL, 2025-26) | 1771 | 2.17 | C1 | 0.99 |
| 2 | Cedric Coward (MEM, 2025-26) | 1598 | 2.20 | C1 | 0.95 |
| 3 | Cameron Johnson (DEN, 2025-26) | 1647 | 2.21 | C1 | 0.96 |
| 4 | Simone Fontecchio (DET, 2024-25) | 1200 | 2.21 | C1 | 0.96 |
| 5 | Tristan da Silva (ORL, 2025-26) | 1869 | 2.24 | C1 | 0.93 |
| 6 | Tosan Evbuomwan (BKN, 2024-25) | 638 | 2.33 | C1 | 0.98 |
| 7 | Tristan da Silva (ORL, 2024-25) | 1608 | 2.43 | C1 | 0.98 |
| 8 | Bilal Coulibaly (WAS, 2024-25) | 1916 | 2.49 | C1 | 0.99 |

**Borderline** (17 members under 0.6; 5 with the most minutes)

| player-season | minutes | prob | second archetype | prob |
|---|---|---|---|---|
| Scottie Barnes (TOR, 2025-26) | 2648 | 0.41 | C4 | 0.40 |
| Bam Adebayo (MIA, 2025-26) | 2332 | 0.47 | C12 | 0.46 |
| Jaden McDaniels (MIN, 2025-26) | 2316 | 0.50 | C2 | 0.49 |
| Kentavious Caldwell-Pope (ORL, 2024-25) | 2245 | 0.52 | C2 | 0.34 |
| Deni Avdija (POR, 2025-26) | 2161 | 0.58 | C4 | 0.28 |

**Tracked players in this cluster**

| player-season | minutes | prob | second | prob |
|---|---|---|---|---|
| Pascal Siakam (IND, 2024-25) | 2485 | 0.85 | C9 | 0.11 |
| Obi Toppin (IND, 2024-25) | 1461 | 0.98 | C2 | 0.01 |
| Ben Sheppard (IND, 2025-26) | 1390 | 0.98 | C2 | 0.02 |
| Aaron Nesmith (IND, 2025-26) | 1335 | 0.62 | C2 | 0.38 |
| Kobe Brown (IND/LAC, 2025-26) | 947 | 0.98 | C3 | 0.01 |
| Quenton Jackson (IND, 2025-26) | 897 | 0.83 | C2 | 0.12 |
| Ethan Thompson (IND, 2025-26) | 653 | 0.85 | C3 | 0.13 |
| Johnny Furphy (IND, 2025-26) | 643 | 0.98 | C3 | 0.01 |

## C2 (142 player-seasons)

**10 most typical**

| # | player-season | minutes | prob | distance |
|---|---|---|---|---|
| 1 | Klay Thompson (DAL, 2025-26) | 1497 | 1.00 | 4.25 |
| 2 | Buddy Hield (GSW, 2024-25) | 1767 | 1.00 | 2.99 |
| 3 | Zach LaVine (SAC, 2025-26) | 1224 | 1.00 | 3.20 |
| 4 | Brandon Miller (CHA, 2024-25) | 924 | 1.00 | 3.43 |
| 5 | Reed Sheppard (HOU, 2025-26) | 2147 | 1.00 | 3.97 |
| 6 | Caleb Love (POR, 2025-26) | 985 | 1.00 | 3.73 |
| 7 | CJ McCollum (NOP, 2024-25) | 1832 | 1.00 | 2.89 |
| 8 | Miles McBride (NYK, 2025-26) | 1080 | 1.00 | 2.63 |
| 9 | Shaedon Sharpe (POR, 2024-25) | 2252 | 1.00 | 2.68 |
| 10 | Sam Merrill (CLE, 2025-26) | 1359 | 0.99 | 3.91 |

**8 nearest the center** (Mahalanobis distance under this cluster's shape, members and non-members)

| # | player-season | minutes | distance | top archetype | prob |
|---|---|---|---|---|---|
| 1 | Cameron Johnson (BKN, 2024-25) | 1775 | 2.09 | C2 | 0.87 |
| 2 | Quentin Grimes (DAL/PHI, 2024-25) | 1941 | 2.11 | C2 | 0.97 |
| 3 | Bogdan Bogdanović (LAC/ATL, 2024-25) | 1348 | 2.12 | C2 | 0.95 |
| 4 | VJ Edgecombe (PHI, 2025-26) | 2623 | 2.27 | C2 | 0.96 |
| 5 | Kevin Huerter (SAC/CHI, 2024-25) | 1619 | 2.43 | C2 | 0.95 |
| 6 | Quentin Grimes (PHI, 2025-26) | 2206 | 2.44 | C2 | 0.94 |
| 7 | Kon Knueppel (CHA, 2025-26) | 2482 | 2.45 | C2 | 0.65 |
| 8 | Nickeil Alexander-Walker (ATL, 2025-26) | 2603 | 2.47 | C2 | 0.79 |

**Borderline** (12 members under 0.6; 5 with the most minutes)

| player-season | minutes | prob | second archetype | prob |
|---|---|---|---|---|
| Donovan Mitchell (CLE, 2025-26) | 2316 | 0.56 | C6 | 0.44 |
| De'Aaron Fox (SAC/SAS, 2024-25) | 2204 | 0.51 | C4 | 0.21 |
| De'Aaron Fox (SAS, 2025-26) | 2197 | 0.59 | C4 | 0.38 |
| Jaylen Brown (BOS, 2024-25) | 2128 | 0.44 | C1 | 0.38 |
| Tyrese Maxey (PHI, 2024-25) | 1960 | 0.51 | C6 | 0.49 |

**Tracked players in this cluster**

| player-season | minutes | prob | second | prob |
|---|---|---|---|---|
| Bennedict Mathurin (IND, 2024-25) | 2056 | 0.99 | C1 | 0.01 |
| Jarace Walker (IND, 2024-25) | 1115 | 0.94 | C1 | 0.06 |
| Jarace Walker (IND, 2025-26) | 1953 | 0.58 | C1 | 0.42 |
| Bennedict Mathurin (IND/LAC, 2025-26) | 1620 | 0.95 | C1 | 0.03 |

## C3 (64 player-seasons)

**10 most typical**

| # | player-season | minutes | prob | distance |
|---|---|---|---|---|
| 1 | Josh Green (CHA, 2025-26) | 871 | 1.00 | 4.57 |
| 2 | Jarred Vanderbilt (LAL, 2025-26) | 1128 | 1.00 | 5.10 |
| 3 | Micah Potter (UTA, 2024-25) | 705 | 1.00 | 4.44 |
| 4 | Nicolas Batum (LAC, 2024-25) | 1367 | 1.00 | 3.72 |
| 5 | Nicolas Batum (LAC, 2025-26) | 1266 | 1.00 | 4.44 |
| 6 | John Konchar (MEM, 2024-25) | 558 | 1.00 | 4.98 |
| 7 | Josh Okogie (HOU, 2025-26) | 1354 | 1.00 | 2.73 |
| 8 | Ben Sheppard (IND, 2024-25) | 1154 | 1.00 | 3.79 |
| 9 | Rasheer Fleming (PHX, 2025-26) | 673 | 1.00 | 4.31 |
| 10 | Jonathan Isaac (ORL, 2024-25) | 1068 | 1.00 | 6.79 |

**8 nearest the center** (Mahalanobis distance under this cluster's shape, members and non-members)

| # | player-season | minutes | distance | top archetype | prob |
|---|---|---|---|---|---|
| 1 | Haywood Highsmith (MIA, 2024-25) | 1818 | 2.09 | C3 | 0.91 |
| 2 | Taylor Hendricks (MEM/UTA, 2025-26) | 1118 | 2.65 | C1 | 0.68 |
| 3 | Ziaire Williams (BKN, 2024-25) | 1523 | 2.73 | C3 | 0.67 |
| 4 | Josh Okogie (HOU, 2025-26) | 1354 | 2.73 | C3 | 1.00 |
| 5 | Josh Green (CHA, 2024-25) | 1861 | 2.80 | C3 | 1.00 |
| 6 | Dorian Finney-Smith (LAL/BKN, 2024-25) | 1781 | 2.81 | C3 | 0.76 |
| 7 | Ja'Kobe Walter (TOR, 2025-26) | 1461 | 2.81 | C3 | 0.96 |
| 8 | Moses Moody (GSW, 2025-26) | 1540 | 2.84 | C1 | 0.71 |

**Borderline** (3 members under 0.6; 5 with the most minutes)

| player-season | minutes | prob | second archetype | prob |
|---|---|---|---|---|
| Ochai Agbaji (TOR, 2024-25) | 1739 | 0.54 | C1 | 0.45 |
| Keon Ellis (SAC/CLE, 2025-26) | 1479 | 0.45 | C1 | 0.39 |
| Dalen Terry (CHI/PHI, 2025-26) | 551 | 0.53 | C1 | 0.46 |

**Tracked players in this cluster**

| player-season | minutes | prob | second | prob |
|---|---|---|---|---|
| Ben Sheppard (IND, 2024-25) | 1154 | 1.00 | C1 | 0.00 |
| Micah Potter (IND, 2025-26) | 908 | 0.89 | C1 | 0.11 |

## C4 (54 player-seasons)

**10 most typical**

| # | player-season | minutes | prob | distance |
|---|---|---|---|---|
| 1 | Elfrid Payton (NOP/CHA, 2024-25) | 511 | 1.00 | 8.34 |
| 2 | T.J. McConnell (IND, 2024-25) | 1362 | 1.00 | 5.70 |
| 3 | Ja Morant (MEM, 2025-26) | 568 | 1.00 | 4.31 |
| 4 | Josh Giddey (CHI, 2025-26) | 1731 | 1.00 | 4.37 |
| 5 | Isaiah Collier (UTA, 2025-26) | 1517 | 1.00 | 4.53 |
| 6 | Davion Mitchell (MIA, 2025-26) | 1968 | 1.00 | 3.63 |
| 7 | Cade Cunningham (DET, 2025-26) | 2099 | 1.00 | 4.29 |
| 8 | Cole Anthony (MIL, 2025-26) | 510 | 1.00 | 4.55 |
| 9 | LeBron James (LAL, 2024-25) | 2401 | 1.00 | 4.24 |
| 10 | Dennis Schröder (SAC/CLE, 2025-26) | 1696 | 1.00 | 3.54 |

**8 nearest the center** (Mahalanobis distance under this cluster's shape, members and non-members)

| # | player-season | minutes | distance | top archetype | prob |
|---|---|---|---|---|---|
| 1 | Jalen Williams (OKC, 2025-26) | 936 | 2.42 | C4 | 0.99 |
| 2 | Isaiah Collier (UTA, 2024-25) | 1839 | 2.82 | C4 | 1.00 |
| 3 | Jared Butler (PHI/WAS, 2024-25) | 1009 | 3.03 | C4 | 0.99 |
| 4 | Jamal Shead (TOR, 2025-26) | 1829 | 3.16 | C4 | 1.00 |
| 5 | Dennis Schröder (BKN/DET/GSW, 2024-25) | 2046 | 3.20 | C4 | 1.00 |
| 6 | Tyler Kolek (NYK, 2025-26) | 727 | 3.34 | C4 | 1.00 |
| 7 | De'Aaron Fox (SAC/SAS, 2024-25) | 2204 | 3.38 | C2 | 0.51 |
| 8 | Ayo Dosunmu (CHI/MIN, 2025-26) | 1881 | 3.43 | C4 | 0.55 |

**Borderline** (3 members under 0.6; 5 with the most minutes)

| player-season | minutes | prob | second archetype | prob |
|---|---|---|---|---|
| Jaime Jaquez Jr. (MIA, 2025-26) | 2092 | 0.60 | C1 | 0.40 |
| Ayo Dosunmu (CHI/MIN, 2025-26) | 1881 | 0.55 | C1 | 0.45 |
| Daniss Jenkins (DET, 2025-26) | 1432 | 0.58 | C2 | 0.30 |

**Tracked players in this cluster**

| player-season | minutes | prob | second | prob |
|---|---|---|---|---|
| Andrew Nembhard (IND, 2024-25) | 1840 | 0.75 | C9 | 0.20 |
| T.J. McConnell (IND, 2024-25) | 1362 | 1.00 | C1 | 0.00 |
| Andrew Nembhard (IND, 2025-26) | 1786 | 0.70 | C2 | 0.18 |
| T.J. McConnell (IND, 2025-26) | 963 | 1.00 | C9 | 0.00 |
| Kam Jones (IND, 2025-26) | 616 | 0.97 | C1 | 0.03 |

## C5 (44 player-seasons)

**10 most typical**

| # | player-season | minutes | prob | distance |
|---|---|---|---|---|
| 1 | Karlo Matković (NOP, 2024-25) | 791 | 1.00 | 3.45 |
| 2 | Jeremy Sochan (SAS, 2024-25) | 1332 | 1.00 | 2.63 |
| 3 | Karlo Matković (NOP, 2025-26) | 912 | 1.00 | 3.92 |
| 4 | Paul Reed (DET, 2025-26) | 880 | 1.00 | 6.49 |
| 5 | Ausar Thompson (DET, 2025-26) | 1844 | 1.00 | 4.36 |
| 6 | Ausar Thompson (DET, 2024-25) | 1294 | 1.00 | 3.81 |
| 7 | Precious Achiuwa (NYK, 2024-25) | 1170 | 1.00 | 3.54 |
| 8 | Gary Payton II (GSW, 2025-26) | 1142 | 1.00 | 4.55 |
| 9 | Thomas Bryant (IND/MIA, 2024-25) | 920 | 1.00 | 3.02 |
| 10 | Day'Ron Sharpe (BKN, 2025-26) | 1160 | 1.00 | 5.03 |

**8 nearest the center** (Mahalanobis distance under this cluster's shape, members and non-members)

| # | player-season | minutes | distance | top archetype | prob |
|---|---|---|---|---|---|
| 1 | Onyeka Okongwu (ATL, 2024-25) | 2034 | 2.50 | C5 | 0.99 |
| 2 | Jonathan Mogbo (TOR, 2024-25) | 1286 | 2.58 | C5 | 0.99 |
| 3 | Jeremy Sochan (SAS, 2024-25) | 1332 | 2.63 | C5 | 1.00 |
| 4 | Dominick Barlow (PHI, 2025-26) | 1689 | 2.84 | C5 | 0.98 |
| 5 | Justin Champagnie (WAS, 2025-26) | 1359 | 2.95 | C5 | 0.98 |
| 6 | Thomas Bryant (IND/MIA, 2024-25) | 920 | 3.02 | C5 | 1.00 |
| 7 | Amen Thompson (HOU, 2024-25) | 2177 | 3.20 | C5 | 0.95 |
| 8 | Karlo Matković (NOP, 2024-25) | 791 | 3.45 | C5 | 1.00 |

**Borderline** (3 members under 0.6; 5 with the most minutes)

| player-season | minutes | prob | second archetype | prob |
|---|---|---|---|---|
| Derrick Jones Jr. (LAC, 2025-26) | 1339 | 0.49 | C1 | 0.47 |
| Isaiah Stewart (DET, 2025-26) | 1282 | 0.53 | C10 | 0.44 |
| Zach Collins (CHI/SAS, 2024-25) | 930 | 0.53 | C12 | 0.47 |

**Tracked players in this cluster**

| player-season | minutes | prob | second | prob |
|---|---|---|---|---|
| Thomas Bryant (IND/MIA, 2024-25) | 920 | 1.00 | C1 | 0.00 |

## C6 (43 player-seasons)

**10 most typical**

| # | player-season | minutes | prob | distance |
|---|---|---|---|---|
| 1 | James Harden (LAC, 2024-25) | 2789 | 1.00 | 4.94 |
| 2 | Chris Paul (SAS, 2024-25) | 2263 | 1.00 | 6.02 |
| 3 | Tyrese Haliburton (IND, 2024-25) | 2411 | 1.00 | 5.00 |
| 4 | Trae Young (ATL, 2024-25) | 2739 | 1.00 | 4.78 |
| 5 | James Harden (LAC/CLE, 2025-26) | 2370 | 1.00 | 3.98 |
| 6 | Javon Small (MEM, 2025-26) | 830 | 1.00 | 4.04 |
| 7 | Jayson Tatum (BOS, 2025-26) | 522 | 1.00 | 6.53 |
| 8 | Jayson Tatum (BOS, 2024-25) | 2562 | 1.00 | 3.95 |
| 9 | Jrue Holiday (POR, 2025-26) | 1560 | 1.00 | 3.72 |
| 10 | Anthony Edwards (MIN, 2024-25) | 2830 | 1.00 | 3.54 |

**8 nearest the center** (Mahalanobis distance under this cluster's shape, members and non-members)

| # | player-season | minutes | distance | top archetype | prob |
|---|---|---|---|---|---|
| 1 | D'Angelo Russell (LAL/BKN, 2024-25) | 1465 | 2.31 | C6 | 0.92 |
| 2 | Bones Hyland (MIN, 2025-26) | 1177 | 2.61 | C6 | 0.98 |
| 3 | Egor Dëmin (BKN, 2025-26) | 1308 | 2.63 | C6 | 0.51 |
| 4 | Keyonte George (UTA, 2024-25) | 2108 | 2.77 | C6 | 0.92 |
| 5 | Donovan Mitchell (CLE, 2024-25) | 2232 | 2.79 | C6 | 0.83 |
| 6 | Marcus Sasser (DET, 2024-25) | 770 | 2.88 | C6 | 0.98 |
| 7 | Fred VanVleet (HOU, 2024-25) | 2046 | 3.10 | C6 | 1.00 |
| 8 | Jamal Murray (DEN, 2025-26) | 2652 | 3.11 | C6 | 0.50 |

**Borderline** (3 members under 0.6; 5 with the most minutes)

| player-season | minutes | prob | second archetype | prob |
|---|---|---|---|---|
| Jamal Murray (DEN, 2025-26) | 2652 | 0.50 | C2 | 0.50 |
| Walter Clayton Jr. (UTA/MEM, 2025-26) | 1411 | 0.50 | C2 | 0.50 |
| Egor Dëmin (BKN, 2025-26) | 1308 | 0.51 | C2 | 0.49 |

**Tracked players in this cluster**

| player-season | minutes | prob | second | prob |
|---|---|---|---|---|
| Tyrese Haliburton (IND, 2024-25) | 2411 | 1.00 | C2 | 0.00 |

## C7 (40 player-seasons)

**10 most typical**

| # | player-season | minutes | prob | distance |
|---|---|---|---|---|
| 1 | Ryan Kalkbrenner (CHA, 2025-26) | 1438 | 1.00 | 4.73 |
| 2 | Daniel Gafford (DAL, 2024-25) | 1226 | 1.00 | 4.20 |
| 3 | Walker Kessler (UTA, 2024-25) | 1740 | 1.00 | 3.91 |
| 4 | Luke Kornet (BOS, 2024-25) | 1309 | 1.00 | 3.65 |
| 5 | Donovan Clingan (POR, 2024-25) | 1311 | 1.00 | 4.09 |
| 6 | Clint Capela (HOU, 2025-26) | 926 | 1.00 | 4.32 |
| 7 | Luke Kornet (SAS, 2025-26) | 1399 | 1.00 | 4.01 |
| 8 | Rudy Gobert (MIN, 2024-25) | 2367 | 1.00 | 3.33 |
| 9 | Goga Bitadze (ORL, 2025-26) | 956 | 1.00 | 3.23 |
| 10 | Yves Missi (NOP, 2025-26) | 1297 | 1.00 | 5.57 |

**8 nearest the center** (Mahalanobis distance under this cluster's shape, members and non-members)

| # | player-season | minutes | distance | top archetype | prob |
|---|---|---|---|---|---|
| 1 | Yves Missi (NOP, 2024-25) | 1956 | 2.40 | C7 | 1.00 |
| 2 | Richaun Holmes (WAS, 2024-25) | 508 | 2.61 | C7 | 1.00 |
| 3 | Goga Bitadze (ORL, 2024-25) | 1402 | 2.80 | C7 | 1.00 |
| 4 | Daniel Gafford (DAL, 2025-26) | 1195 | 2.87 | C7 | 1.00 |
| 5 | Moussa Diabaté (CHA, 2025-26) | 1864 | 2.96 | C7 | 1.00 |
| 6 | Goga Bitadze (ORL, 2025-26) | 956 | 3.23 | C7 | 1.00 |
| 7 | Jalen Duren (DET, 2024-25) | 1939 | 3.30 | C7 | 1.00 |
| 8 | Rudy Gobert (MIN, 2024-25) | 2367 | 3.33 | C7 | 1.00 |

**Borderline** (0 members under 0.6; 5 with the most minutes)

None.

**Tracked players in this cluster**

| player-season | minutes | prob | second | prob |
|---|---|---|---|---|
| Isaiah Jackson (IND/LAC, 2025-26) | 908 | 1.00 | C5 | 0.00 |

## C8 (36 player-seasons)

**10 most typical**

| # | player-season | minutes | prob | distance |
|---|---|---|---|---|
| 1 | Jaylin Williams (OKC, 2024-25) | 774 | 1.00 | 8.09 |
| 2 | Jaylin Williams (OKC, 2025-26) | 1277 | 1.00 | 6.56 |
| 3 | Jae'Sean Tate (HOU, 2024-25) | 573 | 1.00 | 6.41 |
| 4 | Garrison Mathews (ATL, 2024-25) | 830 | 1.00 | 4.37 |
| 5 | Toumani Camara (POR, 2024-25) | 2518 | 1.00 | 4.21 |
| 6 | Marcus Smart (LAL, 2025-26) | 1769 | 1.00 | 3.37 |
| 7 | Brandin Podziemski (GSW, 2024-25) | 1660 | 1.00 | 4.39 |
| 8 | Dru Smith (MIA, 2025-26) | 1121 | 1.00 | 4.91 |
| 9 | Isaiah Joe (OKC, 2024-25) | 1566 | 1.00 | 4.32 |
| 10 | Brandin Podziemski (GSW, 2025-26) | 2333 | 1.00 | 3.56 |

**8 nearest the center** (Mahalanobis distance under this cluster's shape, members and non-members)

| # | player-season | minutes | distance | top archetype | prob |
|---|---|---|---|---|---|
| 1 | Toumani Camara (POR, 2025-26) | 2695 | 2.71 | C8 | 1.00 |
| 2 | Marcus Smart (LAL, 2025-26) | 1769 | 3.37 | C8 | 1.00 |
| 3 | Kenrich Williams (OKC, 2024-25) | 1128 | 3.42 | C8 | 1.00 |
| 4 | Trey Lyles (SAC, 2024-25) | 1331 | 3.43 | C8 | 1.00 |
| 5 | Lindy Waters III (GSW/DET, 2024-25) | 753 | 3.44 | C8 | 0.85 |
| 6 | Aaron Nesmith (IND, 2024-25) | 1099 | 3.54 | C8 | 0.94 |
| 7 | Brandin Podziemski (GSW, 2025-26) | 2333 | 3.56 | C8 | 1.00 |
| 8 | Tim Hardaway Jr. (DET, 2024-25) | 2123 | 3.65 | C8 | 1.00 |

**Borderline** (0 members under 0.6; 5 with the most minutes)

None.

**Tracked players in this cluster**

| player-season | minutes | prob | second | prob |
|---|---|---|---|---|
| Aaron Nesmith (IND, 2024-25) | 1099 | 0.94 | C1 | 0.05 |

## C9 (30 player-seasons)

**10 most typical**

| # | player-season | minutes | prob | distance |
|---|---|---|---|---|
| 1 | DeMar DeRozan (SAC, 2024-25) | 2691 | 1.00 | 5.88 |
| 2 | DeMar DeRozan (SAC, 2025-26) | 2406 | 1.00 | 6.35 |
| 3 | Kevin Durant (HOU, 2025-26) | 2840 | 1.00 | 3.23 |
| 4 | Brandon Ingram (TOR, 2025-26) | 2566 | 1.00 | 2.77 |
| 5 | Brandon Ingram (NOP, 2024-25) | 595 | 1.00 | 3.34 |
| 6 | Khris Middleton (WAS/DAL, 2025-26) | 1417 | 1.00 | 4.57 |
| 7 | Shai Gilgeous-Alexander (OKC, 2025-26) | 2259 | 1.00 | 4.20 |
| 8 | Devin Booker (PHX, 2025-26) | 2146 | 1.00 | 4.53 |
| 9 | Kevin Durant (PHX, 2024-25) | 2242 | 1.00 | 4.70 |
| 10 | Kawhi Leonard (LAC, 2024-25) | 1180 | 1.00 | 3.34 |

**8 nearest the center** (Mahalanobis distance under this cluster's shape, members and non-members)

| # | player-season | minutes | distance | top archetype | prob |
|---|---|---|---|---|---|
| 1 | Brandon Ingram (TOR, 2025-26) | 2566 | 2.77 | C9 | 1.00 |
| 2 | Cooper Flagg (DAL, 2025-26) | 2344 | 3.00 | C9 | 0.85 |
| 3 | Jamal Murray (DEN, 2024-25) | 2338 | 3.09 | C9 | 0.66 |
| 4 | Devin Vassell (SAS, 2024-25) | 1958 | 3.22 | C2 | 0.60 |
| 5 | Kevin Durant (HOU, 2025-26) | 2840 | 3.23 | C9 | 1.00 |
| 6 | Bradley Beal (PHX, 2024-25) | 1702 | 3.27 | C1 | 0.51 |
| 7 | Jalen Williams (OKC, 2024-25) | 2162 | 3.30 | C9 | 0.45 |
| 8 | Kawhi Leonard (LAC, 2024-25) | 1180 | 3.34 | C9 | 1.00 |

**Borderline** (3 members under 0.6; 5 with the most minutes)

| player-season | minutes | prob | second archetype | prob |
|---|---|---|---|---|
| Devin Booker (PHX, 2024-25) | 2764 | 0.49 | C2 | 0.48 |
| Jalen Williams (OKC, 2024-25) | 2162 | 0.45 | C1 | 0.31 |
| Devin Vassell (SAS, 2025-26) | 2044 | 0.46 | C1 | 0.43 |

**Tracked players in this cluster**

| player-season | minutes | prob | second | prob |
|---|---|---|---|---|
| Pascal Siakam (IND, 2025-26) | 2057 | 0.67 | C13 | 0.24 |

## C10 (21 player-seasons)

**10 most typical**

| # | player-season | minutes | prob | distance |
|---|---|---|---|---|
| 1 | Victor Wembanyama (SAS, 2024-25) | 1527 | 1.00 | 7.69 |
| 2 | Jay Huff (IND, 2025-26) | 1719 | 1.00 | 4.58 |
| 3 | Victor Wembanyama (SAS, 2025-26) | 1866 | 1.00 | 6.92 |
| 4 | Myles Turner (IND, 2024-25) | 2117 | 1.00 | 1.97 |
| 5 | Chet Holmgren (OKC, 2024-25) | 815 | 1.00 | 3.56 |
| 6 | Brook Lopez (MIL, 2024-25) | 2506 | 1.00 | 3.93 |
| 7 | Jay Huff (MEM, 2024-25) | 748 | 1.00 | 4.48 |
| 8 | Myles Turner (MIL, 2025-26) | 1883 | 1.00 | 2.34 |
| 9 | Brook Lopez (LAC, 2025-26) | 1615 | 1.00 | 3.28 |
| 10 | Chet Holmgren (OKC, 2025-26) | 1997 | 1.00 | 3.11 |

**8 nearest the center** (Mahalanobis distance under this cluster's shape, members and non-members)

| # | player-season | minutes | distance | top archetype | prob |
|---|---|---|---|---|---|
| 1 | Myles Turner (IND, 2024-25) | 2117 | 1.97 | C10 | 1.00 |
| 2 | Myles Turner (MIL, 2025-26) | 1883 | 2.34 | C10 | 1.00 |
| 3 | Chet Holmgren (OKC, 2025-26) | 1997 | 3.11 | C10 | 1.00 |
| 4 | Brook Lopez (LAC, 2025-26) | 1615 | 3.28 | C10 | 1.00 |
| 5 | Alex Sarr (WAS, 2025-26) | 1274 | 3.34 | C10 | 1.00 |
| 6 | Evan Mobley (CLE, 2025-26) | 2046 | 3.42 | C10 | 0.55 |
| 7 | Alex Sarr (WAS, 2024-25) | 1814 | 3.44 | C10 | 1.00 |
| 8 | Chet Holmgren (OKC, 2024-25) | 815 | 3.56 | C10 | 1.00 |

**Borderline** (1 members under 0.6; 5 with the most minutes)

| player-season | minutes | prob | second archetype | prob |
|---|---|---|---|---|
| Evan Mobley (CLE, 2025-26) | 2046 | 0.55 | C5 | 0.44 |

**Tracked players in this cluster**

| player-season | minutes | prob | second | prob |
|---|---|---|---|---|
| Myles Turner (IND, 2024-25) | 2117 | 1.00 | C1 | 0.00 |
| Jay Huff (IND, 2025-26) | 1719 | 1.00 | C5 | 0.00 |

## C11 (21 player-seasons)

**10 most typical**

| # | player-season | minutes | prob | distance |
|---|---|---|---|---|
| 1 | Oso Ighodaro (PHX, 2024-25) | 1026 | 1.00 | 4.07 |
| 2 | Isaiah Hartenstein (OKC, 2024-25) | 1558 | 1.00 | 3.84 |
| 3 | Drew Eubanks (SAC, 2025-26) | 552 | 1.00 | 4.15 |
| 4 | Bismack Biyombo (SAS, 2024-25) | 528 | 1.00 | 3.32 |
| 5 | Ivica Zubac (LAC, 2024-25) | 2624 | 1.00 | 3.25 |
| 6 | Maxime Raynaud (SAC, 2025-26) | 1964 | 1.00 | 4.54 |
| 7 | Deandre Ayton (LAL, 2025-26) | 1958 | 1.00 | 2.40 |
| 8 | Jarrett Allen (CLE, 2025-26) | 1493 | 1.00 | 3.68 |
| 9 | Drew Eubanks (UTA/LAC, 2024-25) | 746 | 1.00 | 3.15 |
| 10 | Ivica Zubac (LAC/IND, 2025-26) | 1382 | 1.00 | 3.29 |

**8 nearest the center** (Mahalanobis distance under this cluster's shape, members and non-members)

| # | player-season | minutes | distance | top archetype | prob |
|---|---|---|---|---|---|
| 1 | Deandre Ayton (LAL, 2025-26) | 1958 | 2.40 | C11 | 1.00 |
| 2 | Jakob Poeltl (TOR, 2024-25) | 1686 | 2.45 | C11 | 1.00 |
| 3 | Drew Eubanks (UTA/LAC, 2024-25) | 746 | 3.15 | C11 | 1.00 |
| 4 | Mark Williams (CHA, 2024-25) | 1140 | 3.15 | C11 | 1.00 |
| 5 | Ivica Zubac (LAC, 2024-25) | 2624 | 3.25 | C11 | 1.00 |
| 6 | Ivica Zubac (LAC/IND, 2025-26) | 1382 | 3.29 | C11 | 1.00 |
| 7 | Brandon Clarke (MEM, 2024-25) | 1207 | 3.31 | C11 | 1.00 |
| 8 | Bismack Biyombo (SAS, 2024-25) | 528 | 3.32 | C11 | 1.00 |

**Borderline** (0 members under 0.6; 5 with the most minutes)

None.

**Tracked players in this cluster**

| player-season | minutes | prob | second | prob |
|---|---|---|---|---|
| Ivica Zubac (LAC, 2024-25) | 2624 | 1.00 | C7 | 0.00 |
| Ivica Zubac (LAC/IND, 2025-26) | 1382 | 1.00 | C7 | 0.00 |

## C12 (19 player-seasons)

**10 most typical**

| # | player-season | minutes | prob | distance |
|---|---|---|---|---|
| 1 | Jusuf Nurkić (UTA, 2025-26) | 1083 | 1.00 | 3.95 |
| 2 | Jonas Valančiūnas (WAS/SAC, 2024-25) | 1492 | 1.00 | 3.65 |
| 3 | Jusuf Nurkić (PHX/CHA, 2024-25) | 1048 | 1.00 | 3.07 |
| 4 | Domantas Sabonis (SAC, 2024-25) | 2397 | 1.00 | 4.20 |
| 5 | Karl-Anthony Towns (NYK, 2025-26) | 2322 | 1.00 | 4.79 |
| 6 | Nikola Vučević (CHI, 2024-25) | 2220 | 1.00 | 3.58 |
| 7 | Karl-Anthony Towns (NYK, 2024-25) | 2451 | 1.00 | 4.54 |
| 8 | Domantas Sabonis (SAC, 2025-26) | 564 | 1.00 | 3.97 |
| 9 | Jonas Valančiūnas (DEN, 2025-26) | 871 | 1.00 | 5.94 |
| 10 | Nikola Vučević (CHI/BOS, 2025-26) | 1818 | 0.99 | 3.92 |

**8 nearest the center** (Mahalanobis distance under this cluster's shape, members and non-members)

| # | player-season | minutes | distance | top archetype | prob |
|---|---|---|---|---|---|
| 1 | Wendell Carter Jr. (ORL, 2024-25) | 1758 | 2.34 | C12 | 0.99 |
| 2 | Jusuf Nurkić (PHX/CHA, 2024-25) | 1048 | 3.07 | C12 | 1.00 |
| 3 | Wendell Carter Jr. (ORL, 2025-26) | 2257 | 3.35 | C12 | 0.82 |
| 4 | Nikola Vučević (CHI, 2024-25) | 2220 | 3.58 | C12 | 1.00 |
| 5 | Jalen Smith (CHI, 2025-26) | 1095 | 3.59 | C12 | 0.81 |
| 6 | Jonas Valančiūnas (WAS/SAC, 2024-25) | 1492 | 3.65 | C12 | 1.00 |
| 7 | Thomas Bryant (CLE, 2025-26) | 726 | 3.66 | C5 | 0.61 |
| 8 | Zach Collins (CHI/SAS, 2024-25) | 930 | 3.71 | C5 | 0.53 |

**Borderline** (0 members under 0.6; 5 with the most minutes)

None.

**Tracked players in this cluster**

None.

## C13 (13 player-seasons)

**10 most typical**

| # | player-season | minutes | prob | distance |
|---|---|---|---|---|
| 1 | Giannis Antetokounmpo (MIL, 2025-26) | 1007 | 1.00 | 7.03 |
| 2 | Giannis Antetokounmpo (MIL, 2024-25) | 2245 | 1.00 | 4.83 |
| 3 | Nikola Jokić (DEN, 2025-26) | 2265 | 1.00 | 5.26 |
| 4 | Nikola Jokić (DEN, 2024-25) | 2452 | 1.00 | 5.20 |
| 5 | Zion Williamson (NOP, 2024-25) | 857 | 1.00 | 5.25 |
| 6 | Jimmy Butler III (GSW, 2025-26) | 1182 | 1.00 | 5.00 |
| 7 | Joel Embiid (PHI, 2024-25) | 574 | 1.00 | 4.19 |
| 8 | Jimmy Butler III (GSW/MIA, 2024-25) | 1678 | 1.00 | 5.89 |
| 9 | Joel Embiid (PHI, 2025-26) | 1201 | 0.99 | 5.02 |
| 10 | Lauri Markkanen (UTA, 2025-26) | 1443 | 0.98 | 4.40 |

**8 nearest the center** (Mahalanobis distance under this cluster's shape, members and non-members)

| # | player-season | minutes | distance | top archetype | prob |
|---|---|---|---|---|---|
| 1 | Pascal Siakam (IND, 2025-26) | 2057 | 3.87 | C9 | 0.67 |
| 2 | Pascal Siakam (IND, 2024-25) | 2485 | 3.91 | C1 | 0.85 |
| 3 | Alperen Sengun (HOU, 2025-26) | 2398 | 4.01 | C13 | 0.97 |
| 4 | Alperen Sengun (HOU, 2024-25) | 2337 | 4.10 | C13 | 0.81 |
| 5 | John Collins (UTA, 2024-25) | 1220 | 4.17 | C1 | 0.75 |
| 6 | Joel Embiid (PHI, 2024-25) | 574 | 4.19 | C13 | 1.00 |
| 7 | Lauri Markkanen (UTA, 2025-26) | 1443 | 4.40 | C13 | 0.98 |
| 8 | Julius Randle (MIN, 2025-26) | 2610 | 4.45 | C1 | 0.86 |

**Borderline** (0 members under 0.6; 5 with the most minutes)

None.

**Tracked players in this cluster**

None.

## C14 (6 player-seasons)

**10 most typical**

| # | player-season | minutes | prob | distance |
|---|---|---|---|---|
| 1 | Dwight Powell (DAL, 2025-26) | 904 | 1.00 | 8.97 |
| 2 | Dwight Powell (DAL, 2024-25) | 551 | 1.00 | 4.90 |
| 3 | Mason Plumlee (PHX, 2024-25) | 1288 | 1.00 | 5.25 |
| 4 | Steven Adams (HOU, 2025-26) | 730 | 1.00 | 6.77 |
| 5 | Moussa Cisse (DAL, 2025-26) | 530 | 0.99 | 4.82 |
| 6 | Mitchell Robinson (NYK, 2025-26) | 1175 | 0.86 | 6.25 |

**8 nearest the center** (Mahalanobis distance under this cluster's shape, members and non-members)

| # | player-season | minutes | distance | top archetype | prob |
|---|---|---|---|---|---|
| 1 | Moussa Cisse (DAL, 2025-26) | 530 | 4.82 | C14 | 0.99 |
| 2 | Dwight Powell (DAL, 2024-25) | 551 | 4.90 | C14 | 1.00 |
| 3 | Mason Plumlee (PHX, 2024-25) | 1288 | 5.25 | C14 | 1.00 |
| 4 | Isaiah Jackson (IND/LAC, 2025-26) | 908 | 5.92 | C7 | 1.00 |
| 5 | Rudy Gobert (MIN, 2025-26) | 2380 | 5.94 | C7 | 1.00 |
| 6 | Adem Bona (PHI, 2025-26) | 1234 | 5.97 | C7 | 1.00 |
| 7 | Mitchell Robinson (NYK, 2025-26) | 1175 | 6.25 | C14 | 0.86 |
| 8 | Rudy Gobert (MIN, 2024-25) | 2367 | 6.40 | C7 | 1.00 |

**Borderline** (0 members under 0.6; 5 with the most minutes)

None.

**Tracked players in this cluster**

None.
