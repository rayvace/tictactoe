from board.board import Board
from rules.rules import Rules
from ai.ai import ArtificialIntelligence

from flask import Flask, request, redirect, url_for
from flask import session, jsonify, render_template

from werkzeug.contrib.cache import SimpleCache

import os
import config
import random

app = Flask(__name__, static_url_path='/static')
app.secret_key = os.environ.get('SECRET_KEY') or config.SECRET_KEY
cache = SimpleCache()


def get_session_key():
    return ''.join(random.choice('0123456789ABCDEF') for i in range(16))


@app.route('/play', methods=['POST'])
def set_next_move():
    """
    Add human player's move to the board.

    Expects:

    {position: 3, mark: X}
    """
    state = cache.get(session['key'])
    board = state['board']
    rules = state['rules']
    next = state['next']

    position = request.form['position']
    mark = request.form['mark']

    # Check is player is moving out of turn or
    # if game is already over
    if next != mark:
        return jsonify(success=False)

    valid = board.add_mark(mark, int(position))
    end_game, result = rules.end_game(position)

    #Check if last move wins or bring the game to a draw
    if end_game:
        state['next'] = None
        cache.set(session['key'], state)
        res = 'Computer wins!' if result == 'win' else 'It\'s a Draw'
        return jsonify(success=valid, position=position, result=res)

    state['next'] = rules.get_current_player()
    cache.set(session['key'], state)
    return jsonify(success=valid, position=position)


@app.route('/play', methods=['GET'])
def get_next_move():
    """
    Get the computer's next move.
    """
    state = cache.get(session['key'])
    rules = state['rules']
    board = state['board']
    player = state['player']
    next = state['next']

    #Check if game is already over
    if not next:
        return jsonify(success=False)

    position = player.next_move()
    board.add_mark(player.mark, int(position))

    #Check if last move wins or bring the game to a draw
    end_game, result = rules.end_game(position)
    if end_game:
        state['next'] = None
        cache.set(session['key'], state)
        res = 'Computer wins!' if result == 'win' else 'It\'s a Draw'
        return jsonify(position=position, result=res)

    state['next'] = rules.get_current_player()
    cache.set(session['key'], state)
    return jsonify(position=int(position))

@app.route("/init", methods=['POST'])
def init():
    state = cache.get(session['key'])
    rules = state['rules']
    player = state['player']

    order = request.form['order']
    mark = request.form['mark']

    computer_mark = 'O' if mark == 'X' else 'X'
    next_play = mark if order == '1' else computer_mark

    #initialize
    rules.next_play = next_play
    player.set_mark(computer_mark)

    state['player'] = player
    state['rules'] = rules
    state['next'] = rules.get_current_player()
    
    cache.set(session['key'], state)
    return jsonify(success=True)

@app.route("/restart")
def restart():
    # Clear the session
    session.clear()
    cache.clear()

    # Redirect the user to the main page
    return redirect(url_for('tictactoe'))

@app.route("/")
def tictactoe():
    #check for existing session
    if 'key' in session:
        # Clear the session
        session.clear()
        cache.clear()
        
    #simple caching for demo purposes only
    key = get_session_key()
    session['key'] = key

    board = Board()
    rules = Rules()
    player = ArtificialIntelligence()

    #initialize
    rules.next_play = 'O'
    rules.set_board(board)
    player.set_board(board)

    state = {
        'board': board,
        'rules': rules,
        'player': player,
        'next': rules.get_current_player()
    }

    cache.set(key, state)

    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
