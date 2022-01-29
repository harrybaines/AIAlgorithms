from flask import Blueprint, jsonify, render_template, request, make_response
from flaskapp.mcts.tictactoe import TicTacToe
from flaskapp.extensions import cache
from flaskapp.mcts.mcts import Board

home = Blueprint('home', __name__)

@home.route('/')
def homepage():
    return render_template('home.html', title='Home', board_state=Board([[0, 0, 0], [0, 0, 0], [0, 0, 0]]).state)

@home.route('/play', methods=['GET', 'POST'])
def play():
    ttt_board = cache.get('ttt_board')
    if ttt_board is None:
        ttt_board = Board([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
    print(request.form, 'cell' in request.form)
    if 'cell' in request.form:
        cell = int(request.form['cell'])
        ttt = TicTacToe(board=ttt_board) # cache the instance?
        ttt.play(player_position=cell)
        ttt_board = ttt.board
        cache.set("ttt_board", ttt_board)
    else:
        cache.set('ttt_board', None)
        ttt_board = Board([[0, 0, 0], [0, 0, 0], [0, 0, 0]])

    return jsonify(ttt_board.state)