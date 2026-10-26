# Player reveal, k = 2 (full covariance)

Same cluster order as profiles_blind.md. Read that file first.

- **Most typical:** highest membership probability; ties (many are 1.00) broken by smallest Mahalanobis distance to the cluster center (in SDs of that cluster's own shape).
- **8 nearest the center:** smallest Mahalanobis distance to the cluster center, whatever their top archetype.
- **Borderline:** members whose top probability is under 0.6, the 5 with the most minutes, with their second-most-likely archetype.
- **Tracked:** every Pacers player-season (any minutes for IND that season) in the cluster, plus Myles Turner 2024-25 and every Ivica Zubac season. Training seasons only (2026-27 is not projected until the model is frozen). Players under 500 minutes aren't fitted and don't appear.

## Tracked players at a glance

| player-season | minutes | top archetype | prob | second | prob |
|---|---|---|---|---|---|
| Ivica Zubac (LAC, 2024-25) | 2624 | C2 | 1.00 | C1 | 0.00 |
| Pascal Siakam (IND, 2024-25) | 2485 | C2 | 0.51 | C1 | 0.49 |
| Tyrese Haliburton (IND, 2024-25) | 2411 | C1 | 1.00 | C2 | 0.00 |
| Myles Turner (IND, 2024-25) | 2117 | C2 | 1.00 | C1 | 0.00 |
| Bennedict Mathurin (IND, 2024-25) | 2056 | C1 | 1.00 | C2 | 0.00 |
| Andrew Nembhard (IND, 2024-25) | 1840 | C1 | 1.00 | C2 | 0.00 |
| Obi Toppin (IND, 2024-25) | 1461 | C1 | 0.99 | C2 | 0.01 |
| T.J. McConnell (IND, 2024-25) | 1362 | C1 | 1.00 | C2 | 0.00 |
| Ben Sheppard (IND, 2024-25) | 1154 | C1 | 1.00 | C2 | 0.00 |
| Jarace Walker (IND, 2024-25) | 1115 | C1 | 1.00 | C2 | 0.00 |
| Aaron Nesmith (IND, 2024-25) | 1099 | C1 | 1.00 | C2 | 0.00 |
| Thomas Bryant (IND/MIA, 2024-25) | 920 | C2 | 1.00 | C1 | 0.00 |
| Pascal Siakam (IND, 2025-26) | 2057 | C2 | 0.84 | C1 | 0.16 |
| Jarace Walker (IND, 2025-26) | 1953 | C1 | 1.00 | C2 | 0.00 |
| Andrew Nembhard (IND, 2025-26) | 1786 | C1 | 1.00 | C2 | 0.00 |
| Jay Huff (IND, 2025-26) | 1719 | C2 | 1.00 | C1 | 0.00 |
| Bennedict Mathurin (IND/LAC, 2025-26) | 1620 | C1 | 1.00 | C2 | 0.00 |
| Ben Sheppard (IND, 2025-26) | 1390 | C1 | 1.00 | C2 | 0.00 |
| Ivica Zubac (LAC/IND, 2025-26) | 1382 | C2 | 1.00 | C1 | 0.00 |
| Aaron Nesmith (IND, 2025-26) | 1335 | C1 | 1.00 | C2 | 0.00 |
| T.J. McConnell (IND, 2025-26) | 963 | C1 | 1.00 | C2 | 0.00 |
| Kobe Brown (IND/LAC, 2025-26) | 947 | C1 | 0.96 | C2 | 0.04 |
| Isaiah Jackson (IND/LAC, 2025-26) | 908 | C2 | 1.00 | C1 | 0.00 |
| Micah Potter (IND, 2025-26) | 908 | C1 | 0.92 | C2 | 0.08 |
| Quenton Jackson (IND, 2025-26) | 897 | C1 | 1.00 | C2 | 0.00 |
| Ethan Thompson (IND, 2025-26) | 653 | C1 | 1.00 | C2 | 0.00 |
| Johnny Furphy (IND, 2025-26) | 643 | C2 | 0.99 | C1 | 0.01 |
| Kam Jones (IND, 2025-26) | 616 | C1 | 1.00 | C2 | 0.00 |

## C1 (533 player-seasons)

**10 most typical**

| # | player-season | minutes | prob | distance |
|---|---|---|---|---|
| 1 | Cameron Johnson (BKN, 2024-25) | 1775 | 1.00 | 1.95 |
| 2 | Quentin Grimes (DAL/PHI, 2024-25) | 1941 | 1.00 | 2.23 |
| 3 | Bogdan Bogdanović (LAC/ATL, 2024-25) | 1348 | 1.00 | 2.29 |
| 4 | Kon Knueppel (CHA, 2025-26) | 2482 | 1.00 | 2.33 |
| 5 | Nickeil Alexander-Walker (MIN, 2024-25) | 2046 | 1.00 | 2.33 |
| 6 | VJ Edgecombe (PHI, 2025-26) | 2623 | 1.00 | 2.42 |
| 7 | Nickeil Alexander-Walker (ATL, 2025-26) | 2603 | 1.00 | 2.44 |
| 8 | De'Aaron Fox (SAC/SAS, 2024-25) | 2204 | 1.00 | 2.46 |
| 9 | Jamal Murray (DEN, 2025-26) | 2652 | 1.00 | 2.47 |
| 10 | Miles McBride (NYK, 2024-25) | 1547 | 1.00 | 2.48 |

**8 nearest the center** (Mahalanobis distance under this cluster's shape, members and non-members)

| # | player-season | minutes | distance | top archetype | prob |
|---|---|---|---|---|---|
| 1 | Cameron Johnson (BKN, 2024-25) | 1775 | 1.95 | C1 | 1.00 |
| 2 | Cameron Johnson (DEN, 2025-26) | 1647 | 2.04 | C1 | 1.00 |
| 3 | Simone Fontecchio (DET, 2024-25) | 1200 | 2.17 | C1 | 1.00 |
| 4 | Quentin Grimes (DAL/PHI, 2024-25) | 1941 | 2.23 | C1 | 1.00 |
| 5 | Tristan da Silva (ORL, 2025-26) | 1869 | 2.25 | C1 | 1.00 |
| 6 | Bogdan Bogdanović (LAC/ATL, 2024-25) | 1348 | 2.29 | C1 | 1.00 |
| 7 | Kon Knueppel (CHA, 2025-26) | 2482 | 2.33 | C1 | 1.00 |
| 8 | Nickeil Alexander-Walker (MIN, 2024-25) | 2046 | 2.33 | C1 | 1.00 |

**Borderline** (6 members under 0.6; 5 with the most minutes)

| player-season | minutes | prob | second archetype | prob |
|---|---|---|---|---|
| Noah Clowney (BKN, 2025-26) | 1780 | 0.53 | C2 | 0.47 |
| Jaylon Tyson (CLE, 2025-26) | 1754 | 0.53 | C2 | 0.47 |
| Sandro Mamukelashvili (TOR, 2025-26) | 1732 | 0.56 | C2 | 0.44 |
| Ryan Dunn (PHX, 2025-26) | 1355 | 0.57 | C2 | 0.43 |
| Olivier-Maxence Prosper (MEM, 2025-26) | 984 | 0.57 | C2 | 0.43 |

**Tracked players in this cluster**

| player-season | minutes | prob | second | prob |
|---|---|---|---|---|
| Tyrese Haliburton (IND, 2024-25) | 2411 | 1.00 | C2 | 0.00 |
| Bennedict Mathurin (IND, 2024-25) | 2056 | 1.00 | C2 | 0.00 |
| Andrew Nembhard (IND, 2024-25) | 1840 | 1.00 | C2 | 0.00 |
| Obi Toppin (IND, 2024-25) | 1461 | 0.99 | C2 | 0.01 |
| T.J. McConnell (IND, 2024-25) | 1362 | 1.00 | C2 | 0.00 |
| Ben Sheppard (IND, 2024-25) | 1154 | 1.00 | C2 | 0.00 |
| Jarace Walker (IND, 2024-25) | 1115 | 1.00 | C2 | 0.00 |
| Aaron Nesmith (IND, 2024-25) | 1099 | 1.00 | C2 | 0.00 |
| Jarace Walker (IND, 2025-26) | 1953 | 1.00 | C2 | 0.00 |
| Andrew Nembhard (IND, 2025-26) | 1786 | 1.00 | C2 | 0.00 |
| Bennedict Mathurin (IND/LAC, 2025-26) | 1620 | 1.00 | C2 | 0.00 |
| Ben Sheppard (IND, 2025-26) | 1390 | 1.00 | C2 | 0.00 |
| Aaron Nesmith (IND, 2025-26) | 1335 | 1.00 | C2 | 0.00 |
| T.J. McConnell (IND, 2025-26) | 963 | 1.00 | C2 | 0.00 |
| Kobe Brown (IND/LAC, 2025-26) | 947 | 0.96 | C2 | 0.04 |
| Micah Potter (IND, 2025-26) | 908 | 0.92 | C2 | 0.08 |
| Quenton Jackson (IND, 2025-26) | 897 | 1.00 | C2 | 0.00 |
| Ethan Thompson (IND, 2025-26) | 653 | 1.00 | C2 | 0.00 |
| Kam Jones (IND, 2025-26) | 616 | 1.00 | C2 | 0.00 |

## C2 (217 player-seasons)

**10 most typical**

| # | player-season | minutes | prob | distance |
|---|---|---|---|---|
| 1 | Neemias Queta (BOS, 2025-26) | 1893 | 1.00 | 2.70 |
| 2 | Jakob Poeltl (TOR, 2024-25) | 1686 | 1.00 | 2.80 |
| 3 | Goga Bitadze (ORL, 2024-25) | 1402 | 1.00 | 2.86 |
| 4 | Richaun Holmes (WAS, 2024-25) | 508 | 1.00 | 2.90 |
| 5 | Neemias Queta (BOS, 2024-25) | 835 | 1.00 | 2.90 |
| 6 | Yves Missi (NOP, 2024-25) | 1956 | 1.00 | 2.91 |
| 7 | Jalen Duren (DET, 2024-25) | 1939 | 1.00 | 2.96 |
| 8 | Moussa Diabaté (CHA, 2024-25) | 1239 | 1.00 | 2.96 |
| 9 | Isaiah Stewart (DET, 2024-25) | 1385 | 1.00 | 3.01 |
| 10 | Moussa Diabaté (CHA, 2025-26) | 1864 | 1.00 | 3.07 |

**8 nearest the center** (Mahalanobis distance under this cluster's shape, members and non-members)

| # | player-season | minutes | distance | top archetype | prob |
|---|---|---|---|---|---|
| 1 | Onyeka Okongwu (ATL, 2024-25) | 2034 | 2.04 | C2 | 1.00 |
| 2 | Tosan Evbuomwan (BKN, 2024-25) | 638 | 2.27 | C1 | 0.79 |
| 3 | Derrick Jones Jr. (LAC, 2025-26) | 1339 | 2.40 | C2 | 1.00 |
| 4 | John Collins (UTA, 2024-25) | 1220 | 2.47 | C2 | 1.00 |
| 5 | Evan Mobley (CLE, 2025-26) | 2046 | 2.50 | C2 | 1.00 |
| 6 | Olivier-Maxence Prosper (MEM, 2025-26) | 984 | 2.54 | C1 | 0.57 |
| 7 | Jeremy Sochan (SAS, 2024-25) | 1332 | 2.56 | C2 | 1.00 |
| 8 | Jonathan Mogbo (TOR, 2024-25) | 1286 | 2.61 | C2 | 1.00 |

**Borderline** (4 members under 0.6; 5 with the most minutes)

| player-season | minutes | prob | second archetype | prob |
|---|---|---|---|---|
| Pascal Siakam (IND, 2024-25) | 2485 | 0.51 | C1 | 0.49 |
| Jalen Johnson (ATL, 2024-25) | 1284 | 0.58 | C1 | 0.42 |
| Chris Boucher (TOR, 2024-25) | 862 | 0.55 | C1 | 0.45 |
| Carter Bryant (SAS, 2025-26) | 813 | 0.57 | C1 | 0.43 |

**Tracked players in this cluster**

| player-season | minutes | prob | second | prob |
|---|---|---|---|---|
| Ivica Zubac (LAC, 2024-25) | 2624 | 1.00 | C1 | 0.00 |
| Pascal Siakam (IND, 2024-25) | 2485 | 0.51 | C1 | 0.49 |
| Myles Turner (IND, 2024-25) | 2117 | 1.00 | C1 | 0.00 |
| Thomas Bryant (IND/MIA, 2024-25) | 920 | 1.00 | C1 | 0.00 |
| Pascal Siakam (IND, 2025-26) | 2057 | 0.84 | C1 | 0.16 |
| Jay Huff (IND, 2025-26) | 1719 | 1.00 | C1 | 0.00 |
| Ivica Zubac (LAC/IND, 2025-26) | 1382 | 1.00 | C1 | 0.00 |
| Isaiah Jackson (IND/LAC, 2025-26) | 908 | 1.00 | C1 | 0.00 |
| Johnny Furphy (IND, 2025-26) | 643 | 0.99 | C1 | 0.01 |
