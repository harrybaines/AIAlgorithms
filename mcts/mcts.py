import copy
import random
from typing import List, Optional, Tuple

from mcts import utils


class MonteCarloTreeSearch:
    """Monte Carlo Tree Search class"""

    def __init__(self, board: "Board") -> None:
        """Initializes the MonteCarloTreeSearch class by constructing the
        search tree with a new root node, initialized to the board state
        provided.

        The board state can be initialized to any starting point, and is
        iteratively updated during the game so the MCTS algorithm can find the
        best action from the current board state.

        The current player is initialized to -1 (AI) as it is assumed the
        player (1) has already played, and it is now the AI's turn to play.

        Args:
            board (Board): The board to provide to the root node of the search
                tree
        """
        self.root_node = Node(board=board)
        self.cur_player = -1

    def _get_child_node_with_max_visits(self) -> "Node":
        """Returns the child node with the largest number of visits (n_i) from
        the current tree's root node

        Returns:
            Node: The child node with the largest number of visits (n_i).
        """
        return max(
            self.root_node.children,
            key=lambda child_node: child_node.n,
            default=None,
        )

    def find_best_move(self, iterations: int = 100) -> Tuple[int, int]:
        """Given a number of MCTS iterations to run, find the best possible
        move from the tree's current root node and return as the action to take

        Args:
            iterations (int, optional): The number of MCTS iterations. Defaults
                to 100.

        Returns:
            Tuple[int, int]: The (row, column) action to.
        """
        for _ in range(iterations):
            # Selection phase: select the most promising node
            max_uct_node = self._select()

            # Expansion phase: expand the most promising node
            self._expand(max_uct_node)

            # Simulation phase: simulate random playouts for each new child
            # from the most promising node
            for child_node in max_uct_node.children:
                self._simulate(child_node)

            # Backpropagation phase: backpropagate the results from the
            # children up the tree
            self._backpropagate(max_uct_node)

            # Stopping condition
            if max_uct_node.board.is_finished:
                break

            # Alternate between AI and opponent
            self.cur_player = -self.cur_player

        # The child node of the root node with the most visits has the best
        # action to take
        node_with_max_visits = self._get_child_node_with_max_visits()
        return node_with_max_visits.action

    def _select(self) -> "Node":
        """Performs the selection phase of the MCTS algorithm.

        This method traverses the search tree to find the child node with the
        largest UCT score.
        If multiple child nodes of a given node have the same UCT score, the
        first node is returned.

        Returns:
            Node: The node having the largest UCT score.
        """
        node = self.root_node
        while node is not None and node.children:
            for child_node in node.children:
                child_node.uct = utils.calculate_uct(child_node, node)
            node = max(
                node.children,
                key=lambda child_node: child_node.uct,
                default=None,
            )
        return node

    def _expand(self, node: "Node") -> None:
        """Performs the expansion phase of the MCTS algorithm.

        This method creates new child nodes for all possible actions you can
        take from given node, where each child node contains the new state of
        the board after each action was taken.

        Args:
            node (Node): The node to expand.
        """
        node_board = node.board
        for available_action in node_board.get_available_actions():
            (row, col) = available_action
            parent_board_state = copy.deepcopy(node_board.state)
            new_board = Board(state=parent_board_state)
            new_board.play_move(row, col, self.cur_player)
            new_child_node = Node(board=new_board, parent=node)
            new_child_node.action = available_action  #  type: ignore
            node.add_child(new_child_node)

    def _simulate(self, node: "Node") -> None:
        """Performs the simulation phase of the MCTS algorithm.

        This method performs a simulation ('rollout') of the given node's board
        until a terminal state is reached by alternating between player and AI
        moves. Moves are drawn uniformly at random.

        Once a terminal state is reached, the node's number of visits and
        accumulated values are updated accordingly (+1 for number of visits,
        +1/-1 depending on if the current player ending up winning/losing the
        result of the rollout respectively).

        Args:
            node (Node): The node to perform a rollout for.
        """
        cur_player = self.cur_player
        node_player = cur_player
        cur_board = copy.deepcopy(node.board)
        game_state = cur_board.game_state

        while True:
            # Alternate between players, taking random actions until a terminal
            # state is reached
            cur_player = -cur_player
            available_actions = cur_board.get_available_actions()
            if len(available_actions):
                random_action = random.choice(available_actions)
                (row, col) = random_action
                cur_board.play_move(row, col, cur_player)

            # Check if the game is in a terminal state (see the
            # Board.is_finished property)
            game_state = cur_board.game_state
            if cur_board.is_finished:
                break

        # Check for player win relative to the rolled out node (started with
        # player's move)
        if game_state == 1 and node_player == 1:
            node.w += 1
        # Check for player win relative to the rolled out node (started with
        # AI's move)
        elif game_state == 1 and node_player == -1:
            node.w -= 1
        # Check for AI win relative to the rolled out node (started with AI's
        # move)
        elif game_state == -1 and node_player == -1:
            node.w += 1
        # Check for AI win relative to the rolled out node (started with
        # player's move)
        elif game_state == -1 and node_player == 1:
            node.w -= 1

        # Increase number of rollouts for this node
        node.n += 1

    def _backpropagate(self, node: "Node") -> None:  # type: ignore[no-self-use]
        """Performs the backpropagation phase of the MCTS algorithm.

        This method iteratively updates the values of n_i and w_i up the tree
        from the given node until the root of the tree is reached.

        Args:
            node (Node): The node containing the values to backpropagate up the
                tree.
        """
        # Get the values of n_i and w_i to add up the tree
        n_to_add, w_to_add = 0, 0
        for child_node in node.children:
            n_to_add += child_node.n
            w_to_add += child_node.w

        parent_node = node.parent
        if parent_node is None:
            node.n += n_to_add
            node.w += w_to_add

        # For each parent node of this node, update the values of n_i and w_i
        # up to the root
        while parent_node is not None:
            parent_node.n += n_to_add
            parent_node.w += w_to_add
            parent_node = parent_node.parent


