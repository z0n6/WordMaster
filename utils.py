import csv
from collections import Counter

# Frequency count criteria constants
FREQ_TOTAL = 'total'
FREQ_REPEAT = 'repeat'
FREQ_UNIQUE = 'unique'

class WordleHelper:
    def __init__(self, words=None, mode=FREQ_REPEAT):
        if words is None:
            self.words = self.read_words()
        else:
            self.words = words
        self.mode = mode
        self.char_count = self.analyze_freq()
        self.word_scores = self.score(self.mode, self.words, self.char_count)

    @staticmethod
    def read_words(filename='data/vocabularies.csv'):
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            row = next(reader)
            words = [word.strip() for word in row if word.strip()]
        return words

    def analyze_freq(self):
        char_count = None
        if self.mode == FREQ_TOTAL:
            char_count = self._analyze_total_char_freq(self.words)
        elif self.mode == FREQ_REPEAT:
            char_count = self._analyze_repeat_char_freq(self.words)
        elif self.mode == FREQ_UNIQUE:
            char_count = self._analyze_unique_char_freq(self.words)
        if char_count is None:
            raise ValueError(f"Invalid mode: {self.mode}")
        return char_count

    @staticmethod
    def _analyze_total_char_freq(words):
        char_count = Counter()
        for word in words:
            for char in word.lower():
                char_count[char] += 1
        return char_count

    @staticmethod
    def _analyze_repeat_char_freq(words):
        char_count = Counter()
        for word in words:
            word_char_count = Counter(word.lower())
            for char, freq in word_char_count.items():
                for f in range(1, 1 + freq):
                    char_count[char * f] += 1
        return char_count

    @staticmethod
    def _analyze_unique_char_freq(words):
        char_count = Counter()
        for word in words:
            for char in set(word.lower()):
                char_count[char] += 1
        return char_count

    @staticmethod
    def score(mode, words, char_count):
        if mode == FREQ_REPEAT:
            word_scores = []
            for word in words:
                word_char_count = Counter(word.lower())
                score = 0
                for char, freq in word_char_count.items():
                    for f in range(1, 1 + freq):
                        score += char_count[char * f]
                word_scores.append((word, score))
            word_scores.sort(key=lambda x: x[1], reverse=True)
            return word_scores
        else:
            word_scores = []
            for word in words:
                score = sum(char_count[char.lower()] for char in set(word))
                word_scores.append((word, score))
            word_scores.sort(key=lambda x: x[1], reverse=True)
            return word_scores

    def get_best_guess(self):
        return self.word_scores[0][0] if self.word_scores else None

    def get_top_guesses(self, top_n=10):
        return [word for word, score in self.word_scores[:top_n]]

    def print_word_scores(self, top_n=20):
        print(f"Top {top_n} words by score:")
        for word, score in self.word_scores[:top_n]:
            print(f"{word}: {score}")
        print()

    def plot_char_freq(self, output_file='data/char_freq.png'):
        import matplotlib.pyplot as plt
        sorted_char_count = sorted(self.char_count.items(), key=lambda x: x[1], reverse=True)
        sorted_chars, sorted_freqs = zip(*sorted_char_count)
        plt.bar(sorted_chars, sorted_freqs)
        plt.xlabel('Characters')
        plt.ylabel('Frequency')
        plt.title('Character Frequency in Vocabularies')
        plt.savefig(output_file)

    @staticmethod
    def save_word_scores(word_scores, filename='data/word_scores.csv'):
        with open(filename, 'w') as f:
            f.write("word,score\n")
            for word, score in word_scores:
                f.write(f"{word},{score}\n")

    @staticmethod
    def load_word_scores(filename='data/word_scores.csv'):
        word_scores = []
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header
            for row in reader:
                word, score = row
                word_scores.append((word, int(score)))
        return word_scores

    def filter_words(self, guess, feedback):
        """
        Filter words based on Wordle feedback.
        guess: 5-letter string
        feedback: 5-character string, G=green, Y=yellow, X=gray
        """
        filtered = []
        for word in self.words:
            word = word.upper()
            valid = True
            for i in range(5):
                if feedback[i] == 'G':
                    if word[i] != guess[i]:
                        valid = False
                        break
                elif feedback[i] == 'Y':
                    if word[i] == guess[i] or guess[i] not in word:
                        valid = False
                        break
                elif feedback[i] == 'X':
                    if word[i] == guess[i] or any(word[j] == guess[i] and feedback[j] != 'G' for j in range(5) if j != i):
                        valid = False
                        break
            if not valid:
                continue
            filtered.append(word)
        self.words = filtered
        self.char_count = self.analyze_freq()
        self.word_scores = self.score(self.mode, self.words, self.char_count)

    def play(self, num_suggestions=10, quiet=False):
        if not quiet:
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
            if not self.words:
                print("No possible words left!")
                break

            top_guesses = self.get_top_guesses(num_suggestions)
            if quiet:
                if not top_guesses:
                    print("No possible words left!")
                    break
                guess = top_guesses[0]
                print(guess)
            else:
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

            prompt = "" if quiet else "Enter feedback (or 'quit' to stop): "
            feedback = input(prompt).strip().upper()
            if feedback == 'QUIT':
                break
            if len(feedback) != 5 or not all(c in 'GYX' for c in feedback):
                print("Invalid feedback. Please enter 5 characters: G, Y, or X.")
                continue

            if feedback == 'GGGGG':
                if not quiet:
                    print("Congratulations! The word is", guess)
                won = True
                break

            self.filter_words(guess, feedback)
            if not quiet:
                print(f"Remaining possible words: {len(self.words)}")
                print()

        if not won and self.words:
            print("Out of attempts. Possible words:", self.words[:10])

# Backward compatibility functions
# def read_words(filename='data/vocabularies.csv'):
    # return WordleHelper.read_words(filename)

# def analyze_char_freq(words):
    # return WordleHelper._analyze_char_freq(words)

# def analyze_repeat_char_freq(words):
    # return WordleHelper._analyze_repeat_char_freq(words)

# def analyze_unique_char_freq(words):
    # return WordleHelper._analyze_unique_char_freq(words)

# def score_words(words, char_count):
    # helper = WordleHelper(words)
    # helper.char_counts[FREQ_UNIQUE] = char_count
    # return helper.score(words, FREQ_UNIQUE)

# def score_words_with_repeat_characters(words, char_count):
    # helper = WordleHelper(words)
    # helper.char_counts[FREQ_REPEAT] = char_count
    # return helper.score(words, FREQ_REPEAT)

# def print_word_scores(word_scores, top_n=20):
    # WordleHelper.print_word_scores(word_scores, top_n)

# def save_word_scores(word_scores, filename='data/word_scores.csv'):
    # WordleHelper.save_word_scores(word_scores, filename)

# def load_word_scores(filename='data/word_scores.csv'):
    # return WordleHelper.load_word_scores(filename)

# def filter_words(words, guess, feedback):
    # helper = WordleHelper(words)
    # return helper.filter_words(words, guess, feedback)

# def get_best_guess(words, char_count):
    # helper = WordleHelper(words)
    # helper.char_counts[FREQ_REPEAT] = char_count
    # return helper.get_best_guess(words, FREQ_REPEAT)

# def get_top_guesses(words, char_count, top_n=10):
    # helper = WordleHelper(words)
    # helper.char_counts[FREQ_REPEAT] = char_count
    # return helper.get_top_guesses(words, FREQ_REPEAT, top_n)

if __name__ == "__main__":
    helper = WordleHelper()
    helper.print_word_scores()
