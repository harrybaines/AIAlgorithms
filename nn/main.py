import numpy as np

class Neuron:
    def __init__(self, n_inputs, activation_fn) -> None:
        self.n_inputs = n_inputs
        self.activation_fn = activation_fn
        self.w = 0
        self.b = 0

class NeuralNetworkLayer:
    def __init__(self, n_neurons, n_neurons_prev, activation_fn):
        self.n_neurons = n_neurons
        self.activation_fn = activation_fn
        
        # If we are dealing with the input layer, we have no previous neurons
        n_neurons_prev = 1 if n_neurons_prev == -1 else n_neurons_prev

        self.neurons = [
            Neuron(n_inputs=n_neurons, activation_fn=activation_fn)
            for _ in range(n_neurons)
        ]

    def __repr__(self):
        return f'Neural Network Layer (n_neurons={self.n_neurons}, activation_fn={self.activation_fn})'


class NeuralNetwork:
    def __init__(self, n_inputs, n_outputs, activation_fn, hidden_layers) -> None:
        self.n_hidden_layers = len(hidden_layers)

        input_layer = NeuralNetworkLayer(n_neurons=n_inputs, n_neurons_prev=-1, activation_fn=activation_fn)
        self.layers = [input_layer]

        if self.n_hidden_layers:
            _, activation_fn = hidden_layers[0]
            for i, (n_neurons, activation_fn) in enumerate(hidden_layers):
                n_neurons_prev = self.layers[i]
                hidden_layer = NeuralNetworkLayer(n_neurons=n_neurons, n_neurons_prev=n_neurons_prev, activation_fn=activation_fn)
                self.layers.append(hidden_layer)
        
        output_layer = NeuralNetworkLayer(
            n_neurons=n_outputs, 
            n_neurons_prev=self.layers[-1].n_neurons,
            activation_fn=activation_fn
        )
        self.layers += [output_layer]

    def train(self, X):
        # a_i = W_i.T.a_i-1 + b_i (in vector form)
        return X

    def predict(self, y):
        return y

    def __str__(self):
        return '\n  |\n'.join([repr(layer) for layer in self.layers])

if __name__ == "__main__":
    X = np.array([0, 1, 2, 3, 4])
    y = np.array([5, 7, 9, 11, 12])

    n_inputs = 1
    n_outputs = 1
    activation_fn = "sigmoid"

    hidden_layers = [(4, "sigmoid")] # ordered list, where the i'th element represents the number of (input) neurons in the i'th hidden layer

    nn = NeuralNetwork(
        n_inputs=n_inputs, 
        n_outputs=n_outputs, 
        activation_fn=activation_fn, 
        hidden_layers=hidden_layers
    )
    print(nn)
    nn.train(X=X)
    preds = nn.predict(y=[5, 6])
    print(preds)
