# Hypothesis check: combined sub-role weights (reported, not used for selection)

D27: this file is for interpretation only and does not override BIC -> stability -> naming. Sub-role k is not picked.

Weight on sub-role s of family f = P(f) × P(s | f); P(s | f) from projecting the player into every family's sub-model with that family's scaler. Weights add to 1 across all sub-roles. Values under 0.005 shown as ·. With k = 1 in a family, its single sub-role weight equals P(family).

## Candidate set: rule

F1: tied k = 1, F2: tied k = 1, F3: tied k = 1

| player-season | minutes | F1-S1 | F2-S1 | F3-S1 | sum |
|---|---|---|---|---|---|
| Andrew Nembhard (IND, 2024-25) | 1839 | 1.000 | · | · | 1.000 |
| Andrew Nembhard (IND, 2025-26) | 1785 | 1.000 | · | · | 1.000 |
| Ivica Zubac (LAC, 2024-25) | 2624 | · | · | 1.000 | 1.000 |
| Ivica Zubac (LAC/IND, 2025-26) | 1381 | · | · | 1.000 | 1.000 |
| Jarace Walker (IND, 2024-25) | 1114 | 0.049 | 0.951 | · | 1.000 |
| Jarace Walker (IND, 2025-26) | 1953 | 0.021 | 0.979 | · | 1.000 |
| Myles Turner (IND, 2024-25) | 2116 | · | · | 1.000 | 1.000 |
| Pascal Siakam (IND, 2024-25) | 2484 | 0.995 | · | · | 1.000 |
| Pascal Siakam (IND, 2025-26) | 2056 | 1.000 | · | · | 1.000 |
| Tyrese Haliburton (IND, 2024-25) | 2410 | 1.000 | · | · | 1.000 |

## Candidate set: within diag

F1: diag k = 3, F2: diag k = 4, F3: diag k = 3

| player-season | minutes | F1-S1 | F1-S2 | F1-S3 | F2-S1 | F2-S2 | F2-S3 | F2-S4 | F3-S1 | F3-S2 | F3-S3 | sum |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Andrew Nembhard (IND, 2024-25) | 1839 | 0.420 | 0.163 | 0.416 | · | · | · | · | · | · | · | 1.000 |
| Andrew Nembhard (IND, 2025-26) | 1785 | 1.000 | · | · | · | · | · | · | · | · | · | 1.000 |
| Ivica Zubac (LAC, 2024-25) | 2624 | · | · | · | · | · | · | · | · | 1.000 | · | 1.000 |
| Ivica Zubac (LAC/IND, 2025-26) | 1381 | · | · | · | · | · | · | · | · | 1.000 | · | 1.000 |
| Jarace Walker (IND, 2024-25) | 1114 | · | · | 0.049 | · | · | 0.950 | · | · | · | · | 1.000 |
| Jarace Walker (IND, 2025-26) | 1953 | · | · | 0.014 | · | 0.041 | 0.938 | · | · | · | · | 1.000 |
| Myles Turner (IND, 2024-25) | 2116 | · | · | · | · | · | · | · | 0.997 | · | · | 1.000 |
| Pascal Siakam (IND, 2024-25) | 2484 | · | 0.995 | · | · | · | · | · | · | · | · | 1.000 |
| Pascal Siakam (IND, 2025-26) | 2056 | 0.006 | 0.994 | · | · | · | · | · | · | · | · | 1.000 |
| Tyrese Haliburton (IND, 2024-25) | 2410 | 0.995 | · | · | · | · | · | · | · | · | · | 1.000 |

## Turner 2024-25 vs Zubac: top sub-role at each packet k

Each player projected into the sub-models of his top family at every packet (covariance type, k). 'different' / 'same' = sub-roles of the family that is top for both; 'different families' = their top families differ; 'neither's top family' = projection into a family that is top for neither.

| player-season | top family | P |
|---|---|---|
| Myles Turner 2024-25 | F3 Bigs | 1.000 |
| Ivica Zubac 2024-25 | F3 Bigs | 1.000 |
| Ivica Zubac 2025-26 | F3 Bigs | 1.000 |

| family | cov | k | Turner 2024-25 | Zubac 2024-25 | Zubac 2025-26 | Turner vs each Zubac season |
|---|---|---|---|---|---|---|
| F3 | diag | 2 | F3-S1 (1.00) | F3-S2 (1.00) | F3-S2 (1.00) | 2024-25: different; 2025-26: different |
| F3 | diag | 3 | F3-S1 (1.00) | F3-S2 (1.00) | F3-S2 (1.00) | 2024-25: different; 2025-26: different |
| F3 | diag | 4 | F3-S1 (0.99) | F3-S2 (0.92) | F3-S2 (0.95) | 2024-25: different; 2025-26: different |
| F3 | tied | 1 | F3-S1 (1.00) | F3-S1 (1.00) | F3-S1 (1.00) | 2024-25: same; 2025-26: same |
| F3 | tied | 2 | F3-S2 (1.00) | F3-S1 (1.00) | F3-S1 (1.00) | 2024-25: different; 2025-26: different |
