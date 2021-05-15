from abc import ABC, abstractmethod

from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report


class Classifier(ABC):
    def __init__(self, features, labels, test_set_proportion):
        self._features = features
        self._labels = labels
        self._test_set_proportion = test_set_proportion
        self._train_x, self._train_y, self._test_x, self._test_y = self._train_dev_test_split(
            self._features, self._labels
        )
        self._model = self._instantiate_model()

    @abstractmethod
    def _instantiate_model(self, **kwargs):
        raise NotImplementedError()

    def _train_dev_test_split(self, features, labels):
        return train_test_split(features, labels, self._test_set_proportion)

    def _train(self, train_x, train_y):
        self._model.fit(train_x, train_y)

    def _get_predictions(self, test_x):
        return self._model.predict(test_x)

    def _get_evaluation_metrics(self, test_x, test_y):
        test_x_predictions = self._get_predictions(test_x)
        print(classification_report(test_y, test_x_predictions))
