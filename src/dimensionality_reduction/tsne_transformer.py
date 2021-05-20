import plotly.express as px
from sklearn.manifold import TSNE


class tSNETransformer:
    def __init__(self, parameters):
        self.parameters = parameters
        self.tsne = TSNE(**self.parameters)

    def plot_3D(self, features, labels):
        projections = self.tsne.fit_transform(features)

        fig = px.scatter_3d(
            projections, x=0, y=1, z=2,
            color=labels, labels={"color":"occupation category"}
        )
        #fig.update_traces(marker_size=8)
        fig.show()
