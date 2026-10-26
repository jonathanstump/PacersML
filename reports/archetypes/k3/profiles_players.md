# Player reveal, k = 3 (full covariance)

Same cluster order as profiles_blind.md. Read that file first.

- **Most typical:** highest membership probability; ties (many are 1.00) broken by smallest Mahalanobis distance to the cluster center (in SDs of that cluster's own shape).
- **8 nearest the center:** smallest Mahalanobis distance to the cluster center, whatever their top archetype.
- **Borderline:** members whose top probability is under 0.6, the 5 with the most minutes, with their second-most-likely archetype.
- **Tracked:** every Pacers player-season (any minutes for IND that season) in the cluster, plus Myles Turner 2024-25 and every Ivica Zubac season. Training seasons only (2026-27 is not projected until the model is frozen). Players under 500 minutes aren't fitted and don't appear.

## Tracked players at a glance

| player-season | minutes | top archetype | prob | second | prob |
|---|---|---|---|---|---|
| Ivica Zubac (LAC, 2024-25) | 2624 | C3 | 1.00 | C1 | 0.00 |
| Pascal Siakam (IND, 2024-25) | 2485 | C1 | 1.00 | C3 | 0.00 |
| Tyrese Haliburton (IND, 2024-25) | 2411 | C1 | 1.00 | C2 | 0.00 |
| Myles Turner (IND, 2024-25) | 2117 | C3 | 1.00 | C1 | 0.00 |
| Bennedict Mathurin (IND, 2024-25) | 2056 | C1 | 0.99 | C2 | 0.01 |
| Andrew Nembhard (IND, 2024-25) | 1840 | C1 | 1.00 | C2 | 0.00 |
| Obi Toppin (IND, 2024-25) | 1461 | C2 | 1.00 | C1 | 0.00 |
| T.J. McConnell (IND, 2024-25) | 1362 | C1 | 1.00 | C2 | 0.00 |
| Ben Sheppard (IND, 2024-25) | 1154 | C2 | 1.00 | C3 | 0.00 |
| Jarace Walker (IND, 2024-25) | 1115 | C2 | 0.95 | C1 | 0.05 |
| Aaron Nesmith (IND, 2024-25) | 1099 | C2 | 1.00 | C1 | 0.00 |
| Thomas Bryant (IND/MIA, 2024-25) | 920 | C3 | 1.00 | C2 | 0.00 |
| Pascal Siakam (IND, 2025-26) | 2057 | C1 | 1.00 | C3 | 0.00 |
| Jarace Walker (IND, 2025-26) | 1953 | C2 | 0.98 | C1 | 0.02 |
| Andrew Nembhard (IND, 2025-26) | 1786 | C1 | 1.00 | C2 | 0.00 |
| Jay Huff (IND, 2025-26) | 1719 | C3 | 1.00 | C2 | 0.00 |
| Bennedict Mathurin (IND/LAC, 2025-26) | 1620 | C1 | 1.00 | C2 | 0.00 |
| Ben Sheppard (IND, 2025-26) | 1390 | C2 | 0.98 | C1 | 0.02 |
| Ivica Zubac (LAC/IND, 2025-26) | 1382 | C3 | 1.00 | C1 | 0.00 |
| Aaron Nesmith (IND, 2025-26) | 1335 | C1 | 0.97 | C2 | 0.03 |
| T.J. McConnell (IND, 2025-26) | 963 | C1 | 1.00 | C2 | 0.00 |
| Kobe Brown (IND/LAC, 2025-26) | 947 | C2 | 1.00 | C1 | 0.00 |
| Isaiah Jackson (IND/LAC, 2025-26) | 908 | C3 | 1.00 | C2 | 0.00 |
| Micah Potter (IND, 2025-26) | 908 | C2 | 0.97 | C3 | 0.03 |
| Quenton Jackson (IND, 2025-26) | 897 | C1 | 1.00 | C2 | 0.00 |
| Ethan Thompson (IND, 2025-26) | 653 | C2 | 1.00 | C1 | 0.00 |
| Johnny Furphy (IND, 2025-26) | 643 | C3 | 0.93 | C2 | 0.07 |
| Kam Jones (IND, 2025-26) | 616 | C1 | 1.00 | C2 | 0.00 |

## C1 (306 player-seasons)

**10 most typical**

| # | player-season | minutes | prob | distance |
|---|---|---|---|---|
| 1 | Donovan Mitchell (CLE, 2024-25) | 2232 | 1.00 | 2.59 |
| 2 | Donovan Mitchell (CLE, 2025-26) | 2316 | 1.00 | 2.59 |
| 3 | Paolo Banchero (ORL, 2024-25) | 1582 | 1.00 | 3.34 |
| 4 | Cam Thomas (BKN, 2024-25) | 781 | 1.00 | 3.59 |
| 5 | Andrew Nembhard (IND, 2025-26) | 1786 | 1.00 | 3.68 |
| 6 | Ja Morant (MEM, 2024-25) | 1519 | 1.00 | 3.69 |
| 7 | Damian Lillard (MIL, 2024-25) | 2093 | 1.00 | 3.70 |
| 8 | Devin Booker (PHX, 2024-25) | 2764 | 1.00 | 3.71 |
| 9 | Brandon Ingram (NOP, 2024-25) | 595 | 1.00 | 3.83 |
| 10 | Stephen Curry (GSW, 2025-26) | 1329 | 1.00 | 3.87 |

**8 nearest the center** (Mahalanobis distance under this cluster's shape, members and non-members)

| # | player-season | minutes | distance | top archetype | prob |
|---|---|---|---|---|---|
| 1 | Cameron Johnson (BKN, 2024-25) | 1775 | 1.92 | C1 | 0.95 |
| 2 | Quentin Grimes (DAL/PHI, 2024-25) | 1941 | 2.06 | C1 | 1.00 |
| 3 | De'Aaron Fox (SAC/SAS, 2024-25) | 2204 | 2.10 | C1 | 1.00 |
| 4 | Jamal Murray (DEN, 2025-26) | 2652 | 2.32 | C1 | 1.00 |
| 5 | Bradley Beal (PHX, 2024-25) | 1702 | 2.37 | C1 | 1.00 |
| 6 | Nickeil Alexander-Walker (ATL, 2025-26) | 2603 | 2.49 | C1 | 0.95 |
| 7 | Kyrie Irving (DAL, 2024-25) | 1804 | 2.51 | C1 | 1.00 |
| 8 | Shaedon Sharpe (POR, 2024-25) | 2252 | 2.52 | C1 | 1.00 |

**Borderline** (3 members under 0.6; 5 with the most minutes)

| player-season | minutes | prob | second archetype | prob |
|---|---|---|---|---|
| Jabari Smith Jr. (HOU, 2025-26) | 2705 | 0.58 | C2 | 0.42 |
| Ricky Council IV (PHI, 2024-25) | 1213 | 0.53 | C2 | 0.47 |
| Jase Richardson (ORL, 2025-26) | 582 | 0.54 | C2 | 0.46 |

**Tracked players in this cluster**

| player-season | minutes | prob | second | prob |
|---|---|---|---|---|
| Pascal Siakam (IND, 2024-25) | 2485 | 1.00 | C3 | 0.00 |
| Tyrese Haliburton (IND, 2024-25) | 2411 | 1.00 | C2 | 0.00 |
| Bennedict Mathurin (IND, 2024-25) | 2056 | 0.99 | C2 | 0.01 |
| Andrew Nembhard (IND, 2024-25) | 1840 | 1.00 | C2 | 0.00 |
| T.J. McConnell (IND, 2024-25) | 1362 | 1.00 | C2 | 0.00 |
| Pascal Siakam (IND, 2025-26) | 2057 | 1.00 | C3 | 0.00 |
| Andrew Nembhard (IND, 2025-26) | 1786 | 1.00 | C2 | 0.00 |
| Bennedict Mathurin (IND/LAC, 2025-26) | 1620 | 1.00 | C2 | 0.00 |
| Aaron Nesmith (IND, 2025-26) | 1335 | 0.97 | C2 | 0.03 |
| T.J. McConnell (IND, 2025-26) | 963 | 1.00 | C2 | 0.00 |
| Quenton Jackson (IND, 2025-26) | 897 | 1.00 | C2 | 0.00 |
| Kam Jones (IND, 2025-26) | 616 | 1.00 | C2 | 0.00 |

## C2 (291 player-seasons)

**10 most typical**

| # | player-season | minutes | prob | distance |
|---|---|---|---|---|
| 1 | Ben Sheppard (IND, 2024-25) | 1154 | 1.00 | 3.66 |
| 2 | Jaylin Williams (OKC, 2024-25) | 774 | 1.00 | 7.57 |
| 3 | Alec Burks (MIA, 2024-25) | 864 | 1.00 | 4.29 |
| 4 | Taurean Prince (MIL, 2025-26) | 611 | 1.00 | 4.68 |
| 5 | Nicolas Batum (LAC, 2025-26) | 1266 | 1.00 | 4.13 |
| 6 | Jaylin Williams (OKC, 2025-26) | 1277 | 1.00 | 6.51 |
| 7 | Josh Green (CHA, 2025-26) | 871 | 1.00 | 4.58 |
| 8 | Gary Harris (MIL, 2025-26) | 633 | 1.00 | 4.28 |
| 9 | Harrison Barnes (SAS, 2025-26) | 1955 | 1.00 | 3.52 |
| 10 | Micah Potter (UTA, 2024-25) | 705 | 1.00 | 4.50 |

**8 nearest the center** (Mahalanobis distance under this cluster's shape, members and non-members)

| # | player-season | minutes | distance | top archetype | prob |
|---|---|---|---|---|---|
| 1 | Tristan da Silva (ORL, 2025-26) | 1869 | 2.11 | C2 | 0.99 |
| 2 | Tristan da Silva (ORL, 2024-25) | 1608 | 2.34 | C2 | 1.00 |
| 3 | Simone Fontecchio (DET, 2024-25) | 1200 | 2.36 | C2 | 1.00 |
| 4 | Moses Moody (GSW, 2024-25) | 1577 | 2.36 | C2 | 1.00 |
| 5 | Tyrese Martin (BKN, 2024-25) | 1296 | 2.44 | C2 | 1.00 |
| 6 | Haywood Highsmith (MIA, 2024-25) | 1818 | 2.44 | C2 | 1.00 |
| 7 | Ja'Kobe Walter (TOR, 2024-25) | 1103 | 2.49 | C2 | 0.98 |
| 8 | Moses Moody (GSW, 2025-26) | 1540 | 2.50 | C2 | 1.00 |

**Borderline** (10 members under 0.6; 5 with the most minutes)

| player-season | minutes | prob | second archetype | prob |
|---|---|---|---|---|
| Kon Knueppel (CHA, 2025-26) | 2482 | 0.54 | C1 | 0.46 |
| Pelle Larsson (MIA, 2025-26) | 1849 | 0.58 | C1 | 0.42 |
| Brice Sensabaugh (UTA, 2025-26) | 1762 | 0.52 | C1 | 0.48 |
| Amir Coffey (LAC, 2024-25) | 1748 | 0.58 | C1 | 0.42 |
| Will Riley (WAS, 2025-26) | 1622 | 0.52 | C1 | 0.48 |

**Tracked players in this cluster**

| player-season | minutes | prob | second | prob |
|---|---|---|---|---|
| Obi Toppin (IND, 2024-25) | 1461 | 1.00 | C1 | 0.00 |
| Ben Sheppard (IND, 2024-25) | 1154 | 1.00 | C3 | 0.00 |
| Jarace Walker (IND, 2024-25) | 1115 | 0.95 | C1 | 0.05 |
| Aaron Nesmith (IND, 2024-25) | 1099 | 1.00 | C1 | 0.00 |
| Jarace Walker (IND, 2025-26) | 1953 | 0.98 | C1 | 0.02 |
| Ben Sheppard (IND, 2025-26) | 1390 | 0.98 | C1 | 0.02 |
| Kobe Brown (IND/LAC, 2025-26) | 947 | 1.00 | C1 | 0.00 |
| Micah Potter (IND, 2025-26) | 908 | 0.97 | C3 | 0.03 |
| Ethan Thompson (IND, 2025-26) | 653 | 1.00 | C1 | 0.00 |

## C3 (153 player-seasons)

**10 most typical**

| # | player-season | minutes | prob | distance |
|---|---|---|---|---|
| 1 | Neemias Queta (BOS, 2025-26) | 1893 | 1.00 | 2.55 |
| 2 | Neemias Queta (BOS, 2024-25) | 835 | 1.00 | 2.76 |
| 3 | Richaun Holmes (WAS, 2024-25) | 508 | 1.00 | 2.92 |
| 4 | Moussa Diabaté (CHA, 2025-26) | 1864 | 1.00 | 2.95 |
| 5 | Isaiah Stewart (DET, 2024-25) | 1385 | 1.00 | 2.95 |
| 6 | Goga Bitadze (ORL, 2025-26) | 956 | 1.00 | 2.98 |
| 7 | Goga Bitadze (ORL, 2024-25) | 1402 | 1.00 | 2.99 |
| 8 | Rudy Gobert (MIN, 2024-25) | 2367 | 1.00 | 3.00 |
| 9 | Zach Edey (MEM, 2024-25) | 1416 | 1.00 | 3.11 |
| 10 | DeAndre Jordan (DEN, 2024-25) | 691 | 1.00 | 3.13 |

**8 nearest the center** (Mahalanobis distance under this cluster's shape, members and non-members)

| # | player-season | minutes | distance | top archetype | prob |
|---|---|---|---|---|---|
| 1 | Onyeka Okongwu (ATL, 2024-25) | 2034 | 2.37 | C3 | 1.00 |
| 2 | John Collins (UTA, 2024-25) | 1220 | 2.50 | C3 | 0.98 |
| 3 | Neemias Queta (BOS, 2025-26) | 1893 | 2.55 | C3 | 1.00 |
| 4 | Chet Holmgren (OKC, 2025-26) | 1997 | 2.59 | C3 | 1.00 |
| 5 | Jakob Poeltl (TOR, 2024-25) | 1686 | 2.66 | C3 | 1.00 |
| 6 | Neemias Queta (BOS, 2024-25) | 835 | 2.76 | C3 | 1.00 |
| 7 | Evan Mobley (CLE, 2025-26) | 2046 | 2.82 | C3 | 1.00 |
| 8 | Yves Missi (NOP, 2024-25) | 1956 | 2.91 | C3 | 1.00 |

**Borderline** (1 members under 0.6; 5 with the most minutes)

| player-season | minutes | prob | second archetype | prob |
|---|---|---|---|---|
| Christian Braun (DEN, 2024-25) | 2569 | 0.56 | C2 | 0.44 |

**Tracked players in this cluster**

| player-season | minutes | prob | second | prob |
|---|---|---|---|---|
| Ivica Zubac (LAC, 2024-25) | 2624 | 1.00 | C1 | 0.00 |
| Myles Turner (IND, 2024-25) | 2117 | 1.00 | C1 | 0.00 |
| Thomas Bryant (IND/MIA, 2024-25) | 920 | 1.00 | C2 | 0.00 |
| Jay Huff (IND, 2025-26) | 1719 | 1.00 | C2 | 0.00 |
| Ivica Zubac (LAC/IND, 2025-26) | 1382 | 1.00 | C1 | 0.00 |
| Isaiah Jackson (IND/LAC, 2025-26) | 908 | 1.00 | C2 | 0.00 |
| Johnny Furphy (IND, 2025-26) | 643 | 0.93 | C2 | 0.07 |
