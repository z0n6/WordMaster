from flask import Flask, render_template, request, session, jsonify
import random
from utils import WordleHelper
from play_wordle import get_feedback

app = Flask(__name__)
app.secret_key = 'wordle_secret_key'  # Change this in production

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/new_game', methods=['POST'])
def new_game():
    words = WordleHelper.read_words()
    session['secret'] = random.choice(words)
    session['attempts'] = []
    session['won'] = False
    session['lost'] = False
    return jsonify({'status': 'new_game'})

@app.route('/guess', methods=['POST'])
def guess():
    data = request.get_json()
    guess = data['guess'].strip().upper()
    words = WordleHelper.read_words()
    if len(guess) != 5 or not guess.isalpha() or guess not in words:
        return jsonify({'error': 'Invalid guess'}), 400

    if 'secret' not in session:
        return jsonify({'error': 'No active game'}), 400

    secret = session['secret']
    feedback = get_feedback(secret, guess)
    session['attempts'].append({'guess': guess, 'feedback': feedback})
    session.modified = True

    if feedback == 'GGGGG':
        session['won'] = True
    elif len(session['attempts']) >= 6:
        session['lost'] = True

    response = {
        'feedback': feedback,
        'won': session.get('won', False),
        'lost': session.get('lost', False),
        'attempts': session['attempts']
    }
    if session.get('lost', False):
        response['secret'] = secret
    return jsonify(response)

@app.route('/suggestions', methods=['GET'])
def suggestions():
    if 'secret' not in session or session.get('won') or session.get('lost'):
        return jsonify({'suggestions': [], 'count': 0})

    offset = int(request.args.get('offset', 0))
    limit = int(request.args.get('limit', 10))

    helper = WordleHelper()
    # Filter based on previous attempts
    for attempt in session['attempts']:
        helper.filter_words(attempt['guess'], attempt['feedback'])

    all_suggestions = helper.get_top_guesses(len(helper.words))  # Get all to slice
    suggestions = all_suggestions[offset:offset + limit]
    return jsonify({'suggestions': suggestions, 'count': len(helper.words)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
