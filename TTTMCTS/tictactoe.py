import random
import math
import copy

random.seed(42)


class Board:
    def __init__(self, state=None) -> None:
        """Initialise a new Board object with empty state if no state is provided,
        otherwise initialise the Board with the provided state

         1: Player (naughts)
        -1: AI (crosses)
         0: Empty space

        Args:
            state ([type], optional): [description]. Defaults to None.
        """
        self.state = state if state else [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    def play_move(self, row, col, player):
        self.state[row][col] = player

    @property
    def available_actions(self):
        return [
            (i, j)
            for i, row in enumerate(self.state)
            for j, col in enumerate(row)
            if col == 0
        ]

    @property
    def is_finished(self):
        return self.game_state in [-1, 0, 1]

    @property
    def game_state(self):
        """
        The game is complete when there are no empty spaces on the board

        If the board has a complete row/column/diagonal where the values are:
             1 (player): player has won
            -1 (AI): AI has won

        If the board is full with no winner, 0 is returned as the game finished as a draw.
        If the board still has empty spaces wth no winner, None is returned as the game is still in progress.
        """
        # for i, row in enumerate(self.state):

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

        # Check for a draw (i.e. all board spaces have been filled and we have no winner)
        if all(col for row in self.state for col in row):
            return 0

        # Otherwise game is still in progress
        return None

    def print_board(self):
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


class Tree:
    def __init__(self, board) -> None:
        # Add test board to tests:
        #   [[1, 0, 0], [0, -1, 0], [1, 0, -1]]
        self.root = Node(board=board)


class Node:
    def __init__(self, board, parent=None) -> None:
        self.board = board
        self.parent = parent
        self.children = []
        self.w = 0
        self.n = 0

    def add_child(self, node):
        self.children.append(node)


class MonteCarloTreeSearch:
    def __init__(self, board) -> None:
        self.tree = Tree(board=board)
        self.cur_player = -1

    def _get_leaf_node_with_max_ucb(self):
        # By default returns the first child with the highest UCB if there are equal UCB's
        node = self.tree.root
        while node is not None and len(node.children):
            for child_node in node.children:
                child_node.ucb = self._calculate_ucb(child_node, node)
            node = max(
                node.children, key=lambda child_node: child_node.ucb, default=None
            )
        return node

    def _get_child_node_with_max_visits(self):
        node = self.tree.root
        return max(node.children, key=lambda child_node: child_node.n, default=None)

    def _calculate_ucb(self, child_node, parent_node, c=2):
        """
        UCB = (w_i / n_i) + c * sqrt(ln(n_p) / n_i)
        """
        return (child_node.w / child_node.n) + c * (
            (math.log(parent_node.n) / child_node.n) ** 0.5
        )

    def find_best_move(self, iterations=100):
        # NOTE: Add tqdm

        for i in range(iterations):
            # Select most promising node
            max_ucb_node = self.select()

            # Expand the node
            self.expand(max_ucb_node)

            # Simulate a random playout
            for child_node in max_ucb_node.children:
                self.simulate(child_node)

            # Backpropagate the result up the tree
            self.backpropagate(max_ucb_node)

            # Stopping condition
            if max_ucb_node.board.is_finished:
                break

            # Alternate between AI and opponent
            self.cur_player = -self.cur_player

        node_with_max_visits = self._get_child_node_with_max_visits()
        return (*node_with_max_visits.action, node_with_max_visits)

    def select(self):
        return self._get_leaf_node_with_max_ucb()

    def expand(self, node):
        max_ucb_node_board = node.board
        for available_action in max_ucb_node_board.available_actions:
            (row, col) = available_action
            parent_board_state = copy.deepcopy(max_ucb_node_board.state)
            new_board = Board(state=parent_board_state)
            new_board.play_move(row, col, self.cur_player)
            new_child_node = Node(board=new_board, parent=node)
            new_child_node.action = (row, col)
            node.add_child(new_child_node)

    def simulate(self, node):
        """Perform a random rollout by drawing moves uniformly at random"""
        cur_player = self.cur_player
        cur_board = copy.deepcopy(node.board)
        game_state = cur_board.game_state

        while True:
            cur_player = -cur_player
            available_actions = cur_board.available_actions
            random_action = random.choice(available_actions)
            (row, col) = random_action
            cur_board.play_move(row, col, cur_player)

            # Check game state (see Board.game_state property)
            # game_state = cur_board.game_state
            if cur_board.is_finished:
                break

        # Check for player win
        if game_state == 1:
            node.w += 1
        # Check for AI win
        elif game_state == -1:
            node.w -= 1

        # Increase number of rollouts for this node
        node.n += 1

    def backpropagate(self, node):
        n_to_add = 0
        w_to_add = 0
        for child_node in node.children:
            n_to_add += child_node.n
            w_to_add += child_node.w

        node.n += n_to_add
        node.w += w_to_add

        parent_node = node.parent
        if parent_node is None:
            node.n += n_to_add
            node.w += w_to_add

        while parent_node != None:
            parent_node.n += n_to_add
            parent_node.w += w_to_add
            parent_node = parent_node.parent


class TicTacToe:
    def play(self):
        board = Board()
        self.mcts = MonteCarloTreeSearch(board=board)
        while True:
            player_position = -1
            while True:
                player_position = int(input("Enter a position (1-9) to play > "))
                row = (player_position - 1) // 3
                col = (player_position - 1) % 3
                if board.state[row][col] == 0:
                    break
                print("Not a legal move. Please try again.")

            print("Players move:")
            board.play_move(row, col, 1)
            board.print_board()

            (row, col, best_move_node) = self.mcts.find_best_move(iterations=100)
            board.play_move(row, col, -1)

            if board.is_finished:
                break

            self.mcts.tree.root = best_move_node
            self.mcts.tree.root.board = board  #  fix!

            print("TTTAI's move:")
            board.print_board()


if __name__ == "__main__":
    tic_tac_toe = TicTacToe()
    tic_tac_toe.play()
