from scipy.cluster.hierarchy import dendrogram
from matplotlib import pyplot as plt


def show_dendrogram(linkage_matrix, labels=None):
    fig = plt.figure(figsize=(10, 7))
    fig.canvas.set_window_title('Dendrogram')
    fig.suptitle('Dendrogram')

    if labels is None:
        dendrogram(linkage_matrix,
                   orientation='right',
                   distance_sort='descending',
                   show_leaf_counts=True)

    else:
        dendrogram(linkage_matrix,
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

