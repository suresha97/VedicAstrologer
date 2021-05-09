import pandas as pd


class ProcessedAstroSageDataLoader:
    def __init__(self, raw_astro_sage_data):
        self._raw_astro_sage_data = raw_astro_sage_data

    def load_processed_astro_sage_data(self):
        self._clean_raw_astro_sage_data()
        return self._raw_astro_sage_data

    def _clean_raw_astro_sage_data(self):
        self._raw_astro_sage_data.columns = [col[:-1] for col in self._raw_astro_sage_data.columns[:-1]] + \
                                            [self._raw_astro_sage_data.columns[-1]]

        self._raw_astro_sage_data.dropna(inplace=True)
        self._raw_astro_sage_data["birth_day"] = self._raw_astro_sage_data["Date of Birth"].apply(lambda x: x.split(' ')[1][:-1])
        self._raw_astro_sage_data["birth_month"] = self._raw_astro_sage_data["Date of Birth"].apply(lambda x: x.split(' ')[0])
        self._raw_astro_sage_data["birth_year"] = self._raw_astro_sage_data["Date of Birth"].apply(lambda x: x.split(' ')[2])

        self._raw_astro_sage_data["birth_hour"] = self._raw_astro_sage_data["Time of Birth"].apply(lambda x: x.split(':')[0])
        self._raw_astro_sage_data["birth_minute"] = self._raw_astro_sage_data["Time of Birth"].apply(lambda x: x.split(':')[1])

        self._raw_astro_sage_data.drop(["Date of Birth", "Time of Birth"], axis=1, inplace=True)

        rename_map = {
            old_col_name: old_col_name.lower().replace(" ", "_") for old_col_name in self._raw_astro_sage_data.columns
        }
        self._raw_astro_sage_data.rename(rename_map, axis="columns", inplace=True)

if __name__ == "__main__":
    raw_astro_sage_data = pd.read_csv("raw_astro_sage_chart_data.csv")
    processed_astro_sage_data_loader = ProcessedAstroSageDataLoader(raw_astro_sage_data)
    processed_astro_sage_data = processed_astro_sage_data_loader.load_processed_astro_sage_data()
    processed_astro_sage_data.to_csv("processed_astro_sage_data.csv")

    print(processed_astro_sage_data.columns)
    print(processed_astro_sage_data.head())
    print(processed_astro_sage_data.isnull().sum(axis=0))