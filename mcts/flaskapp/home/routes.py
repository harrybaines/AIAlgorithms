from flask import Blueprint, render_template, request, make_response
from flaskapp.mcts.tictactoe import TicTacToe
from flaskapp.extensions import cache
from flaskapp.mcts.mcts import Board

home = Blueprint('home', __name__)

@home.route('/', methods=['GET', 'POST'])
def homepage():
    return render_template('home.html', title='Home')

@home.route('/play', methods=['GET', 'POST'])
def play():
    ttt_board = cache.get('ttt_board')
    if ttt_board is None:
        ttt_board = Board([[0, 0, 0], [0, 0, 0], [0, 0, 0]])

    if 'cell' in request.form:
        cell = int(request.form['cell'])
        ttt = TicTacToe(board=ttt_board)
        ttt.play(player_position=cell)
        ttt_board = ttt.board
        cache.set("ttt_board", ttt_board)

    resp = make_response(
        render_template(
            'home.html', 
            board_state=ttt_board.state, 
            msg='Hi'
        )
    )
    return resp

@home.route('/about')
def about():
    return render_template('about.html', title='About')
