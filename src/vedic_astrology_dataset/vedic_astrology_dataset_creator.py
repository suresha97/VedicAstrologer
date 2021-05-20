import json

import pandas as pd


class ProcessedVedicAstrologyDatasetCreator:
    def __init__(self, planetary_positions_and_occupation_data):
        self._planetary_positons_and_occupation_data = planetary_positions_and_occupation_data

    def load_vedic_astrology_data(self, categorical_feature_encoding_type):
        self._drop_features()

        features_to_encode = [
            feature for feature, data_type in self._planetary_positons_and_occupation_data.dtypes.items()
            if ((data_type == "object") or (data_type == "bool")) and (feature != "occupation_category")
        ]

        self._encode_categorical_features(categorical_feature_encoding_type, features_to_encode)
        self._encode_occupation_category()

        processed_vedic_astrology_dataset = self._planetary_positons_and_occupation_data

        return processed_vedic_astrology_dataset

    def _drop_features(self):
        features_to_drop = [
            feature for feature in self._planetary_positons_and_occupation_data.columns if
            ("name" in feature) or ("id" in feature)
        ]
        features_to_drop.extend([
            feature for feature in self._planetary_positons_and_occupation_data.columns if "Ascendant" in feature
        ])

        features_to_drop.extend([
            feature for feature in self._planetary_positons_and_occupation_data.columns if
            (len(self._planetary_positons_and_occupation_data[feature].unique())) == 1
        ])

        self._planetary_positons_and_occupation_data.drop(features_to_drop, axis=1, inplace=True)

    def _encode_categorical_features(self, categorical_feature_encoding_type, features_to_encode):
        if categorical_feature_encoding_type == "label":
            self._one_hot_encode_features(features_to_encode)
        if categorical_feature_encoding_type == "one_hot":
            self._label_encode_features(features_to_encode)

    def _one_hot_encode_features(self, features_to_encode):
        for feature in features_to_encode:
            self._planetary_positons_and_occupation_data[feature] = self._planetary_positons_and_occupation_data[feature].astype("category").cat.codes

    def _label_encode_features(self, features_to_encode):
        for feature in features_to_encode:
            self._planetary_positons_and_occupation_data = pd.concat(
                [self._planetary_positons_and_occupation_data, pd.get_dummies(self._planetary_positons_and_occupation_data[feature], prefix=feature)],
                axis=1
            ).drop([feature], axis=1)

    def _encode_occupation_category(self):
        int_to_occupation_map = dict(
            enumerate(self._planetary_positons_and_occupation_data.occupation_category.astype("category").cat.categories)
        )
        occupation_to_int_map = {v:k for k,v in int_to_occupation_map.items()}
        self._planetary_positons_and_occupation_data.occupation_category.replace(occupation_to_int_map, inplace=True)
        print("Mapping from occupation category to training label: ")
        print(json.dumps(occupation_to_int_map, indent=2))


if __name__ == "__main__":
    planetary_positions_and_occupation_data = pd.read_csv("../data_loaders/planetary_positions/processed_planetary_positions_data.csv")

    vedic_astrology_dataset_creator = ProcessedVedicAstrologyDatasetCreator(planetary_positions_and_occupation_data)
    vedic_astrology_dataset = vedic_astrology_dataset_creator.load_vedic_astrology_data("one_hot")

    print(vedic_astrology_dataset.shape)
    vedic_astrology_dataset.to_csv("vedic_astrology_dataset.csv")
