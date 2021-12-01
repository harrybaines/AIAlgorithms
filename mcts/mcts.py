import copy
import random
from typing import List, Optional, Tuple

from tqdm import tqdm

import utils


class MonteCarloTreeSearch:
    """Monte Carlo Tree Search class"""

    def find_best_move(
        self, board: "Board", iterations: int = 1_000
    ) -> Tuple[int, int]:
        """Given a number of MCTS iterations to run, find the best possible
        move from the tree's current root node and return the action to take.

        A new root node is constructed and initialized with the board state
        provided. The board state can be initialized to any starting point, and
        is iteratively updated during the game so the MCTS algorithm can find
        the best action from the current board state.

        The current player is initialized to 1 (human player) as it is assumed
        the AI (-1) has already played, but this can be configured.

        Args:
            board (Board): The board to provide to the root node of the search
                tree.
            iterations (int, optional): The number of MCTS iterations. Defaults
                to 1_000.

        Returns:
            Tuple[int, int]: The (row, column) action to take.
        """
        self.root_node = Node(board=board, player=1)

        # Start by expanding the root node
        self._expand(self.root_node)

        for _ in tqdm(range(iterations)):
            # Selection phase: select the most promising leaf node
            selected_node = self._select()

            # Expansion phase: expand the most promising node which has already
            # been visited and is not a terminal state
            if selected_node.visited and not selected_node.is_terminal:
                # Expand the node with all possible actions from the current
                # state, and perform a rollout from the first new child node
                # (this could be changed to a random selection)
                self._expand(selected_node)
                selected_node = (
                    selected_node.children[0]
                    if selected_node.children
                    else selected_node
                )

            # Simulation phase: perform rollouts for leaf nodes which haven't
            # been visited yet or for terminal states
            # Backpropagation phase: backpropagate the results from the rollout
            # up the tree
            result = self._rollout(selected_node)
            self._backpropagate(selected_node, result)

        # Get the node with the largest number of visits and the action
        node_to_choose = self._get_child_node_with_max_visits()
        return node_to_choose.action

    def _select(self) -> "Node":
        """Performs the selection phase of the MCTS algorithm.

        This method traverses the search tree to find the child node with the
        largest UCT score.
        If multiple child nodes of a given node have the same UCT score, the
        first node is returned.
        If a node has no children (i.e. it hasn't been expanded yet) then
        return this node ready for expansion.

        Returns:
            Node: The node having the largest UCT score.
        """
        node = self.root_node
        while node.children:
            for child_node in node.children:
                child_node.uct = utils.calculate_uct(child_node, node)
            node = max(node.children, key=lambda child_node: child_node.uct)
        return node

    def _expand(self, node: "Node") -> None:
        """Performs the expansion phase of the MCTS algorithm.

        This method creates new child nodes for all possible actions you can
        take from the given node, where each child node contains the new state
        of the board after each action was taken.

        Args:
            node (Node): The node to expand.
        """
        next_player = -node.player
        for available_action in node.board.get_available_actions():
            (row, col) = available_action
            parent_board_state = copy.deepcopy(node.board.state)
            new_board = Board(state=parent_board_state)
            new_board.play_move(row, col, next_player)
            new_child_node = Node(
                board=new_board, parent=node, player=next_player
            )
            new_child_node.action = available_action
            node.add_child(new_child_node)

    def _rollout(self, node: "Node") -> None:
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
        # If the node is a terminal state, we simply return the value of that
        # state and backpropagate it up the tree
        game_state = node.board.game_state
        if node.is_terminal:
            if game_state == 0:
                return 0
            elif node.player == game_state:
                return 1
            else:
                return -1

        cur_board = copy.deepcopy(node.board)
        cur_player = node.player

        while True:
            cur_player = -cur_player

            # Check if the game is in a terminal state (see the
            # Board.is_complete property)
            if cur_board.is_complete:
                break

            # Alternate between players, taking random actions until a terminal
            # state is reached
            available_actions = cur_board.get_available_actions()
            (row, col) = random.choice(available_actions)
            cur_board.play_move(row, col, cur_player)

        return cur_board.game_state

    def _backpropagate(self, node: "Node", result: int) -> None:  # type: ignore[no-self-use]
        """Performs the backpropagation phase of the MCTS algorithm.

        This method iteratively updates the values of n_i and w_i up the tree
        from the given node until the root of the tree is reached.

        Args:
            node (Node): The node containing the child nodes to backpropagate
                their values up the tree.
            result (int): The result of the game from the rollout phase (i.e.
                the game state).
        """
        # Update w_i and n_i for this node based on the result of the game
        node_player = node.player
        node.n += 1

        if node.is_terminal:
            node.w += 1
        else:
            if node.player == result:
                node.w += 1
            elif result != 0:
                node.w -= 1

        # For each parent node of this node, update the values of n_i and w_i
        # up to the root
        parent_node = node.parent
        sign = -1
        while parent_node is not None:
            parent_node.n += 1
            # Each parent up the tree has an incremented/decremented value
            # because this indicates whether the player at this current node
            # won or lost as a result of their actions
            # (i.e. if the result was a win for the current node, then the parent
            # node records a loss, and vice versa)
            if result != 0:
                if node.is_terminal or node.player == result:
                    parent_node.w = parent_node.w + (1 * sign)
                    sign = -sign
                else:
                    sign = -sign
                    parent_node.w = parent_node.w + (1 * sign)

            parent_node = parent_node.parent

    def _get_child_node_with_max_visits(self) -> "Node":
        """Returns the child node with the largest number of visits (n_i) from
        the current tree's root node

        Returns:
            Node: The child node with the largest number of visits (n_i).
        """
        return max(
            self.root_node.children, key=lambda child_node: child_node.n
        )

    def _get_child_node_with_max_score(self) -> "Node":
        """Returns the child node with the largest score (w_i) from the current
        tree's root node

        Returns:
            Node: The child node with the largest score (w_i).
        """
        return max(
            self.root_node.children, key=lambda child_node: child_node.w
        )


