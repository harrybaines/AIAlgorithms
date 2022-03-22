import numpy as np

import activations


class NeuralNetworkLayer:
    def __init__(self, n_neurons, n_neurons_prev, activation):
        self.n_neurons = n_neurons
        self.activation = "relu"

        if activation == "sigmoid":
            self.activation_fn = activations.sigmoid
        elif activation == "relu":
            self.activation_fn = activations.relu

        # If we are dealing with the input layer, we have no previous neurons
        n_neurons_prev = 1 if n_neurons_prev == -1 else n_neurons_prev

        # Initialise parameters
        self.W = np.random.rand(n_neurons, n_neurons_prev) * 0.01
        self.b = np.random.rand(n_neurons, 1) * 0.01

    def initialize_parameters(self):
        # TODO: initialize to small random numbers
        pass

    def __repr__(self):
        return f"Neural Network Layer (n_neurons={self.n_neurons}, activation={self.activation})"


class NeuralNetwork:
    def __init__(
        self, n_inputs, n_outputs, activation, hidden_layers, seed
    ) -> None:
        self.n_hidden_layers = len(hidden_layers)

        input_layer = NeuralNetworkLayer(
            n_neurons=n_inputs, n_neurons_prev=-1, activation=activation
        )
        self.layers = [input_layer]

        if seed:
            np.random.seed(seed)

        if self.n_hidden_layers:
            _, activation = hidden_layers[0]
            for i, (n_neurons, activation) in enumerate(hidden_layers):
                n_neurons_prev = self.layers[i].n_neurons
                hidden_layer = NeuralNetworkLayer(
                    n_neurons=n_neurons,
                    n_neurons_prev=n_neurons_prev,
                    activation=activation,
                )
                self.layers.append(hidden_layer)

        output_layer = NeuralNetworkLayer(
            n_neurons=n_outputs,
            n_neurons_prev=self.layers[-1].n_neurons,
            activation=activation,
        )
        self.layers += [output_layer]

    def forward(self, X, y):
        # Initialise activations of input layer to be equal to the input data (i.e. a[0])
        self.layers[0].A = X.copy()

        for layer_i in range(1, len(self.layers)):
            cur_layer = self.layers[layer_i]
            prev_layer = self.layers[layer_i - 1]

            # Compute activations
            Z_i = cur_layer.W.dot(prev_layer.A) + cur_layer.b
            cur_layer.A = cur_layer.activation_fn(Z_i)

    def backward(self):
        # dZ = A - Y
        pass

    def loss(self):
        # TODO: compute the loss
        pass

    def train(self, X, y):
        self.forward(X, y)
        self.backward()
        return X

    def predict(self, y):
        return y

    def __str__(self):
        return "\n  |\n".join([repr(layer) for layer in self.layers])


if __name__ == "__main__":
    # (n_x, m)
    X = np.array([[10, 12, 20], [11, 13, 22], [9, 12, 19]])
    y = np.array([1, 1, 0])

    n_inputs = X.shape[1]
    n_outputs = 1
    activation = "relu"

    hidden_layers = [
        (4, "relu")
    ]  # ordered list, where the i'th element represents the number of (input) neurons in the i'th hidden layer

    nn = NeuralNetwork(
        n_inputs=n_inputs,
        n_outputs=n_outputs,
        activation=activation,
        hidden_layers=hidden_layers,
        seed=42,
    )
    print(nn)
    nn.forward(X=X, y=y)
    preds = nn.predict(y=[5, 6])
    print(preds)
