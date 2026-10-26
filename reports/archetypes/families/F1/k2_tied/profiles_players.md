# Player reveal: F1, k = 2 (tied covariance)

Same sub-role order as profiles_blind.md. Read that file first.

- **Most typical:** highest sub-role probability; ties broken by smallest Mahalanobis distance to the sub-role center.
- **Borderline:** members with top probability under 0.6, the 5 with the most minutes, with their second-most-likely sub-role.
- **Pacers:** every Pacers player-season (any IND minutes that season) in F1's training set. Pacers player-seasons whose top family is F1 but under 0.6 are projected and listed separately.

## F1-S1 (207 player-seasons)

**10 most typical**

| # | player-season | minutes | prob | distance |
|---|---|---|---|---|
| 1 | Cameron Payne (NYK, 2024-25) | 1059 | 1.00 | 6.31 |
| 2 | Bones Hyland (MIN, 2025-26) | 1177 | 1.00 | 3.43 |
| 3 | Maxi Kleber (DAL, 2024-25) | 637 | 1.00 | 5.12 |
| 4 | Pat Connaughton (MIL, 2024-25) | 579 | 1.00 | 4.37 |
| 5 | Davion Mitchell (TOR/MIA, 2024-25) | 2027 | 1.00 | 3.72 |
| 6 | Buddy Hield (GSW/ATL, 2025-26) | 819 | 1.00 | 3.67 |
| 7 | Reed Sheppard (HOU, 2024-25) | 631 | 1.00 | 4.20 |
| 8 | Ace Bailey (UTA, 2025-26) | 1988 | 1.00 | 4.47 |
| 9 | Antonio Reeves (NOP, 2024-25) | 660 | 1.00 | 3.84 |
| 10 | Craig Porter Jr. (CLE, 2024-25) | 513 | 1.00 | 4.85 |

**Borderline** (2 members under 0.6; 5 with the most minutes)

| player-season | minutes | prob | second sub-role | prob |
|---|---|---|---|---|
| Dillon Brooks (PHX, 2025-26) | 1702 | 0.53 | F1-S2 | 0.47 |
| Malik Monk (SAC, 2025-26) | 1364 | 0.52 | F1-S2 | 0.48 |

**Pacers player-seasons**

| player-season | minutes | prob | second | prob |
|---|---|---|---|---|
| Tyrese Haliburton (IND, 2024-25) | 2411 | 0.99 | F1-S2 | 0.01 |
| Bennedict Mathurin (IND, 2024-25) | 2056 | 1.00 | F1-S2 | 0.00 |
| Andrew Nembhard (IND, 2024-25) | 1840 | 0.65 | F1-S2 | 0.35 |
| Bennedict Mathurin (IND/LAC, 2025-26) | 1620 | 0.78 | F1-S2 | 0.22 |
| Aaron Nesmith (IND, 2025-26) | 1335 | 1.00 | F1-S2 | 0.00 |
| Quenton Jackson (IND, 2025-26) | 897 | 0.99 | F1-S2 | 0.01 |
| Kam Jones (IND, 2025-26) | 616 | 0.95 | F1-S2 | 0.05 |

## F1-S2 (96 player-seasons)

**10 most typical**

| # | player-season | minutes | prob | distance |
|---|---|---|---|---|
| 1 | Kevin Durant (PHX, 2024-25) | 2242 | 1.00 | 5.79 |
| 2 | Nikola Jokić (DEN, 2025-26) | 2265 | 1.00 | 6.46 |
| 3 | Ja Morant (MEM, 2025-26) | 568 | 1.00 | 4.27 |
| 4 | Nikola Jokić (DEN, 2024-25) | 2452 | 1.00 | 6.31 |
| 5 | Isaiah Collier (UTA, 2025-26) | 1517 | 1.00 | 4.89 |
| 6 | Kevin Durant (HOU, 2025-26) | 2840 | 1.00 | 4.10 |
| 7 | T.J. McConnell (IND, 2025-26) | 963 | 1.00 | 6.25 |
| 8 | Ben Simmons (BKN/LAC, 2024-25) | 1101 | 1.00 | 7.71 |
| 9 | Devin Booker (PHX, 2025-26) | 2146 | 1.00 | 4.32 |
| 10 | Luka Dončić (LAL, 2025-26) | 2289 | 1.00 | 4.96 |

**Borderline** (2 members under 0.6; 5 with the most minutes)

| player-season | minutes | prob | second sub-role | prob |
|---|---|---|---|---|
| Cooper Flagg (DAL, 2025-26) | 2344 | 0.56 | F1-S1 | 0.44 |
| Jayson Tatum (BOS, 2025-26) | 522 | 0.50 | F1-S1 | 0.50 |

**Pacers player-seasons**

| player-season | minutes | prob | second | prob |
|---|---|---|---|---|
| Pascal Siakam (IND, 2024-25) | 2485 | 0.94 | F1-S1 | 0.06 |
| T.J. McConnell (IND, 2024-25) | 1362 | 0.99 | F1-S1 | 0.01 |
| Pascal Siakam (IND, 2025-26) | 2057 | 0.98 | F1-S1 | 0.02 |
| Andrew Nembhard (IND, 2025-26) | 1786 | 0.95 | F1-S1 | 0.05 |
| T.J. McConnell (IND, 2025-26) | 963 | 1.00 | F1-S1 | 0.00 |

## Pacers player-seasons with top family F1 under 0.6 (not in training, projected)

None.
