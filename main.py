import argparse
from core.helper import WordleHelper

def main():
    parser = argparse.ArgumentParser(description='WordMaster: A Wordle assistant')
    parser.add_argument('--num_suggestions', type=int, default=10, help='Number of suggestions (default: 10)')
    parser.add_argument('--quiet', action='store_true', help='Quiet mode')
    
    # 策略選項
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--wordle', action='store_true', help='Pure Wordle Mode: Exclude past answers from the start')
    group.add_argument('--hybrid', action='store_true', help='Hybrid Mode: Exclude past answers after 1st guess (Recommended)')
    
    args = parser.parse_args()

    # 初始化 Helper
    helper = WordleHelper(
        exclude_history=args.wordle,  # 純 Wordle 模式
        hybrid_mode=args.hybrid       # 混合模式
    )
    
    helper.play(num_suggestions=args.num_suggestions, quiet=args.quiet)

if __name__ == "__main__":
    main()
