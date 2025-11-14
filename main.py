import argparse
from utils import WordleHelper

def main():
    parser = argparse.ArgumentParser(description='WordMaster: A Wordle assistant')
    parser.add_argument('--num_suggestions', type=int, default=10, help='Number of suggestion guesses to show (default: 10)')
    parser.add_argument('--quiet', action='store_true', help='Quiet mode: only show top suggestion and wait for feedback')
    args = parser.parse_args()

    helper = WordleHelper()
    helper.play(num_suggestions=args.num_suggestions, quiet=args.quiet)

if __name__ == "__main__":
    main()
