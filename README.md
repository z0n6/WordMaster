# WordMaster

This project is a Python-based assistant tool designed to help users solve Wordle puzzles more efficiently. It analyzes a vocabulary of 5-letter words, suggests optimal guesses based on character frequency, and narrows down possible answers using feedback from your Wordle attempts.

## Features

- **Intelligent Guess Suggestions**: Recommends the top 10 words to guess next based on character frequency analysis in the remaining possible words.
- **Interactive Feedback Loop**: After each guess, input the Wordle feedback (Green/Yellow/Gray) to filter the word list.
- **Word Scoring System**: Scores words by the uniqueness and frequency of their letters to prioritize informative guesses.
- **Comprehensive Vocabulary**: Uses a large dataset of valid 5-letter words.

## How to Use

### Prerequisites

- Python 3.x
- `matplotlib` library (automatically installed via requirements.txt)

### Installation and Setup

1. Clone or download this project to your local machine.
2. Navigate to the project directory.
3. Run the setup script:

   ```bash
   ./run.sh
   ```

   This will:
   - Create a Python virtual environment (if it doesn't exist)
   - Install required dependencies
   - Launch the Wordle Answer Bot

### Playing with the Bot

1. **Start the Program**: Run `./run.sh` or activate the virtual environment and run `python main.py`.

2. **Understand Feedback Codes**:
   - `G`: Green - Correct letter in correct position
   - `Y`: Yellow - Correct letter in wrong position
   - `X`: Gray - Letter not in the word

3. **Gameplay Loop**:
   - The bot displays the top 10 suggested guesses.
   - Choose a guess by entering its number (1-10).
   - Play that word on Wordle.
   - Enter the feedback as a 5-character string (e.g., `GYXXG`).
   - The bot filters possible words and suggests new guesses.
   - Repeat until you win or run out of attempts.

4. **Winning**: If you enter `GGGGG`, the bot congratulates you.

5. **Quitting**: Type `quit` at any prompt to exit.

### Playing Wordle (Practice Mode)

For practice or to play Wordle without the assistant:

1. Run `python play_wordle.py` (after setting up the environment).
2. Guess 5-letter words and receive feedback.
3. Use `--quiet` flag for minimal output (useful for scripting).

### Example Session

```
Welcome to WordMaster!
I will suggest guesses. After each guess, enter feedback as 5 characters:
G for green (correct letter, correct position)
Y for yellow (correct letter, wrong position)
X for gray (letter not in word)
Example: GYXXG

Attempt 1: Top suggested guesses:
1. AROSE
2. IRATE
3. RAISE
...
Choose a guess by number (1-10) or 'quit' to stop: 1
Enter feedback (or 'quit' to stop): YXYYX
Remaining possible words: 234
...
```

## Project Structure

- `main.py`: Main entry point for the Wordle assistant and interactive loop.
- `play_wordle.py`: Standalone Wordle game simulator for practice.
- `utils.py`: Core logic for word analysis, scoring, and filtering.
- `data/vocabularies.csv`: List of valid 5-letter words.
- `data/word_scores.csv`: Pre-computed word scores (generated if needed).
- `data/char_freq.png`: Character frequency visualization (generated if needed).
- `requirements.txt`: Python dependencies.
- `run.sh`: Setup and run script.

## How It Works

1. **Vocabulary Loading**: Loads words from `data/vocabularies.csv`.
2. **Character Analysis**: Analyzes frequency of unique characters across all words.
3. **Word Scoring**: Scores each word based on the frequency of its unique letters.
4. **Guess Suggestion**: Recommends highest-scoring words from remaining possibilities.
5. **Filtering**: Uses Wordle feedback to eliminate impossible words:
   - Green: Must match letter and position.
   - Yellow: Must contain letter but not in that position.
   - Gray: Must not contain letter (unless it's green elsewhere).

This approach maximizes information gained per guess, helping you solve Wordle in fewer attempts.

