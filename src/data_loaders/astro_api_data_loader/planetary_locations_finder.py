import json

import pandas as pd

from data_loaders.astro_api_data_loader.astro_api_sdk import VRClient
from data_loaders.utils import pretty_print_recommendations_decisions

USER_ID = "616579"
API_KEY = "69f3de4bb75f5231aa8f7a6cfc016403"
RESOURCE = "planets"

class PlanetaryLocationsFinder:
    def __init__(self, astro_chart_data):
        self._astro_chart_data = astro_chart_data
        self._astro_api_client = VRClient(USER_ID, API_KEY)

    def load_planetary_locations(self):
        planetary_position_data_for_person = self._get_planetary_position_data_for_person(
            RESOURCE,
            19,
            1,
            1930,
            12,
            35,
            "44 N 19",
            "94 W 28",
            0
        )

        pretty_print_recommendations_decisions(json.loads(planetary_position_data_for_person.text))
        with open('coordinate_text.txt', 'w') as outfile:
            json.dump(json.loads(planetary_position_data_for_person.text), outfile)
        pass

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
    astro_chart_data = pd.read_csv("../astro_sage_data_loader/processed_astro_sage_data.csv")
    planetary_locations_finder = PlanetaryLocationsFinder(astro_chart_data)
    planetary_locations_finder.load_planetary_locations()

