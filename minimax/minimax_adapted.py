# Adapted code from minimax/minimax_solution.py
# Reference: https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-1-introduction/
#
# Author: Harry Baines
# Date: 19/11/2021
import math


def minimax(
    cur_depth: int,
    node_index: int,
    max_turn: bool,
    scores: list[int],
    target_depth: int,
) -> int:
    """Recursive minimax function

    Args:
        cur_depth (int): The current depth of the tree during the recursion.
        node_index (int): The current index of the node in the scores list.
        max_turn (bool): True if it is currently the maxmimizing players turn, False if it is currently the minimizing
          players turn.
        scores (list[int]): An list of scores, with each score representing the value in each leaf node.
        target_depth (int): The target depth of the tree to visit.

    Returns:
        int: The optimal value the player can expect to achieve assuming the opponent plays optimally.
    """
    if cur_depth == target_depth:
        return scores[node_index]

    if max_turn:
        return max(
            minimax(
                cur_depth + 1, node_index * 2, False, scores, target_depth
            ),
            minimax(
                cur_depth + 1, node_index * 2 + 1, False, scores, target_depth
            ),
        )
    else:
        return min(
            minimax(cur_depth + 1, node_index * 2, True, scores, target_depth),
            minimax(
                cur_depth + 1, node_index * 2 + 1, True, scores, target_depth
            ),
        )


if __name__ == "__main__":
    #                 o
    #        o        o        o
    #    o       o        o        o
    #  3   5   2   9   12   5   23   23
    scores = [3, 5, 2, 9, 12, 5, 23, 23]
    assert len(scores) % 2 == 0
    tree_depth = math.log(len(scores), 2)
    optimal_value = minimax(0, 0, False, scores, tree_depth)
    print(f"The optimal value is: {optimal_value}")
