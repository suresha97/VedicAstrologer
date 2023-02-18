import os

import pandas as pd

from data_loaders.planetary_positions.astrology_api_sdk import VRClient

USER_ID = os.environ.get("USER_ID")
API_KEY = os.environ.get("API_KEY")
RESOURCE = "planets"


class AstrologyAPILoader:
    def __init__(self, astro_chart_data):
        self._astro_chart_data = astro_chart_data
        self._astro_api_client = VRClient(USER_ID, API_KEY)

    def load_planetary_locations(self):
        all_plantary_position_data = []

        for _, row in self._astro_chart_data.iterrows():
            print(_)
            planetary_position_data_for_person = self._get_planetary_position_data_for_person(
                RESOURCE,
                row.birth_day,
                row.birth_month,
                row.birth_year,
                row.birth_hour,
                row.birth_minute,
                row.birth_latitude,
                row.birth_longitude,
                row.time_zone
            )

            all_plantary_position_data.append(planetary_position_data_for_person.text)

        self._astro_chart_data["planetary_position_data"] = all_plantary_position_data

        return self._astro_chart_data

    def _get_planetary_position_data_for_person(
            self, RESOURCE, day_of_birth, month_of_birth, year_of_birth,
            hour_of_birth, minute_of_birth, birth_latitude, birth_longitude,
            birth_timezone
    ):
        planetary_position_data = self._astro_api_client.call(
            RESOURCE, day_of_birth, month_of_birth, year_of_birth,
            hour_of_birth, minute_of_birth, birth_latitude, birth_longitude,
            birth_timezone
        )

        return planetary_position_data


if __name__ == "__main__":
    astro_chart_data = pd.read_csv("../../vedic_astrology_dataset/combined_astro_chart_data.csv")

    print(astro_chart_data.head())
    print(astro_chart_data.columns)
    planetary_locations_finder = AstrologyAPILoader(astro_chart_data)
    planetary_locations_data = planetary_locations_finder.load_planetary_locations()
    planetary_locations_data.to_csv("plantary_positions_data.csv")
    print(planetary_locations_data.head())
