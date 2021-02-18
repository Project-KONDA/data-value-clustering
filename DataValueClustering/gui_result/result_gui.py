from matplotlib import pyplot as plt, cm
import numpy as np
from sklearn.manifold import MDS

from distance.distance_matrix import get_symmetric


def show_mds_scatter_plot(values_compressed, distance_matrix, clusters_compressed, savepath=None, show=True, show_labels=True):
    if not show and savepath is None:
        return
    
    symmetric_distance_matrix = get_symmetric(distance_matrix)
    n_clusters = max(clusters_compressed) + 1
    n_compressed_values = len(clusters_compressed)

    # represent each cluster by a unique color:
    color_set = cm.rainbow(np.linspace(0, 1, n_clusters))
    value_colors = np.empty(n_compressed_values, dtype=object)
    for i in range(len(clusters_compressed)):
        if clusters_compressed[i] == -1:
            value_colors[i] = 'black'
        else:
            value_colors[i] = color_set[clusters_compressed[i]]

    # compute MDS:
    model = MDS(n_components=2, dissimilarity='precomputed')  # random_state
    out = model.fit_transform(symmetric_distance_matrix)

    plt.scatter(out[:, 0], out[:, 1], color=value_colors)

    # label points:
    if show_labels:
        for i, val in enumerate(values_compressed):
            plt.annotate(val, (out[i, 0], out[i, 1]))

    def quit_figure(event):
        if event.key == 'enter':
            plt.close(event.canvas.figure)

    plt.gcf().canvas.mpl_connect('key_press_event', quit_figure)

    plt.axis('equal')
    if savepath != None:
        savepath += ".png"
        plt.savefig(savepath)
        print("Saved as png in: " + savepath)

    if show:
        plt.show()


if __name__ == "__main__":
    values_compressed = ["a", "1", "?"]
    distance_matrix = np.array([
        [0, 1, 2],
        [0, 0, 1.5],
        [0, 0, 0]
    ])
    clusters_compressed = [0, 1, 2]
    show_mds_scatter_plot(values_compressed, distance_matrix, clusters_compressed)
