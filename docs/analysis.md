# Analysis Results

The strategy analysis simulates all possible Wordle games using different guessing strategies based on character frequency scoring modes (Total, Repeat, Unique) and selection methods (Best guess vs. Random from top N).

### Success Rates by Strategy
![Success Rates](data/success_rates_line.png)

This chart shows success rates across strategies. The Unique Frequency (Best) strategy achieves the highest success rate at 99.01%, while random selection from top guesses slightly reduces performance.

### Failed Games by Strategy
![Failed Games](data/failed_games_line.png)

The number of failed games (unable to solve in 6 attempts) is lowest for the Unique Frequency (Best) strategy with only 23 failures.

### Average Guesses by Strategy
![Average Guesses](data/average_guesses_line.png)

Average guesses for successful games is around 3.65-3.75 across strategies, with the Unique Frequency (Best) at 3.67.

### Character Frequency Distribution
![Character Frequency](data/char_freq_unique.png)

This bar chart displays the frequency of each letter in the vocabulary, used for scoring words in the Unique Frequency mode.