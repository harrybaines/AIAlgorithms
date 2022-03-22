import numpy as np
import pytest

from activations import sigmoid
from main import NeuralNetwork

SEED = 42


@pytest.fixture
def nn():
    # (n_x, m)
    X = np.array([[10, 12, 20], [11, 13, 22], [9, 12, 19]])
    y = np.array([1, 1, 0])

    n_inputs = X.shape[1]
    n_outputs = 1
    activation = "sigmoid"

    hidden_layers = [
        (4, "relu")
    ]  # ordered list, where the i'th element represents the number of (input) neurons in the i'th hidden layer

    return NeuralNetwork(
        n_inputs=n_inputs,
        n_outputs=n_outputs,
        activation=activation,
        hidden_layers=hidden_layers,
        seed=SEED,
    )


# def test_nn_forward(nn):
# pass


def test_sigmoid():
    assert sigmoid(-1000) == 0
    assert sigmoid(0) == 0.5
    assert sigmoid(1000) == 1
