from sklearn.linear_model import LogisticRegression

from vedic_astrology_classifiers.classifier import Classifier


class LogisticRegressionClassifier(Classifier):
    def __init__(self, features, labels, hyperparameters, is_scaling_required):
        super().__init__(features, labels, is_scaling_required)
        self._hyperparameters = hyperparameters
        self.model = self._instantiate_model(**self._hyperparameters)

    def _instantiate_model(self, **kwargs):
        return LogisticRegression(**kwargs)