class Board:
    """Board class which represents a simple 3x3 Tic-Tac-Toe board"""

    def __init__(self, state: Optional[List[List[int]]] = None) -> None:
        """initialize a new Board object with empty state if no state is
        provided, otherwise initialize the Board with the provided state.

        The state is a list of lists of the following format (for a 3x3 board):
            [
                [0, 0, 0],
                [1, 0, 0],
                [0,-1, 0]
            ]
        where:
            1: Player (naughts)
            -1: AI (crosses)
            0: Empty space

        Args:
            state (Optional[List[List[int]]], optional): The state of the board
                to use. Defaults to an empty board state.
        """
        self.state = (
            state if state is not None else [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        )

    def play_move(self, row: int, col: int, player: int) -> None:
        """Updates the state of the board with the player's chosen row and
        column to play

        Args:
            row (int): The row index of the row to play (0-based).
            col (int): The column index of the column to play (0-based).
            player (int): The player value to place at the given row/column.
        """
        self.state[row][col] = player

    def get_available_actions(self) -> List[Tuple[int, int]]:
        """Returns the available actions to take from the board (i.e. the
        board's empty spaces)

        Returns:
            List[Tuple[row, col]]: A list of tuples, where each tuple consists
                of a row-column pair, representing a possible action to take.
        """
        return [
            (i, j)
            for i, row in enumerate(self.state)
            for j, col in enumerate(row)
            if col == 0
        ]

    @property
    def is_finished(self) -> bool:
        """Returns True if the state of this board has a winner or has ended in
            a tie

        Returns:
            bool: True if the board is in a finished state (i.e. the game has
                finished), False otherwise.
        """
        return self.game_state in [-1, 0, 1]

    @property
    def game_state(self) -> Optional[int]:
        """
        The game is complete when there are no empty spaces on the board.

        If the board has a complete row/column/diagonal where the values are:
             1 (player): player has won
                -1 (AI): AI has won

        Returns:
            Optional[int]: An optional integer:
                 0: game finished as a tie;
                 1: player has won;
                -1: AI has won
              None: game is still in progress
        """
        for i, row in enumerate(self.state):
            # Check if there is a complete row (return the player value)
            col_count = 0
            for col in row:
                if col != 0 and row[0] == col:
                    col_count += 1
            if col_count == len(row):
                return row[0]

            # Check if there is a complete column (return the player value)
            row_count = 0
            for j in range(len(row)):
                col = self.state[j][i]
                if col != 0 and row[0] == col:
                    row_count += 1
            if row_count == len(row):
                return row[0]

        # Check if there is a complete diagonal (return the player value)
        if (
            self.state[0][0] == self.state[1][1]
            and self.state[1][1] == self.state[2][2]
        ) or (
            self.state[0][2] == self.state[1][1]
            and self.state[1][1] == self.state[2][0]
        ):
            return self.state[1][1]

        # Check for a draw (i.e. all board spaces have been filled and we have
        # no winner)
        if all(col for row in self.state for col in row):
            return 0

        # Otherwise game is still in progress
        return None

    def print_board(self) -> None:
        """Prints the current state of the board.

        A player with a value of 1 is represented as a 'O' and a player with a
        value of -1 is represented as a 'X'.

        Currently, only a 3x3 board is supported.
        """
        print("\n")
        for i, row in enumerate(self.state):
            col_values = []
            for col in row:
                if col == 1:
                    col_values.append("O")
                elif col == -1:
                    col_values.append("X")
                elif col == 0:
                    col_values.append(" ")
            print("\t     |     |     ")
            row_str = f"\t  {'  |  '.join(col_values)}  "
            print(row_str)
            if i != 2:
                print("\t_____|_____|_____")
            else:
                print("\t     |     |     ")
        print("\n")


class Node:
    """Node class to represent the state of a Tic-Tac-Toe board for use in a
    tree"""

    def __init__(self, board: Board, parent: "Node" = None) -> None:
        """Initializes a new node with the state of a Tic-Tac-Toe board

        Args:
            board (Board): The board for this node.
            parent (Node, optional): The parent node of this new node. Defaults
                to None.
        """
        self.board = board
        self.parent = parent
        self.children: List["Node"] = []
        self.action = None
        self.uct = None
        self.w = 0
        self.n = 0

    def add_child(self, node: "Node") -> None:
        """Adds the provided node as a child to this node

        Args:
            node (Node): The node to add as a child.
        """
        self.children.append(node)
