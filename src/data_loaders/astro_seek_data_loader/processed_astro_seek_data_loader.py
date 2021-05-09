import numpy as np
import pandas as pd


class ProcessedAstroSeekDataLoader:
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

        cleaned_astro_seek_data["Birth time - local"] = pd.to_datetime(cleaned_astro_seek_data["Birth time - local"], errors='coerce')
        cleaned_astro_seek_data["Birth time - GMT"] = pd.to_datetime(cleaned_astro_seek_data["Birth time - GMT"], errors='coerce')

        return cleaned_astro_seek_data

    def _process_cleaned_astro_seek_data(self, cleaned_astro_seek_data):
        cleaned_astro_seek_data["birth_date"] = cleaned_astro_seek_data["Birth time - GMT"].dt.date
        cleaned_astro_seek_data["birth_time"] = cleaned_astro_seek_data["Birth time - GMT"].dt.time
        cleaned_astro_seek_data["timezone"] = np.zeros(len(cleaned_astro_seek_data)).astype(int)

        cleaned_astro_seek_data.occupation = cleaned_astro_seek_data.occupation.map(lambda x: x[:-1])
        cleaned_astro_seek_data.rename(
            {
                "Birth longitude": "longitude",
                "Birth latitude": "latitude"
            }, inplace=True, axis="columns"
        )

        cleaned_astro_seek_data.drop(["Birth time - local", "Birth time - GMT"], axis=1, inplace=True)

        return cleaned_astro_seek_data

if __name__ == "__main__":
    raw_astro_seek_data = pd.read_csv("raw_astro_seek_chart_data.csv")
    processed_astro_seek_data_loader = ProcessedAstroSeekDataLoader(raw_astro_seek_data)
    processed_astro_seek_data = processed_astro_seek_data_loader.load_processed_astro_seek_data()

    print(processed_astro_seek_data.head())
    print(processed_astro_seek_data.isnull().sum(axis=0))