import pandas as pd

class AstroChartDataCombiner:
    def __init__(self, astro_chart_data_dfs):
        self._astro_chart_data_dfs = astro_chart_data_dfs

    def load_combined_astro_chart_data(self):
        occupation_categories = self._get_unique_occupation_categories()
        print(occupation_categories)

        return

    def _get_unique_occupation_categories(self):
        unique_occupation_categories = []
        for df in self._astro_chart_data_dfs:
            unique_occupation_categories.extend(list(df.occupation.unique()))

        return unique_occupation_categories



if __name__ == "__main__":
    astro_sage_data = pd.read_csv("../data_loaders/astro_sage_data_loader/processed_astro_sage_data.csv")
    astro_seek_data = pd.read_csv("../data_loaders/astro_seek_data_loader/processed_astro_seek_data.csv")

    astro_chart_data_dfs = [astro_sage_data, astro_seek_data]
    astro_chart_data_combiner = AstroChartDataCombiner(astro_chart_data_dfs)
    astro_chart_data_combiner.load_combined_astro_chart_data()