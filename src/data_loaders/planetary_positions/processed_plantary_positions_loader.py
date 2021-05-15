import json

import pandas as pd


class ProcessedPlanetaryPositionsLoader:
    def __init__(self, raw_planetary_positions_data):
        self._raw_planetary_positions_data = raw_planetary_positions_data
        pass

    def _load_processed_planetary_positions_data(self):
        planetary_positions_feature_names = self._get_planetary_position_feature_names()

        cleaned_data = []
        for _, row in self._raw_planetary_positions_data.iterrows():
            planetary_positions_features = []
            planetary_positions_sample = json.loads(row.planetary_position_data)

            if isinstance(planetary_positions_sample, dict):
                if planetary_positions_sample["status"] == False:
                    continue

            for planet in planetary_positions_sample:
                planetary_positions_features.extend(list(planet.values()))

            planetary_positions_features_and_occupation_labels = [row.occupation_category] + planetary_positions_features
            cleaned_data.append(planetary_positions_features_and_occupation_labels)

        processed_planetary_positions_data = pd.DataFrame(data=cleaned_data, columns=["occupation_category"]+planetary_positions_feature_names)

        return processed_planetary_positions_data

    def _get_planetary_position_feature_names(self):
        planetary_position_data_sample = json.loads(self._raw_planetary_positions_data.planetary_position_data.values[0])

        planetary_position_feature_names = []
        for planet in planetary_position_data_sample:
            planet_name = planet["name"]
            planet_features = [f"{planet_name}_{feature}" for feature in list(planet.keys())]
            planetary_position_feature_names.extend(planet_features)

        return planetary_position_feature_names


if __name__ == "__main__":
    raw_planetary_positions_data = pd.read_csv("plantary_positions_data.csv")

    processed_planetart_positions_data_loader = ProcessedPlanetaryPositionsLoader(raw_planetary_positions_data)
    processed_planetary_positions_data = processed_planetart_positions_data_loader._load_processed_planetary_positions_data()
    print(processed_planetary_positions_data.head())
    print(processed_planetary_positions_data.shape)
    processed_planetary_positions_data.to_csv("processed_planetary_positions_data.csv")
