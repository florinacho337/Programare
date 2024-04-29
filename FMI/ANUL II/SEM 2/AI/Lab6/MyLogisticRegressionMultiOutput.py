from MyLogisticRegression import MyLogisticRegression


class MyLogisticRegressionMultiOutputs:
    def __init__(self, classes):
        self.classes_ = classes
        self.intercept_ = {c: 0.0 for c in classes}
        self.coefficient_ = {c: [] for c in classes}

    def fit(self, x, y, learning_rate=0.001, no_epochs=1000):
        for cls in self.classes_:
            binary_y = [1 if label == cls else 0 for label in y]
            classifier = MyLogisticRegression()
            classifier.fit(x, binary_y, learning_rate, no_epochs)
            self.intercept_[cls] = classifier.intercept_
            self.coefficient_[cls] = classifier.coefficient_

    def predict_one_sample(self, sample_features):
        predictions = {cls: self.evaluate(sample_features, self.intercept_[cls], self.coefficient_[cls]) for cls in
                       self.classes_}
        predicted_class = max(predictions, key=predictions.get)
        return predicted_class

    def predict(self, x):
        return [self.predict_one_sample(sample) for sample in x]

    @staticmethod
    def evaluate(xi, intercept, coefficients):
        yi = intercept
        for j in range(len(xi)):
            yi += coefficients[j] * xi[j]
        return yi
