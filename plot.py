from utils import WordleHelper, FREQ_TOTAL, FREQ_REPEAT, FREQ_UNIQUE

if __name__ == "__main__":
    modes = {FREQ_TOTAL, FREQ_REPEAT, FREQ_UNIQUE}
    for mode in modes:
        helper = WordleHelper(mode=mode)
        helper.plot_char_freq(output_file=f'data/char_freq_{mode}')
