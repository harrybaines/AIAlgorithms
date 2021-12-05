# Description: Implementation of the Monte Carlo Tree Search algorithm for
# Tic-Tac-Toe
# Author: Harry Baines
# Date: 26/11/2021
#
# References:
#   [1]: http://tim.hibal.org/blog/alpha-zero-how-and-why-it-works/ (algorithm
#        description)
#   [2]: https://www.youtube.com/watch?v=UXW2yZndl7U (YouTube demo of MCTS by
#        John Levine)
#   [3]: https://vgarciasc.github.io/mcts-viz/ (Tic Tac Toe browser demo)
#   [4]: https://www.youtube.com/watch?v=ghhznqBoESY (YouTube video for [3])
#   [5]: https://nestedsoftware.com/2019/08/07/tic-tac-toe-with-mcts-2h5k.152104.html
#        (general MCTS description)
#   [6]: https://medium.com/swlh/tic-tac-toe-at-the-monte-carlo-a5e0394c7bc2
#        (MCTS overview)
#   [7]: https://en.wikipedia.org/wiki/Monte_Carlo_tree_search#/media/File:MCTS-steps.svg
#        (MCTS Wikipedia)

import random
from typing import Tuple

from mcts import Board, MonteCarloTreeSearch

# Initialize a random seed for deterministic games
SEED = 42
# random.seed(SEED)


class TicTacToe:
    """TicTacToe class to initialize a new Tic-Tac-Toe game"""

    def __init__(self, board: Board = None) -> None:
        """Initializes a new Tic-Tac-Toe game.

        By default, an empty board state is used, however a partial board can
        be used to play the game from a non-starting position by initializing
        MonteCarloTreeSearch with a custom board state.

        Args:
            board (Board, optional): An optional Board object to use at the
                start of the game.
        """
        self.board = Board() if board is None else board

    def play(self) -> None:
        """Begins Tic-Tac-Toe by alternating between human and AI moves"""
        # Initialize MCTS
        self.mcts = MonteCarloTreeSearch()
        self.board.print_board()

        # Game loop
        while True:
            # Player's turn
            (player_row, player_col) = self.get_user_position()
            print("\nPlayers move:")
            self.board.play_move(player_row, player_col, 1)
            self.board.print_board()
            if self.board.is_complete:
                self.print_game_state()
                break

            # AI's turn
            (row, col) = self.mcts.find_best_move(
                board=self.board, iterations=1_000
            )
            print("\nTTTAI's move:")
            self.board.play_move(row, col, -1)
            self.board.print_board()
            if self.board.is_complete:
                self.print_game_state()
                break

    def print_game_state(self) -> None:
        """Prints the result of the game"""
        if self.board.game_state == 0:
            print("Tie!")
        elif self.board.game_state == -1:
            print("Oh no, the AI has won!")
        elif self.board.game_state == 1:
            print("Yay, player has won!")
        return

    def get_user_position(self) -> Tuple[int, int]:
        """Gets the user's input position from the command line.

        The input is a number from 1-9 representing the following positions:
            [
                1 | 2 | 3
                ----------
                4 | 5 | 6
                ----------
                7 | 8 | 9
            ]

        This value is transformed to a row, column pair to index the board
        state.

        Returns:
            Tuple[int, int]: The row, column pair to play on the board state.
        """
        board_size = self.board.size
        total_positions = board_size * board_size
        while True:
            player_position = int(
                input(f"Enter a position (1-{total_positions}): ")
            )
            row = (player_position - 1) // board_size
            col = (player_position - 1) % board_size
            if (
                1 <= player_position <= total_positions
                and self.board.state[row][col] == 0
            ):
                return (row, col)
            print("Not a legal move. Please try again.")


# Entry point
if __name__ == "__main__":
    # TicTacToe(board=Board(state=[[1, -1, -1], [0, 1, 0], [0, 0, 0]])).play()
    TicTacToe().play()
