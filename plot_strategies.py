import csv
import matplotlib.pyplot as plt
import numpy as np

def main():
    data = []
    with open('data/strategy_results.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)

    # Group data by strategy type
    total_data = [row for row in data if 'Total Frequency' in row['Strategy']]
    repeat_data = [row for row in data if 'Repeat Frequency' in row['Strategy']]
    unique_data = [row for row in data if 'Unique Frequency' in row['Strategy']]

    # Extract x-axis labels (top n guesses)
    x_labels = ['Best', 'Random Top 3', 'Random Top 5', 'Random Top 10']

    # Success rates for each strategy type
    total_success = [float(row['Success Rate (%)']) for row in total_data]
    repeat_success = [float(row['Success Rate (%)']) for row in repeat_data]
    unique_success = [float(row['Success Rate (%)']) for row in unique_data]

    # Failed games for each strategy type
    total_failed = [int(row['Failed']) for row in total_data]
    repeat_failed = [int(row['Failed']) for row in repeat_data]
    unique_failed = [int(row['Failed']) for row in unique_data]

    # Average guesses for each strategy type
    total_avg_guesses = [float(row['Avg Guesses (Successful)']) for row in total_data]
    repeat_avg_guesses = [float(row['Avg Guesses (Successful)']) for row in repeat_data]
    unique_avg_guesses = [float(row['Avg Guesses (Successful)']) for row in unique_data]

    # Line chart for success rates
    plt.figure(figsize=(10, 6))
    plt.plot(x_labels, total_success, marker='o', label='Total', color='blue')
    plt.plot(x_labels, repeat_success, marker='s', label='Repeat', color='green')
    plt.plot(x_labels, unique_success, marker='^', label='Unique', color='red')
    plt.title('Success Rates by Strategy Type and Selection Method')
    plt.xlabel('Selection Method')
    plt.ylabel('Success Rate (%)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('data/success_rates_line.png')
    plt.close()

    # Line chart for failed games
    plt.figure(figsize=(10, 6))
    plt.plot(x_labels, total_failed, marker='o', label='Total', color='blue')
    plt.plot(x_labels, repeat_failed, marker='s', label='Repeat', color='green')
    plt.plot(x_labels, unique_failed, marker='^', label='Unique', color='red')
    plt.title('Failed Games by Strategy Type and Selection Method')
    plt.xlabel('Selection Method')
    plt.ylabel('Number of Failed Games')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('data/failed_games_line.png')
    plt.close()

    # Line chart for average guesses
    plt.figure(figsize=(10, 6))
    plt.plot(x_labels, total_avg_guesses, marker='o', label='Total', color='blue')
    plt.plot(x_labels, repeat_avg_guesses, marker='s', label='Repeat', color='green')
    plt.plot(x_labels, unique_avg_guesses, marker='^', label='Unique', color='red')
    plt.title('Average Guesses by Strategy Type and Selection Method')
    plt.xlabel('Selection Method')
    plt.ylabel('Average Guesses (Successful)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('data/average_guesses_line.png')
    plt.close()

if __name__ == "__main__":
    main()
