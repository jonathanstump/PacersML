# Player reveal, k = 13 (tied covariance)

Same cluster order as profiles_blind.md. Read that file first.

- **Most typical:** highest membership probability; ties (many are 1.00) broken by smallest Mahalanobis distance to the cluster center (in SDs of that cluster's own shape).
- **8 nearest the center:** smallest Mahalanobis distance to the cluster center, whatever their top archetype.
- **Borderline:** members whose top probability is under 0.6, the 5 with the most minutes, with their second-most-likely archetype.
- **Tracked:** every Pacers player-season (any minutes for IND that season) in the cluster, plus Myles Turner 2024-25 and every Ivica Zubac season. Training seasons only (2026-27 is not projected until the model is frozen). Players under 500 minutes aren't fitted and don't appear.

## Tracked players at a glance

| player-season | minutes | top archetype | prob | second | prob |
|---|---|---|---|---|---|
| Ivica Zubac (LAC, 2024-25) | 2624 | C10 | 1.00 | C4 | 0.00 |
| Pascal Siakam (IND, 2024-25) | 2485 | C1 | 0.87 | C8 | 0.06 |
| Tyrese Haliburton (IND, 2024-25) | 2411 | C5 | 1.00 | C2 | 0.00 |
| Myles Turner (IND, 2024-25) | 2117 | C11 | 1.00 | C1 | 0.00 |
| Bennedict Mathurin (IND, 2024-25) | 2056 | C2 | 0.99 | C1 | 0.00 |
| Andrew Nembhard (IND, 2024-25) | 1840 | C3 | 0.68 | C8 | 0.25 |
| Obi Toppin (IND, 2024-25) | 1461 | C1 | 0.99 | C2 | 0.01 |
| T.J. McConnell (IND, 2024-25) | 1362 | C3 | 1.00 | C1 | 0.00 |
| Ben Sheppard (IND, 2024-25) | 1154 | C6 | 1.00 | C1 | 0.00 |
| Jarace Walker (IND, 2024-25) | 1115 | C2 | 0.95 | C1 | 0.05 |
| Aaron Nesmith (IND, 2024-25) | 1099 | C7 | 0.82 | C1 | 0.18 |
| Thomas Bryant (IND/MIA, 2024-25) | 920 | C4 | 0.97 | C1 | 0.03 |
| Pascal Siakam (IND, 2025-26) | 2057 | C12 | 0.48 | C8 | 0.35 |
| Jarace Walker (IND, 2025-26) | 1953 | C2 | 0.62 | C1 | 0.38 |
| Andrew Nembhard (IND, 2025-26) | 1786 | C3 | 0.57 | C2 | 0.32 |
| Jay Huff (IND, 2025-26) | 1719 | C11 | 1.00 | C1 | 0.00 |
| Bennedict Mathurin (IND/LAC, 2025-26) | 1620 | C2 | 0.96 | C8 | 0.02 |
| Ben Sheppard (IND, 2025-26) | 1390 | C1 | 0.98 | C2 | 0.01 |
| Ivica Zubac (LAC/IND, 2025-26) | 1382 | C10 | 1.00 | C4 | 0.00 |
| Aaron Nesmith (IND, 2025-26) | 1335 | C1 | 0.55 | C2 | 0.45 |
| T.J. McConnell (IND, 2025-26) | 963 | C3 | 1.00 | C8 | 0.00 |
| Kobe Brown (IND/LAC, 2025-26) | 947 | C1 | 0.99 | C3 | 0.00 |
| Isaiah Jackson (IND/LAC, 2025-26) | 908 | C9 | 1.00 | C13 | 0.00 |
| Micah Potter (IND, 2025-26) | 908 | C6 | 0.87 | C1 | 0.13 |
| Quenton Jackson (IND, 2025-26) | 897 | C1 | 0.76 | C2 | 0.14 |
| Ethan Thompson (IND, 2025-26) | 653 | C1 | 0.96 | C2 | 0.02 |
| Johnny Furphy (IND, 2025-26) | 643 | C1 | 0.98 | C4 | 0.01 |
| Kam Jones (IND, 2025-26) | 616 | C3 | 0.96 | C1 | 0.04 |

## C1 (246 player-seasons)

**10 most typical**

| # | player-season | minutes | prob | distance |
|---|---|---|---|---|
| 1 | Jalen Wilson (BKN, 2025-26) | 859 | 1.00 | 4.13 |
| 2 | Tidjane Salaün (CHA, 2025-26) | 558 | 1.00 | 3.76 |
| 3 | Naji Marshall (DAL, 2025-26) | 2184 | 1.00 | 4.29 |
| 4 | Jalen Wilson (BKN, 2024-25) | 2002 | 1.00 | 2.98 |
| 5 | Tosan Evbuomwan (BKN, 2024-25) | 638 | 1.00 | 2.22 |
| 6 | Ziaire Williams (BKN, 2025-26) | 1281 | 1.00 | 3.72 |
| 7 | Kelly Oubre Jr. (PHI, 2025-26) | 1574 | 1.00 | 2.60 |
| 8 | Javonte Green (DET, 2025-26) | 1417 | 1.00 | 4.30 |
| 9 | Noah Clowney (BKN, 2025-26) | 1780 | 1.00 | 3.53 |
| 10 | Bruce Brown (NOP/TOR, 2024-25) | 922 | 1.00 | 3.27 |

**8 nearest the center** (Mahalanobis distance under this cluster's shape, members and non-members)

| # | player-season | minutes | distance | top archetype | prob |
|---|---|---|---|---|---|
| 1 | Simone Fontecchio (DET, 2024-25) | 1200 | 2.19 | C1 | 0.97 |
| 2 | Cedric Coward (MEM, 2025-26) | 1598 | 2.21 | C1 | 0.95 |
| 3 | Tosan Evbuomwan (BKN, 2024-25) | 638 | 2.22 | C1 | 1.00 |
| 4 | Tristan da Silva (ORL, 2025-26) | 1869 | 2.23 | C1 | 0.95 |
| 5 | Cameron Johnson (DEN, 2025-26) | 1647 | 2.26 | C1 | 0.96 |
| 6 | Kyle Kuzma (MIL, 2025-26) | 1771 | 2.34 | C1 | 0.99 |
| 7 | Tristan da Silva (ORL, 2024-25) | 1608 | 2.44 | C1 | 0.99 |
| 8 | Moses Moody (GSW, 2024-25) | 1577 | 2.50 | C1 | 0.99 |

**Borderline** (14 members under 0.6; 5 with the most minutes)

| player-season | minutes | prob | second archetype | prob |
|---|---|---|---|---|
| Scottie Barnes (TOR, 2025-26) | 2648 | 0.33 | C3 | 0.31 |
| Jalen Williams (OKC, 2024-25) | 2162 | 0.42 | C8 | 0.32 |
| Deni Avdija (POR, 2025-26) | 2161 | 0.46 | C3 | 0.41 |
| Nickeil Alexander-Walker (MIN, 2024-25) | 2046 | 0.51 | C2 | 0.48 |
| Derik Queen (NOP, 2025-26) | 2023 | 0.59 | C3 | 0.39 |

**Tracked players in this cluster**

| player-season | minutes | prob | second | prob |
|---|---|---|---|---|
| Pascal Siakam (IND, 2024-25) | 2485 | 0.87 | C8 | 0.06 |
| Obi Toppin (IND, 2024-25) | 1461 | 0.99 | C2 | 0.01 |
| Ben Sheppard (IND, 2025-26) | 1390 | 0.98 | C2 | 0.01 |
| Aaron Nesmith (IND, 2025-26) | 1335 | 0.55 | C2 | 0.45 |
| Kobe Brown (IND/LAC, 2025-26) | 947 | 0.99 | C3 | 0.00 |
| Quenton Jackson (IND, 2025-26) | 897 | 0.76 | C2 | 0.14 |
| Ethan Thompson (IND, 2025-26) | 653 | 0.96 | C2 | 0.02 |
| Johnny Furphy (IND, 2025-26) | 643 | 0.98 | C4 | 0.01 |

## C2 (145 player-seasons)

**10 most typical**

| # | player-season | minutes | prob | distance |
|---|---|---|---|---|
| 1 | Klay Thompson (DAL, 2025-26) | 1497 | 1.00 | 4.28 |
| 2 | Zach LaVine (SAC, 2025-26) | 1224 | 1.00 | 3.21 |
| 3 | Brandon Miller (CHA, 2024-25) | 924 | 1.00 | 3.43 |
| 4 | Caleb Love (POR, 2025-26) | 985 | 1.00 | 3.66 |
| 5 | Buddy Hield (GSW, 2024-25) | 1767 | 1.00 | 2.99 |
| 6 | Reed Sheppard (HOU, 2025-26) | 2147 | 1.00 | 4.07 |
| 7 | CJ McCollum (NOP, 2024-25) | 1832 | 1.00 | 2.84 |
| 8 | Shaedon Sharpe (POR, 2024-25) | 2252 | 1.00 | 2.67 |
| 9 | CJ McCollum (ATL/WAS, 2025-26) | 2236 | 1.00 | 2.96 |
| 10 | Tyler Herro (MIA, 2025-26) | 1033 | 1.00 | 3.14 |

**8 nearest the center** (Mahalanobis distance under this cluster's shape, members and non-members)

| # | player-season | minutes | distance | top archetype | prob |
|---|---|---|---|---|---|
| 1 | Cameron Johnson (BKN, 2024-25) | 1775 | 2.01 | C2 | 0.90 |
| 2 | Quentin Grimes (DAL/PHI, 2024-25) | 1941 | 2.04 | C2 | 0.98 |
| 3 | Bogdan Bogdanović (LAC/ATL, 2024-25) | 1348 | 2.08 | C2 | 0.96 |
| 4 | VJ Edgecombe (PHI, 2025-26) | 2623 | 2.37 | C2 | 0.97 |
| 5 | Nickeil Alexander-Walker (ATL, 2025-26) | 2603 | 2.38 | C2 | 0.83 |
| 6 | Kon Knueppel (CHA, 2025-26) | 2482 | 2.43 | C2 | 0.68 |
| 7 | Quentin Grimes (PHI, 2025-26) | 2206 | 2.43 | C2 | 0.96 |
| 8 | Patrick Williams (CHI, 2024-25) | 1564 | 2.49 | C2 | 0.85 |

**Borderline** (9 members under 0.6; 5 with the most minutes)

| player-season | minutes | prob | second archetype | prob |
|---|---|---|---|---|
| Jaden McDaniels (MIN, 2025-26) | 2316 | 0.54 | C1 | 0.45 |
| De'Aaron Fox (SAC/SAS, 2024-25) | 2204 | 0.55 | C3 | 0.20 |
| Jaylen Brown (BOS, 2024-25) | 2128 | 0.51 | C1 | 0.40 |
| Tyrese Maxey (PHI, 2024-25) | 1960 | 0.55 | C5 | 0.45 |
| Duncan Robinson (MIA, 2024-25) | 1786 | 0.51 | C5 | 0.49 |

**Tracked players in this cluster**

| player-season | minutes | prob | second | prob |
|---|---|---|---|---|
| Bennedict Mathurin (IND, 2024-25) | 2056 | 0.99 | C1 | 0.00 |
| Jarace Walker (IND, 2024-25) | 1115 | 0.95 | C1 | 0.05 |
| Jarace Walker (IND, 2025-26) | 1953 | 0.62 | C1 | 0.38 |
| Bennedict Mathurin (IND/LAC, 2025-26) | 1620 | 0.96 | C8 | 0.02 |

## C3 (55 player-seasons)

**10 most typical**

| # | player-season | minutes | prob | distance |
|---|---|---|---|---|
| 1 | Elfrid Payton (NOP/CHA, 2024-25) | 511 | 1.00 | 8.31 |
| 2 | Josh Giddey (CHI, 2025-26) | 1731 | 1.00 | 4.27 |
| 3 | T.J. McConnell (IND, 2024-25) | 1362 | 1.00 | 5.77 |
| 4 | Isaiah Collier (UTA, 2025-26) | 1517 | 1.00 | 4.68 |
| 5 | Ja Morant (MEM, 2025-26) | 568 | 1.00 | 4.32 |
| 6 | Davion Mitchell (MIA, 2025-26) | 1968 | 1.00 | 3.56 |
| 7 | LeBron James (LAL, 2024-25) | 2401 | 1.00 | 4.24 |
| 8 | Cade Cunningham (DET, 2025-26) | 2099 | 1.00 | 4.28 |
| 9 | Cole Anthony (MIL, 2025-26) | 510 | 1.00 | 4.59 |
| 10 | Dennis Schröder (SAC/CLE, 2025-26) | 1696 | 1.00 | 3.50 |

**8 nearest the center** (Mahalanobis distance under this cluster's shape, members and non-members)

| # | player-season | minutes | distance | top archetype | prob |
|---|---|---|---|---|---|
| 1 | Jalen Williams (OKC, 2025-26) | 936 | 2.43 | C3 | 0.99 |
| 2 | Isaiah Collier (UTA, 2024-25) | 1839 | 2.98 | C3 | 1.00 |
| 3 | Jared Butler (PHI/WAS, 2024-25) | 1009 | 3.02 | C3 | 0.99 |
| 4 | Dennis Schröder (BKN/DET/GSW, 2024-25) | 2046 | 3.15 | C3 | 1.00 |
| 5 | Jamal Shead (TOR, 2025-26) | 1829 | 3.17 | C3 | 1.00 |
| 6 | Ayo Dosunmu (CHI/MIN, 2025-26) | 1881 | 3.22 | C3 | 0.73 |
| 7 | Russell Westbrook (DEN, 2024-25) | 1994 | 3.25 | C3 | 1.00 |
| 8 | Tyler Kolek (NYK, 2025-26) | 727 | 3.32 | C3 | 0.99 |

**Borderline** (3 members under 0.6; 5 with the most minutes)

| player-season | minutes | prob | second archetype | prob |
|---|---|---|---|---|
| Stephon Castle (SAS, 2024-25) | 2139 | 0.39 | C1 | 0.39 |
| Andrew Nembhard (IND, 2025-26) | 1786 | 0.57 | C2 | 0.32 |
| Dalano Banton (POR, 2024-25) | 1112 | 0.47 | C1 | 0.47 |

**Tracked players in this cluster**

| player-season | minutes | prob | second | prob |
|---|---|---|---|---|
| Andrew Nembhard (IND, 2024-25) | 1840 | 0.68 | C8 | 0.25 |
| T.J. McConnell (IND, 2024-25) | 1362 | 1.00 | C1 | 0.00 |
| Andrew Nembhard (IND, 2025-26) | 1786 | 0.57 | C2 | 0.32 |
| T.J. McConnell (IND, 2025-26) | 963 | 1.00 | C8 | 0.00 |
| Kam Jones (IND, 2025-26) | 616 | 0.96 | C1 | 0.04 |

## C4 (53 player-seasons)

**10 most typical**

| # | player-season | minutes | prob | distance |
|---|---|---|---|---|
| 1 | Domantas Sabonis (SAC, 2025-26) | 564 | 1.00 | 4.55 |
| 2 | Zach Collins (CHI/SAS, 2024-25) | 930 | 1.00 | 3.51 |
| 3 | Jeremy Sochan (SAS, 2024-25) | 1332 | 1.00 | 2.88 |
| 4 | Andre Drummond (PHI, 2024-25) | 726 | 1.00 | 5.32 |
| 5 | Ausar Thompson (DET, 2025-26) | 1844 | 1.00 | 4.52 |
| 6 | Jusuf Nurkić (UTA, 2025-26) | 1083 | 1.00 | 4.91 |
| 7 | Onyeka Okongwu (ATL, 2024-25) | 2034 | 1.00 | 2.28 |
| 8 | Karlo Matković (NOP, 2024-25) | 791 | 1.00 | 3.85 |
| 9 | Daniel Theis (NOP, 2024-25) | 621 | 1.00 | 4.38 |
| 10 | Ausar Thompson (DET, 2024-25) | 1294 | 1.00 | 4.07 |

**8 nearest the center** (Mahalanobis distance under this cluster's shape, members and non-members)

| # | player-season | minutes | distance | top archetype | prob |
|---|---|---|---|---|---|
| 1 | Onyeka Okongwu (ATL, 2024-25) | 2034 | 2.28 | C4 | 1.00 |
| 2 | Jonathan Mogbo (TOR, 2024-25) | 1286 | 2.36 | C4 | 1.00 |
| 3 | Jeremy Sochan (SAS, 2024-25) | 1332 | 2.88 | C4 | 1.00 |
| 4 | Wendell Carter Jr. (ORL, 2024-25) | 1758 | 3.11 | C4 | 0.99 |
| 5 | Dominick Barlow (PHI, 2025-26) | 1689 | 3.25 | C4 | 0.85 |
| 6 | Amen Thompson (HOU, 2024-25) | 2177 | 3.35 | C4 | 0.92 |
| 7 | Anthony Gill (WAS, 2025-26) | 949 | 3.39 | C4 | 1.00 |
| 8 | Thomas Bryant (CLE, 2025-26) | 726 | 3.43 | C4 | 0.98 |

**Borderline** (2 members under 0.6; 5 with the most minutes)

| player-season | minutes | prob | second archetype | prob |
|---|---|---|---|---|
| Josh Hart (NYK, 2024-25) | 2828 | 0.56 | C1 | 0.37 |
| Gui Santos (GSW, 2024-25) | 687 | 0.55 | C1 | 0.43 |

**Tracked players in this cluster**

| player-season | minutes | prob | second | prob |
|---|---|---|---|---|
| Thomas Bryant (IND/MIA, 2024-25) | 920 | 0.97 | C1 | 0.03 |

## C5 (41 player-seasons)

**10 most typical**

| # | player-season | minutes | prob | distance |
|---|---|---|---|---|
| 1 | James Harden (LAC, 2024-25) | 2789 | 1.00 | 4.79 |
| 2 | Chris Paul (SAS, 2024-25) | 2263 | 1.00 | 5.95 |
| 3 | Tyrese Haliburton (IND, 2024-25) | 2411 | 1.00 | 4.96 |
| 4 | Trae Young (ATL, 2024-25) | 2739 | 1.00 | 4.67 |
| 5 | James Harden (LAC/CLE, 2025-26) | 2370 | 1.00 | 3.82 |
| 6 | Javon Small (MEM, 2025-26) | 830 | 1.00 | 3.87 |
| 7 | Collin Gillespie (PHX, 2025-26) | 2282 | 1.00 | 3.92 |
| 8 | Jayson Tatum (BOS, 2025-26) | 522 | 1.00 | 6.57 |
| 9 | Jayson Tatum (BOS, 2024-25) | 2562 | 1.00 | 3.90 |
| 10 | Anthony Edwards (MIN, 2024-25) | 2830 | 1.00 | 3.43 |

**8 nearest the center** (Mahalanobis distance under this cluster's shape, members and non-members)

| # | player-season | minutes | distance | top archetype | prob |
|---|---|---|---|---|---|
| 1 | D'Angelo Russell (LAL/BKN, 2024-25) | 1465 | 2.32 | C5 | 0.90 |
| 2 | Bones Hyland (MIN, 2025-26) | 1177 | 2.53 | C5 | 0.98 |
| 3 | Egor Dëmin (BKN, 2025-26) | 1308 | 2.61 | C5 | 0.55 |
| 4 | Keyonte George (UTA, 2024-25) | 2108 | 2.77 | C5 | 0.89 |
| 5 | Marcus Sasser (DET, 2024-25) | 770 | 2.90 | C5 | 0.99 |
| 6 | Donovan Mitchell (CLE, 2024-25) | 2232 | 2.91 | C5 | 0.79 |
| 7 | Fred VanVleet (HOU, 2024-25) | 2046 | 3.09 | C5 | 1.00 |
| 8 | Immanuel Quickley (TOR, 2024-25) | 918 | 3.13 | C5 | 0.51 |

**Borderline** (3 members under 0.6; 5 with the most minutes)

| player-season | minutes | prob | second archetype | prob |
|---|---|---|---|---|
| Spencer Dinwiddie (DAL, 2024-25) | 2136 | 0.52 | C2 | 0.48 |
| Egor Dëmin (BKN, 2025-26) | 1308 | 0.55 | C2 | 0.45 |
| Immanuel Quickley (TOR, 2024-25) | 918 | 0.51 | C2 | 0.49 |

**Tracked players in this cluster**

| player-season | minutes | prob | second | prob |
|---|---|---|---|---|
| Tyrese Haliburton (IND, 2024-25) | 2411 | 1.00 | C2 | 0.00 |

## C6 (36 player-seasons)

**10 most typical**

| # | player-season | minutes | prob | distance |
|---|---|---|---|---|
| 1 | Micah Potter (UTA, 2024-25) | 705 | 1.00 | 3.82 |
| 2 | Josh Green (CHA, 2025-26) | 871 | 1.00 | 3.99 |
| 3 | Nicolas Batum (LAC, 2025-26) | 1266 | 1.00 | 4.08 |
| 4 | Nicolas Batum (LAC, 2024-25) | 1367 | 1.00 | 3.22 |
| 5 | Ben Sheppard (IND, 2024-25) | 1154 | 1.00 | 3.23 |
| 6 | Jarred Vanderbilt (LAL, 2025-26) | 1128 | 1.00 | 4.77 |
| 7 | Alec Burks (MIA, 2024-25) | 864 | 1.00 | 4.36 |
| 8 | Rasheer Fleming (PHX, 2025-26) | 673 | 1.00 | 4.02 |
| 9 | John Konchar (MEM, 2024-25) | 558 | 1.00 | 4.73 |
| 10 | Josh Okogie (HOU, 2025-26) | 1354 | 1.00 | 2.45 |

**8 nearest the center** (Mahalanobis distance under this cluster's shape, members and non-members)

| # | player-season | minutes | distance | top archetype | prob |
|---|---|---|---|---|---|
| 1 | Haywood Highsmith (MIA, 2024-25) | 1818 | 2.36 | C6 | 0.54 |
| 2 | Josh Okogie (HOU, 2025-26) | 1354 | 2.45 | C6 | 1.00 |
| 3 | Josh Green (CHA, 2024-25) | 1861 | 2.49 | C6 | 1.00 |
| 4 | Julian Phillips (CHI, 2024-25) | 1078 | 2.64 | C6 | 1.00 |
| 5 | Ryan Dunn (PHX, 2025-26) | 1355 | 2.80 | C6 | 1.00 |
| 6 | DaQuan Jeffries (CHA, 2024-25) | 1056 | 2.93 | C1 | 0.64 |
| 7 | Dorian Finney-Smith (LAL/BKN, 2024-25) | 1781 | 2.98 | C1 | 0.63 |
| 8 | Isaac Okoro (CLE, 2024-25) | 1053 | 3.01 | C6 | 0.99 |

**Borderline** (2 members under 0.6; 5 with the most minutes)

| player-season | minutes | prob | second archetype | prob |
|---|---|---|---|---|
| Haywood Highsmith (MIA, 2024-25) | 1818 | 0.54 | C1 | 0.46 |
| Carter Bryant (SAS, 2025-26) | 813 | 0.52 | C1 | 0.48 |

**Tracked players in this cluster**

| player-season | minutes | prob | second | prob |
|---|---|---|---|---|
| Ben Sheppard (IND, 2024-25) | 1154 | 1.00 | C1 | 0.00 |
| Micah Potter (IND, 2025-26) | 908 | 0.87 | C1 | 0.13 |

## C7 (31 player-seasons)

**10 most typical**

| # | player-season | minutes | prob | distance |
|---|---|---|---|---|
| 1 | Jaylin Williams (OKC, 2024-25) | 774 | 1.00 | 7.70 |
| 2 | Jae'Sean Tate (HOU, 2024-25) | 573 | 1.00 | 6.26 |
| 3 | Jaylin Williams (OKC, 2025-26) | 1277 | 1.00 | 6.30 |
| 4 | Garrison Mathews (ATL, 2024-25) | 830 | 1.00 | 4.27 |
| 5 | Toumani Camara (POR, 2024-25) | 2518 | 1.00 | 4.00 |
| 6 | Brandin Podziemski (GSW, 2024-25) | 1660 | 1.00 | 4.22 |
| 7 | Marcus Smart (LAL, 2025-26) | 1769 | 1.00 | 3.18 |
| 8 | Jalen Brunson (NYK, 2025-26) | 2590 | 1.00 | 5.33 |
| 9 | Isaiah Joe (OKC, 2024-25) | 1566 | 1.00 | 4.22 |
| 10 | Cameron Payne (NYK, 2024-25) | 1059 | 1.00 | 5.27 |

**8 nearest the center** (Mahalanobis distance under this cluster's shape, members and non-members)

| # | player-season | minutes | distance | top archetype | prob |
|---|---|---|---|---|---|
| 1 | Toumani Camara (POR, 2025-26) | 2695 | 2.72 | C7 | 0.99 |
| 2 | Marcus Smart (LAL, 2025-26) | 1769 | 3.18 | C7 | 1.00 |
| 3 | Brandin Podziemski (GSW, 2025-26) | 2333 | 3.33 | C7 | 1.00 |
| 4 | Kenrich Williams (OKC, 2024-25) | 1128 | 3.35 | C7 | 1.00 |
| 5 | Trey Lyles (SAC, 2024-25) | 1331 | 3.58 | C7 | 0.99 |
| 6 | Austin Reaves (LAL, 2024-25) | 2518 | 3.62 | C7 | 1.00 |
| 7 | Tim Hardaway Jr. (DET, 2024-25) | 2123 | 3.63 | C7 | 1.00 |
| 8 | Aaron Nesmith (IND, 2024-25) | 1099 | 3.69 | C7 | 0.82 |

**Borderline** (1 members under 0.6; 5 with the most minutes)

| player-season | minutes | prob | second archetype | prob |
|---|---|---|---|---|
| Isaiah Joe (OKC, 2025-26) | 1507 | 0.49 | C1 | 0.40 |

**Tracked players in this cluster**

| player-season | minutes | prob | second | prob |
|---|---|---|---|---|
| Aaron Nesmith (IND, 2024-25) | 1099 | 0.82 | C1 | 0.18 |

## C8 (31 player-seasons)

**10 most typical**

| # | player-season | minutes | prob | distance |
|---|---|---|---|---|
| 1 | DeMar DeRozan (SAC, 2025-26) | 2406 | 1.00 | 6.27 |
| 2 | DeMar DeRozan (SAC, 2024-25) | 2691 | 1.00 | 5.91 |
| 3 | Brandon Ingram (TOR, 2025-26) | 2566 | 1.00 | 2.80 |
| 4 | Kevin Durant (HOU, 2025-26) | 2840 | 1.00 | 3.25 |
| 5 | Khris Middleton (WAS/DAL, 2025-26) | 1417 | 1.00 | 4.35 |
| 6 | Brandon Ingram (NOP, 2024-25) | 595 | 1.00 | 3.19 |
| 7 | Shai Gilgeous-Alexander (OKC, 2025-26) | 2259 | 1.00 | 4.19 |
| 8 | Devin Booker (PHX, 2025-26) | 2146 | 1.00 | 4.68 |
| 9 | Kevin Durant (PHX, 2024-25) | 2242 | 1.00 | 4.73 |
| 10 | Kawhi Leonard (LAC, 2024-25) | 1180 | 1.00 | 3.34 |

**8 nearest the center** (Mahalanobis distance under this cluster's shape, members and non-members)

| # | player-season | minutes | distance | top archetype | prob |
|---|---|---|---|---|---|
| 1 | Brandon Ingram (TOR, 2025-26) | 2566 | 2.80 | C8 | 1.00 |
| 2 | Jamal Murray (DEN, 2024-25) | 2338 | 2.94 | C8 | 0.78 |
| 3 | Cooper Flagg (DAL, 2025-26) | 2344 | 2.99 | C8 | 0.85 |
| 4 | Devin Vassell (SAS, 2024-25) | 1958 | 3.00 | C8 | 0.61 |
| 5 | Bradley Beal (PHX, 2024-25) | 1702 | 3.07 | C1 | 0.46 |
| 6 | Brandon Ingram (NOP, 2024-25) | 595 | 3.19 | C8 | 1.00 |
| 7 | Kevin Durant (HOU, 2025-26) | 2840 | 3.25 | C8 | 1.00 |
| 8 | Kawhi Leonard (LAC, 2024-25) | 1180 | 3.34 | C8 | 1.00 |

**Borderline** (3 members under 0.6; 5 with the most minutes)

| player-season | minutes | prob | second archetype | prob |
|---|---|---|---|---|
| Kentavious Caldwell-Pope (ORL, 2024-25) | 2245 | 0.38 | C1 | 0.37 |
| Scottie Barnes (TOR, 2024-25) | 2134 | 0.55 | C1 | 0.30 |
| Jordan Hawkins (NOP, 2025-26) | 692 | 0.54 | C2 | 0.46 |

**Tracked players in this cluster**

None.

## C9 (29 player-seasons)

**10 most typical**

| # | player-season | minutes | prob | distance |
|---|---|---|---|---|
| 1 | Yves Missi (NOP, 2025-26) | 1297 | 1.00 | 4.88 |
| 2 | Donovan Clingan (POR, 2024-25) | 1311 | 1.00 | 3.38 |
| 3 | Steven Adams (HOU, 2025-26) | 730 | 1.00 | 6.95 |
| 4 | Steven Adams (HOU, 2024-25) | 772 | 1.00 | 6.51 |
| 5 | Clint Capela (HOU, 2025-26) | 926 | 1.00 | 3.53 |
| 6 | Mitchell Robinson (NYK, 2025-26) | 1175 | 1.00 | 5.65 |
| 7 | Walker Kessler (UTA, 2024-25) | 1740 | 1.00 | 3.56 |
| 8 | Robert Williams III (POR, 2025-26) | 1008 | 1.00 | 4.75 |
| 9 | Donovan Clingan (POR, 2025-26) | 2059 | 1.00 | 4.93 |
| 10 | Zach Edey (MEM, 2024-25) | 1416 | 1.00 | 3.43 |

**8 nearest the center** (Mahalanobis distance under this cluster's shape, members and non-members)

| # | player-season | minutes | distance | top archetype | prob |
|---|---|---|---|---|---|
| 1 | Yves Missi (NOP, 2024-25) | 1956 | 2.76 | C9 | 1.00 |
| 2 | Goga Bitadze (ORL, 2025-26) | 956 | 2.77 | C9 | 1.00 |
| 3 | Goga Bitadze (ORL, 2024-25) | 1402 | 3.12 | C9 | 1.00 |
| 4 | Moussa Diabaté (CHA, 2025-26) | 1864 | 3.18 | C9 | 1.00 |
| 5 | Donovan Clingan (POR, 2024-25) | 1311 | 3.38 | C9 | 1.00 |
| 6 | Isaiah Jackson (IND/LAC, 2025-26) | 908 | 3.39 | C9 | 1.00 |
| 7 | Zach Edey (MEM, 2024-25) | 1416 | 3.43 | C9 | 1.00 |
| 8 | Clint Capela (HOU, 2025-26) | 926 | 3.53 | C9 | 1.00 |

**Borderline** (0 members under 0.6; 5 with the most minutes)

None.

**Tracked players in this cluster**

| player-season | minutes | prob | second | prob |
|---|---|---|---|---|
| Isaiah Jackson (IND/LAC, 2025-26) | 908 | 1.00 | C13 | 0.00 |

## C10 (26 player-seasons)

**10 most typical**

| # | player-season | minutes | prob | distance |
|---|---|---|---|---|
| 1 | Bismack Biyombo (SAS, 2024-25) | 528 | 1.00 | 3.64 |
| 2 | Oso Ighodaro (PHX, 2024-25) | 1026 | 1.00 | 4.53 |
| 3 | Drew Eubanks (SAC, 2025-26) | 552 | 1.00 | 4.35 |
| 4 | Deandre Ayton (LAL, 2025-26) | 1958 | 1.00 | 2.41 |
| 5 | Isaiah Hartenstein (OKC, 2024-25) | 1558 | 1.00 | 4.08 |
| 6 | Ivica Zubac (LAC, 2024-25) | 2624 | 1.00 | 3.32 |
| 7 | Drew Eubanks (UTA/LAC, 2024-25) | 746 | 1.00 | 3.23 |
| 8 | Jarrett Allen (CLE, 2025-26) | 1493 | 1.00 | 3.65 |
| 9 | Maxime Raynaud (SAC, 2025-26) | 1964 | 1.00 | 4.90 |
| 10 | Ivica Zubac (LAC/IND, 2025-26) | 1382 | 1.00 | 3.24 |

**8 nearest the center** (Mahalanobis distance under this cluster's shape, members and non-members)

| # | player-season | minutes | distance | top archetype | prob |
|---|---|---|---|---|---|
| 1 | Deandre Ayton (LAL, 2025-26) | 1958 | 2.41 | C10 | 1.00 |
| 2 | Jakob Poeltl (TOR, 2024-25) | 1686 | 2.73 | C10 | 1.00 |
| 3 | Mark Williams (CHA, 2024-25) | 1140 | 2.92 | C10 | 1.00 |
| 4 | Drew Eubanks (UTA/LAC, 2024-25) | 746 | 3.23 | C10 | 1.00 |
| 5 | Mark Williams (PHX, 2025-26) | 1416 | 3.23 | C10 | 0.98 |
| 6 | Ivica Zubac (LAC/IND, 2025-26) | 1382 | 3.24 | C10 | 1.00 |
| 7 | Ivica Zubac (LAC, 2024-25) | 2624 | 3.32 | C10 | 1.00 |
| 8 | Brandon Clarke (MEM, 2024-25) | 1207 | 3.49 | C10 | 1.00 |

**Borderline** (0 members under 0.6; 5 with the most minutes)

None.

**Tracked players in this cluster**

| player-season | minutes | prob | second | prob |
|---|---|---|---|---|
| Ivica Zubac (LAC, 2024-25) | 2624 | 1.00 | C4 | 0.00 |
| Ivica Zubac (LAC/IND, 2025-26) | 1382 | 1.00 | C4 | 0.00 |

## C11 (24 player-seasons)

**10 most typical**

| # | player-season | minutes | prob | distance |
|---|---|---|---|---|
| 1 | Victor Wembanyama (SAS, 2024-25) | 1527 | 1.00 | 7.89 |
| 2 | Jay Huff (IND, 2025-26) | 1719 | 1.00 | 4.57 |
| 3 | Chet Holmgren (OKC, 2024-25) | 815 | 1.00 | 3.26 |
| 4 | Myles Turner (IND, 2024-25) | 2117 | 1.00 | 2.01 |
| 5 | Victor Wembanyama (SAS, 2025-26) | 1866 | 1.00 | 7.08 |
| 6 | Jay Huff (MEM, 2024-25) | 748 | 1.00 | 4.33 |
| 7 | Brook Lopez (MIL, 2024-25) | 2506 | 1.00 | 3.81 |
| 8 | Myles Turner (MIL, 2025-26) | 1883 | 1.00 | 2.28 |
| 9 | Chet Holmgren (OKC, 2025-26) | 1997 | 1.00 | 2.91 |
| 10 | Brook Lopez (LAC, 2025-26) | 1615 | 1.00 | 3.33 |

**8 nearest the center** (Mahalanobis distance under this cluster's shape, members and non-members)

| # | player-season | minutes | distance | top archetype | prob |
|---|---|---|---|---|---|
| 1 | Myles Turner (IND, 2024-25) | 2117 | 2.01 | C11 | 1.00 |
| 2 | Myles Turner (MIL, 2025-26) | 1883 | 2.28 | C11 | 1.00 |
| 3 | Chet Holmgren (OKC, 2025-26) | 1997 | 2.91 | C11 | 1.00 |
| 4 | Evan Mobley (CLE, 2025-26) | 2046 | 3.18 | C11 | 0.70 |
| 5 | Alex Sarr (WAS, 2025-26) | 1274 | 3.22 | C11 | 1.00 |
| 6 | Chet Holmgren (OKC, 2024-25) | 815 | 3.26 | C11 | 1.00 |
| 7 | Alex Sarr (WAS, 2024-25) | 1814 | 3.31 | C11 | 1.00 |
| 8 | Brook Lopez (LAC, 2025-26) | 1615 | 3.33 | C11 | 1.00 |

**Borderline** (1 members under 0.6; 5 with the most minutes)

| player-season | minutes | prob | second archetype | prob |
|---|---|---|---|---|
| Peyton Watson (DEN, 2024-25) | 1600 | 0.57 | C4 | 0.35 |

**Tracked players in this cluster**

| player-season | minutes | prob | second | prob |
|---|---|---|---|---|
| Myles Turner (IND, 2024-25) | 2117 | 1.00 | C1 | 0.00 |
| Jay Huff (IND, 2025-26) | 1719 | 1.00 | C1 | 0.00 |

## C12 (18 player-seasons)

**10 most typical**

| # | player-season | minutes | prob | distance |
|---|---|---|---|---|
| 1 | Giannis Antetokounmpo (MIL, 2025-26) | 1007 | 1.00 | 7.02 |
| 2 | Nikola Jokić (DEN, 2025-26) | 2265 | 1.00 | 5.50 |
| 3 | Giannis Antetokounmpo (MIL, 2024-25) | 2245 | 1.00 | 4.91 |
| 4 | Zion Williamson (NOP, 2024-25) | 857 | 1.00 | 5.01 |
| 5 | Nikola Jokić (DEN, 2024-25) | 2452 | 1.00 | 5.65 |
| 6 | Karl-Anthony Towns (NYK, 2025-26) | 2322 | 1.00 | 4.97 |
| 7 | Jimmy Butler III (GSW, 2025-26) | 1182 | 1.00 | 4.97 |
| 8 | Joel Embiid (PHI, 2024-25) | 574 | 1.00 | 4.39 |
| 9 | Anthony Davis (DAL, 2025-26) | 626 | 1.00 | 5.17 |
| 10 | Jimmy Butler III (GSW/MIA, 2024-25) | 1678 | 1.00 | 5.87 |

**8 nearest the center** (Mahalanobis distance under this cluster's shape, members and non-members)

| # | player-season | minutes | distance | top archetype | prob |
|---|---|---|---|---|---|
| 1 | John Collins (UTA, 2024-25) | 1220 | 3.56 | C1 | 0.65 |
| 2 | Pascal Siakam (IND, 2025-26) | 2057 | 3.69 | C12 | 0.48 |
| 3 | Pascal Siakam (IND, 2024-25) | 2485 | 3.73 | C1 | 0.87 |
| 4 | Alperen Sengun (HOU, 2025-26) | 2398 | 3.96 | C12 | 0.96 |
| 5 | Alperen Sengun (HOU, 2024-25) | 2337 | 4.00 | C12 | 0.93 |
| 6 | Julius Randle (MIN, 2025-26) | 2610 | 4.15 | C1 | 0.84 |
| 7 | Lauri Markkanen (UTA, 2025-26) | 1443 | 4.32 | C12 | 0.98 |
| 8 | Joel Embiid (PHI, 2024-25) | 574 | 4.39 | C12 | 1.00 |

**Borderline** (1 members under 0.6; 5 with the most minutes)

| player-season | minutes | prob | second archetype | prob |
|---|---|---|---|---|
| Pascal Siakam (IND, 2025-26) | 2057 | 0.48 | C8 | 0.35 |

**Tracked players in this cluster**

| player-season | minutes | prob | second | prob |
|---|---|---|---|---|
| Pascal Siakam (IND, 2025-26) | 2057 | 0.48 | C8 | 0.35 |

## C13 (15 player-seasons)

**10 most typical**

| # | player-season | minutes | prob | distance |
|---|---|---|---|---|
| 1 | Dwight Powell (DAL, 2025-26) | 904 | 1.00 | 11.84 |
| 2 | Dwight Powell (DAL, 2024-25) | 551 | 1.00 | 5.54 |
| 3 | Jaxson Hayes (LAL, 2025-26) | 1207 | 1.00 | 2.73 |
| 4 | Jericho Sims (MIL, 2025-26) | 1318 | 1.00 | 4.67 |
| 5 | Mason Plumlee (PHX, 2024-25) | 1288 | 1.00 | 4.89 |
| 6 | Rudy Gobert (MIN, 2024-25) | 2367 | 1.00 | 2.23 |
| 7 | Jaxson Hayes (LAL, 2024-25) | 1059 | 1.00 | 4.06 |
| 8 | DeAndre Jordan (DEN, 2024-25) | 691 | 1.00 | 3.18 |
| 9 | Jericho Sims (NYK/MIL, 2024-25) | 607 | 1.00 | 5.42 |
| 10 | Rudy Gobert (MIN, 2025-26) | 2380 | 1.00 | 3.32 |

**8 nearest the center** (Mahalanobis distance under this cluster's shape, members and non-members)

| # | player-season | minutes | distance | top archetype | prob |
|---|---|---|---|---|---|
| 1 | Rudy Gobert (MIN, 2024-25) | 2367 | 2.23 | C13 | 1.00 |
| 2 | Jaxson Hayes (LAL, 2025-26) | 1207 | 2.73 | C13 | 1.00 |
| 3 | DeAndre Jordan (DEN, 2024-25) | 691 | 3.18 | C13 | 1.00 |
| 4 | Rudy Gobert (MIN, 2025-26) | 2380 | 3.32 | C13 | 1.00 |
| 5 | Neemias Queta (BOS, 2024-25) | 835 | 3.55 | C13 | 0.88 |
| 6 | Richaun Holmes (WAS, 2024-25) | 508 | 3.56 | C13 | 0.70 |
| 7 | Luke Kornet (SAS, 2025-26) | 1399 | 3.86 | C13 | 0.99 |
| 8 | Daniel Gafford (DAL, 2025-26) | 1195 | 3.96 | C9 | 0.83 |

**Borderline** (0 members under 0.6; 5 with the most minutes)

None.

**Tracked players in this cluster**

None.
