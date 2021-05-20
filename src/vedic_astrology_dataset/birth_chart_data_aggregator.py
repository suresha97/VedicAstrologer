import pandas as pd


class BirthChartDataAggregator:
    def __init__(self, astro_chart_data_dfs):
        self._astro_chart_data_dfs = astro_chart_data_dfs

    def load_combined_astro_chart_data(self, occupation_category_map, data_columns_to_keep):
        unique_occupation_categories = self._get_unique_occupation_categories()
        print(unique_occupation_categories)

        occupation_category_df_column_map = self._get_occpation_category_df_column_map(
            unique_occupation_categories,
            occupation_category_map
        )

        processed_astro_chart_dfs = []
        for df in self._astro_chart_data_dfs:
            df["occupation_category"] = df["occupation"].map(occupation_category_df_column_map)
            df = df[df.occupation_category.isin(list(occupation_category_map.keys()))]
            df.drop([col for col in df.columns if col not in data_columns_to_keep], axis=1, inplace=True)
            processed_astro_chart_dfs.append(df[data_columns_to_keep])

        return pd.concat(processed_astro_chart_dfs)

    def _get_unique_occupation_categories(self):
        unique_occupation_categories = []
        for df in self._astro_chart_data_dfs:
            unique_occupation_categories.extend(list(df.occupation.unique()))

        return set(unique_occupation_categories)

    def _get_occpation_category_df_column_map(self, unique_occupation_categories, occupation_category_map):
        occupation_category_df_column_map = {}

        for occupation in unique_occupation_categories:
            for occupation_category, occupations_in_category in occupation_category_map.items():
                if occupation in occupations_in_category:
                    occupation_category_df_column_map[occupation] = occupation_category

        return occupation_category_df_column_map


if __name__ == "__main__":
    astro_sage_data = pd.read_csv("../data_loaders/astro_sage_birth_charts/processed_astro_sage_data.csv")
    astro_seek_data = pd.read_csv("../data_loaders/astro_seek_birth_charts/processed_astro_seek_data.csv")

    print(astro_sage_data.columns.unique())
    print(astro_seek_data.columns.unique())
    astro_chart_data_dfs = [astro_seek_data]
    astro_chart_data_combiner = BirthChartDataAggregator(astro_chart_data_dfs)

    occupation_category_map = {
        "show business worker": ['hollywood', 'bollywood', 'musician', 'singer', 'cameraman', 'composer', 'conductor', 'script-writer', 'producer', 'dancer', 'opera-singer', 'fashion-model', 'children-of-celebritie'],
        "athlete": ['cricket', 'sports',  'football', 'hockey', 'athlete', 'baseball-player', 'basketball-player', 'figure-skater', 'football-soccer-playe',  'runners-sprinter', 'tennis-player', 'gymnast', 'martial-artist', 'racer', 'swimmer', 'golfer'],
        "businessman": ['businessman', 'lawyer', 'entrepreneur', 'founder'],
        "government employee": ['politician', 'diplomat'],
        "scientist": ['scientist', 'doctor',  'chemist', 'mathematician', 'physicist', 'psychologist', 'scientists-inventor', 'astrologer'],
        "artist": ['artist', 'sculptor', 'painter', 'poet', 'designer', 'photographer'],
        "writer": ['literature', 'writer', 'journalists-publicist', 'philosopher']
    }
    data_columns_to_keep = ['name', 'birth_longitude', 'birth_latitude', 'birth_day', 'birth_month', 'birth_year', 'birth_hour', 'birth_minute', 'time_zone', 'occupation_category']

    combined_astro_chart_data = astro_chart_data_combiner.load_combined_astro_chart_data(occupation_category_map, data_columns_to_keep)
    combined_astro_chart_data.to_csv("combined_astro_chart_data.csv", index=False)
    print(combined_astro_chart_data.shape)
    print(combined_astro_chart_data.head())
    print(combined_astro_chart_data.occupation_category.unique())