from flask import Blueprint, jsonify, render_template, request
from flaskapp.mcts.tictactoe import TicTacToe
from flaskapp.extensions import cache
from flaskapp.mcts.mcts import Board
import copy

home = Blueprint('home', __name__)

@home.route('/')
def homepage():
    cache.set('ttt_board', None)
    return render_template('home.html', title='Home', board_state=Board().state)

@home.route('/play', methods=['GET', 'POST'])
def play():
    game_state_message = None
    ttt_board = cache.get('ttt_board')
    if ttt_board is None:
        ttt_board = Board([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
    if 'cell' in request.form:
        cell = int(request.form['cell'])
        ttt = TicTacToe(board=ttt_board)
        ttt.play(player_position=cell)
        ttt_board = ttt.board
        cache.set("ttt_board", ttt_board)
        game_state_message = ttt.game_state_msg
    else:
        ttt_board = copy.deepcopy(Board())
        cache.set('ttt_board', None)

    return jsonify({
        'board': ttt_board.state,
        'game_state_message': game_state_message
    })