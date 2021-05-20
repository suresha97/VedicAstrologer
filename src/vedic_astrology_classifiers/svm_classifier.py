from sklearn.svm import SVC

from vedic_astrology_classifiers.classifier import Classifier


class SVMClassifier(Classifier):
    def __init__(self, train_data, test_data, hyperparameters, is_scaling_required):
        super().__init__(train_data, test_data, is_scaling_required)
        self._hyperparameters = hyperparameters
        self.model = self._instantiate_model(**self._hyperparameters)

    def _instantiate_model(self, **kwargs):
        return SVC(**kwargs)
