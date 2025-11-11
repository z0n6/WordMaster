import csv
from collections import Counter

def read_words(filename='data/vocabularies.csv'):
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        row = next(reader)
        words = [word.strip() for word in row if word.strip()]
    return words

def analyze_char_freq(words):
    char_count = Counter()
    for word in words:
        for char in word.lower():
            char_count[char] += 1
    return char_count

def analyze_repeat_char_freq(words):
    char_count = Counter()
    for word in words:
        count = Counter(word.lower())
        while count.most_common()[0][1] > 1:
            char, times = count.most_common()[0]
            count[char] -= 1
            count[char*times] += 1
        char_count.update(count)
    
    return char_count

def analyze_unique_char_freq(words):
    char_count = Counter()
    for word in words:
        for char in set(word.lower()):
            char_count[char] += 1
    return char_count

def score_words(words, char_count):
    word_scores = []
    for word in words:
        score = sum(char_count[char.lower()] for char in set(word))
        word_scores.append((word, score))
    word_scores.sort(key=lambda x: x[1], reverse=True)
    return word_scores

def print_word_scores(word_scores, top_n=20):
    print(f"Top {top_n} words by score:")
    for word, score in word_scores[:top_n]:
        print(f"{word}: {score}")
    print()

def save_word_scores(word_scores, filename='data/word_scores.csv'):
    with open(filename, 'w') as f:
        f.write("word,score\n")
        for word, score in word_scores:
            f.write(f"{word},{score}\n")

def load_word_scores(filename='data/word_scores.csv'):
    word_scores = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        for row in reader:
            word, score = row
            word_scores.append((word, int(score)))
    return word_scores

def filter_words(words, guess, feedback):
    """
    Filter words based on Wordle feedback.
    guess: 5-letter string
    feedback: 5-character string, G=green, Y=yellow, X=gray
    """
    filtered = []
    for word in words:
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
                if guess[i] in word and feedback[word.index(guess[i])] != 'G':
                    valid = False
                    break
        if not valid:
            continue
        filtered.append(word)
    return filtered

def get_best_guess(words, char_count):
    """
    Get the highest scored word from the list.
    """
    if not words:
        return None
    word_scores = score_words(words, char_count)
    return word_scores[0][0]

def get_top_guesses(words, char_count, top_n=10):
    """
    Get the top n highest scored words from the list.
    """
    if not words:
        return []
    word_scores = score_words(words, char_count)
    return [word for word, score in word_scores[:top_n]]
