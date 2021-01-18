from matplotlib import pyplot as plt, cm
import numpy as np
from sklearn.manifold import MDS

from utility.distance_matrix import get_symmetric


def show_mds_scatter_plot(values_compressed, distance_matrix, clusters_compressed):
    symmetric_distance_matrix = get_symmetric(distance_matrix)
    n_clusters = max(clusters_compressed) + 1
    n_compressed_values = len(clusters_compressed)

    # represent each cluster by a unique color:
    color_set = cm.rainbow(np.linspace(0, 1, n_clusters))
    value_colors = np.empty(n_compressed_values, dtype=object)
    for i in range(len(clusters_compressed)):
        value_colors[i] = color_set[clusters_compressed[i]]

    # compute MDS:
    model = MDS(n_components=2, dissimilarity='precomputed')  # random_state
    out = model.fit_transform(symmetric_distance_matrix)

    plt.scatter(out[:, 0], out[:, 1], color=value_colors)

    # label points:
    for i, val in enumerate(values_compressed):
        plt.annotate(val, (out[i, 0], out[i, 1]))

    plt.axis('equal')
    plt.show()