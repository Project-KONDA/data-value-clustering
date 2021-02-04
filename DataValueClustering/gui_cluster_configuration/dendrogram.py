from scipy.cluster.hierarchy import dendrogram
from matplotlib import pyplot as plt


def show_dendrogram(clusters, labels=None):
    plt.figure(figsize=(10, 7))
    if labels is None:
        dendrogram(clusters,
                   orientation='right',
                   distance_sort='descending',
                   show_leaf_counts=True)

    else:
        dendrogram(clusters,
                   orientation='right',
                   labels=labels,
                   distance_sort='descending',
                   show_leaf_counts=True)

    def quit_figure(event):
        if event.key == 'enter':
            plt.close(event.canvas.figure)

    plt.gcf().canvas.mpl_connect('key_press_event', quit_figure)

    print("showing dendrogram ...")
    plt.show()

