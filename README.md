# Tic-Tac-Toe AI using Monte Carlo Tree Search (MCTS)
## Quickstart

Create a new virtual environment:

```bash
pipenv shell
```

Install all dependencies (including dev dependencies):

```bash
pipenv install --dev
```

Create an `.env` file and populate it with the environment variables:

```bash
touch .env
echo FLASK_APP=flaskapp >> .env
echo FLASK_ENV=development >> .env
```

To check everything is working you can:


1. Run the flask app to play against the Tic-Tac-Toe AI in the browser using:

```bash
python -m flask run
```

2. Or run the Tic-Tac-Toe script and play in the shell:

```bash
cd flaskapp/mcts
python tictactoe.py
```

## Example Board States

Some example starting states for the `flaskapp.mcts.Board` class, where the next player is the human (used in the `Board` constructor in `flaskapp.mcts.tictactoe.TicTacToe.__init__`):

- `[[0, 0, 0], [0, 0, 0], [0, 0, 0]]`: empty board state
- `[[0, 0, 0], [0, -1, 0], [1, 0, -1]]`: tutorial diagram example
- `[[0, 0, 1], [1, 1, -1], [-1, -1, 0]]`: h plays 2, machine should play 9
- `[[0, 0, 0], [-1, 1, 1], [0, 0, -1]]`: h plays 3, machine should play 7
- `[[0, 0, 1], [1, 0, -1], [-1, 1, 0]]`: h plays 2, machine should play 5
- `[[-1, -1, 1], [1, 1, -1], [0, 1, 0]]`: endgame example, h plays 3, machine should play 7
- `[[-1, 1, -1], [1, 1, -1], [0, 0, 0]]`: endgame example, h plays 9, machine should play 8

