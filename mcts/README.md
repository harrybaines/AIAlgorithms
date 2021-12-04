# Monte Carlo Tree Search

## Get Started

Follow the instructions in the [`README.md`](https://github.com/harrybaines/AIAlgorithms) from the root of this repository.

Then run:

```
python tictactoe.py
```

## Example Board States

Some example starting states for the `mcts.Board` class, where the next player is the human (used in the `Board` constructor in `tictactoe.TicTacToe.__init__`):

- `[[0, 0, 0], [0, 0, 0], [0, 0, 0]]`: empty board state
- `[[0, 0, 0], [0, -1, 0], [1, 0, -1]]`: tutorial diagram example
- `[[0, 0, 1], [1, 1, -1], [-1, -1, 0]]`: h plays 2, machine should play 9
- `[[0, 0, 0], [-1, 1, 1], [0, 0, -1]]`: h plays 3, machine should play 7
- `[[0, 0, 1], [1, 0, -1], [-1, 1, 0]]`: h plays 2, machine should play 5
- `[[-1, -1, 1], [1, 1, -1], [0, 1, 0]]`: endgame example, h plays 3, machine should play 7
- `[[-1, 1, -1], [1, 1, -1], [0, 0, 0]]`: endgame example, h plays 9, machine should play 8
