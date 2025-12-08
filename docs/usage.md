# How to Use

### Prerequisites

- Python 3.x
- `tkinter` (usually included with Python)
- `matplotlib` (optional, for plotting)

### Graphical Interface (GUI)

The easiest way to use WordMaster is via the desktop app.

1. **Run the App**:

    ```bash
    python gui.py
    ```

2. Select Mode: Choose "Hybrid (Recommended)" from the right panel.

3. Input Guess: Type your guess in the "Word" field or click a word from the "Top Suggestions" list.

4. Set Feedback:
   - Click the colored blocks to match the Wordle feedback.
   - Click once for Yellow, twice for Green, again to reset to Gray.

5. Submit: Click "Submit Feedback".

6. Update History: When you win (GGGGG), the app will ask if you want to save the word to data/answers.csv. Click "Yes" to exclude it from future games.

### Command Line Interface (CLI)

For power users or scripting.

Basic Usage:

```bash
python main.py --hybrid
```

Arguments:

- `--hybrid`: (Recommended) Excludes past answers starting from the 2nd guess. Balances information gathering and answer targeting.
- `--wordle`: Excludes past answers from the 1st guess. Good if you are sure the answer hasn't appeared yet.
- `--algo {entropy,unique}`: Choose the scoring algorithm.
  - `entropy`: Uses Global Information Entropy (slower but smarter).
  - `unique`: Uses Character Frequency (faster).
- `--num_suggestions N`: Show top N suggestions.
- `--quiet`: Minimal output mode.

Example Session:

```bash
python main.py --hybrid --algo entropy
```

### Web Interface

WordMaster also provides a web-based Wordle game with integrated assistant suggestions.

#### Features

- **Interactive Game Board**: Visual Wordle grid with color-coded feedback (green for correct position, yellow for correct letter wrong position, gray for incorrect).
- **Virtual Keyboard**: On-screen keyboard that updates with letter statuses.
- **Assistant Suggestions**: Get top word suggestions based on remaining possibilities, accessible via a collapsible suggestions panel.
- **Session Management**: Start new games and track attempts.

#### Running the Web App

**Using Docker (Recommended):**

1. Ensure Docker and Docker Compose are installed.
2. Navigate to the project root directory.
3. Run `docker-compose up --build`.
4. Open your browser and go to `http://localhost:8000`.

**Running Directly:**

1. Navigate to the `app/` directory.
2. Install dependencies: `pip install -r requirements.txt`.
3. Run the Flask app: `python app.py`.
4. Open your browser and go to `http://localhost:8000`.

#### How to Play

1. Click "New Game" to start.
2. Type your guess using the on-screen keyboard or your physical keyboard.
3. Press Enter to submit.
4. View the colored feedback on the game board.
5. Check the "Suggestions" panel for assistant recommendations for your next guess.
6. Continue until you win or reach 6 attempts.

### Analyzing Strategies

To analyze different word guessing strategies:

1. Run `python analyze_strategies.py`.
2. The script simulates all strategies against the full vocabulary and saves results to `data/strategy_results.csv`.
3. Strategies include variations based on frequency scoring (Total, Repeat, Unique) and selection methods (Best guess vs. Random from top N).

### Plotting Results

To visualize strategy performance:

1. Ensure `matplotlib` is installed (`pip install -r requirements.txt`).
2. Run `python plot_strategies.py`.
3. The script generates line charts for success rates and failed games, saved as `data/success_rates_line.png` and `data/failed_games_line.png`.