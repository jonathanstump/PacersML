# Player reveal, k = 12 (tied covariance)

Same cluster order as profiles_blind.md. Read that file first.

- **Most typical:** highest membership probability; ties (many are 1.00) broken by smallest Mahalanobis distance to the cluster center (in SDs of that cluster's own shape).
- **8 nearest the center:** smallest Mahalanobis distance to the cluster center, whatever their top archetype.
- **Borderline:** members whose top probability is under 0.6, the 5 with the most minutes, with their second-most-likely archetype.
- **Tracked:** every Pacers player-season (any minutes for IND that season) in the cluster, plus Myles Turner 2024-25 and every Ivica Zubac season. Training seasons only (2026-27 is not projected until the model is frozen). Players under 500 minutes aren't fitted and don't appear.

## Tracked players at a glance

| player-season | minutes | top archetype | prob | second | prob |
|---|---|---|---|---|---|
| Ivica Zubac (LAC, 2024-25) | 2624 | C12 | 1.00 | C5 | 0.00 |
| Pascal Siakam (IND, 2024-25) | 2485 | C1 | 0.78 | C11 | 0.21 |
| Tyrese Haliburton (IND, 2024-25) | 2411 | C6 | 1.00 | C2 | 0.00 |
| Myles Turner (IND, 2024-25) | 2117 | C10 | 1.00 | C5 | 0.00 |
| Bennedict Mathurin (IND, 2024-25) | 2056 | C1 | 0.99 | C2 | 0.01 |
| Andrew Nembhard (IND, 2024-25) | 1840 | C4 | 0.86 | C1 | 0.13 |
| Obi Toppin (IND, 2024-25) | 1461 | C1 | 0.96 | C3 | 0.03 |
| T.J. McConnell (IND, 2024-25) | 1362 | C4 | 1.00 | C2 | 0.00 |
| Ben Sheppard (IND, 2024-25) | 1154 | C8 | 1.00 | C3 | 0.00 |
| Jarace Walker (IND, 2024-25) | 1115 | C1 | 0.95 | C3 | 0.04 |
| Aaron Nesmith (IND, 2024-25) | 1099 | C9 | 0.90 | C1 | 0.09 |
| Thomas Bryant (IND/MIA, 2024-25) | 920 | C5 | 0.97 | C3 | 0.01 |
| Pascal Siakam (IND, 2025-26) | 2057 | C11 | 0.97 | C1 | 0.03 |
| Jarace Walker (IND, 2025-26) | 1953 | C1 | 1.00 | C2 | 0.00 |
| Andrew Nembhard (IND, 2025-26) | 1786 | C4 | 0.95 | C11 | 0.03 |
| Jay Huff (IND, 2025-26) | 1719 | C10 | 1.00 | C5 | 0.00 |
| Bennedict Mathurin (IND/LAC, 2025-26) | 1620 | C1 | 0.96 | C2 | 0.04 |
| Ben Sheppard (IND, 2025-26) | 1390 | C1 | 0.98 | C3 | 0.01 |
| Ivica Zubac (LAC/IND, 2025-26) | 1382 | C12 | 1.00 | C5 | 0.00 |
| Aaron Nesmith (IND, 2025-26) | 1335 | C1 | 1.00 | C3 | 0.00 |
| T.J. McConnell (IND, 2025-26) | 963 | C4 | 1.00 | C11 | 0.00 |
| Kobe Brown (IND/LAC, 2025-26) | 947 | C1 | 0.99 | C3 | 0.01 |
| Isaiah Jackson (IND/LAC, 2025-26) | 908 | C7 | 1.00 | C5 | 0.00 |
| Micah Potter (IND, 2025-26) | 908 | C8 | 0.62 | C1 | 0.27 |
| Quenton Jackson (IND, 2025-26) | 897 | C1 | 0.91 | C4 | 0.04 |
| Ethan Thompson (IND, 2025-26) | 653 | C1 | 0.87 | C8 | 0.06 |
| Johnny Furphy (IND, 2025-26) | 643 | C1 | 0.54 | C3 | 0.46 |
| Kam Jones (IND, 2025-26) | 616 | C4 | 0.99 | C1 | 0.01 |

## C1 (271 player-seasons)

**10 most typical**

| # | player-season | minutes | prob | distance |
|---|---|---|---|---|
| 1 | Corey Kispert (WAS, 2024-25) | 1572 | 1.00 | 3.75 |
| 2 | Corey Kispert (ATL/WAS, 2025-26) | 1059 | 1.00 | 3.52 |
| 3 | Eric Gordon (PHI, 2024-25) | 768 | 1.00 | 5.65 |
| 4 | Aaron Nesmith (IND, 2025-26) | 1335 | 1.00 | 3.70 |
| 5 | Santi Aldama (MEM, 2025-26) | 1198 | 1.00 | 3.98 |
| 6 | Julian Strawther (DEN, 2024-25) | 1356 | 1.00 | 4.22 |
| 7 | Jarace Walker (IND, 2025-26) | 1953 | 1.00 | 3.14 |
| 8 | Tim Hardaway Jr. (DEN, 2025-26) | 2102 | 1.00 | 3.80 |
| 9 | Lauri Markkanen (UTA, 2024-25) | 1476 | 1.00 | 4.20 |
| 10 | Bobby Portis (MIL, 2025-26) | 1593 | 1.00 | 5.92 |

**8 nearest the center** (Mahalanobis distance under this cluster's shape, members and non-members)

| # | player-season | minutes | distance | top archetype | prob |
|---|---|---|---|---|---|
| 1 | Cameron Johnson (DEN, 2025-26) | 1647 | 2.14 | C1 | 1.00 |
| 2 | Kon Knueppel (CHA, 2025-26) | 2482 | 2.15 | C1 | 1.00 |
| 3 | Cedric Coward (MEM, 2025-26) | 1598 | 2.18 | C1 | 0.99 |
| 4 | Cameron Johnson (BKN, 2024-25) | 1775 | 2.18 | C1 | 0.97 |
| 5 | Simone Fontecchio (DET, 2024-25) | 1200 | 2.24 | C1 | 0.97 |
| 6 | Kyle Kuzma (MIL, 2025-26) | 1771 | 2.27 | C1 | 1.00 |
| 7 | Tristan da Silva (ORL, 2025-26) | 1869 | 2.28 | C1 | 0.92 |
| 8 | Aaron Wiggins (OKC, 2025-26) | 1414 | 2.42 | C1 | 0.96 |

**Borderline** (19 members under 0.6; 5 with the most minutes)

| player-season | minutes | prob | second archetype | prob |
|---|---|---|---|---|
| Dyson Daniels (ATL, 2025-26) | 2520 | 0.58 | C4 | 0.34 |
| Stephon Castle (SAS, 2024-25) | 2139 | 0.45 | C4 | 0.31 |
| Kelly Oubre Jr. (PHI, 2024-25) | 2044 | 0.57 | C3 | 0.43 |
| Brandon Miller (CHA, 2025-26) | 1902 | 0.58 | C2 | 0.42 |
| Keyonte George (UTA, 2025-26) | 1786 | 0.58 | C2 | 0.24 |

**Tracked players in this cluster**

| player-season | minutes | prob | second | prob |
|---|---|---|---|---|
| Pascal Siakam (IND, 2024-25) | 2485 | 0.78 | C11 | 0.21 |
| Bennedict Mathurin (IND, 2024-25) | 2056 | 0.99 | C2 | 0.01 |
| Obi Toppin (IND, 2024-25) | 1461 | 0.96 | C3 | 0.03 |
| Jarace Walker (IND, 2024-25) | 1115 | 0.95 | C3 | 0.04 |
| Jarace Walker (IND, 2025-26) | 1953 | 1.00 | C2 | 0.00 |
| Bennedict Mathurin (IND/LAC, 2025-26) | 1620 | 0.96 | C2 | 0.04 |
| Ben Sheppard (IND, 2025-26) | 1390 | 0.98 | C3 | 0.01 |
| Aaron Nesmith (IND, 2025-26) | 1335 | 1.00 | C3 | 0.00 |
| Kobe Brown (IND/LAC, 2025-26) | 947 | 0.99 | C3 | 0.01 |
| Quenton Jackson (IND, 2025-26) | 897 | 0.91 | C4 | 0.04 |
| Ethan Thompson (IND, 2025-26) | 653 | 0.87 | C8 | 0.06 |
| Johnny Furphy (IND, 2025-26) | 643 | 0.54 | C3 | 0.46 |

## C2 (77 player-seasons)

**10 most typical**

| # | player-season | minutes | prob | distance |
|---|---|---|---|---|
| 1 | Jalen Green (PHX, 2025-26) | 828 | 1.00 | 3.90 |
| 2 | Tyrese Maxey (PHI, 2024-25) | 1960 | 1.00 | 2.73 |
| 3 | Jalen Green (HOU, 2024-25) | 2636 | 1.00 | 3.08 |
| 4 | Anthony Edwards (MIN, 2025-26) | 2137 | 1.00 | 3.56 |
| 5 | Paul George (PHI, 2024-25) | 1334 | 1.00 | 4.31 |
| 6 | Donovan Mitchell (CLE, 2025-26) | 2316 | 1.00 | 2.21 |
| 7 | Luka Dončić (LAL, 2025-26) | 2289 | 1.00 | 6.30 |
| 8 | Donovan Mitchell (CLE, 2024-25) | 2232 | 1.00 | 2.12 |
| 9 | Shaedon Sharpe (POR, 2025-26) | 1443 | 1.00 | 3.83 |
| 10 | Tyrese Maxey (PHI, 2025-26) | 2661 | 1.00 | 2.68 |

**8 nearest the center** (Mahalanobis distance under this cluster's shape, members and non-members)

| # | player-season | minutes | distance | top archetype | prob |
|---|---|---|---|---|---|
| 1 | Quentin Grimes (DAL/PHI, 2024-25) | 1941 | 2.03 | C2 | 0.65 |
| 2 | Kyrie Irving (DAL, 2024-25) | 1804 | 2.10 | C2 | 0.95 |
| 3 | Donovan Mitchell (CLE, 2024-25) | 2232 | 2.12 | C2 | 1.00 |
| 4 | Donovan Mitchell (CLE, 2025-26) | 2316 | 2.21 | C2 | 1.00 |
| 5 | Shaedon Sharpe (POR, 2024-25) | 2252 | 2.37 | C2 | 0.91 |
| 6 | Coby White (CHI, 2024-25) | 2416 | 2.46 | C2 | 0.93 |
| 7 | De'Aaron Fox (SAC/SAS, 2024-25) | 2204 | 2.49 | C2 | 0.92 |
| 8 | Tyrese Maxey (PHI, 2025-26) | 2661 | 2.68 | C2 | 1.00 |

**Borderline** (10 members under 0.6; 5 with the most minutes)

| player-season | minutes | prob | second archetype | prob |
|---|---|---|---|---|
| Darius Garland (CLE, 2024-25) | 2301 | 0.59 | C4 | 0.30 |
| Malik Monk (SAC, 2024-25) | 2019 | 0.45 | C1 | 0.30 |
| Malik Monk (SAC, 2025-26) | 1364 | 0.48 | C1 | 0.32 |
| Darius Garland (CLE/LAC, 2025-26) | 1316 | 0.49 | C4 | 0.41 |
| De'Anthony Melton (GSW, 2025-26) | 1125 | 0.58 | C1 | 0.26 |

**Tracked players in this cluster**

None.

## C3 (60 player-seasons)

**10 most typical**

| # | player-season | minutes | prob | distance |
|---|---|---|---|---|
| 1 | Jaylen Clark (MIN, 2024-25) | 514 | 1.00 | 3.63 |
| 2 | John Konchar (UTA/MEM, 2025-26) | 1115 | 1.00 | 4.02 |
| 3 | Cam Reddish (LAL, 2024-25) | 589 | 1.00 | 5.22 |
| 4 | Nae'Qwan Tomlin (CLE, 2025-26) | 998 | 0.99 | 4.28 |
| 5 | Kris Dunn (LAC, 2024-25) | 1783 | 0.99 | 4.30 |
| 6 | Ronald Holland II (DET, 2025-26) | 1527 | 0.99 | 3.01 |
| 7 | Josh Okogie (PHX/CHA, 2024-25) | 625 | 0.99 | 5.36 |
| 8 | Mouhamed Gueye (ATL, 2024-25) | 511 | 0.99 | 4.95 |
| 9 | Jamir Watkins (WAS, 2025-26) | 1012 | 0.99 | 2.83 |
| 10 | Javonte Green (DET, 2025-26) | 1417 | 0.98 | 3.85 |

**8 nearest the center** (Mahalanobis distance under this cluster's shape, members and non-members)

| # | player-season | minutes | distance | top archetype | prob |
|---|---|---|---|---|---|
| 1 | Jaden McDaniels (MIN, 2024-25) | 2582 | 2.26 | C3 | 0.69 |
| 2 | Taylor Hendricks (MEM/UTA, 2025-26) | 1118 | 2.50 | C3 | 0.56 |
| 3 | Haywood Highsmith (MIA, 2024-25) | 1818 | 2.50 | C3 | 0.62 |
| 4 | Javonte Green (NOP/CLE, 2024-25) | 1258 | 2.55 | C3 | 0.97 |
| 5 | Jake LaRavia (LAL, 2025-26) | 2061 | 2.55 | C3 | 0.97 |
| 6 | Derrick Jones Jr. (LAC, 2024-25) | 1873 | 2.67 | C3 | 0.90 |
| 7 | Bruce Brown (DEN, 2025-26) | 1972 | 2.68 | C3 | 0.63 |
| 8 | Tristan da Silva (ORL, 2025-26) | 1869 | 2.70 | C1 | 0.92 |

**Borderline** (4 members under 0.6; 5 with the most minutes)

| player-season | minutes | prob | second archetype | prob |
|---|---|---|---|---|
| OG Anunoby (NYK, 2025-26) | 2224 | 0.52 | C1 | 0.45 |
| Herbert Jones (NOP, 2025-26) | 1588 | 0.60 | C1 | 0.40 |
| Taylor Hendricks (MEM/UTA, 2025-26) | 1118 | 0.56 | C1 | 0.42 |
| Chris Boucher (TOR, 2024-25) | 862 | 0.48 | C1 | 0.47 |

**Tracked players in this cluster**

None.

## C4 (55 player-seasons)

**10 most typical**

| # | player-season | minutes | prob | distance |
|---|---|---|---|---|
| 1 | Elfrid Payton (NOP/CHA, 2024-25) | 511 | 1.00 | 8.18 |
| 2 | T.J. McConnell (IND, 2025-26) | 963 | 1.00 | 7.33 |
| 3 | Isaiah Collier (UTA, 2025-26) | 1517 | 1.00 | 4.50 |
| 4 | Ryan Nembhard (DAL, 2025-26) | 1171 | 1.00 | 4.78 |
| 5 | T.J. McConnell (IND, 2024-25) | 1362 | 1.00 | 5.57 |
| 6 | Josh Giddey (CHI, 2025-26) | 1731 | 1.00 | 4.29 |
| 7 | Davion Mitchell (MIA, 2025-26) | 1968 | 1.00 | 3.60 |
| 8 | Dennis Schröder (SAC/CLE, 2025-26) | 1696 | 1.00 | 3.37 |
| 9 | Jamal Shead (TOR, 2025-26) | 1829 | 1.00 | 3.15 |
| 10 | Ja Morant (MEM, 2025-26) | 568 | 1.00 | 4.41 |

**8 nearest the center** (Mahalanobis distance under this cluster's shape, members and non-members)

| # | player-season | minutes | distance | top archetype | prob |
|---|---|---|---|---|---|
| 1 | Jalen Williams (OKC, 2025-26) | 936 | 2.53 | C4 | 0.99 |
| 2 | Isaiah Collier (UTA, 2024-25) | 1839 | 2.74 | C4 | 1.00 |
| 3 | Jared Butler (PHI/WAS, 2024-25) | 1009 | 2.82 | C4 | 1.00 |
| 4 | Dennis Schröder (BKN/DET/GSW, 2024-25) | 2046 | 2.99 | C4 | 1.00 |
| 5 | Tyler Kolek (NYK, 2025-26) | 727 | 3.15 | C4 | 1.00 |
| 6 | Jamal Shead (TOR, 2025-26) | 1829 | 3.15 | C4 | 1.00 |
| 7 | Malik Monk (SAC, 2024-25) | 2019 | 3.24 | C2 | 0.45 |
| 8 | Russell Westbrook (DEN, 2024-25) | 1994 | 3.29 | C4 | 1.00 |

**Borderline** (3 members under 0.6; 5 with the most minutes)

| player-season | minutes | prob | second archetype | prob |
|---|---|---|---|---|
| Scoot Henderson (POR, 2024-25) | 1731 | 0.54 | C2 | 0.43 |
| Dalano Banton (POR, 2024-25) | 1112 | 0.53 | C1 | 0.33 |
| Jalen Pickett (DEN, 2024-25) | 632 | 0.43 | C6 | 0.32 |

**Tracked players in this cluster**

| player-season | minutes | prob | second | prob |
|---|---|---|---|---|
| Andrew Nembhard (IND, 2024-25) | 1840 | 0.86 | C1 | 0.13 |
| T.J. McConnell (IND, 2024-25) | 1362 | 1.00 | C2 | 0.00 |
| Andrew Nembhard (IND, 2025-26) | 1786 | 0.95 | C11 | 0.03 |
| T.J. McConnell (IND, 2025-26) | 963 | 1.00 | C11 | 0.00 |
| Kam Jones (IND, 2025-26) | 616 | 0.99 | C1 | 0.01 |

## C5 (49 player-seasons)

**10 most typical**

| # | player-season | minutes | prob | distance |
|---|---|---|---|---|
| 1 | Jonas Valančiūnas (WAS/SAC, 2024-25) | 1492 | 1.00 | 3.94 |
| 2 | Andre Drummond (PHI, 2024-25) | 726 | 1.00 | 5.35 |
| 3 | Day'Ron Sharpe (BKN, 2025-26) | 1160 | 1.00 | 4.73 |
| 4 | Jock Landale (MEM/ATL, 2025-26) | 1506 | 1.00 | 4.02 |
| 5 | Jonas Valančiūnas (DEN, 2025-26) | 871 | 1.00 | 5.94 |
| 6 | Domantas Sabonis (SAC, 2025-26) | 564 | 1.00 | 4.42 |
| 7 | Zach Collins (CHI/SAS, 2024-25) | 930 | 1.00 | 3.09 |
| 8 | Domantas Sabonis (SAC, 2024-25) | 2397 | 1.00 | 4.92 |
| 9 | Jusuf Nurkić (UTA, 2025-26) | 1083 | 1.00 | 4.77 |
| 10 | Onyeka Okongwu (ATL, 2024-25) | 2034 | 1.00 | 2.40 |

**8 nearest the center** (Mahalanobis distance under this cluster's shape, members and non-members)

| # | player-season | minutes | distance | top archetype | prob |
|---|---|---|---|---|---|
| 1 | Onyeka Okongwu (ATL, 2024-25) | 2034 | 2.40 | C5 | 1.00 |
| 2 | Wendell Carter Jr. (ORL, 2024-25) | 1758 | 2.89 | C5 | 1.00 |
| 3 | Jonathan Mogbo (TOR, 2024-25) | 1286 | 2.91 | C5 | 0.98 |
| 4 | Zach Collins (CHI/SAS, 2024-25) | 930 | 3.09 | C5 | 1.00 |
| 5 | Jeremy Sochan (SAS, 2024-25) | 1332 | 3.24 | C5 | 0.99 |
| 6 | Thomas Bryant (CLE, 2025-26) | 726 | 3.31 | C5 | 0.98 |
| 7 | Wendell Carter Jr. (ORL, 2025-26) | 2257 | 3.49 | C5 | 0.95 |
| 8 | Precious Achiuwa (SAC, 2025-26) | 1745 | 3.58 | C5 | 1.00 |

**Borderline** (2 members under 0.6; 5 with the most minutes)

| player-season | minutes | prob | second archetype | prob |
|---|---|---|---|---|
| Amen Thompson (HOU, 2025-26) | 2953 | 0.50 | C1 | 0.46 |
| Dominick Barlow (PHI, 2025-26) | 1689 | 0.44 | C3 | 0.43 |

**Tracked players in this cluster**

| player-season | minutes | prob | second | prob |
|---|---|---|---|---|
| Thomas Bryant (IND/MIA, 2024-25) | 920 | 0.97 | C3 | 0.01 |

## C6 (45 player-seasons)

**10 most typical**

| # | player-season | minutes | prob | distance |
|---|---|---|---|---|
| 1 | Tyrese Haliburton (IND, 2024-25) | 2411 | 1.00 | 4.69 |
| 2 | Chris Paul (SAS, 2024-25) | 2263 | 1.00 | 5.89 |
| 3 | Cam Spencer (MEM, 2025-26) | 1714 | 1.00 | 3.65 |
| 4 | Mike Conley (MIN, 2024-25) | 1724 | 1.00 | 4.55 |
| 5 | Javon Small (MEM, 2025-26) | 830 | 1.00 | 3.83 |
| 6 | Mike Conley (MIN, 2025-26) | 991 | 1.00 | 5.10 |
| 7 | Collin Gillespie (PHX, 2025-26) | 2282 | 1.00 | 3.87 |
| 8 | James Harden (LAC, 2024-25) | 2789 | 1.00 | 5.33 |
| 9 | Lonzo Ball (CLE, 2025-26) | 728 | 1.00 | 4.35 |
| 10 | Trae Young (ATL, 2024-25) | 2739 | 1.00 | 5.32 |

**8 nearest the center** (Mahalanobis distance under this cluster's shape, members and non-members)

| # | player-season | minutes | distance | top archetype | prob |
|---|---|---|---|---|---|
| 1 | D'Angelo Russell (LAL/BKN, 2024-25) | 1465 | 2.27 | C6 | 0.89 |
| 2 | Egor Dëmin (BKN, 2025-26) | 1308 | 2.41 | C6 | 0.89 |
| 3 | Walter Clayton Jr. (UTA/MEM, 2025-26) | 1411 | 2.75 | C6 | 0.98 |
| 4 | Bones Hyland (MIN, 2025-26) | 1177 | 2.78 | C6 | 0.90 |
| 5 | Jrue Holiday (BOS, 2024-25) | 1866 | 2.81 | C6 | 0.56 |
| 6 | Keyonte George (UTA, 2024-25) | 2108 | 2.91 | C6 | 0.95 |
| 7 | Marcus Sasser (DET, 2024-25) | 770 | 2.94 | C6 | 0.95 |
| 8 | Miles McBride (NYK, 2024-25) | 1547 | 2.99 | C6 | 0.34 |

**Borderline** (5 members under 0.6; 5 with the most minutes)

| player-season | minutes | prob | second archetype | prob |
|---|---|---|---|---|
| Jrue Holiday (BOS, 2024-25) | 1866 | 0.56 | C1 | 0.40 |
| Duncan Robinson (MIA, 2024-25) | 1786 | 0.59 | C1 | 0.37 |
| Donte DiVincenzo (MIN, 2024-25) | 1574 | 0.43 | C1 | 0.39 |
| Miles McBride (NYK, 2024-25) | 1547 | 0.34 | C2 | 0.32 |
| Jose Alvarado (NOP, 2024-25) | 1366 | 0.57 | C2 | 0.32 |

**Tracked players in this cluster**

| player-season | minutes | prob | second | prob |
|---|---|---|---|---|
| Tyrese Haliburton (IND, 2024-25) | 2411 | 1.00 | C2 | 0.00 |

## C7 (45 player-seasons)

**10 most typical**

| # | player-season | minutes | prob | distance |
|---|---|---|---|---|
| 1 | Mitchell Robinson (NYK, 2025-26) | 1175 | 1.00 | 6.25 |
| 2 | Moussa Cisse (DAL, 2025-26) | 530 | 1.00 | 5.44 |
| 3 | Dwight Powell (DAL, 2025-26) | 904 | 1.00 | 12.57 |
| 4 | Adem Bona (PHI, 2025-26) | 1234 | 1.00 | 4.00 |
| 5 | Walker Kessler (UTA, 2024-25) | 1740 | 1.00 | 4.10 |
| 6 | Donovan Clingan (POR, 2024-25) | 1311 | 1.00 | 4.29 |
| 7 | Adem Bona (PHI, 2024-25) | 867 | 1.00 | 4.40 |
| 8 | Steven Adams (HOU, 2025-26) | 730 | 1.00 | 7.39 |
| 9 | Ryan Kalkbrenner (CHA, 2025-26) | 1438 | 1.00 | 4.64 |
| 10 | Dwight Powell (DAL, 2024-25) | 551 | 1.00 | 6.77 |

**8 nearest the center** (Mahalanobis distance under this cluster's shape, members and non-members)

| # | player-season | minutes | distance | top archetype | prob |
|---|---|---|---|---|---|
| 1 | Yves Missi (NOP, 2024-25) | 1956 | 2.61 | C7 | 1.00 |
| 2 | Richaun Holmes (WAS, 2024-25) | 508 | 2.83 | C7 | 1.00 |
| 3 | Moussa Diabaté (CHA, 2025-26) | 1864 | 2.92 | C7 | 1.00 |
| 4 | Goga Bitadze (ORL, 2024-25) | 1402 | 2.97 | C7 | 1.00 |
| 5 | Daniel Gafford (DAL, 2025-26) | 1195 | 3.00 | C7 | 1.00 |
| 6 | Goga Bitadze (ORL, 2025-26) | 956 | 3.17 | C7 | 1.00 |
| 7 | Rudy Gobert (MIN, 2024-25) | 2367 | 3.24 | C7 | 1.00 |
| 8 | Jalen Duren (DET, 2024-25) | 1939 | 3.30 | C7 | 1.00 |

**Borderline** (0 members under 0.6; 5 with the most minutes)

None.

**Tracked players in this cluster**

| player-season | minutes | prob | second | prob |
|---|---|---|---|---|
| Isaiah Jackson (IND/LAC, 2025-26) | 908 | 1.00 | C5 | 0.00 |

## C8 (40 player-seasons)

**10 most typical**

| # | player-season | minutes | prob | distance |
|---|---|---|---|---|
| 1 | Josh Green (CHA, 2025-26) | 871 | 1.00 | 3.96 |
| 2 | Micah Potter (UTA, 2024-25) | 705 | 1.00 | 3.75 |
| 3 | Nicolas Batum (LAC, 2025-26) | 1266 | 1.00 | 3.80 |
| 4 | Alec Burks (MIA, 2024-25) | 864 | 1.00 | 3.61 |
| 5 | Ben Sheppard (IND, 2024-25) | 1154 | 1.00 | 3.08 |
| 6 | Taurean Prince (MIL, 2025-26) | 611 | 1.00 | 4.00 |
| 7 | Nicolas Batum (LAC, 2024-25) | 1367 | 1.00 | 3.28 |
| 8 | Harrison Barnes (SAS, 2025-26) | 1955 | 1.00 | 3.04 |
| 9 | Gary Harris (MIL, 2025-26) | 633 | 1.00 | 3.02 |
| 10 | Taurean Prince (MIL, 2024-25) | 2121 | 1.00 | 3.12 |

**8 nearest the center** (Mahalanobis distance under this cluster's shape, members and non-members)

| # | player-season | minutes | distance | top archetype | prob |
|---|---|---|---|---|---|
| 1 | Josh Green (CHA, 2024-25) | 1861 | 2.39 | C8 | 1.00 |
| 2 | Jamison Battle (TOR, 2024-25) | 1042 | 2.50 | C8 | 0.98 |
| 3 | Haywood Highsmith (MIA, 2024-25) | 1818 | 2.53 | C3 | 0.62 |
| 4 | Josh Okogie (HOU, 2025-26) | 1354 | 2.67 | C8 | 0.99 |
| 5 | Isaac Okoro (CLE, 2024-25) | 1053 | 2.77 | C8 | 0.99 |
| 6 | DaQuan Jeffries (CHA, 2024-25) | 1056 | 2.89 | C8 | 0.55 |
| 7 | Dorian Finney-Smith (LAL/BKN, 2024-25) | 1781 | 2.93 | C8 | 0.60 |
| 8 | Julian Phillips (CHI, 2024-25) | 1078 | 2.96 | C8 | 0.95 |

**Borderline** (4 members under 0.6; 5 with the most minutes)

| player-season | minutes | prob | second archetype | prob |
|---|---|---|---|---|
| Ochai Agbaji (TOR, 2024-25) | 1739 | 0.50 | C3 | 0.37 |
| Max Strus (CLE, 2024-25) | 1273 | 0.51 | C1 | 0.47 |
| DaQuan Jeffries (CHA, 2024-25) | 1056 | 0.55 | C1 | 0.34 |
| Caleb Houstan (ORL, 2024-25) | 788 | 0.57 | C1 | 0.40 |

**Tracked players in this cluster**

| player-season | minutes | prob | second | prob |
|---|---|---|---|---|
| Ben Sheppard (IND, 2024-25) | 1154 | 1.00 | C3 | 0.00 |
| Micah Potter (IND, 2025-26) | 908 | 0.62 | C1 | 0.27 |

## C9 (34 player-seasons)

**10 most typical**

| # | player-season | minutes | prob | distance |
|---|---|---|---|---|
| 1 | Jaylin Williams (OKC, 2024-25) | 774 | 1.00 | 7.79 |
| 2 | Jae'Sean Tate (HOU, 2024-25) | 573 | 1.00 | 6.19 |
| 3 | Jaylin Williams (OKC, 2025-26) | 1277 | 1.00 | 6.21 |
| 4 | Toumani Camara (POR, 2024-25) | 2518 | 1.00 | 3.89 |
| 5 | Brandin Podziemski (GSW, 2024-25) | 1660 | 1.00 | 4.06 |
| 6 | Marcus Smart (LAL, 2025-26) | 1769 | 1.00 | 2.98 |
| 7 | Garrison Mathews (ATL, 2024-25) | 830 | 1.00 | 4.21 |
| 8 | Isaiah Joe (OKC, 2024-25) | 1566 | 1.00 | 3.76 |
| 9 | Dru Smith (MIA, 2025-26) | 1121 | 1.00 | 4.82 |
| 10 | Cameron Payne (NYK, 2024-25) | 1059 | 1.00 | 5.27 |

**8 nearest the center** (Mahalanobis distance under this cluster's shape, members and non-members)

| # | player-season | minutes | distance | top archetype | prob |
|---|---|---|---|---|---|
| 1 | Toumani Camara (POR, 2025-26) | 2695 | 2.65 | C9 | 1.00 |
| 2 | Marcus Smart (LAL, 2025-26) | 1769 | 2.98 | C9 | 1.00 |
| 3 | Brandin Podziemski (GSW, 2025-26) | 2333 | 3.19 | C9 | 1.00 |
| 4 | Kenrich Williams (OKC, 2024-25) | 1128 | 3.36 | C9 | 1.00 |
| 5 | Trey Lyles (SAC, 2024-25) | 1331 | 3.38 | C9 | 1.00 |
| 6 | Austin Reaves (LAL, 2024-25) | 2518 | 3.52 | C9 | 1.00 |
| 7 | Lindy Waters III (GSW/DET, 2024-25) | 753 | 3.57 | C9 | 0.65 |
| 8 | Aaron Nesmith (IND, 2024-25) | 1099 | 3.71 | C9 | 0.90 |

**Borderline** (0 members under 0.6; 5 with the most minutes)

None.

**Tracked players in this cluster**

| player-season | minutes | prob | second | prob |
|---|---|---|---|---|
| Aaron Nesmith (IND, 2024-25) | 1099 | 0.90 | C1 | 0.09 |

## C10 (27 player-seasons)

**10 most typical**

| # | player-season | minutes | prob | distance |
|---|---|---|---|---|
| 1 | Victor Wembanyama (SAS, 2024-25) | 1527 | 1.00 | 7.65 |
| 2 | Jay Huff (IND, 2025-26) | 1719 | 1.00 | 4.70 |
| 3 | Victor Wembanyama (SAS, 2025-26) | 1866 | 1.00 | 6.87 |
| 4 | Chet Holmgren (OKC, 2024-25) | 815 | 1.00 | 3.26 |
| 5 | Myles Turner (IND, 2024-25) | 2117 | 1.00 | 2.37 |
| 6 | Jay Huff (MEM, 2024-25) | 748 | 1.00 | 4.20 |
| 7 | Brook Lopez (MIL, 2024-25) | 2506 | 1.00 | 3.97 |
| 8 | Myles Turner (MIL, 2025-26) | 1883 | 1.00 | 2.37 |
| 9 | Chet Holmgren (OKC, 2025-26) | 1997 | 1.00 | 2.71 |
| 10 | Isaiah Stewart (DET, 2025-26) | 1282 | 1.00 | 4.19 |

**8 nearest the center** (Mahalanobis distance under this cluster's shape, members and non-members)

| # | player-season | minutes | distance | top archetype | prob |
|---|---|---|---|---|---|
| 1 | Myles Turner (IND, 2024-25) | 2117 | 2.37 | C10 | 1.00 |
| 2 | Myles Turner (MIL, 2025-26) | 1883 | 2.37 | C10 | 1.00 |
| 3 | Evan Mobley (CLE, 2025-26) | 2046 | 2.68 | C10 | 0.96 |
| 4 | Chet Holmgren (OKC, 2025-26) | 1997 | 2.71 | C10 | 1.00 |
| 5 | Alex Sarr (WAS, 2025-26) | 1274 | 3.12 | C10 | 1.00 |
| 6 | Evan Mobley (CLE, 2024-25) | 2167 | 3.15 | C10 | 0.82 |
| 7 | Chet Holmgren (OKC, 2024-25) | 815 | 3.26 | C10 | 1.00 |
| 8 | Alex Sarr (WAS, 2024-25) | 1814 | 3.43 | C10 | 1.00 |

**Borderline** (0 members under 0.6; 5 with the most minutes)

None.

**Tracked players in this cluster**

| player-season | minutes | prob | second | prob |
|---|---|---|---|---|
| Myles Turner (IND, 2024-25) | 2117 | 1.00 | C5 | 0.00 |
| Jay Huff (IND, 2025-26) | 1719 | 1.00 | C5 | 0.00 |

## C11 (27 player-seasons)

**10 most typical**

| # | player-season | minutes | prob | distance |
|---|---|---|---|---|
| 1 | Giannis Antetokounmpo (MIL, 2025-26) | 1007 | 1.00 | 7.84 |
| 2 | Joel Embiid (PHI, 2024-25) | 574 | 1.00 | 3.84 |
| 3 | Joel Embiid (PHI, 2025-26) | 1201 | 1.00 | 4.67 |
| 4 | Giannis Antetokounmpo (MIL, 2024-25) | 2245 | 1.00 | 4.83 |
| 5 | DeMar DeRozan (SAC, 2025-26) | 2406 | 1.00 | 6.35 |
| 6 | DeMar DeRozan (SAC, 2024-25) | 2691 | 1.00 | 6.17 |
| 7 | Kevin Durant (HOU, 2025-26) | 2840 | 1.00 | 3.41 |
| 8 | Devin Booker (PHX, 2025-26) | 2146 | 1.00 | 3.75 |
| 9 | Nikola Jokić (DEN, 2025-26) | 2265 | 1.00 | 6.34 |
| 10 | Jimmy Butler III (GSW, 2025-26) | 1182 | 1.00 | 4.86 |

**8 nearest the center** (Mahalanobis distance under this cluster's shape, members and non-members)

| # | player-season | minutes | distance | top archetype | prob |
|---|---|---|---|---|---|
| 1 | Pascal Siakam (IND, 2025-26) | 2057 | 3.02 | C11 | 0.97 |
| 2 | Julius Randle (MIN, 2025-26) | 2610 | 3.06 | C1 | 0.64 |
| 3 | Pascal Siakam (IND, 2024-25) | 2485 | 3.12 | C1 | 0.78 |
| 4 | Scottie Barnes (TOR, 2024-25) | 2134 | 3.34 | C11 | 0.73 |
| 5 | Kevin Durant (HOU, 2025-26) | 2840 | 3.41 | C11 | 1.00 |
| 6 | Brandon Ingram (TOR, 2025-26) | 2566 | 3.56 | C11 | 1.00 |
| 7 | Brandon Ingram (NOP, 2024-25) | 595 | 3.60 | C11 | 1.00 |
| 8 | Paolo Banchero (ORL, 2024-25) | 1582 | 3.63 | C11 | 0.59 |

**Borderline** (2 members under 0.6; 5 with the most minutes)

| player-season | minutes | prob | second archetype | prob |
|---|---|---|---|---|
| Paolo Banchero (ORL, 2025-26) | 2502 | 0.50 | C1 | 0.45 |
| Paolo Banchero (ORL, 2024-25) | 1582 | 0.59 | C2 | 0.41 |

**Tracked players in this cluster**

| player-season | minutes | prob | second | prob |
|---|---|---|---|---|
| Pascal Siakam (IND, 2025-26) | 2057 | 0.97 | C1 | 0.03 |

## C12 (20 player-seasons)

**10 most typical**

| # | player-season | minutes | prob | distance |
|---|---|---|---|---|
| 1 | Oso Ighodaro (PHX, 2024-25) | 1026 | 1.00 | 3.98 |
| 2 | Drew Eubanks (SAC, 2025-26) | 552 | 1.00 | 4.08 |
| 3 | Bismack Biyombo (SAS, 2024-25) | 528 | 1.00 | 3.32 |
| 4 | Deandre Ayton (LAL, 2025-26) | 1958 | 1.00 | 2.29 |
| 5 | Isaiah Hartenstein (OKC, 2024-25) | 1558 | 1.00 | 3.92 |
| 6 | Maxime Raynaud (SAC, 2025-26) | 1964 | 1.00 | 4.62 |
| 7 | Ivica Zubac (LAC, 2024-25) | 2624 | 1.00 | 3.14 |
| 8 | Drew Eubanks (UTA/LAC, 2024-25) | 746 | 1.00 | 3.25 |
| 9 | Jarrett Allen (CLE, 2025-26) | 1493 | 1.00 | 3.55 |
| 10 | Jarrett Allen (CLE, 2024-25) | 2296 | 1.00 | 3.66 |

**8 nearest the center** (Mahalanobis distance under this cluster's shape, members and non-members)

| # | player-season | minutes | distance | top archetype | prob |
|---|---|---|---|---|---|
| 1 | Deandre Ayton (LAL, 2025-26) | 1958 | 2.29 | C12 | 1.00 |
| 2 | Jakob Poeltl (TOR, 2024-25) | 1686 | 2.56 | C12 | 1.00 |
| 3 | Mark Williams (CHA, 2024-25) | 1140 | 3.01 | C12 | 1.00 |
| 4 | Ivica Zubac (LAC, 2024-25) | 2624 | 3.14 | C12 | 1.00 |
| 5 | Drew Eubanks (UTA/LAC, 2024-25) | 746 | 3.25 | C12 | 1.00 |
| 6 | Ivica Zubac (LAC/IND, 2025-26) | 1382 | 3.27 | C12 | 1.00 |
| 7 | Bismack Biyombo (SAS, 2024-25) | 528 | 3.32 | C12 | 1.00 |
| 8 | Brandon Clarke (MEM, 2024-25) | 1207 | 3.53 | C12 | 1.00 |

**Borderline** (0 members under 0.6; 5 with the most minutes)

None.

**Tracked players in this cluster**

| player-season | minutes | prob | second | prob |
|---|---|---|---|---|
| Ivica Zubac (LAC, 2024-25) | 2624 | 1.00 | C5 | 0.00 |
| Ivica Zubac (LAC/IND, 2025-26) | 1382 | 1.00 | C5 | 0.00 |
