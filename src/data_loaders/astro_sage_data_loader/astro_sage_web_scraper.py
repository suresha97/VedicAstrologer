import pandas as pd
from bs2json import bs2json

from data_loaders.utils import get_beauiful_soup_object_from_base_url, pretty_print_recommendations_decisions


class AstroSageWebScraper:
    def __init__(self, astro_sage_base_url):
        self._astro_sage_base_url = astro_sage_base_url

    def load_raw_astro_sage_data(self):
        astro_sage_soup = get_beauiful_soup_object_from_base_url(self._astro_sage_base_url)
        all_occupation_category_hrefs = self._get_all_occupation_category_hrefs(astro_sage_soup)
        all_occupation_categories = [category_href.split("=")[-1] for category_href in all_occupation_category_hrefs]
        print(all_occupation_categories)

        all_names_in_each_occupation_category = {
            occupation_category_href.split("=")[-1]: self._get_hrefs_for_all_names_in_category(occupation_category_href)
            for occupation_category_href in all_occupation_category_hrefs
        }

        raw_astro_chart_data = []
        for category in all_occupation_categories:
            astro_chart_data_for_celebrities_in_category = self._get_astro_chart_data_for_all_names_in_category(
                all_names_in_each_occupation_category[category],
                category
            )

            raw_astro_chart_data.extend(astro_chart_data_for_celebrities_in_category)

        return raw_astro_chart_data

    def _get_all_occupation_category_hrefs(self, astro_sage_soup):
        all_occupation_categories_container = astro_sage_soup.find_all(class_="ui-morecategorybox")
        all_occupation_categories = [item.find_all("a") for item in all_occupation_categories_container][0]

        all_occuaption_category_hrefs = [
            category["href"] for category in all_occupation_categories
        ]

        return all_occuaption_category_hrefs

    def _get_hrefs_for_names_from_soup(self, occupation_category_soup):
        all_name_hrefs_container = occupation_category_soup.find_all(class_="ui-img-container")
        all_name_hrefs = [
            item.a["href"] for item in all_name_hrefs_container
        ]

        return all_name_hrefs

    def _get_hrefs_for_all_names_in_category(self, occupation_category_href):
        category_name = occupation_category_href.split("=")[-1]
        print(f"Fetching names for {category_name}...")
        url = f"{self._astro_sage_base_url}/{occupation_category_href}"
        page_number = 1

        hrefs_for_all_names_in_category = []
        while True:
            next_page_url = f"{url}&page={page_number}"
            occupation_category_soup = get_beauiful_soup_object_from_base_url(next_page_url)
            if "No Records found" in occupation_category_soup.text:
                break

            page_number += 1
            hrefs_for_all_names_in_category.extend(
                self._get_hrefs_for_names_from_soup(occupation_category_soup)
            )

        return hrefs_for_all_names_in_category

    def _get_astro_chart_data_for_all_names_in_category(self, hrefs_for_names_in_category, category):
        converter = bs2json()
        celebrities_astro_chart_data = []

        for category_href in hrefs_for_names_in_category:
            url = f"{self._astro_sage_base_url}{category_href}"
            soup = get_beauiful_soup_object_from_base_url(url)
            celebrity_astro_chart_data_container = soup.find_all(class_="celebcont")

            celebrity_atro_chart_data = {
                converter.convert(astro_chart_data)["div"]["b"]["text"]: converter.convert(astro_chart_data)["div"]["text"]
                for astro_chart_data in celebrity_astro_chart_data_container[0:7]
            }
            celebrity_atro_chart_data["occupation"] = category

            celebrities_astro_chart_data.append(celebrity_atro_chart_data)

        return celebrities_astro_chart_data


if __name__ == "__main__":
    astro_sage_base_url = "https://celebrity.astrosage.com/"
    astro_sage_web_scraper = AstroSageWebScraper(astro_sage_base_url)
    raw_astro_chart_data = astro_sage_web_scraper.load_raw_astro_sage_data()

    pretty_print_recommendations_decisions(raw_astro_chart_data)

    raw_astro_chart_data_df = pd.DataFrame(raw_astro_chart_data)
    print(raw_astro_chart_data_df.occupation.unique())
    raw_astro_chart_data_df.to_csv("raw_astro_sage_chart_data.csv", index=False)
