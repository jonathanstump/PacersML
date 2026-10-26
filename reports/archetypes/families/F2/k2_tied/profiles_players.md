# Player reveal: F2, k = 2 (tied covariance)

Same sub-role order as profiles_blind.md. Read that file first.

- **Most typical:** highest sub-role probability; ties broken by smallest Mahalanobis distance to the sub-role center.
- **Borderline:** members with top probability under 0.6, the 5 with the most minutes, with their second-most-likely sub-role.
- **Pacers:** every Pacers player-season (any IND minutes that season) in F2's training set. Pacers player-seasons whose top family is F2 but under 0.6 are projected and listed separately.

## F2-S1 (146 player-seasons)

**10 most typical**

| # | player-season | minutes | prob | distance |
|---|---|---|---|---|
| 1 | Ausar Thompson (DET, 2024-25) | 1294 | 1.00 | 4.95 |
| 2 | Ausar Thompson (DET, 2025-26) | 1844 | 1.00 | 5.29 |
| 3 | Jarred Vanderbilt (LAL, 2025-26) | 1128 | 1.00 | 5.55 |
| 4 | Amen Thompson (HOU, 2024-25) | 2177 | 1.00 | 4.78 |
| 5 | Justin Champagnie (WAS, 2025-26) | 1359 | 1.00 | 4.29 |
| 6 | Tari Eason (HOU, 2024-25) | 1395 | 1.00 | 4.14 |
| 7 | Josh Okogie (PHX/CHA, 2024-25) | 625 | 1.00 | 6.58 |
| 8 | Ronald Holland II (DET, 2025-26) | 1527 | 1.00 | 3.80 |
| 9 | Josh Hart (NYK, 2024-25) | 2828 | 1.00 | 4.84 |
| 10 | Kelly Oubre Jr. (PHI, 2024-25) | 2044 | 1.00 | 3.52 |

**Borderline** (4 members under 0.6; 5 with the most minutes)

| player-season | minutes | prob | second sub-role | prob |
|---|---|---|---|---|
| Toumani Camara (POR, 2025-26) | 2695 | 0.59 | F2-S2 | 0.41 |
| Naz Reid (MIN, 2025-26) | 2007 | 0.52 | F2-S2 | 0.48 |
| Landry Shamet (NYK, 2024-25) | 756 | 0.52 | F2-S2 | 0.48 |
| Sandro Mamukelashvili (SAS, 2024-25) | 675 | 0.51 | F2-S2 | 0.49 |

**Pacers player-seasons**

| player-season | minutes | prob | second | prob |
|---|---|---|---|---|
| Obi Toppin (IND, 2024-25) | 1461 | 0.93 | F2-S2 | 0.07 |
| Jarace Walker (IND, 2024-25) | 1115 | 0.98 | F2-S2 | 0.02 |
| Aaron Nesmith (IND, 2024-25) | 1099 | 0.97 | F2-S2 | 0.03 |
| Jarace Walker (IND, 2025-26) | 1953 | 0.79 | F2-S2 | 0.21 |
| Kobe Brown (IND/LAC, 2025-26) | 947 | 0.99 | F2-S2 | 0.01 |

## F2-S2 (135 player-seasons)

**10 most typical**

| # | player-season | minutes | prob | distance |
|---|---|---|---|---|
| 1 | Caleb Houstan (ORL, 2024-25) | 788 | 1.00 | 3.64 |
| 2 | Nicolas Batum (LAC, 2025-26) | 1266 | 1.00 | 4.16 |
| 3 | Tyus Jones (PHX, 2024-25) | 2159 | 1.00 | 6.02 |
| 4 | AJ Green (MIL, 2025-26) | 2270 | 1.00 | 3.59 |
| 5 | Sam Hauser (BOS, 2025-26) | 1927 | 1.00 | 3.41 |
| 6 | Grant Williams (CHA, 2025-26) | 686 | 1.00 | 4.70 |
| 7 | Sam Merrill (CLE, 2024-25) | 1401 | 1.00 | 3.69 |
| 8 | Max Strus (CLE, 2024-25) | 1273 | 1.00 | 3.84 |
| 9 | Nicolas Batum (LAC, 2024-25) | 1367 | 1.00 | 3.82 |
| 10 | Al Horford (BOS, 2024-25) | 1632 | 1.00 | 4.05 |

**Borderline** (5 members under 0.6; 5 with the most minutes)

| player-season | minutes | prob | second sub-role | prob |
|---|---|---|---|---|
| Max Christie (DAL, 2025-26) | 2245 | 0.56 | F2-S1 | 0.44 |
| Kris Dunn (LAC, 2025-26) | 2181 | 0.53 | F2-S1 | 0.47 |
| Kyshawn George (WAS, 2024-25) | 1772 | 0.58 | F2-S1 | 0.42 |
| Sandro Mamukelashvili (TOR, 2025-26) | 1732 | 0.55 | F2-S1 | 0.45 |
| Rasheer Fleming (PHX, 2025-26) | 673 | 0.59 | F2-S1 | 0.41 |

**Pacers player-seasons**

| player-season | minutes | prob | second | prob |
|---|---|---|---|---|
| Ben Sheppard (IND, 2024-25) | 1154 | 0.91 | F2-S1 | 0.09 |
| Ben Sheppard (IND, 2025-26) | 1390 | 0.74 | F2-S1 | 0.26 |
| Micah Potter (IND, 2025-26) | 908 | 0.96 | F2-S1 | 0.04 |
| Ethan Thompson (IND, 2025-26) | 653 | 0.91 | F2-S1 | 0.09 |

## Pacers player-seasons with top family F2 under 0.6 (not in training, projected)

None.
