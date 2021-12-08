from matplotlib import pyplot as plt, cm
import numpy as np
from sklearn.manifold import MDS

import matplotlib
matplotlib.use('TkAgg')
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from distance.distance_matrix import get_symmetric


def show_mds_scatter_plot_integrated(root, values_compressed, distance_matrix, clusters_compressed, savepath=None, show=True,
                          show_labels=False):
    if not show and savepath is None:
        return

    symmetric_distance_matrix = get_symmetric(distance_matrix)

    # compute MDS:
    model = MDS(n_components=2, dissimilarity='precomputed')  # random_state
    out = model.fit_transform(symmetric_distance_matrix)

    # define figure with scatter subplot and legend:
    fig = Figure(figsize=(4, 3))
    a = fig.add_subplot(111)
    a.set_title("MDS Scatter Plot", fontsize=10)
    a.axis('equal')
    clusters_compressed_plus_one = np.copy(clusters_compressed)
    for i, e in enumerate(clusters_compressed):
        clusters_compressed_plus_one[i] = clusters_compressed[i]+1
    scatter = a.scatter(out[:, 0], out[:, 1], c=clusters_compressed_plus_one, norm=plt.Normalize(vmin=min(clusters_compressed_plus_one), vmax=max(clusters_compressed_plus_one)), cmap="nipy_spectral")
    handles, labels = scatter.legend_elements()
    for i, l in enumerate(labels):
        if l == "$\\mathdefault{0}$":
            labels[i] = "$\\mathdefault{noise}$"
    fig.legend(handles, labels, title="Clusters", loc=7)
    # fig.tight_layout()
    fig.subplots_adjust(right=0.75)

    # label points:
    if show_labels:
        for i, val in enumerate(values_compressed):
            a.annotate(val, (out[i, 0], out[i, 1]))

    if savepath is not None:
        savepath += ".png"
        plt.savefig(savepath)
        print("Saved as png in: " + savepath)

    if show:
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.get_tk_widget().grid(row=2, column=0, sticky='nwse', pady=(20,0), padx=10)
        canvas.draw()


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