class Board:
    """Board class which represents a simple 3x3 Tic-Tac-Toe board"""

    DEFAULT_BOARD_SIZE: int = 3

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
            state if state is not None else self.get_empty_board_state()
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
        board's empty spaces).

        The method scans available actions by going across the columns then
        down the rows in a clockwise fashion.

        Returns:
            List[Tuple[int, int]]: A list of tuples, where each tuple consists
                of a row-column pair, representing a possible action to take.
        """
        return [
            (i, j)
            for i, row in enumerate(self.state)
            for j, col in enumerate(row)
            if col == 0
        ]

    @property
    def size(self) -> int:
        """Returns the size of the board

        The board should be symmetrical in size (i.e. the number of rows should
        always equal the number of columns so correct diagonals can be
        detected)

        Returns:
            int: The size of the board as an integer (i.e. rows/columns).
        """
        return len(self.state[0])

    @property
    def is_empty(self) -> bool:
        """Returns True if the current board is empty

        Returns:
            bool: True if the current board is empty, False otherwise.
        """
        return all(col == 0 for row in self.state for col in row)

    @property
    def is_complete(self) -> bool:
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
                -1: AI has won;
              None: game is still in progress
        """
        # Check if there is a complete row (return the player value)
        for row in self.state:
            if abs(sum(row)) == len(row):
                return row[0]

        # Check if there is a complete column (return the player value)
        n_cols = len(self.state[0])
        for col_idx in range(n_cols):
            column = [
                self.state[row_idx][col_idx] for row_idx in range(n_cols)
            ]
            if abs(sum(column)) == n_cols:
                return column[0]

        # Check if there is a complete diagonal (return the player value)
        # Detect downward diagonal from the top left
        first_row_len = len(self.state[0])
        downward_diagonal = [
            self.state[idx][idx] for idx in range(first_row_len)
        ]
        if 0 not in downward_diagonal and all(
            x == downward_diagonal[0] for x in downward_diagonal
        ):
            return downward_diagonal[0]

        # Detect upward diagonal from the bottom left
        upward_diagonal = [
            self.state[first_row_len - 1 - idx][idx]
            for idx in range(first_row_len)
        ]
        if 0 not in upward_diagonal and all(
            x == upward_diagonal[0] for x in upward_diagonal
        ):
            return upward_diagonal[0]

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
        board_size = self.size
        print("\n")
        for i, row in enumerate(self.state):
            col_values = []
            for j, col in enumerate(row):
                cell_no = (i * board_size) + (j + 1)
                pad = " "
                if col == 1:
                    col_values.append(f"\033[92m{pad}o\033[0;0m")
                elif col == -1:
                    col_values.append(f"\033[91m{pad}x\033[0;0m")
                elif col == 0:
                    pad = "" if cell_no >= 10 else " "
                    col_values.append(f"\033[90m{pad}{cell_no}\033[0;0m")
            row_str = f"\t  {' | '.join(col_values)} "
            print(row_str)
            if i != board_size - 1:
                print("\t", "-" * (board_size * 5 - 1))
        print("\n")

    def get_empty_board_state(self) -> List[List[int]]:
        """Returns an empty board state to use from the beginning of a tic tac
        toe game

        Returns:
            List[List[int]]: A list of lists of 0's representing empty board
                positions.
        """
        return [
            [0 for _ in range(self.DEFAULT_BOARD_SIZE)]
            for _ in range(self.DEFAULT_BOARD_SIZE)
        ]


class Node:
    """Node class to represent the state of a Tic-Tac-Toe board for use in a
    tree"""

    def __init__(
        self, board: Board, player: int, parent: "Node" = None
    ) -> None:
        """Initializes a new node with the state of a Tic-Tac-Toe board

        Args:
            board (Board): The board for this node.
            player (int): The value of the player which will perform an action
                on the board associated with this node (i.e. 1 if the human
                performs the action, -1 if the AI performs the action).
            parent (Node, optional): The parent node of this new node. Defaults
                to None.
        """
        self.board = board
        self.parent = parent
        self.player = player
        self.children: List["Node"] = []
        self.action = None
        self.uct = None
        self.w = 0
        self.n = 0

    @property
    def visited(self) -> bool:
        """Returns True if this node has already been visited

        Returns:
            bool: True if this node has already been visited, False otherwise.
        """
        return self.n > 0

    @property
    def is_terminal(self) -> bool:
        """Returns True if this node represents a terminal state

        Returns:
            bool: True if this node is a terminal state, False otherwise.
        """
        return self.board.is_complete

    def add_child(self, node: "Node") -> None:
        """Adds the provided node as a child to this node

        Args:
            node (Node): The node to add as a child.
        """
        self.children.append(node)
