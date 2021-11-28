import copy
import random
from typing import List, Optional, Tuple

import utils


class MonteCarloTreeSearch:
    """Monte Carlo Tree Search class"""

    def find_best_move(
        self, board: "Board", iterations: int = 100
    ) -> Tuple[int, int]:
        """Given a number of MCTS iterations to run, find the best possible
        move from the tree's current root node and return as the action to
        take.

        A new root node is constructed and initialized with the board state
        provided. The board state can be initialized to any starting point, and
        is iteratively updated during the game so the MCTS algorithm can find
        the best action from the current board state.

        The current player is initialized to -1 (AI) as it is assumed the
        player (1) has already played, and it is now the AI's turn to play.

        Args:
            board (Board): The board to provide to the root node of the search
                tree.
            iterations (int, optional): The number of MCTS iterations. Defaults
                to 100.

        Returns:
            Tuple[int, int]: The (row, column) action to.
        """
        self.root_node = Node(board=board, player=1)

        # Start by expanding the root node
        self._expand(self.root_node)

        for _ in range(iterations):
            # Selection phase: select the most promising leaf node
            selected_node = self._select()

            # Expansion phase: expand the most promising node which has already
            # been visited
            if selected_node.visited:
                # If the selected node has already been visited, expand the
                # node with all possible actions from the current state, and
                # perform a rollout from the first new child node
                # If the selected node is a terminal state, we simply return
                # the value of that state and backpropagate it up the tree
                # NOTE: can be a random selection
                self._expand(selected_node)
                selected_node = (
                    selected_node.children[0]
                    if selected_node.children
                    else selected_node
                )

            # Simulation phase: perform rollouts for leaf nodes which haven't
            # been visited yet
            # Backpropagation phase: backpropagate the results from the rollout
            # up the tree
            self._rollout(selected_node)
            self._backpropagate(selected_node)

        # Get the best action
        node_to_choose = self._get_child_node_with_max_score()
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
        while node is not None and node.children:
            for child_node in node.children:
                child_node.uct = utils.calculate_uct(child_node, node)
            node = max(node.children, key=lambda child_node: child_node.uct)
        return node

    def _expand(self, node: "Node") -> None:
        """Performs the expansion phase of the MCTS algorithm.

        This method creates new child nodes for all possible actions you can
        take from given node, where each child node contains the new state of
        the board after each action was taken.

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

        # Check for player win where the most recent move was taken by the player
        game_state = cur_board.game_state
        if game_state == 1 and cur_player == 1:
            node.w = 1
        # Check for player loss where the most recent move was taken by the AI
        elif game_state == 1 and cur_player == -1:
            node.w = -1
        # Check for AI win where the most recent move was taken by the AI
        elif game_state == -1 and cur_player == -1:
            node.w = 1
        # Check for AI loss where the most recent move was taken by the player
        elif game_state == -1 and cur_player == 1:
            node.w = -1

        # Increase number of visits this node
        node.n += 1

    def _backpropagate(self, node: "Node") -> None:  # type: ignore[no-self-use]
        """Performs the backpropagation phase of the MCTS algorithm.

        This method iteratively updates the values of n_i and w_i up the tree
        from the given node until the root of the tree is reached.

        Args:
            node (Node): The node containing the child nodes to backpropagate
                their values up the tree.
        """
        # For each parent node of this node, update the values of n_i and w_i
        # up to the root
        parent_node = node.parent
        while parent_node is not None:
            parent_node.n += 1
            # Each parent up the tree has an incremented/decremented value
            # because this indicates whether the player at this current node
            # won or lost as a result of their actions
            # (i.e. if the result was a win for the current node, then the parent
            # node records a loss, and vice versa)
            parent_node.w = (
                parent_node.w + 1
                if node.player == parent_node.player
                else parent_node.w - 1
            )
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
        board's empty spaces).

        The method scans available actions by going across the columns then
        down the rows in a clockwise fashion.

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

        # NOTE: refactor
        # Check if there is a complete diagonal (return the player value)
        equal_diags = 0
        for row_idx, row in enumerate(self.state):
            cell_value = row[row_idx]
            if cell_value == 0:
                break
            if row_idx == 0:
                equal_diags += 1
                continue
            prev_cell_value = self.state[row_idx - 1][row_idx - 1]
            if cell_value != prev_cell_value:
                break
            equal_diags += 1

        if equal_diags == len(row):
            return cell_value

        equal_diags = 0
        for row_idx, row in enumerate(self.state):
            cell_value = row[len(row) - 1 - row_idx]
            if cell_value == 0:
                break
            if row_idx == 0:
                equal_diags += 1
                continue
            prev_cell_value = self.state[row_idx - 1][len(row) - row_idx]
            if cell_value != prev_cell_value:
                break
            equal_diags += 1

        if equal_diags == len(row):
            return cell_value

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

    def __init__(
        self, board: Board, player: int, parent: "Node" = None
    ) -> None:
        """Initializes a new node with the state of a Tic-Tac-Toe board

        Args:
            board (Board): The board for this node.
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

    def add_child(self, node: "Node") -> None:
        """Adds the provided node as a child to this node

        Args:
            node (Node): The node to add as a child.
        """
        self.children.append(node)
