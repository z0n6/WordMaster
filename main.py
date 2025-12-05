import argparse
from core.helper import WordleHelper, FREQ_ENTROPY, FREQ_UNIQUE

def main():
    parser = argparse.ArgumentParser(description='WordMaster: A Wordle assistant')
    parser.add_argument('--num_suggestions', type=int, default=10, help='Number of suggestions (default: 10)')
    parser.add_argument('--quiet', action='store_true', help='Quiet mode')
    
    # 策略模式
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--wordle', action='store_true', help='Pure Wordle Mode: Exclude past answers from the start')
    group.add_argument('--hybrid', action='store_true', help='Hybrid Mode: Exclude past answers after 1st guess (Recommended)')
    
    # 演算法選項
    parser.add_argument('--algo', choices=['entropy', 'unique'], default='entropy', help='Algorithm (entropy=Smart Entropy, unique=Char Frequency)')
    
    args = parser.parse_args()

    mode = FREQ_ENTROPY if args.algo == 'entropy' else FREQ_UNIQUE

    helper = WordleHelper(
        mode=mode,
        exclude_history=args.wordle,
        hybrid_mode=args.hybrid
    )
    
    helper.play(num_suggestions=args.num_suggestions, quiet=args.quiet)

if __name__ == "__main__":
    main()
