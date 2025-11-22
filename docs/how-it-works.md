# How It Works

1. **Vocabulary Loading**: Loads words from `data/vocabularies.csv`.
2. **Character Analysis**: Analyzes frequency of unique characters across all words.
3. **Word Scoring**: Scores each word based on the frequency of its unique letters.
4. **Guess Suggestion**: Recommends highest-scoring words from remaining possibilities.
5. **Filtering**: Uses Wordle feedback to eliminate impossible words:
   - Green: Must match letter and position.
   - Yellow: Must contain letter but not in that position.
   - Gray: Must not contain letter (unless it's green elsewhere).

This approach maximizes information gained per guess, helping you solve Wordle in fewer attempts.