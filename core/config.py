import os
from pathlib import Path

# 取得專案根目錄路徑
# __file__ 是 config.py 的路徑，parent 是 wordmaster_core，parent.parent 就是專案根目錄
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / 'data'

# 定義具體的資料檔案路徑
VOCAB_PATH = DATA_DIR / 'vocabularies.csv'
# 預留給之後的歷史檔案
PAST_ANSWERS_PATH = DATA_DIR / 'answers.csv' 
STRATEGY_RESULTS_PATH = DATA_DIR / 'strategy_results.csv'
