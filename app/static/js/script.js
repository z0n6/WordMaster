document.addEventListener('DOMContentLoaded', function() {
    const messageDiv = document.getElementById('message');
    const suggestionList = document.getElementById('suggestion-list');
    let currentRow = 0;
    let currentCol = 0;
    let suggestionsOffset = 0;
    let gameOver = false;

    function startNewGame() {
        fetch('/new_game', { method: 'POST' })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'new_game') {
                    resetBoard();
                    messageDiv.innerHTML = '';
                    document.getElementById('new-game-container').innerHTML = '';
                    gameOver = false;
                    document.getElementById('keyboard').classList.remove('disabled');
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
                messageDiv.textContent = 'Congratulations! You Won! 🏆';
                const newGameBtn = document.createElement('button');
                newGameBtn.id = 'new-game-btn';
                newGameBtn.textContent = 'New Game';
                newGameBtn.addEventListener('click', startNewGame);
                document.getElementById('new-game-container').appendChild(newGameBtn);
                gameOver = true;
                document.getElementById('keyboard').classList.add('disabled');
            } else if (data.lost) {
                messageDiv.textContent = 'Game over! The word was ' + data.secret;
                const newGameBtn = document.createElement('button');
                newGameBtn.id = 'new-game-btn';
                newGameBtn.textContent = 'New Game';
                newGameBtn.addEventListener('click', startNewGame);
                document.getElementById('new-game-container').appendChild(newGameBtn);
                gameOver = true;
                document.getElementById('keyboard').classList.add('disabled');
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
        suggestionsOffset = 0;
        fetch(`/suggestions?offset=${suggestionsOffset}&limit=10`)
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
                // Remove existing more button
                const existingMore = document.querySelector('.load-more');
                if (existingMore) existingMore.remove();
                if (data.suggestions.length >= 10 && data.count > 10) {
                    const moreBtn = document.createElement('button');
                    moreBtn.textContent = 'More';
                    moreBtn.classList.add('load-more');
                    moreBtn.addEventListener('click', loadMoreSuggestions);
                    document.getElementById('suggestions').appendChild(moreBtn);
                }
                document.querySelector('#suggestions summary').textContent = `Suggestions (${data.count})`;
            });
    }

    function loadMoreSuggestions() {
        suggestionsOffset += 10;
        fetch(`/suggestions?offset=${suggestionsOffset}&limit=10`)
            .then(response => response.json())
            .then(data => {
                // Remove existing more button
                const existingMore = document.querySelector('.load-more');
                if (existingMore) existingMore.remove();
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
                if (data.suggestions.length >= 10 && suggestionsOffset + 10 < data.count) {
                    const moreBtn = document.createElement('button');
                    moreBtn.textContent = 'More';
                    moreBtn.classList.add('load-more');
                    moreBtn.addEventListener('click', loadMoreSuggestions);
                    document.getElementById('suggestions').appendChild(moreBtn);
                }
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

    function handleKeyPress(key) {
        if (gameOver) return;
        const row = document.getElementById(`row-${currentRow}`);
        const letters = row.querySelectorAll('.letter');

        if (key === 'Enter') {
            submitGuess();
        } else if (key === 'Backspace') {
            if (currentCol > 0) {
                currentCol--;
                letters[currentCol].textContent = '';
            }
        } else if (key.length === 1 && key.match(/[a-zA-Z]/) && currentCol < 5) {
            letters[currentCol].textContent = key.toUpperCase();
            currentCol++;
        }
    }

    document.addEventListener('keydown', function(e) {
        handleKeyPress(e.key);
    });

    // Add click event listeners for virtual keyboard
    document.querySelectorAll('.key').forEach(button => {
        button.addEventListener('click', function() {
            const key = this.getAttribute('data-key');
            handleKeyPress(key);
        });
    });

    // Start a new game on load
    startNewGame();
});
