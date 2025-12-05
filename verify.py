import time
import statistics
import copy
from core.helper import WordleHelper
from core import config

def get_feedback(secret, guess):
    """產生 Wordle 回饋 (G=Green, Y=Yellow, X=Gray)"""
    feedback = ['X'] * 5
    secret_list = list(secret)
    guess_list = list(guess)
    
    # 1. 處理綠色 (G)
    for i in range(5):
        if guess_list[i] == secret_list[i]:
            feedback[i] = 'G'
            secret_list[i] = None
            guess_list[i] = None
            
    # 2. 處理黃色 (Y)
    for i in range(5):
        if guess_list[i] is not None and guess_list[i] in secret_list:
            feedback[i] = 'Y'
            # 移除 secret 中的對應字母確保不會重複匹配
            secret_list[secret_list.index(guess_list[i])] = None
            
    return "".join(feedback)

def simulate_game(secret, strategy_type, past_answers_set, switch_after=0):
    """
    模擬一局遊戲
    :param strategy_type: 'standard', 'exclude', 'hybrid'
    :param switch_after: 僅用於 hybrid 模式，表示在第幾次猜測後排除歷史答案
    """
    # 初始設定：Hybrid 模式一開始也是 Standard (不排除歷史)
    initial_exclude = True if strategy_type == 'exclude' else False
    helper = WordleHelper(exclude_history=initial_exclude)
    
    attempts = 0
    max_attempts = 6
    
    while attempts < max_attempts:
        attempts += 1
        
        # --- 混合策略的核心邏輯 ---
        # 如果是 Hybrid 模式，且剛好達到切換點（例如 switch_after=1，代表第1次猜完後，第2次猜之前）
        if strategy_type == 'hybrid' and attempts == (switch_after + 1):
            # 手動執行排除歷史答案的操作
            original_len = len(helper.words)
            helper.words = [w for w in helper.words if w not in past_answers_set]
            
            # 如果詞彙表有變動，必須重新計算分數
            if len(helper.words) != original_len:
                helper.char_count = helper.analyze_freq()
                helper.word_scores = helper.score(helper.mode, helper.words, helper.char_count)

        guess = helper.get_best_guess()
        
        if guess is None:
            return max_attempts + 1  # 失敗
        
        if guess == secret:
            return attempts
            
        # 產生回饋並過濾
        feedback = get_feedback(secret, guess)
        helper.filter_words(guess, feedback)
        
    return max_attempts + 1  # 失敗

def main():
    print("正在讀取資料...")
    # 1. 讀取所有單字與過往答案
    all_words = WordleHelper.read_words()
    past_answers = WordleHelper.read_past_answers()
    
    if not past_answers:
        print("警告：找不到過往答案資料，無法進行測試。")
        return

    # 2. 定義「未來題目」樣本
    future_secrets = [w for w in all_words if w not in past_answers]
    
    # 為了快速驗證，如果樣本數非常大，可以考慮只取前 500-1000 個
    # future_secrets = future_secrets[:1000] 
    
    print(f"總單字量: {len(all_words)}")
    print(f"過往答案數: {len(past_answers)}")
    print(f"測試樣本數 (未來題目): {len(future_secrets)}")
    print("\n開始進行策略 A/B/C 測試...")
    print("=" * 60)
    
    # 定義要測試的策略
    strategies = [
        # (顯示名稱, 策略類型, 切換回合數)
        ("標準模式 (保留歷史)", 'standard', 0),
        ("純 Wordle 模式 (排除歷史)", 'exclude', 0),
        ("混合模式 (第1猜後排除)", 'hybrid', 1),
        ("混合模式 (第2猜後排除)", 'hybrid', 2),
    ]
    
    results = {}

    for name, s_type, switch_val in strategies:
        print(f"測試中: {name} ...")
        start_time = time.time()
        guesses_record = []
        failures = 0
        
        for secret in future_secrets:
            guesses = simulate_game(secret, s_type, past_answers, switch_after=switch_val)
            
            if guesses > 6:
                failures += 1
            else:
                guesses_record.append(guesses)
                
        duration = time.time() - start_time
        avg_guesses = statistics.mean(guesses_record) if guesses_record else 0
        success_rate = (len(future_secrets) - failures) / len(future_secrets) * 100
        
        results[name] = avg_guesses
        
        print(f"  -> 平均猜測: {avg_guesses:.4f}")
        print(f"  -> 成功率: {success_rate:.2f}% (失敗: {failures})")
        print(f"  -> 耗時: {duration:.2f} 秒")
        print("-" * 60)

    # 最終比較
    print("\n=== 策略排名 (平均猜測次數，越低越好) ===")
    sorted_results = sorted(results.items(), key=lambda x: x[1])
    
    base_score = sorted_results[0][1]
    for i, (name, score) in enumerate(sorted_results):
        diff = score - base_score
        diff_str = f"(+ {diff:.4f})" if i > 0 else "(最佳)"
        print(f"{i+1}. {name}: {score:.4f} {diff_str}")

if __name__ == "__main__":
    main()
