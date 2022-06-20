import math

from flaskapp.mcts.mcts import Node


def calculate_uct(
    child_node: "Node", parent_node: "Node", c: int = 2
) -> float:
    """Calculates the UCT (upper confidence tree) score for the given
    child_node using the following equation:

        UCT_i = (w_i / n_i) + c * sqrt(ln(n_p) / n_i)

    where:
        w_i: is the accumulated value of the i'th child;
        n_i: is the visit count for the i'th child;
        c: is a hyperparameter to control the exploration/exploitation
            tradeoff;
        n_p: is the visit count for the parent of the i'th child;

    Args:
        child_node (Node): The child node to calculate the UCT value for.
        parent_node (Node): The parent node of the child node.
        c (int): Hyperparameter to control the exploration/exploitation
            tradeoff in the equation.

    Returns:
        float: infinity if the child has never been visited, otherwise the UCT
            score
    """
    if child_node.n == 0:
        return float("inf")
    return (child_node.w / child_node.n) + c * (
        (math.log(parent_node.n) / child_node.n) ** 0.5
    )
