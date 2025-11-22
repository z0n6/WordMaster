document.addEventListener('DOMContentLoaded', function() {
    const messageDiv = document.getElementById('message');
    const suggestionList = document.getElementById('suggestion-list');
    let currentRow = 0;
    let currentCol = 0;

    function startNewGame() {
        fetch('/new_game', { method: 'POST' })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'new_game') {
                    resetBoard();
                    messageDiv.innerHTML = '';
                    document.getElementById('new-game-container').innerHTML = '';
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
        currentCol = 0;
    }

    function submitGuess() {
        const row = document.getElementById(`row-${currentRow}`);
        const letters = row.querySelectorAll('.letter');
        let guess = '';
        for (let i = 0; i < 5; i++) {
            guess += letters[i].textContent;
        }
        guess = guess.trim().toUpperCase();
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
                const newGameBtn = document.createElement('button');
                newGameBtn.id = 'new-game-btn';
                newGameBtn.textContent = 'New Game';
                newGameBtn.addEventListener('click', startNewGame);
                document.getElementById('new-game-container').appendChild(newGameBtn);
            } else if (data.lost) {
                messageDiv.textContent = 'Game over! The word was ' + data.secret;
                const newGameBtn = document.createElement('button');
                newGameBtn.id = 'new-game-btn';
                newGameBtn.textContent = 'New Game';
                newGameBtn.addEventListener('click', startNewGame);
                document.getElementById('new-game-container').appendChild(newGameBtn);
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
        for (let i = 0; i < 5; i++) {
            if (feedback[i] === 'G') {
                letters[i].classList.add('correct');
            } else if (feedback[i] === 'Y') {
                letters[i].classList.add('present');
            } else {
                letters[i].classList.add('absent');
            }
        }
        currentRow++;
        currentCol = 0;
    }

    function updateSuggestions() {
        fetch('/suggestions')
            .then(response => response.json())
            .then(data => {
                suggestionList.innerHTML = '';
                data.suggestions.forEach(suggestion => {
                    const li = document.createElement('li');
                    li.textContent = suggestion;
                    li.style.cursor = 'pointer';
                    li.addEventListener('click', function() {
                        fillRowWithSuggestion(suggestion);
                        submitGuess();
                    });
                    suggestionList.appendChild(li);
                });
            });
    }

    function fillRowWithSuggestion(suggestion) {
        const row = document.getElementById(`row-${currentRow}`);
        const letters = row.querySelectorAll('.letter');
        for (let i = 0; i < 5; i++) {
            letters[i].textContent = suggestion[i].toUpperCase();
        }
        currentCol = 5;
    }

    document.addEventListener('keydown', function(e) {
        if (currentRow >= 6) return; // Game over
        const row = document.getElementById(`row-${currentRow}`);
        const letters = row.querySelectorAll('.letter');

        if (e.key === 'Enter') {
            submitGuess();
        } else if (e.key === 'Backspace') {
            if (currentCol > 0) {
                currentCol--;
                letters[currentCol].textContent = '';
            }
        } else if (e.key.length === 1 && e.key.match(/[a-zA-Z]/) && currentCol < 5) {
            letters[currentCol].textContent = e.key.toUpperCase();
            currentCol++;
        }
    });

    // Start a new game on load
    startNewGame();
});