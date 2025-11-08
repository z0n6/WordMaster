import argparse
from utils import *

def main():
    parser = argparse.ArgumentParser(description='WordMaster: A Wordle assistant')
    parser.add_argument('--num_suggestions', type=int, default=10, help='Number of suggestion guesses to show (default: 10)')
    args = parser.parse_args()
    num_suggestions = args.num_suggestions

    words = read_words()
    char_count = analyze_unique_char_freq(words)
    possible_words = words

    print("Welcome to WordMaster!")
    print("I will suggest guesses. After each guess, enter feedback as 5 characters:")
    print("G for green (correct letter, correct position)")
    print("Y for yellow (correct letter, wrong position)")
    print("X for gray (letter not in word)")
    print("Example: GYXXG")
    print("You can choose from suggested guesses or enter your own 5-letter word.")
    print()

    won = False
    for attempt in range(1, 7):
        if not possible_words:
            print("No possible words left!")
            break

        top_guesses = get_top_guesses(possible_words, char_count, num_suggestions)
        print(f"Attempt {attempt}: Top suggested guesses:")
        for i, guess in enumerate(top_guesses, 1):
            print(f"{i}. {guess}")

        guess = None
        while True:
            choice = input(f"Choose a guess by number (1-{num_suggestions}), enter a 5-letter word, or 'quit' to stop: ").strip()
            if choice.upper() == 'QUIT':
                won = True  # to prevent printing possible words
                break
            try:
                if choice.isalpha() and len(choice) == 5:
                    guess = choice.upper()
                    break
                choice_num = int(choice)
                if 1 <= choice_num <= len(top_guesses):
                    guess = top_guesses[choice_num - 1]
                    break
                else:
                    print(f"Please enter a number between 1 and {len(top_guesses)}.")
            except ValueError:
                print("Invalid input. Please enter a number or 'quit'.")

        if choice.upper() == 'QUIT':
            break

        if guess is None:
            continue  # shouldn't happen, but safety

        feedback = input("Enter feedback (or 'quit' to stop): ").strip().upper()
        if feedback == 'QUIT':
            break
        if len(feedback) != 5 or not all(c in 'GYX' for c in feedback):
            print("Invalid feedback. Please enter 5 characters: G, Y, or X.")
            continue

        if feedback == 'GGGGG':
            print("Congratulations! The word is", guess)
            won = True
            break

        possible_words = filter_words(possible_words, guess, feedback)
        print(f"Remaining possible words: {len(possible_words)}")
        print()

    if not won and possible_words:
        print("Out of attempts. Possible words:", possible_words[:10])

if __name__ == "__main__":
    main()
