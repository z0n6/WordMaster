import random
from utils import read_words

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

def main():
    words = read_words()
    secret = random.choice(words)
    print("Welcome to Wordle!")
    print("Guess the 5-letter word in 6 tries.")
    print("Feedback: G=green (correct position), Y=yellow (wrong position), X=gray (not in word)")
    for attempt in range(1, 7):
        guess = input(f"Attempt {attempt}: Enter a 5-letter word: ").strip().upper()
        if len(guess) != 5 or not guess.isalpha():
            print("Please enter a 5-letter word.")
            continue
        if guess not in words:
            print("Word not in vocabulary.")
            continue
        feedback = get_feedback(secret, guess)
        print(f"Feedback: {feedback}")
        if feedback == 'GGGGG':
            print("Congratulations! You guessed it!")
            break
    else:
        print(f"Sorry, the word was {secret}")

if __name__ == "__main__":
    main()