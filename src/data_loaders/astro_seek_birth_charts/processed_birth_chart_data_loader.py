import datetime

import numpy as np
import pandas as pd


class ProcessedBirthChartLoader:
    def __init__(self, raw_astro_seek_data):
        self._raw_astro_seek_data = raw_astro_seek_data

    def load_processed_astro_seek_data(self):
        cleaned_astro_seek_data = self._clean_astro_seek_data()
        processed_astro_seek_data = self._process_cleaned_astro_seek_data(cleaned_astro_seek_data)

        return processed_astro_seek_data

    def _clean_astro_seek_data(self):
        cleaned_astro_seek_data = self._raw_astro_seek_data[
            (~self._raw_astro_seek_data["Birth time - local"].str.contains("uknown time")) &
            (~self._raw_astro_seek_data["Birth time - GMT"].str.contains("no system")) &
            (~self._raw_astro_seek_data["Birth longitude"].str.contains("Wikipedia")) &
            (~self._raw_astro_seek_data["Birth latitude"].str.contains(","))
        ]

        cleaned_astro_seek_data.dropna(inplace=True)

        return cleaned_astro_seek_data

    def _process_cleaned_astro_seek_data(self, cleaned_astro_seek_data):
        cleaned_astro_seek_data["birth_day"] = cleaned_astro_seek_data["Birth time - GMT"].apply(lambda x: x.split(' ')[0])
        cleaned_astro_seek_data["birth_month"] = cleaned_astro_seek_data["Birth time - GMT"].apply(lambda x: x.split(' ')[1])
        cleaned_astro_seek_data["birth_month"] = cleaned_astro_seek_data["birth_month"].apply(lambda x: self._convert_month_str_to_integer(x))
        cleaned_astro_seek_data["birth_year"] = cleaned_astro_seek_data["Birth time - GMT"].apply(lambda x: x.split(' ')[2])

        cleaned_astro_seek_data["birth_hour"] = cleaned_astro_seek_data["Birth time - GMT"].apply(lambda x: x.split('-')[-1].split(':')[0])
        cleaned_astro_seek_data["birth_minute"] = cleaned_astro_seek_data["Birth time - GMT"].apply(lambda x: x.split('-')[-1].split(':')[1])
        cleaned_astro_seek_data.drop(["Birth time - local", "Birth time - GMT"], axis=1, inplace=True)

        cleaned_astro_seek_data["time_zone"] = np.zeros(len(cleaned_astro_seek_data)).astype(int)
        cleaned_astro_seek_data.occupation = cleaned_astro_seek_data.occupation.map(lambda x: x[:-1])
        rename_map = {
            old_col_name: old_col_name.lower().replace(" ", "_") for old_col_name in cleaned_astro_seek_data.columns
        }
        cleaned_astro_seek_data.rename(rename_map, inplace=True, axis="columns")

        return cleaned_astro_seek_data

    def _convert_month_str_to_integer(self, month):
        try:
            month_int = datetime.datetime.strptime(month, "%B").month
        except ValueError:
            month_int = datetime.datetime.strptime(month, "%b").month


        return month_int


if __name__ == "__main__":
    raw_astro_seek_data = pd.read_csv("raw_astro_seek_chart_data.csv")
    processed_astro_seek_data_loader = ProcessedBirthChartLoader(raw_astro_seek_data)
    processed_astro_seek_data = processed_astro_seek_data_loader.load_processed_astro_seek_data()
    processed_astro_seek_data.to_csv("processed_astro_seek_data.csv")

    print(processed_astro_seek_data.columns)
    print(processed_astro_seek_data.head())
    print(processed_astro_seek_data.isnull().sum(axis=0))
