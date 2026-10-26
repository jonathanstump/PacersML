# Player reveal: F3, k = 2 (diag covariance)

Same sub-role order as profiles_blind.md. Read that file first.

- **Most typical:** highest sub-role probability; ties broken by smallest Mahalanobis distance to the sub-role center.
- **Borderline:** members with top probability under 0.6, the 5 with the most minutes, with their second-most-likely sub-role.
- **Pacers:** every Pacers player-season (any IND minutes that season) in F3's training set. Pacers player-seasons whose top family is F3 but under 0.6 are projected and listed separately.

## F3-S1 (79 player-seasons)

**10 most typical**

| # | player-season | minutes | prob | distance |
|---|---|---|---|---|
| 1 | Kyle Filipowski (UTA, 2024-25) | 1522 | 1.00 | 2.08 |
| 2 | John Collins (UTA, 2024-25) | 1220 | 1.00 | 2.10 |
| 3 | Onyeka Okongwu (ATL, 2025-26) | 2297 | 1.00 | 2.22 |
| 4 | Wendell Carter Jr. (ORL, 2024-25) | 1758 | 1.00 | 2.25 |
| 5 | Wendell Carter Jr. (ORL, 2025-26) | 2257 | 1.00 | 2.49 |
| 6 | John Collins (LAC, 2025-26) | 1816 | 1.00 | 2.59 |
| 7 | Thomas Bryant (IND/MIA, 2024-25) | 920 | 1.00 | 2.61 |
| 8 | Chet Holmgren (OKC, 2025-26) | 1997 | 1.00 | 2.63 |
| 9 | Alex Sarr (WAS, 2025-26) | 1274 | 1.00 | 2.63 |
| 10 | Jock Landale (MEM/ATL, 2025-26) | 1506 | 1.00 | 2.66 |

**Borderline** (0 members under 0.6; 5 with the most minutes)

None.

**Pacers player-seasons**

| player-season | minutes | prob | second | prob |
|---|---|---|---|---|
| Myles Turner (IND, 2024-25) | 2117 | 1.00 | F3-S2 | 0.00 |
| Thomas Bryant (IND/MIA, 2024-25) | 920 | 1.00 | F3-S2 | 0.00 |
| Jay Huff (IND, 2025-26) | 1719 | 1.00 | F3-S2 | 0.00 |
| Johnny Furphy (IND, 2025-26) | 643 | 1.00 | F3-S2 | 0.00 |

## F3-S2 (73 player-seasons)

**10 most typical**

| # | player-season | minutes | prob | distance |
|---|---|---|---|---|
| 1 | Dwight Powell (DAL, 2025-26) | 904 | 1.00 | 7.53 |
| 2 | Mitchell Robinson (NYK, 2025-26) | 1175 | 1.00 | 5.60 |
| 3 | Moussa Cisse (DAL, 2025-26) | 530 | 1.00 | 4.74 |
| 4 | Rudy Gobert (MIN, 2025-26) | 2380 | 1.00 | 3.35 |
| 5 | Steven Adams (HOU, 2025-26) | 730 | 1.00 | 4.51 |
| 6 | Rudy Gobert (MIN, 2024-25) | 2367 | 1.00 | 2.82 |
| 7 | Steven Adams (HOU, 2024-25) | 772 | 1.00 | 4.85 |
| 8 | Clint Capela (ATL, 2024-25) | 1158 | 1.00 | 5.51 |
| 9 | Dwight Powell (DAL, 2024-25) | 551 | 1.00 | 6.54 |
| 10 | Isaiah Jackson (IND/LAC, 2025-26) | 908 | 1.00 | 3.03 |

**Borderline** (0 members under 0.6; 5 with the most minutes)

None.

**Pacers player-seasons**

| player-season | minutes | prob | second | prob |
|---|---|---|---|---|
| Ivica Zubac (LAC/IND, 2025-26) | 1382 | 1.00 | F3-S1 | 0.00 |
| Isaiah Jackson (IND/LAC, 2025-26) | 908 | 1.00 | F3-S1 | 0.00 |

## Pacers player-seasons with top family F3 under 0.6 (not in training, projected)

None.
