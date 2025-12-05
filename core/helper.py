import csv
from collections import Counter
from . import config

# Frequency count criteria constants
FREQ_TOTAL = 'total'
FREQ_REPEAT = 'repeat'
FREQ_UNIQUE = 'unique'

class WordleHelper:
    def __init__(self, words=None, mode=FREQ_UNIQUE, exclude_history=False, hybrid_mode=False):
        # 1. 讀取基礎詞彙表
        if words is None:
            self.words = self.read_words()
        else:
            self.words = words
            
        self.mode = mode
        self.hybrid_mode = hybrid_mode
        self.history_excluded = False  # 標記是否已經執行過排除

        # 2. 如果是「純 Wordle 模式」，初始化時直接排除
        # (如果是混合模式，初始化時先不排除，等第二回合再做)
        if exclude_history and not hybrid_mode:
            self.exclude_past_answers()
            print(f"[Mode] Pure Wordle Mode: Past answers excluded from start.")
        elif hybrid_mode:
            print(f"[Mode] Hybrid Mode: Past answers will be excluded after the 1st guess.")

        # 3. 初始化分數
        self.char_count = self.analyze_freq()
        self.word_scores = self.score(self.mode, self.words, self.char_count)

    def exclude_past_answers(self):
        """讀取並排除過往答案的核心邏輯"""
        if self.history_excluded:
            return  # 避免重複執行

        past_answers = self.read_past_answers()
        if not past_answers:
            return

        original_count = len(self.words)
        # 過濾掉已經出現過的字
        self.words = [w for w in self.words if w not in past_answers]
        self.history_excluded = True
        
        # 資料變動後，必須重新計算頻率與分數
        self.char_count = self.analyze_freq()
        self.word_scores = self.score(self.mode, self.words, self.char_count)

        print(f"\n[Strategy Update] Loaded {len(past_answers)} past answers.")
        print(f"[Strategy Update] Vocabulary reduced from {original_count} to {len(self.words)} words.")

    @staticmethod
    def read_words(filename=None):
        target_path = filename if filename else config.VOCAB_PATH
        try:
            with open(target_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                try:
                    row = next(reader)
                    words = [word.strip() for word in row if word.strip()]
                except StopIteration:
                    words = []
            return words
        except FileNotFoundError:
            print(f"Error: Vocabulary file not found at {target_path}")
            return []

    @staticmethod
    def read_past_answers():
        """讀取過往答案 (格式：單行，以逗號分隔)"""
        target_path = config.PAST_ANSWERS_PATH
        past_answers = set()
        
        if target_path.exists():
            try:
                with open(target_path, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    if content:
                        words = content.split(',')
                        past_answers = {w.strip().upper() for w in words if w.strip()}
            except Exception as e:
                print(f"Warning: Failed to read past answers: {e}")
        else:
            print(f"Warning: Past answers file not found at {target_path}")
            
        return past_answers

    # --- 分析與評分邏輯 (保持不變) ---
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
    
    def filter_words(self, guess, feedback):
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
            print("Example: GYXXG")
            print()

        won = False
        for attempt in range(1, 7):
            if not self.words:
                print("No possible words left!")
                break

            # --- 混合模式邏輯：第 2 回合前排除歷史答案 ---
            if self.hybrid_mode and attempt == 2:
                self.exclude_past_answers()
            # ----------------------------------------

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
                    choice = input(f"Choose a guess (1-{num_suggestions}), enter word, or 'quit': ").strip()
                    if choice.upper() == 'QUIT':
                        won = True
                        break
                    try:
                        if choice.isalpha() and len(choice) == 5:
                            guess = choice.upper()
                            break
                        choice_num = int(choice)
                        if 1 <= choice_num <= len(top_guesses):
                            guess = top_guesses[choice_num - 1]
                            break
                    except ValueError:
                        pass
                    print("Invalid input.")

                if choice.upper() == 'QUIT':
                    break

            prompt = "" if quiet else "Enter feedback (or 'quit'): "
            feedback = input(prompt).strip().upper()
            if feedback == 'QUIT':
                break
            if len(feedback) != 5 or not all(c in 'GYX' for c in feedback):
                print("Invalid feedback. Use G, Y, X.")
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
