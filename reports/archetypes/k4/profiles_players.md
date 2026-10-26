# Player reveal, k = 4 (full covariance)

Same cluster order as profiles_blind.md. Read that file first.

- **Most typical:** highest membership probability; ties (many are 1.00) broken by smallest Mahalanobis distance to the cluster center (in SDs of that cluster's own shape).
- **8 nearest the center:** smallest Mahalanobis distance to the cluster center, whatever their top archetype.
- **Borderline:** members whose top probability is under 0.6, the 5 with the most minutes, with their second-most-likely archetype.
- **Tracked:** every Pacers player-season (any minutes for IND that season) in the cluster, plus Myles Turner 2024-25 and every Ivica Zubac season. Training seasons only (2026-27 is not projected until the model is frozen). Players under 500 minutes aren't fitted and don't appear.

## Tracked players at a glance

| player-season | minutes | top archetype | prob | second | prob |
|---|---|---|---|---|---|
| Ivica Zubac (LAC, 2024-25) | 2624 | C4 | 1.00 | C3 | 0.00 |
| Pascal Siakam (IND, 2024-25) | 2485 | C3 | 0.99 | C2 | 0.01 |
| Tyrese Haliburton (IND, 2024-25) | 2411 | C2 | 1.00 | C1 | 0.00 |
| Myles Turner (IND, 2024-25) | 2117 | C3 | 1.00 | C1 | 0.00 |
| Bennedict Mathurin (IND, 2024-25) | 2056 | C2 | 0.99 | C1 | 0.01 |
| Andrew Nembhard (IND, 2024-25) | 1840 | C2 | 1.00 | C3 | 0.00 |
| Obi Toppin (IND, 2024-25) | 1461 | C1 | 0.99 | C3 | 0.01 |
| T.J. McConnell (IND, 2024-25) | 1362 | C2 | 0.99 | C3 | 0.01 |
| Ben Sheppard (IND, 2024-25) | 1154 | C1 | 1.00 | C3 | 0.00 |
| Jarace Walker (IND, 2024-25) | 1115 | C1 | 1.00 | C2 | 0.00 |
| Aaron Nesmith (IND, 2024-25) | 1099 | C1 | 1.00 | C2 | 0.00 |
| Thomas Bryant (IND/MIA, 2024-25) | 920 | C4 | 1.00 | C3 | 0.00 |
| Pascal Siakam (IND, 2025-26) | 2057 | C2 | 0.68 | C3 | 0.32 |
| Jarace Walker (IND, 2025-26) | 1953 | C1 | 0.99 | C2 | 0.01 |
| Andrew Nembhard (IND, 2025-26) | 1786 | C2 | 1.00 | C3 | 0.00 |
| Jay Huff (IND, 2025-26) | 1719 | C3 | 1.00 | C4 | 0.00 |
| Bennedict Mathurin (IND/LAC, 2025-26) | 1620 | C2 | 1.00 | C3 | 0.00 |
| Ben Sheppard (IND, 2025-26) | 1390 | C1 | 0.95 | C2 | 0.05 |
| Ivica Zubac (LAC/IND, 2025-26) | 1382 | C4 | 1.00 | C3 | 0.00 |
| Aaron Nesmith (IND, 2025-26) | 1335 | C2 | 0.96 | C1 | 0.04 |
| T.J. McConnell (IND, 2025-26) | 963 | C2 | 1.00 | C3 | 0.00 |
| Kobe Brown (IND/LAC, 2025-26) | 947 | C1 | 1.00 | C3 | 0.00 |
| Isaiah Jackson (IND/LAC, 2025-26) | 908 | C4 | 1.00 | C3 | 0.00 |
| Micah Potter (IND, 2025-26) | 908 | C1 | 1.00 | C4 | 0.00 |
| Quenton Jackson (IND, 2025-26) | 897 | C2 | 0.90 | C3 | 0.10 |
| Ethan Thompson (IND, 2025-26) | 653 | C1 | 0.98 | C2 | 0.02 |
| Johnny Furphy (IND, 2025-26) | 643 | C1 | 0.62 | C4 | 0.32 |
| Kam Jones (IND, 2025-26) | 616 | C2 | 1.00 | C3 | 0.00 |

## C1 (264 player-seasons)

**10 most typical**

| # | player-season | minutes | prob | distance |
|---|---|---|---|---|
| 1 | Ben Sheppard (IND, 2024-25) | 1154 | 1.00 | 3.61 |
| 2 | Nicolas Batum (LAC, 2024-25) | 1367 | 1.00 | 3.92 |
| 3 | Nicolas Batum (LAC, 2025-26) | 1266 | 1.00 | 4.18 |
| 4 | Jaylin Williams (OKC, 2025-26) | 1277 | 1.00 | 6.31 |
| 5 | Jaylin Williams (OKC, 2024-25) | 774 | 1.00 | 7.42 |
| 6 | Grant Williams (CHA, 2025-26) | 686 | 1.00 | 4.70 |
| 7 | Taurean Prince (MIL, 2025-26) | 611 | 1.00 | 4.72 |
| 8 | Jae'Sean Tate (HOU, 2024-25) | 573 | 1.00 | 6.76 |
| 9 | Alec Burks (MIA, 2024-25) | 864 | 1.00 | 4.31 |
| 10 | Toumani Camara (POR, 2024-25) | 2518 | 1.00 | 5.01 |

**8 nearest the center** (Mahalanobis distance under this cluster's shape, members and non-members)

| # | player-season | minutes | distance | top archetype | prob |
|---|---|---|---|---|---|
| 1 | Tristan da Silva (ORL, 2025-26) | 1869 | 2.22 | C1 | 0.99 |
| 2 | Nickeil Alexander-Walker (MIN, 2024-25) | 2046 | 2.27 | C1 | 1.00 |
| 3 | Simone Fontecchio (DET, 2024-25) | 1200 | 2.30 | C1 | 1.00 |
| 4 | Moses Moody (GSW, 2024-25) | 1577 | 2.38 | C1 | 1.00 |
| 5 | Haywood Highsmith (MIA, 2024-25) | 1818 | 2.38 | C1 | 1.00 |
| 6 | Tristan da Silva (ORL, 2024-25) | 1608 | 2.42 | C1 | 1.00 |
| 7 | Tyrese Martin (BKN, 2024-25) | 1296 | 2.45 | C1 | 1.00 |
| 8 | Moses Moody (GSW, 2025-26) | 1540 | 2.47 | C1 | 1.00 |

**Borderline** (8 members under 0.6; 5 with the most minutes)

| player-season | minutes | prob | second archetype | prob |
|---|---|---|---|---|
| Bilal Coulibaly (WAS, 2024-25) | 1916 | 0.54 | C2 | 0.33 |
| Kyle Kuzma (MIL, 2025-26) | 1771 | 0.60 | C2 | 0.24 |
| Cameron Johnson (DEN, 2025-26) | 1647 | 0.58 | C2 | 0.42 |
| Brice Sensabaugh (UTA, 2024-25) | 1432 | 0.57 | C2 | 0.43 |
| Ricky Council IV (PHI, 2024-25) | 1213 | 0.53 | C2 | 0.46 |

**Tracked players in this cluster**

| player-season | minutes | prob | second | prob |
|---|---|---|---|---|
| Obi Toppin (IND, 2024-25) | 1461 | 0.99 | C3 | 0.01 |
| Ben Sheppard (IND, 2024-25) | 1154 | 1.00 | C3 | 0.00 |
| Jarace Walker (IND, 2024-25) | 1115 | 1.00 | C2 | 0.00 |
| Aaron Nesmith (IND, 2024-25) | 1099 | 1.00 | C2 | 0.00 |
| Jarace Walker (IND, 2025-26) | 1953 | 0.99 | C2 | 0.01 |
| Ben Sheppard (IND, 2025-26) | 1390 | 0.95 | C2 | 0.05 |
| Kobe Brown (IND/LAC, 2025-26) | 947 | 1.00 | C3 | 0.00 |
| Micah Potter (IND, 2025-26) | 908 | 1.00 | C4 | 0.00 |
| Ethan Thompson (IND, 2025-26) | 653 | 0.98 | C2 | 0.02 |
| Johnny Furphy (IND, 2025-26) | 643 | 0.62 | C4 | 0.32 |

## C2 (259 player-seasons)

**10 most typical**

| # | player-season | minutes | prob | distance |
|---|---|---|---|---|
| 1 | Donovan Mitchell (CLE, 2025-26) | 2316 | 1.00 | 2.54 |
| 2 | Donovan Mitchell (CLE, 2024-25) | 2232 | 1.00 | 2.71 |
| 3 | Cam Thomas (BKN, 2024-25) | 781 | 1.00 | 3.59 |
| 4 | Damian Lillard (MIL, 2024-25) | 2093 | 1.00 | 4.12 |
| 5 | Stephen Curry (GSW, 2025-26) | 1329 | 1.00 | 4.20 |
| 6 | Luka Dončić (LAL/DAL, 2024-25) | 1725 | 1.00 | 4.24 |
| 7 | Jordan Poole (WAS, 2024-25) | 1971 | 1.00 | 4.27 |
| 8 | Paul George (PHI, 2024-25) | 1334 | 1.00 | 4.30 |
| 9 | Jayson Tatum (BOS, 2024-25) | 2562 | 1.00 | 4.51 |
| 10 | James Harden (LAC/CLE, 2025-26) | 2370 | 1.00 | 4.58 |

**8 nearest the center** (Mahalanobis distance under this cluster's shape, members and non-members)

| # | player-season | minutes | distance | top archetype | prob |
|---|---|---|---|---|---|
| 1 | De'Aaron Fox (SAC/SAS, 2024-25) | 2204 | 2.26 | C2 | 1.00 |
| 2 | Jamal Murray (DEN, 2025-26) | 2652 | 2.27 | C2 | 1.00 |
| 3 | Cameron Johnson (BKN, 2024-25) | 1775 | 2.47 | C2 | 0.96 |
| 4 | Quentin Grimes (DAL/PHI, 2024-25) | 1941 | 2.48 | C2 | 1.00 |
| 5 | Donovan Mitchell (CLE, 2025-26) | 2316 | 2.54 | C2 | 1.00 |
| 6 | Bogdan Bogdanović (LAC/ATL, 2024-25) | 1348 | 2.59 | C2 | 0.89 |
| 7 | Shaedon Sharpe (POR, 2024-25) | 2252 | 2.59 | C2 | 1.00 |
| 8 | Bradley Beal (PHX, 2024-25) | 1702 | 2.60 | C2 | 1.00 |

**Borderline** (7 members under 0.6; 5 with the most minutes)

| player-season | minutes | prob | second archetype | prob |
|---|---|---|---|---|
| Anthony Black (ORL, 2024-25) | 1862 | 0.56 | C3 | 0.40 |
| Amir Coffey (LAC, 2024-25) | 1748 | 0.49 | C3 | 0.44 |
| Kevin Huerter (SAC/CHI, 2024-25) | 1619 | 0.59 | C1 | 0.41 |
| Aaron Holiday (HOU, 2024-25) | 766 | 0.54 | C1 | 0.46 |
| Jaden Ivey (DET/CHI, 2025-26) | 657 | 0.53 | C1 | 0.47 |

**Tracked players in this cluster**

| player-season | minutes | prob | second | prob |
|---|---|---|---|---|
| Tyrese Haliburton (IND, 2024-25) | 2411 | 1.00 | C1 | 0.00 |
| Bennedict Mathurin (IND, 2024-25) | 2056 | 0.99 | C1 | 0.01 |
| Andrew Nembhard (IND, 2024-25) | 1840 | 1.00 | C3 | 0.00 |
| T.J. McConnell (IND, 2024-25) | 1362 | 0.99 | C3 | 0.01 |
| Pascal Siakam (IND, 2025-26) | 2057 | 0.68 | C3 | 0.32 |
| Andrew Nembhard (IND, 2025-26) | 1786 | 1.00 | C3 | 0.00 |
| Bennedict Mathurin (IND/LAC, 2025-26) | 1620 | 1.00 | C3 | 0.00 |
| Aaron Nesmith (IND, 2025-26) | 1335 | 0.96 | C1 | 0.04 |
| T.J. McConnell (IND, 2025-26) | 963 | 1.00 | C3 | 0.00 |
| Quenton Jackson (IND, 2025-26) | 897 | 0.90 | C3 | 0.10 |
| Kam Jones (IND, 2025-26) | 616 | 1.00 | C3 | 0.00 |

## C3 (118 player-seasons)

**10 most typical**

| # | player-season | minutes | prob | distance |
|---|---|---|---|---|
| 1 | Karl-Anthony Towns (NYK, 2025-26) | 2322 | 1.00 | 4.26 |
| 2 | Nikola Jokić (DEN, 2024-25) | 2452 | 1.00 | 4.93 |
| 3 | Nikola Jokić (DEN, 2025-26) | 2265 | 1.00 | 5.04 |
| 4 | Victor Wembanyama (SAS, 2025-26) | 1866 | 1.00 | 5.15 |
| 5 | Ben Simmons (BKN/LAC, 2024-25) | 1101 | 1.00 | 5.87 |
| 6 | Giannis Antetokounmpo (MIL, 2025-26) | 1007 | 1.00 | 6.17 |
| 7 | Victor Wembanyama (SAS, 2024-25) | 1527 | 1.00 | 6.55 |
| 8 | Jaren Jackson Jr. (MEM, 2024-25) | 2207 | 1.00 | 4.71 |
| 9 | Kristaps Porziņģis (ATL/GSW, 2025-26) | 769 | 1.00 | 4.33 |
| 10 | Elfrid Payton (NOP/CHA, 2024-25) | 511 | 1.00 | 6.73 |

**8 nearest the center** (Mahalanobis distance under this cluster's shape, members and non-members)

| # | player-season | minutes | distance | top archetype | prob |
|---|---|---|---|---|---|
| 1 | Pascal Siakam (IND, 2024-25) | 2485 | 2.02 | C3 | 0.99 |
| 2 | John Collins (UTA, 2024-25) | 1220 | 2.41 | C3 | 0.96 |
| 3 | Kyle Kuzma (MIL, 2025-26) | 1771 | 2.49 | C1 | 0.60 |
| 4 | Tosan Evbuomwan (BKN, 2024-25) | 638 | 2.55 | C1 | 0.81 |
| 5 | Scottie Barnes (TOR, 2025-26) | 2648 | 2.61 | C3 | 1.00 |
| 6 | Jabari Smith Jr. (HOU, 2025-26) | 2705 | 2.65 | C3 | 0.98 |
| 7 | P.J. Washington (DAL, 2025-26) | 1736 | 2.67 | C3 | 0.78 |
| 8 | Evan Mobley (CLE, 2025-26) | 2046 | 2.71 | C3 | 1.00 |

**Borderline** (4 members under 0.6; 5 with the most minutes)

| player-season | minutes | prob | second archetype | prob |
|---|---|---|---|---|
| Jaime Jaquez Jr. (MIA, 2025-26) | 2092 | 0.59 | C2 | 0.41 |
| Kyle Filipowski (UTA, 2024-25) | 1522 | 0.52 | C1 | 0.46 |
| Bilal Coulibaly (WAS, 2025-26) | 1468 | 0.58 | C1 | 0.25 |
| Jalen Wilson (BKN, 2025-26) | 859 | 0.51 | C1 | 0.48 |

**Tracked players in this cluster**

| player-season | minutes | prob | second | prob |
|---|---|---|---|---|
| Pascal Siakam (IND, 2024-25) | 2485 | 0.99 | C2 | 0.01 |
| Myles Turner (IND, 2024-25) | 2117 | 1.00 | C1 | 0.00 |
| Jay Huff (IND, 2025-26) | 1719 | 1.00 | C4 | 0.00 |

## C4 (109 player-seasons)

**10 most typical**

| # | player-season | minutes | prob | distance |
|---|---|---|---|---|
| 1 | Clint Capela (HOU, 2025-26) | 926 | 1.00 | 3.36 |
| 2 | Moussa Cisse (DAL, 2025-26) | 530 | 1.00 | 4.11 |
| 3 | Mitchell Robinson (NYK, 2025-26) | 1175 | 1.00 | 4.28 |
| 4 | Dwight Powell (DAL, 2024-25) | 551 | 1.00 | 4.99 |
| 5 | Jonathan Isaac (ORL, 2024-25) | 1068 | 1.00 | 5.34 |
| 6 | Steven Adams (HOU, 2024-25) | 772 | 1.00 | 5.37 |
| 7 | Steven Adams (HOU, 2025-26) | 730 | 1.00 | 5.54 |
| 8 | Dylan Cardwell (SAC, 2025-26) | 906 | 1.00 | 5.65 |
| 9 | Dwight Powell (DAL, 2025-26) | 904 | 1.00 | 7.48 |
| 10 | Donovan Clingan (POR, 2024-25) | 1311 | 1.00 | 3.47 |

**8 nearest the center** (Mahalanobis distance under this cluster's shape, members and non-members)

| # | player-season | minutes | distance | top archetype | prob |
|---|---|---|---|---|---|
| 1 | Onyeka Okongwu (ATL, 2024-25) | 2034 | 2.25 | C4 | 1.00 |
| 2 | Rudy Gobert (MIN, 2024-25) | 2367 | 2.70 | C4 | 1.00 |
| 3 | Neemias Queta (BOS, 2024-25) | 835 | 2.71 | C4 | 1.00 |
| 4 | Yves Missi (NOP, 2024-25) | 1956 | 2.80 | C4 | 1.00 |
| 5 | Neemias Queta (BOS, 2025-26) | 1893 | 2.81 | C4 | 1.00 |
| 6 | Jakob Poeltl (TOR, 2024-25) | 1686 | 2.86 | C4 | 1.00 |
| 7 | Karlo Matković (NOP, 2024-25) | 791 | 2.94 | C4 | 1.00 |
| 8 | Goga Bitadze (ORL, 2025-26) | 956 | 2.94 | C4 | 1.00 |

**Borderline** (0 members under 0.6; 5 with the most minutes)

None.

**Tracked players in this cluster**

| player-season | minutes | prob | second | prob |
|---|---|---|---|---|
| Ivica Zubac (LAC, 2024-25) | 2624 | 1.00 | C3 | 0.00 |
| Thomas Bryant (IND/MIA, 2024-25) | 920 | 1.00 | C3 | 0.00 |
| Ivica Zubac (LAC/IND, 2025-26) | 1382 | 1.00 | C3 | 0.00 |
| Isaiah Jackson (IND/LAC, 2025-26) | 908 | 1.00 | C3 | 0.00 |
