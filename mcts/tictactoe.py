# Description: Implementation of the Monte Carlo Tree Search algorithm for
# Tic-Tac-Toe
# Author: Harry Baines
# Date: 26/11/2021
#
# References:
#   [1]: http://tim.hibal.org/blog/alpha-zero-how-and-why-it-works/ (algorithm
#        description)

import random
from typing import Tuple

from mcts.mcts import Board, MonteCarloTreeSearch, Node

# Initialize a random seed for deterministic games
SEED = 42
random.seed(SEED)


class TicTacToe:
    """TicTacToe class to initialize a new Tic-Tac-Toe game"""

    def __init__(self) -> None:
        """Initializes a new Tic-Tac-Toe game.

        By default, an empty board state is used, however a partial board can
        be used to play the game from a non-starting position.
        """
        self.board = Board()  # [[0, 0, 0], [0, -1, 0], [1, 0, -1]]

    def play(self) -> None:
        """Begins the Tic-Tac-Toe game by alternating between human and AI
        moves"""
        self.board.print_board()
        self.mcts = MonteCarloTreeSearch(board=self.board)
        while True:
            (player_row, player_col) = self.get_user_position()
            print("Players move:")
            self.board.play_move(player_row, player_col, 1)
            self.board.print_board()

            (row, col) = self.mcts.find_best_move(iterations=100)
            self.board.play_move(row, col, -1)
            print("TTTAI's move:")
            self.board.print_board()

            # Update root for next round of play
            self.mcts.root_node = Node(board=self.board)

            if self.board.is_finished:
                print("Finished!")
                break

    def get_user_position(self) -> Tuple[int, int]:
        """Gets the user's input position from the command line.

        The input is a number from 1-9 representing the following positions:

            [
                [1, 2, 3],
                [4, 5, 6],
                [7, 8, 9]
            ]

        This value is transformed to a row, column pair to index the board
        state.

        Returns:
            Tuple[int, int]: The row, column pair to play on the board state.
        """
        while True:
            player_position = int(input("Enter a position (1-9) to play > "))
            row = (player_position - 1) // 3
            col = (player_position - 1) % 3
            if 1 <= player_position <= 9 and self.board.state[row][col] == 0:
                return (row, col)
            print("Not a legal move. Please try again.")


# Entry point
if __name__ == "__main__":
    TicTacToe().play()
