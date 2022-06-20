import copy
import json

from flask import Blueprint, jsonify, render_template, request
from flaskapp.mcts.mcts import Board
from flaskapp.mcts.tictactoe import TicTacToe

home = Blueprint("home", __name__)


@home.route("/", methods=["GET", "POST"])
def homepage():
    return render_template(
        "home.html", title="Tic-Tac-Toe MCTS", board_state=Board().state
    )


@home.route("/board", methods=["GET", "POST"])
def board():
    board_size = (
        None
        if "board_size" not in request.form
        else int(request.form["board_size"])
    )
    return render_template(
        "board.html", board_state=Board(board_size=board_size).state
    )


@home.route("/play", methods=["GET", "POST"])
def play():
    game_state_message = None
    board_size = (
        None
        if "board_size" not in request.form
        else int(request.form["board_size"])
    )
    mcts_iterations = (
        1000
        if "mcts_iterations" not in request.form
        else int(request.form["mcts_iterations"])
    )

    board_state = json.loads(request.form["board_state"])

    if board_state is None:
        ttt_board = Board(board_size=board_size)
    else:
        ttt_board = Board(state=board_state, board_size=board_size)

    if "cell" in request.form:
        cell = int(request.form["cell"])
        ttt = TicTacToe(board=ttt_board)
        ttt.play(player_position=cell, iterations=mcts_iterations)
        ttt_board = ttt.board
        game_state_message = ttt.game_state_msg
    else:
        ttt_board = copy.deepcopy(Board(board_size=board_size))

    return jsonify(
        {"board": ttt_board.state, "game_state_message": game_state_message}
    )
