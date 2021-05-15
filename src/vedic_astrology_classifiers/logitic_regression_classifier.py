from sklearn.linear_model import LogisticRegression

from vedic_astrology_classifiers.classifier import Classifier


class LogisticRegressionClassifier(Classifier):
    def _instantiate_model(self, **kwargs):
        return LogisticRegression(**kwargs)
