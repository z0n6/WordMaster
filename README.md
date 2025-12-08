# WordMaster

WordMaster is an advanced Wordle solver and analysis tool powered by Information Theory. It uses **Global Information Entropy** and **Hybrid Strategies** to maximize your winning probability, balancing between information gathering and answer targeting.

## New Features (v1.1)

- **🖥️ Interactive GUI**: A user-friendly desktop interface with visual feedback and instant suggestions.
- **🧠 Smart Entropy Algorithm**: Uses information theory ($E[I] = \sum p \log_2(1/p)$) to select guesses that maximally prune the search space.
- **🚀 Hybrid Strategy**:
  - **Opening**: Uses global best openers (e.g., `SOARE`) to gather information.
  - **Mid-game**: Excludes past Wordle answers (from `data/answers.csv`) to narrow down possibilities.
  - **Endgame**: Switches to "Greedy Mode" on the last attempt to ensure survival.
- **📚 History Management**: Automatically filters out past answers and allows updating the history file upon solving a puzzle.

## Quick Start

### Graphical Interface (Recommended)

Launch the desktop GUI:

```bash
python gui.py
```

### Command Line Interface

Run the solver with the recommended Hybrid strategy:

```bash
python main.py --hybrid
```

## Project Structure

- `core/`: Core application logic package.
  - `helper.py`: Algorithms for entropy calculation, scoring, and filtering.
  - `config.py`: Centralized configuration and path management.
- `gui.py`: Tkinter-based desktop graphical interface.
- `main.py`: Command-line entry point.
- `play_wordle.py`: Standalone Wordle game simulator.
- `analyze_strategies.py`: Script to simulate strategies (Standard vs Hybrid vs Entropy).
- `data/`:
  - `vocabularies.csv`: Complete list of valid 5-letter words.
  - `answers.csv`: Database of past Wordle answers (auto-updated).
- `app/`: Legacy Flask web application (requires update).

## Analysis

View strategy analysis results in [docs/analysis.md](docs/analysis.md).

## Example

See an example session in [docs/example.md](docs/example.md).

## How It Works

See docs/how-it-works.md for details on the Entropy algorithm and Hybrid strategy.

## Usage

For detailed CLI arguments and GUI controls, see docs/usage.md.

## TODO

See upcoming features in [docs/todo.md](docs/todo.md).

