from xgboost import XGBClassifier
import matplotlib.pyplot as plt

from vedic_astrology_classifiers.classifier import Classifier


class XGBoostClassifier(Classifier):
    def __init__(self, train_data, test_data, hyperparameters, is_scaling_required):
        super().__init__(train_data, test_data, is_scaling_required)
        self._hyperparameters = hyperparameters
        self.model = self._instantiate_model(**self._hyperparameters)

    def _instantiate_model(self, **kwargs):
        return XGBClassifier(**kwargs)

    def plot_feature_importance(self, feature_names):
        sorted_idx = self.model.feature_importances_.argsort()
        plt.barh(feature_names[sorted_idx], self.model.feature_importances_[sorted_idx])
        plt.xlabel("Random Forest Feature Importance")

        return
