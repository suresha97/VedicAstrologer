import pandas as pd
from sklearn.model_selection import train_test_split

from vedic_astrology_dataset.vedic_astrology_dataset_creator import ProcessedVedicAstrologyDatasetCreator
from vedic_astrology_classifiers.logitic_regression_classifier import LogisticRegressionClassifier
from dimensionality_reduction.pca_transformer import PCATransformer
from dimensionality_reduction.tsne_transformer import tSNETransformer


def get_vedic_astrology_dataset(planetary_positions_dataset):
    processed_vedic_astrology_dataset_creator = ProcessedVedicAstrologyDatasetCreator(planetary_positions_dataset)
    vedic_astrology_dataset = processed_vedic_astrology_dataset_creator.load_vedic_astrology_data("label")

    return vedic_astrology_dataset


def get_vedic_astrology_featuers_and_labels(vedic_astrology_dataset):
    vedic_astrology_features = vedic_astrology_dataset.iloc[:, 1:]
    vedic_astrology_labels = vedic_astrology_dataset.iloc[:, 0]

    return vedic_astrology_features, vedic_astrology_labels


def get_train_test_split(features, labels, test_set_size=0.2):
    return train_test_split(features, labels, test_size=test_set_size)


def get_reduced_dimensions(train_features, test_features, number_of_componenets):
    pca_transformer = PCATransformer(number_of_componenets)
    train_features_reduced, test_features_reduced = pca_transformer.get_principal_componenets(train_features, test_features)
    print(pca_transformer.explained_variance_ratio)

    return train_features_reduced, test_features_reduced


def plot_pca_components(features, labels, number_of_componenets_to_plot, three_D=False):
    if three_D:
        pca_transformer = PCATransformer(3)
        pca_transformer.plot_3D(features, labels)

    pca_transformer = PCATransformer(number_of_componenets_to_plot)
    pca_transformer.plot_principal_componenets(features, labels)


def plot_tsne_projections(features, labels):
    tsne_parameters = {
        "n_components": 3,
        "perplexity": 50,
        "early_exaggeration": 120,
        "learning_rate": 100,
        "n_iter": 3000,
        "verbose": 1
    }
    tsne_transformer = tSNETransformer(tsne_parameters)
    tsne_transformer.plot_3D(features, labels)


def train_and_evaluate_logistic_regression_classifier(train_data, test_data):
    hyperparameters = {
        "solver": "liblinear",
        "penalty": "l1",
        "C": 1000,
        "max_iter": 100,
    }

    LogisticRegressionClf = LogisticRegressionClassifier(train_data, test_data, hyperparameters, is_scaling_required=True)
    LogisticRegressionClf.train_and_evaluate_model()

def plot_feature_importance(model, features):
    model.plot_featuere_importance(list(features.columns))


if __name__ == "__main__":
    planetary_positions_and_occupation_data = pd.read_csv("data_loaders/planetary_positions/processed_planetary_positions_data.csv")

    vedic_astrology_dataset = get_vedic_astrology_dataset(planetary_positions_and_occupation_data)
    vedic_astrology_dataset = vedic_astrology_dataset[(vedic_astrology_dataset.occupation_category == 4) | (vedic_astrology_dataset.occupation_category == 0)]
    vedic_astrology_features, vedic_astrology_labels = get_vedic_astrology_featuers_and_labels(vedic_astrology_dataset)
    vedic_astrology_train_x, vedic_astrology_test_x, vedic_astrology_train_y, vedic_astrology_test_y = get_train_test_split(
        vedic_astrology_features, vedic_astrology_labels
    )

    vedic_astrology_train_x, vedic_astrology_test_x = get_reduced_dimensions(
        vedic_astrology_train_x,
        vedic_astrology_test_x,
        number_of_componenets=50
    )
    #plot_pca_components(vedic_astrology_train_x, vedic_astrology_train_y, 3, three_D=True)

    #plot_tsne_projections(vedic_astrology_train_x, vedic_astrology_train_y)

    vedic_astrology_train_data = (vedic_astrology_train_x, vedic_astrology_train_y)
    vedic_astrology_test_data = (vedic_astrology_test_x, vedic_astrology_test_y)
    #train_and_evaluate_logistic_regression_classifier(vedic_astrology_train_data, vedic_astrology_test_data)
