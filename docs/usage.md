# How to Use

### Prerequisites

- Python 3.x
- `matplotlib` library (only required for plotting functionality)

### Installation and Setup

1. Clone or download this project to your local machine.
2. Navigate to the project directory.
3. (Optional) Install dependencies for plotting functionality:

    ```bash
    pip install -r requirements.txt
    ```

### Playing with the Bot

1. **Start the Program**: Run `python main.py`.

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