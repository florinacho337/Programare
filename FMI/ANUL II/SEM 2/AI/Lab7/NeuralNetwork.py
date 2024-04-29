import numpy as np
from numpy import mean


def sigmoid_derivative(x):
    return x * (1 - x)


class NeuralNetwork:
    def __init__(self, hidden_layer_size=12, max_iter=7000, learning_rate=.001):
        self.__weights = []
        self.loss = []
        self.__hidden_layer_size = hidden_layer_size
        self.__max_iter = max_iter
        self.__learning_rate = learning_rate

    @staticmethod
    def __softmax(x):
        exp_vector = np.exp(x - np.max(x, axis=1, keepdims=True))
        return exp_vector / exp_vector.sum(axis=1, keepdims=True)

    @staticmethod
    def __sigmoid(x):
        return 1 / (1 + np.exp(-x))

    def __forward(self, x):
        weight_ih, coefficient_ih, weight_ho, coefficient_ho = self.__weights
        self.__hidden_activation = self.__sigmoid(np.dot(x, weight_ih) + coefficient_ih)
        output_activation = self.__softmax(np.dot(self.__hidden_activation, weight_ho) + coefficient_ho)
        return output_activation

    def __backward(self, x, y, y_output_softmax):
        weights_input_hidden, coefficient_input_hidden, weights_hidden_output, coefficient_hidden_output = self.__weights
        error = y_output_softmax - y

        weights_hidden_output -= self.__learning_rate * np.dot(self.__hidden_activation.T, error)
        coefficient_hidden_output -= self.__learning_rate * error.sum(axis=0)

        hidden_error = np.dot(error, weights_hidden_output.T)
        hidden_delta = hidden_error * sigmoid_derivative(self.__hidden_activation)

        error_weight_ih = np.dot(x.T, hidden_delta)
        self.loss.append(mean(error_weight_ih))

        weights_input_hidden -= self.__learning_rate * error_weight_ih
        coefficient_input_hidden -= self.__learning_rate * hidden_delta.sum(axis=0)

        self.__weights = [weights_input_hidden, coefficient_input_hidden, weights_hidden_output,
                          coefficient_hidden_output]

    def fit(self, x, y):
        no_features = len(x[0])
        no_outputs = len(set(y))
        new_y = np.zeros((len(y), no_outputs))
        for i in range(len(y)):
            new_y[i, y[i]] = 1
        y = new_y
        weights_hidden_input = np.random.rand(no_features, self.__hidden_layer_size)  # input X hidden
        coefficient_hidden_input = np.random.randn(self.__hidden_layer_size)
        weights_hidden_output = np.random.rand(self.__hidden_layer_size, no_outputs)  # hidden  X output
        coefficient_hidden_output = np.random.randn(no_outputs)
        self.__weights = [weights_hidden_input, coefficient_hidden_input, weights_hidden_output,
                          coefficient_hidden_output]
        for epoch in range(self.__max_iter):
            y_output_softmax = self.__forward(x)  # forward propagation
            self.__backward(x, y, y_output_softmax)  # backward propagation

    def predict(self, x):
        return np.argmax(self.__forward(x), axis=1)
