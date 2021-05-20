from abc import ABC, abstractmethod

from sklearn.metrics import classification_report
from sklearn.preprocessing import StandardScaler


class Classifier(ABC):
    def __init__(self, train_data, test_data, is_scaling_required):
        self.train_x, self.train_y = train_data
        self.test_x, self.test_y = test_data
        self.model = self._instantiate_model()
        self.is_sclaing_required = is_scaling_required

        if self.is_sclaing_required:
            self.train_x, self.test_x = self._scale_data()

    @abstractmethod
    def _instantiate_model(self, **kwargs):
        raise NotImplementedError()

    def train(self):
        self.model.fit(self.train_x, self.train_y)

    def get_predictions(self, test_x):
        return self.model.predict(test_x)

    def get_evaluation_metrics(self):
        test_x_predictions = self.get_predictions(self.test_x)
        print(classification_report(self.test_y, test_x_predictions))

    def train_and_evaluate_model(self):
        self.train()
        self.get_evaluation_metrics()

    def _scale_data(self):
        standard_scaler = StandardScaler()
        standard_scaler.fit(self.train_x)

        return standard_scaler.transform(self.train_x), standard_scaler.transform(self.test_x)
