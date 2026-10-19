# Pacers Archetype Project

## Who decides what

- I (Jonathan) make every modeling judgment call: k, minutes cutoffs,
  feature sets, lambda ranges, interaction terms, what counts as signal.
- When a decision comes up, stop and give me 2-3 options with trade-offs.
  Do not pick silently. Log my choice in docs/DECISIONS.md.

## Explaining your work

- For every new modeling component, add a section to docs/METHODS.md:
  what it does in plain language, a toy example with ~5 rows,
  what could make it wrong, and 3 questions I should be able to answer.
- Every model run produces diagnostic plots in reports/, not just a score.
- Never write conclusions or interpretations into findings files. Give me
  the numbers and uncertainty; I write what they mean.

## Data rules

- The archetype model is frozen after fitting on 2024-25 + 2025-26.
  New-season data is projected into it, never used to refit it.
- Any number shown on the site carries its sample size (possessions or games).
- Validation splits are by time, never random.
- Hypotheses in docs/HYPOTHESES.md are locked. Don't edit them.

## Stack

- Python (pandas, scikit-learn), data cached as parquet in data/.
- Website: static site built from JSON exports, redeployed weekly.

## Commits

- Include the Phase Number in each commit along with the description
- Commit often but where it makes sense
