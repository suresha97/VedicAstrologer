import plotly.express as px
from sklearn.decomposition import PCA


class PCATransformer:
    def __init__(self, number_of_components):
        self._number_of_components = number_of_components
        self.pca = PCA(self._number_of_components)

    def get_principal_componenets(self, train_x, test_x):
        self.pca.fit(train_x)

        return self.pca.transform(train_x), self.pca.transform(test_x)

    @property
    def explained_variance_ratio(self):
        return self.pca.explained_variance_ratio_

    def plot_principal_componenets(self, features, labels):
        components = self.pca.fit_transform(features)

        explained_variance_for_each_componenet = {
            str(i): f"PC {i + 1} ({var:.1f}%)"
            for i, var in enumerate(self.explained_variance_ratio * 100)
        }

        fig = px.scatter_matrix(
            components,
            labels=explained_variance_for_each_componenet,
            dimensions=range(self._number_of_components),
            color=labels
        )

        fig.update_traces(diagonal_visible=False)
        fig.show()

    def plot_3D(self, features, labels):
        components = self.pca.fit_transform(features)

        total_explained_variance = self.explained_variance_ratio.sum() * 100

        fig = px.scatter_3d(
            components, x=0, y=1, z=2, color=labels,
            title=f'Total Explained Variance: {total_explained_variance:.2f}%',
            labels={'0': 'PC 1', '1': 'PC 2', '2': 'PC 3'}
        )

        fig.show()
