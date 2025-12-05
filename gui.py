import tkinter as tk
from tkinter import ttk, messagebox
import threading

# 引用您的核心模組
try:
    from core.helper import WordleHelper, FREQ_ENTROPY
except ImportError:
    # fallback if run from inside a folder
    import sys
    import os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from core.helper import WordleHelper, FREQ_ENTROPY

class WordleSolverGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("WordMaster Solver")
        self.root.geometry("700x500")
        self.root.resizable(False, False)

        # 樣式設定
        self.colors = {
            'X': '#787c7e', # Gray
            'Y': '#c9b458', # Yellow
            'G': '#6aaa64', # Green
            'DEFAULT': '#ffffff',
            'TEXT': '#000000'
        }
        
        # 遊戲狀態
        self.helper = None
        self.attempt = 0
        self.current_feedback = ['X'] * 5  # 預設全灰
        
        self._init_ui()
        self.start_new_game()

    def _init_ui(self):
        # 主框架：左右分割
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 左側：遊戲盤面 (History)
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        ttk.Label(left_frame, text="Game History", font=("Arial", 12, "bold")).pack(pady=(0, 10))
        
        self.rows = []
        board_frame = ttk.Frame(left_frame)
        board_frame.pack()
        
        for i in range(6):
            row_widgets = []
            row_frame = ttk.Frame(board_frame)
            row_frame.pack(pady=2)
            for j in range(5):
                lbl = tk.Label(
                    row_frame, 
                    text="", 
                    width=4, 
                    height=2, 
                    font=("Helvetica", 16, "bold"),
                    bg="white", 
                    relief="solid", 
                    borderwidth=1
                )
                lbl.pack(side=tk.LEFT, padx=2)
                row_widgets.append(lbl)
            self.rows.append(row_widgets)

        # 右側：控制區與建議區
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # 1. 策略選擇
        strategy_frame = ttk.LabelFrame(right_frame, text="Strategy Mode", padding="5")
        strategy_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.mode_var = tk.StringVar(value="hybrid")
        ttk.Radiobutton(strategy_frame, text="Hybrid (Recommended)", variable=self.mode_var, value="hybrid", command=self.start_new_game).pack(anchor=tk.W)
        ttk.Radiobutton(strategy_frame, text="Pure Wordle (Exclude All)", variable=self.mode_var, value="wordle", command=self.start_new_game).pack(anchor=tk.W)
        ttk.Radiobutton(strategy_frame, text="Standard (Include All)", variable=self.mode_var, value="standard", command=self.start_new_game).pack(anchor=tk.W)

        # 2. 輸區
        input_frame = ttk.LabelFrame(right_frame, text="Enter Guess & Feedback", padding="10")
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 單字輸入
        entry_frame = ttk.Frame(input_frame)
        entry_frame.pack(fill=tk.X, pady=(0, 5))
        ttk.Label(entry_frame, text="Word:").pack(side=tk.LEFT)
        self.word_entry = ttk.Entry(entry_frame, font=("Courier", 12))
        self.word_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.word_entry.bind('<Return>', lambda e: self.submit_guess())
        
        # === 修正部分：回饋按鈕 (改用 Label 以支援 Mac 背景色) ===
        feedback_frame = ttk.Frame(input_frame)
        feedback_frame.pack(pady=5)
        self.feedback_btns = []
        for i in range(5):
            # 使用 Label 模擬按鈕
            lbl = tk.Label(
                feedback_frame, 
                text="X", 
                width=6, # 稍微加寬一點
                height=2,
                font=("Arial", 12, "bold"),
                bg=self.colors['X'],
                fg='white',
                relief="raised", # 增加立體感
                cursor="hand2"   # 滑鼠游標變手型
            )
            lbl.pack(side=tk.LEFT, padx=5)
            # 綁定點擊事件
            lbl.bind("<Button-1>", lambda event, idx=i: self.toggle_feedback(idx))
            self.feedback_btns.append(lbl)
            
        ttk.Label(input_frame, text="(Click blocks to change color)", font=("Arial", 8)).pack()
        
        # 送出按鈕
        self.submit_btn = ttk.Button(input_frame, text="Submit Feedback", command=self.submit_guess)
        self.submit_btn.pack(fill=tk.X, pady=(10, 0))

        # 3. 建議列表
        suggest_frame = ttk.LabelFrame(right_frame, text="Top Suggestions", padding="5")
        suggest_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar and Listbox
        scrollbar = ttk.Scrollbar(suggest_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.suggest_list = tk.Listbox(suggest_frame, font=("Courier", 11), yscrollcommand=scrollbar.set)
        self.suggest_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.suggest_list.bind('<<ListboxSelect>>', self.on_suggest_select)
        
        scrollbar.config(command=self.suggest_list.yview)
        
        # 底部狀態列
        self.status_var = tk.StringVar()
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def start_new_game(self):
        mode = self.mode_var.get()
        
        # 初始化 Helper
        exclude = (mode == "wordle")
        hybrid = (mode == "hybrid")
        
        self.status_var.set("Loading vocabulary...")
        self.root.update()
        
        try:
            self.helper = WordleHelper(exclude_history=exclude, hybrid_mode=hybrid)
            self.attempt = 0
            self.update_suggestions()
            self.clear_board()
            self.reset_inputs()
            
            # 更新狀態文字
            count = len(self.helper.words)
            if hybrid:
                msg = f"Hybrid Mode: {count} words. (Excludes history after guess #1)"
            elif exclude:
                msg = f"Wordle Mode: {count} words. (History excluded)"
            else:
                msg = f"Standard Mode: {count} words."
            self.status_var.set(msg)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to initialize helper: {e}")

    def clear_board(self):
        for row in self.rows:
            for lbl in row:
                lbl.config(text="", bg="white")

    def reset_inputs(self):
        self.word_entry.delete(0, tk.END)
        self.current_feedback = ['X'] * 5
        for btn in self.feedback_btns:
            btn.config(text="X", bg=self.colors['X'])
        self.word_entry.focus()

    def toggle_feedback(self, idx):
        # 循環切換狀態: X -> Y -> G -> X
        current = self.current_feedback[idx]
        if current == 'X':
            new_state = 'Y'
        elif current == 'Y':
            new_state = 'G'
        else:
            new_state = 'X'
            
        self.current_feedback[idx] = new_state
        # 對 Label 使用 config 設定顏色是跨平台有效的
        self.feedback_btns[idx].config(
            text=new_state, 
            bg=self.colors[new_state]
        )

    def on_suggest_select(self, event):
        # 點擊建議列表時，自動填入輸入框
        selection = self.suggest_list.curselection()
        if selection:
            word = self.suggest_list.get(selection[0])
            clean_word = word.split('.')[-1].strip()
            self.word_entry.delete(0, tk.END)
            self.word_entry.insert(0, clean_word)

    def update_suggestions(self):
        self.suggest_list.delete(0, tk.END)
        if not self.helper.words:
            self.suggest_list.insert(tk.END, "No possible words!")
            return

        suggestions = self.helper.get_top_guesses(20)
        for i, word in enumerate(suggestions, 1):
            self.suggest_list.insert(tk.END, f"{i}. {word}")

    def submit_guess(self):
        guess = self.word_entry.get().strip().upper()
        
        # 驗證輸入
        if len(guess) != 5 or not guess.isalpha():
            messagebox.showwarning("Invalid Input", "Please enter a valid 5-letter word.")
            return
        
        if self.attempt >= 6:
            messagebox.showinfo("Game Over", "Max attempts reached. Start a new game.")
            return

        # 更新盤面顯示
        row_widgets = self.rows[self.attempt]
        feedback_str = "".join(self.current_feedback)
        
        for i in range(5):
            char = guess[i]
            color_code = self.current_feedback[i]
            row_widgets[i].config(text=char, bg=self.colors[color_code])

        # 增加嘗試次數
        self.attempt += 1
        
        # --- 混合模式邏輯 ---
        if self.helper.hybrid_mode and self.attempt == 1:
            self.helper.exclude_past_answers()
            self.status_var.set(f"Hybrid Mode: Past answers excluded. {len(self.helper.words)} words remaining.")
        
        # 執行過濾
        try:
            self.helper.filter_words(guess, feedback_str)
            
            # 更新建議
            self.update_suggestions()
            
            # 更新狀態列
            remaining = len(self.helper.words)
            if feedback_str == "GGGGG":
                messagebox.showinfo("Success", f"Congratulations! Word found: {guess}")
                self.status_var.set("Solved!")

                should_save = messagebox.askyesno(
                    "Update History", 
                    f"Do you want to add '{guess}' to the past answers list?\n(This will exclude it from future games)"
                )
                
                if should_save:
                    success, msg = self.helper.save_new_answer(guess)
                    if success:
                        messagebox.showinfo("History Updated", msg)
                    else:
                        messagebox.showwarning("Update Skipped", msg)
            else:
                current_msg = self.status_var.get().split('.')[0]
                self.status_var.set(f"{current_msg}. Remaining words: {remaining}")
                self.reset_inputs()
                
        except Exception as e:
            messagebox.showerror("Error", f"Error filtering words: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = WordleSolverGUI(root)
    root.mainloop()
