document.addEventListener('DOMContentLoaded', function() {
    const guessInput = document.getElementById('guess-input');
    const submitButton = document.getElementById('submit-guess');
    const newGameButton = document.getElementById('new-game');
    const messageDiv = document.getElementById('message');
    const suggestionList = document.getElementById('suggestion-list');
    let currentRow = 0;

    function startNewGame() {
        fetch('/new_game', { method: 'POST' })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'new_game') {
                    resetBoard();
                    messageDiv.textContent = '';
                    updateSuggestions();
                }
            });
    }

    function resetBoard() {
        for (let i = 0; i < 6; i++) {
            const row = document.getElementById(`row-${i}`);
            const letters = row.querySelectorAll('.letter');
            letters.forEach(letter => {
                letter.textContent = '';
                letter.className = 'letter';
            });
        }
        currentRow = 0;
        guessInput.value = '';
        guessInput.disabled = false;
        submitButton.disabled = false;
    }

    function submitGuess() {
        const guess = guessInput.value.trim().toUpperCase();
        if (guess.length !== 5) {
            messageDiv.textContent = 'Please enter a 5-letter word.';
            return;
        }

        fetch('/guess', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ guess: guess })
        })
        .then(response => {
            if (response.status === 400) {
                return response.json().then(data => {
                    messageDiv.textContent = data.error;
                    throw new Error(data.error);
                });
            }
            return response.json();
        })
        .then(data => {
            updateBoard(data.feedback);
            if (data.won) {
                messageDiv.textContent = 'Congratulations! You won!';
                guessInput.disabled = true;
                submitButton.disabled = true;
            } else if (data.lost) {
                messageDiv.textContent = 'Game over! The word was ' + data.attempts[data.attempts.length - 1].guess;
                guessInput.disabled = true;
                submitButton.disabled = true;
            } else {
                messageDiv.textContent = '';
            }
            updateSuggestions();
        })
        .catch(error => console.error('Error:', error));
    }

    function updateBoard(feedback) {
        const row = document.getElementById(`row-${currentRow}`);
        const letters = row.querySelectorAll('.letter');
        const guess = guessInput.value.trim().toUpperCase();
        for (let i = 0; i < 5; i++) {
            letters[i].textContent = guess[i];
            if (feedback[i] === 'G') {
                letters[i].classList.add('correct');
            } else if (feedback[i] === 'Y') {
                letters[i].classList.add('present');
            } else {
                letters[i].classList.add('absent');
            }
        }
        currentRow++;
        guessInput.value = '';
    }

    function updateSuggestions() {
        fetch('/suggestions')
            .then(response => response.json())
            .then(data => {
                suggestionList.innerHTML = '';
                data.suggestions.forEach(suggestion => {
                    const li = document.createElement('li');
                    li.textContent = suggestion;
                    suggestionList.appendChild(li);
                });
            });
    }

    submitButton.addEventListener('click', submitGuess);
    newGameButton.addEventListener('click', startNewGame);
    guessInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            submitGuess();
        }
    });

    // Start a new game on load
    startNewGame();
});