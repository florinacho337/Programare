import random
from statistics import mean


class BGDRegression:
    def __init__(self):
        self.intercept_ = 0.0
        self.coefficient_ = []

    def fit(self, x, y, learning_rate=0.001, no_epochs=1000):
        self.coefficient_ = [random.random() for _ in range(len(x[0]) + 1)]
        for _ in range(no_epochs):
            errors = []
            for i in range(len(x)):
                y_computed = self.eval(x[i])
                errors.append(y_computed - y[i])
            error = mean(errors)
            for i in range(len(x)):
                for j in range(0, len(x[0])):
                    self.coefficient_[j + 1] = self.coefficient_[j + 1] - learning_rate * error * x[i][j]
                self.coefficient_[0] = self.coefficient_[0] - learning_rate * error * 1
        self.intercept_ = self.coefficient_[0]
        self.coefficient_ = self.coefficient_[1:]

    def eval(self, xi):
        yi = self.coefficient_[-1]
        for j in range(len(xi)):
            yi += self.coefficient_[j] * xi[j]
        return yi

    def predict(self, x):
        y_computed = [self.eval(xi) for xi in x]
        return y_computed
