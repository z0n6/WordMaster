from utils import read_words 
from utils import analyze_char_freq, analyze_repeat_char_freq, analyze_unique_char_freq
import matplotlib.pyplot as plt

def plot_char_freq(char_count, output_file='data/char_freq.png'):
    sorted_char_count = sorted(char_count.items(), key=lambda x: x[1], reverse=True)
    sorted_chars, sorted_freqs = zip(*sorted_char_count)
    plt.bar(sorted_chars, sorted_freqs)
    plt.xlabel('Characters')
    plt.ylabel('Frequency')
    plt.title('Character Frequency in Vocabularies')
    plt.savefig(output_file)

if __name__ == "__main__":
   words = read_words()
   char_count = analyze_repeat_char_freq(words) # choose function to count character frequency
   plot_char_freq(char_count)
