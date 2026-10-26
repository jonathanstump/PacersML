# Level 1: families (full covariance, k = 3, frozen)

750 fitted player-seasons (500+ regular-season minutes, 2024-25 + 2025-26). Families F1-F3 are C1-C3 of the k = 3 packet (numbered by size). No names.

Frozen model: `models/archetypes/level1_full_k3.pkl` (+ `.json` with every parameter); hashes in `data/manifest.json` under `archetype_model.level1`.

## Family x listed position

Counts (NBA playerindex position, current listing):

| family | G | G-F | F-G | F | F-C | C-F | C | total |
|---|---|---|---|---|---|---|---|---|
| F1 | 195 | 30 | 12 | 57 | 6 | 2 | 4 | 306 |
| F2 | 115 | 27 | 9 | 122 | 11 | 2 | 5 | 291 |
| F3 | 3 | 0 | 0 | 31 | 31 | 22 | 66 | 153 |

Row shares (share of the family in each listed position):

| family | G | G-F | F-G | F | F-C | C-F | C |
|---|---|---|---|---|---|---|---|
| F1 | 64% | 10% | 4% | 19% | 2% | 1% | 1% |
| F2 | 40% | 9% | 3% | 42% | 4% | 1% | 2% |
| F3 | 2% | 0% | 0% | 20% | 20% | 14% | 43% |

Chart: [position_crosstab.png](position_crosstab.png)

## Top family probability

Chart: [top_prob_hist.png](top_prob_hist.png)

| family | members | median top prob | under 0.9 | under 0.7 | under 0.6 |
|---|---|---|---|---|---|
| F1 | 306 | 1.000 | 27 | 7 | 3 |
| F2 | 291 | 0.996 | 59 | 25 | 10 |
| F3 | 153 | 1.000 | 11 | 3 | 1 |

## Straddlers: every player-season with top family probability under 0.7 (35)

