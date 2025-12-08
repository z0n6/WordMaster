# How It Works

WordMaster v1.1 uses a sophisticated combination of Information Theory and Game Theory strategies.

## 1. Global Information Entropy (The "Brain")

Instead of just counting letter frequency, the solver calculates the **Expected Information Gain (Entropy)** for each possible guess.

- **Formula**: $E[I] = \sum_{p} P(pattern) \times \log_2(\frac{1}{P(pattern)})$
- **Goal**: Select words that split the remaining candidates into the smallest possible groups, regardless of whether the word itself is the answer.
- **Global Search**: The solver considers *all* valid 5-letter words as potential probes, not just the remaining candidates.

## 2. Hybrid Strategy (The "Tactic")

Pure entropy can be too "greedy" for information, sometimes causing losses in the endgame. The Hybrid Strategy fixes this:

1. **Opening (Turn 1)**: Use Global Entropy to find the best "splitter" (e.g., `SOARE`), *including* words that may have been answers in the past.
2. **Mid-Game (Turn 2-5)**:
   - **Filter History**: Remove words found in `data/answers.csv` from the candidate pool.
   - **Narrow Down**: Continue using Entropy to prune the search space.
3. **Endgame (Turn 6)**:
   - **Survival Mode**: If on the last attempt, the solver forces a guess from the remaining *candidates* only (disabling global search) to ensure a chance of winning, rather than probing for information.

## 3. Filtering Logic

Standard Wordle rules apply:

- **Green**: Letter must be in that exact position.
- **Yellow**: Letter must be in the word but NOT in that position.
- **Gray**: Letter must not be in the word (accounting for duplicate letters).