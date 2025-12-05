import random
import csv
from utils import WordleHelper, FREQ_TOTAL, FREQ_REPEAT, FREQ_UNIQUE

def get_feedback(secret, guess):
    feedback = ['X'] * 5
    secret_list = list(secret)
    guess_list = list(guess)
    # Greens
    for i in range(5):
        if guess_list[i] == secret_list[i]:
            feedback[i] = 'G'
            secret_list[i] = None
            guess_list[i] = None
    # Yellows
    for i in range(5):
        if guess_list[i] is not None and guess_list[i] in secret_list:
            feedback[i] = 'Y'
            idx = secret_list.index(guess_list[i])
            secret_list[idx] = None
    return ''.join(feedback)

def simulate_game(secret, mode, random_top=None):
    helper = WordleHelper(mode=mode)
    for attempt in range(1, 7):
        if random_top != None:
            top_guesses = helper.get_top_guesses(random_top)
            if not top_guesses:
                return 7  # failed
            guess = random.choice(top_guesses)
        else:
            guess = helper.get_best_guess()
            if guess is None:
                return 7  # failed
        feedback = get_feedback(secret, guess)
        if feedback == 'GGGGG':
            return attempt
        helper.filter_words(guess, feedback)
    return 7  # failed

def main():
    words = WordleHelper.read_words()
    answers = WordleHelper.read_words('data/answers.csv')
    possible = [word for word in words if word not in answers]
    modes = [FREQ_TOTAL, FREQ_REPEAT, FREQ_UNIQUE]
    mode_names = {
        FREQ_TOTAL: 'Total Frequency',
        FREQ_REPEAT: 'Repeat Frequency',
        FREQ_UNIQUE: 'Unique Frequency'
    }
    strategies = []
    for mode in modes:
        strategies.append((mode, None, f"{mode_names[mode]} (Best)"))
        strategies.append((mode, 3, f"{mode_names[mode]} (Random Top 3)"))
        # strategies.append((mode, 5, f"{mode_names[mode]} (Random Top 5)"))
        # strategies.append((mode, 10, f"{mode_names[mode]} (Random Top 10)"))

    results = {strategy[2]: [] for strategy in strategies}

    print("Analyzing strategies... This may take a few minutes.")
    for mode, random_top, name in strategies:
        print(f"Simulating {name} strategy...")
        for secret in possible:
            guesses = simulate_game(secret, mode, random_top)
            results[name].append(guesses)

    print("\nResults:")
    for name in results:
        guesses_list = results[name]
        total_games = len(guesses_list)
        one_guess = sum(1 for g in guesses_list if g == 1)
        two_guess = sum(1 for g in guesses_list if g == 2)
        three_guess = sum(1 for g in guesses_list if g == 3)
        four_guess = sum(1 for g in guesses_list if g == 4)
        five_guess = sum(1 for g in guesses_list if g == 5)
        six_guess = sum(1 for g in guesses_list if g == 6)
        failed = sum(1 for g in guesses_list if g == 7)
        successful_games = [g for g in guesses_list if g != 7]
        if successful_games:
            avg_guesses = sum(successful_games) / len(successful_games)
        else:
            avg_guesses = 0
        success_rate = (total_games - failed) / total_games * 100
        print(f"\n{name}:")
        print(f"  Total games: {total_games}")
        print(f"  Successful games: {len(successful_games)}")
        print(f"  One guess: {one_guess}")
        print(f"  Two guess: {two_guess}")
        print(f"  Three guess: {three_guess}")
        print(f"  Four guess: {four_guess}")
        print(f"  Five guess: {five_guess}")
        print(f"  Six guess: {six_guess}")
        print(f"  Failed games: {failed}")
        print(f"  Success rate: {success_rate:.2f}%")
        print(f"  Average guesses (successful only): {avg_guesses:.2f}")

    # Save results to CSV
    with open('data/strategy_results.csv', 'w', newline='') as csvfile:
        fieldnames = ['Strategy', 'Total Games', 'Successful Games', '1 Guess', '2 Guesses', '3 Guesses', '4 Guesses', '5 Guesses', '6 Guesses', 'Failed', 'Success Rate (%)', 'Avg Guesses (Successful)']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for name in results:
            guesses_list = results[name]
            total_games = len(guesses_list)
            one_guess = sum(1 for g in guesses_list if g == 1)
            two_guess = sum(1 for g in guesses_list if g == 2)
            three_guess = sum(1 for g in guesses_list if g == 3)
            four_guess = sum(1 for g in guesses_list if g == 4)
            five_guess = sum(1 for g in guesses_list if g == 5)
            six_guess = sum(1 for g in guesses_list if g == 6)
            failed = sum(1 for g in guesses_list if g == 7)
            successful_games = [g for g in guesses_list if g != 7]
            success_rate = (total_games - failed) / total_games * 100
            avg_guesses = sum(successful_games) / len(successful_games) if successful_games else 0
            writer.writerow({
                'Strategy': name,
                'Total Games': total_games,
                'Successful Games': len(successful_games),
                '1 Guess': one_guess,
                '2 Guesses': two_guess,
                '3 Guesses': three_guess,
                '4 Guesses': four_guess,
                '5 Guesses': five_guess,
                '6 Guesses': six_guess,
                'Failed': failed,
                'Success Rate (%)': round(success_rate, 2),
                'Avg Guesses (Successful)': round(avg_guesses, 2)
            })

if __name__ == "__main__":
    main()