| player-season | minutes | position | top family | prob | second | prob |
|---|---|---|---|---|---|---|
| Brice Sensabaugh (UTA, 2025-26) | 1762 | F | F2 | 0.522 | F1 | 0.478 |
| Mohamed Diawara (NYK, 2025-26) | 634 | F | F2 | 0.523 | F1 | 0.477 |
| Will Riley (WAS, 2025-26) | 1622 | F | F2 | 0.523 | F1 | 0.477 |
| Ricky Council IV (PHI, 2024-25) | 1213 | G | F1 | 0.532 | F2 | 0.468 |
| Jase Richardson (ORL, 2025-26) | 582 | G | F1 | 0.541 | F2 | 0.459 |
| Kon Knueppel (CHA, 2025-26) | 2482 | G-F | F2 | 0.543 | F1 | 0.457 |
| Aaron Holiday (HOU, 2024-25) | 766 | G | F2 | 0.556 | F1 | 0.444 |
| Christian Braun (DEN, 2024-25) | 2569 | G | F3 | 0.560 | F2 | 0.440 |
| Tidjane Salaün (CHA, 2025-26) | 558 | F | F2 | 0.560 | F3 | 0.420 |
| Jett Howard (ORL, 2024-25) | 687 | G | F2 | 0.572 | F1 | 0.428 |
| Pelle Larsson (MIA, 2025-26) | 1849 | G | F2 | 0.576 | F1 | 0.424 |
| Amir Coffey (LAC, 2024-25) | 1748 | G-F | F2 | 0.580 | F1 | 0.420 |
| Jabari Smith Jr. (HOU, 2025-26) | 2705 | F | F1 | 0.584 | F2 | 0.415 |
| Ayo Dosunmu (CHI, 2024-25) | 1359 | G | F2 | 0.596 | F1 | 0.404 |
| Bogdan Bogdanović (LAC/ATL, 2024-25) | 1348 | G | F1 | 0.608 | F2 | 0.392 |
| Jake LaRavia (MEM/SAC, 2024-25) | 1326 | F | F2 | 0.610 | F1 | 0.390 |
| Luke Kennard (ATL/LAL, 2025-26) | 1681 | G | F2 | 0.613 | F1 | 0.387 |
| Keon Johnson (BKN, 2024-25) | 1893 | G | F2 | 0.613 | F1 | 0.387 |
| Gradey Dick (TOR, 2025-26) | 1052 | G-F | F1 | 0.615 | F2 | 0.385 |
| Donte DiVincenzo (MIN, 2024-25) | 1574 | G | F1 | 0.623 | F2 | 0.377 |
| Malik Beasley (DET, 2024-25) | 2175 | G | F2 | 0.625 | F1 | 0.375 |
| Jerami Grant (POR, 2024-25) | 1490 | F | F3 | 0.636 | F2 | 0.354 |
| Cody Williams (UTA, 2025-26) | 1631 | F | F2 | 0.644 | F1 | 0.348 |
| Jaden Ivey (DET/CHI, 2025-26) | 657 | G | F2 | 0.649 | F1 | 0.351 |
| Anthony Black (ORL, 2025-26) | 1881 | G | F2 | 0.650 | F1 | 0.350 |
| Jonathan Mogbo (TOR, 2024-25) | 1286 | F | F3 | 0.661 | F2 | 0.339 |
| Caris LeVert (CLE/ATL, 2024-25) | 1596 | G | F2 | 0.661 | F1 | 0.339 |
| Bilal Coulibaly (WAS, 2025-26) | 1468 | G | F2 | 0.662 | F1 | 0.338 |
| Jalen Wilson (BKN, 2025-26) | 859 | F | F2 | 0.663 | F3 | 0.324 |
| Kyle Kuzma (MIL, 2025-26) | 1771 | F | F2 | 0.664 | F1 | 0.335 |
| Bruce Brown (NOP/TOR, 2024-25) | 922 | G-F | F2 | 0.675 | F1 | 0.265 |
| Cedric Coward (MEM, 2025-26) | 1598 | G | F2 | 0.677 | F1 | 0.323 |
| Miles Bridges (CHA, 2024-25) | 1995 | F | F1 | 0.683 | F2 | 0.317 |
| Jordan Miller (LAC, 2025-26) | 1314 | G | F2 | 0.687 | F1 | 0.313 |
| Bilal Coulibaly (WAS, 2024-25) | 1916 | G | F2 | 0.694 | F1 | 0.306 |

## Family probabilities for the hypothesis-check players

| player-season | minutes | tier | P(F1) | P(F2) | P(F3) |
|---|---|---|---|---|---|
| Andrew Nembhard (IND, 2024-25) | 1839 | fit | 1.000 | 0.000 | 0.000 |
| Andrew Nembhard (IND, 2025-26) | 1785 | fit | 1.000 | 0.000 | 0.000 |
| Ivica Zubac (LAC, 2024-25) | 2624 | fit | 0.000 | 0.000 | 1.000 |
| Ivica Zubac (LAC/IND, 2025-26) | 1381 | fit | 0.000 | 0.000 | 1.000 |
| Jarace Walker (IND, 2024-25) | 1114 | fit | 0.049 | 0.951 | 0.000 |
| Jarace Walker (IND, 2025-26) | 1953 | fit | 0.021 | 0.979 | 0.000 |
| Myles Turner (IND, 2024-25) | 2116 | fit | 0.000 | 0.000 | 1.000 |
| Pascal Siakam (IND, 2024-25) | 2484 | fit | 0.995 | 0.000 | 0.005 |
| Pascal Siakam (IND, 2025-26) | 2056 | fit | 1.000 | 0.000 | 0.000 |
| Tyrese Haliburton (IND, 2024-25) | 2410 | fit | 1.000 | 0.000 | 0.000 |

## Level-2 training sets (top family with probability >= 0.6)

| family | top-assigned | training | excluded | excluded share | over 15%? |
|---|---|---|---|---|---|
| F1 | 306 | 303 | 3 | 1.0% | no |
| F2 | 291 | 281 | 10 | 3.4% | no |
| F3 | 153 | 152 | 1 | 0.7% | no |
