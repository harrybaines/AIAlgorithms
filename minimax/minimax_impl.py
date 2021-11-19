# MiniMax algorithm implementation for perfect binary trees (i.e. 2 child nodes per node)
# This is a custom implementation from first principles
#
# Author: Harry Baines
# Date: 19/11/2021

from typing import Any, Optional


class Node:
    def __init__(self, left: "Node" = None, right: "Node" = None, value: Any = None):
        """Initialises a single Node, with or without a value, with left and right Nodes

        Args:
            left (Node, optional): Defines the left subtree for this new Node. Defaults to None.
            right (Node, optional): Defines the right subtree for this new Node. Defaults to None.
            value (Any, optional): Defines the value associated with this Node. Defaults to None.
        """
        self.left = left
        self.right = right
        self.value = value

    def fill_intermediate_nodes(self, depth: int = 0, maximizer: bool = True) -> Any:
        """Recursively completes intermediate Node values in the tree with minimum/maximum values
        from the subtrees according to whether or not the minimizing/maximizing player is choosing
        values respectively

        Args:
            depth (int, optional): The current depth of the tree during the recursion. Defaults to 0.
            maximizer (bool, optional): True if the maximizing player goes first from the root, False if
                the minimizing player goes first from the root. Defaults to True.

        Returns:
            Any: The value associated with the root Node. This value will correspond to the value in the
                child Node containing the same value, so we know which Node to choose from the start.
        """
        while self.left.value == None:
            self.left.fill_intermediate_nodes(depth=depth + 1, maximizer=not maximizer)
        while self.right.value == None:
            self.right.fill_intermediate_nodes(depth=depth + 1, maximizer=not maximizer)

        left_value = self.left.value
        right_value = self.right.value
        min_max_func = max if maximizer else min
        node_value = min_max_func(left_value, right_value)
        self.value = node_value
        return self.value

    def __repr__(self) -> str:
        """String representation of a Node

        Returns:
            str: String representation of a Node
        """
        left_value = self.left if not self.left else self.left.value
        right_value = self.right if not self.right else self.right.value
        return f"Node({self.value}, left={left_value}, right={right_value})"


class MiniMax:
    def __init__(self, root_node: Node) -> None:
        """Initializes a new MiniMax game

        Args:
            root_node (Node): The root Node element to start the game from.
        """
        self.root_node = root_node

    def play(self, maximizer: bool) -> Optional[Node]:
        """Play a MiniMax game with the provided root node (see self.root_node)

        Args:
            maximizer (bool): True if the maximizing player goes first, False if the minimizing player
                goes first.

        Returns:
            Optional[Node]: The optimal Node to choose from the root node. None if there was an error
                playing the game.
        """
        root_value = self.root_node.fill_intermediate_nodes(
            depth=0, maximizer=maximizer
        )
        if self.root_node.left.value == root_value:
            return self.root_node.left
        if self.root_node.right.value == root_value:
            return self.root_node.right
        return None


if __name__ == "__main__":
    # node_3 = Node(value=3)
    # node_5 = Node(value=5)
    # node_2 = Node(value=2)
    # node_9 = Node(value=9)

    left_subtree = Node(left=node_3, right=node_5)
    right_subtree = Node(left=node_2, right=node_9)
    root_node = Node(left=left_subtree, right=right_subtree)
    minimax = MiniMax(root_node=root_node)
    maximizer = False
    node_to_choose = minimax.play(maximizer=maximizer)
    print(
        f"Optimal node to choose for {'maximizing' if maximizer else 'minimising'} player: {node_to_choose} (optimal score = {node_to_choose.value})"
    )
