import csv
import math
from collections import Counter
from . import config

# Frequency count criteria constants
FREQ_TOTAL = 'total'
FREQ_REPEAT = 'repeat'
FREQ_UNIQUE = 'unique'
FREQ_ENTROPY = 'entropy'  # 新增演算法常數

class WordleHelper:
    def __init__(self, words=None, mode=FREQ_UNIQUE, exclude_history=False, hybrid_mode=False):
        # 1. 讀取基礎詞彙表
        self.all_words = self.read_words()
        
        if words is None:
            self.words = self.all_words.copy()
        else:
            self.words = words
            
        self.mode = mode
        self.hybrid_mode = hybrid_mode
        self.history_excluded = False

        # 2. 純 Wordle 模式初始化排除
        if exclude_history and not hybrid_mode:
            self.exclude_past_answers()
            print(f"[Mode] Pure Wordle Mode: Past answers excluded from start.")
        elif hybrid_mode:
            print(f"[Mode] Hybrid Mode: Past answers will be excluded after the 1st guess.")

        # 3. 初始化分數
        self.char_count = self.analyze_freq()
        self.word_scores = self.score(self.mode, self.words, self.char_count)

    def exclude_past_answers(self):
        if self.history_excluded:
            return

        past_answers = self.read_past_answers()
        if not past_answers:
            return

        original_count = len(self.words)
        self.words = [w for w in self.words if w not in past_answers]
        self.history_excluded = True
        
        # 重新計算
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
        return past_answers

    def save_new_answer(self, new_answer):
        """將新答案存入歷史檔案 (並維持字母順序)"""
        target_path = config.PAST_ANSWERS_PATH
        new_answer = new_answer.strip().upper()
        
        # 1. 讀取現有答案 (複用現有邏輯)
        current_answers = self.read_past_answers() # 回傳的是 set
        
        # 2. 檢查是否已存在 (避免重複)
        if new_answer in current_answers:
            print(f"[History] '{new_answer}' already exists in history.")
            return False, f"'{new_answer}' 已經在歷史記錄中了。"
            
        # 3. 新增並排序 (Sorting)
        # 對 2000 個字串排序非常快，不會有效能問題
        current_answers.add(new_answer)
        sorted_answers = sorted(list(current_answers))
        
        # 4. 寫回檔案 (單行，逗號分隔)
        try:
            # 確保目錄存在
            target_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(target_path, 'w', encoding='utf-8') as f:
                f.write(",".join(sorted_answers))
                
            print(f"[History] Added '{new_answer}'. Total count: {len(sorted_answers)}")
            return True, f"已成功將 '{new_answer}' 加入歷史記錄。\n目前總數: {len(sorted_answers)}"
        except Exception as e:
            print(f"[History] Save error: {e}")
            return False, f"存檔失敗: {e}"

    # --- 分析邏輯 ---
    def analyze_freq(self):
        # Entropy 模式不需要依賴這裡的 char_count，但為了相容性保留計算
        return self._analyze_unique_char_freq(self.words)

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

    # --- 核心：評分與 Entropy 邏輯 ---
    
    @staticmethod
    def get_feedback_pattern(secret, guess):
        """
        快速計算 Wordle 回饋模式 (用於 Entropy 計算)
        回傳 tuple: (2, 0, 1, 0, 0) 代表 G, X, Y, X, X
        2=Green, 1=Yellow, 0=Gray
        """
        # 優化：直接操作 list/set 
        # 這裡必須準確模擬 Wordle 的黃色判定邏輯
        pattern = [0] * 5
        secret_list = list(secret)
        guess_list = list(guess)
        
        # 1. Green (優先處理)
        for i in range(5):
            if secret_list[i] == guess_list[i]:
                pattern[i] = 2
                secret_list[i] = None # 標記為已使用
                guess_list[i] = None
        
        # 2. Yellow
        for i in range(5):
            if guess_list[i] is not None and guess_list[i] in secret_list:
                pattern[i] = 1
                secret_list[secret_list.index(guess_list[i])] = None # 移除第一個匹配到的字母
                
        return tuple(pattern)

    def calculate_entropy(self, candidates):
        """
        Global Entropy Calculation:
        使用「所有合法單字 (self.all_words)」作為猜測候選 (Guesses)，
        去切割「剩餘的可能答案 (candidates)」(Secrets)。
        """
        scores = []
        total_candidates = len(candidates)
        
        # 如果候選字只剩 1-2 個，直接猜候選字即可，不需要用 Global 搜尋
        if total_candidates <= 2:
            guess_pool = candidates
        else:
            guess_pool = self.all_words  # 開啟上帝視角：允許猜所有字

        # 優化：如果 guess_pool 太大 (例如開局)，這裡會很慢。
        # 但我們的 score() 已經有 >500 切換頻率法的保護，所以這裡通常 candidates < 500。
        # 計算量 = 2300 (all words) * 200 (candidates) ≈ 460,000 次，Python 跑得動 (~0.5s)。

        for guess in guess_pool:
            pattern_counts = Counter()
            
            # 針對每一個可能的答案 (secret)，計算 guess 會得到什麼 pattern
            for secret in candidates:
                pat = self.get_feedback_pattern(secret, guess)
                pattern_counts[pat] += 1
            
            entropy = 0.0
            for count in pattern_counts.values():
                p = count / total_candidates
                if p > 0:
                    entropy -= p * math.log2(p)
            
            # 【加分邏輯】：如果 Entropy 差不多，優先選「是候選字」的詞
            # 這樣如果運氣好可以直接猜中
            is_candidate_bonus = 0.0001 if guess in candidates else 0
            
            scores.append((guess, entropy + is_candidate_bonus))
            
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores

    def score(self, mode, words, char_count):
        # 智慧切換邏輯
        count = len(words)
        
        # 如果指定 Entropy 模式，但單字量太大 (>500)，自動降級為 Unique Frequency
        if mode == FREQ_ENTROPY:
            if count > 500:
                # 為了速度，暫時切換回頻率模式
                mode = FREQ_UNIQUE 
            else:
                return self.calculate_entropy(words)

        # 既有的 Frequency 邏輯
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
        else: # FREQ_UNIQUE or Fallback
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
            # 分數可能是 float (entropy) 或 int (frequency)
            if isinstance(score, float):
                print(f"{word}: {score:.4f} bits")
            else:
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
        # 這裡的 play 邏輯保持不變，因為主要的改變是在 score() 內部
        # 為了完整性，您可以保留之前 helper.py 中的 play 方法
        if not quiet:
            print("Welcome to WordMaster!")
            if self.hybrid_mode:
                print("(Hybrid Mode: Past answers excluded after 1st guess)")
            elif self.history_excluded:
                print("(Wordle Mode: Past answers excluded from start)")
            
            if self.mode == FREQ_ENTROPY:
                print("(Algorithm: Smart Entropy - Auto-switch based on remaining words)")
            
            print("Example: GYXXG")
            print()

        won = False
        for attempt in range(1, 7):
            if not self.words:
                print("No possible words left!")
                break

            if self.hybrid_mode and attempt == 2:
                self.exclude_past_answers()

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
                    # 判斷分數類型來顯示不同單位
                    score = self.word_scores[i-1][1]
                    if isinstance(score, float):
                        print(f"{i}. {guess} ({score:.2f} bits)")
                    else:
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
