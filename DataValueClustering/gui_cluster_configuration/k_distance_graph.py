'''View showing k-distance graph.'''
import numpy as np
from matplotlib import pyplot as plt


def show_k_distance_graph(distance_matrix, k):
    distances = np.empty(len(distance_matrix), dtype=float)
    for i in range(len(distance_matrix)):
        d = distance_matrix[i, :]
        sorted = np.sort(d)
        # distances[i] = sum(sorted[0:k-1])/k
        distances[i] = sum(sorted[1:k + 1]) / k
        # distances[i] = sorted[k+1]
    distances_sorted = np.sort(distances)
    plt.plot(distances_sorted)

    plt.title('K-Distance Graph')

    def quit_figure(event):
        if event.key == 'enter':
            plt.close(event.canvas.figure)

    plt.gcf().canvas.mpl_connect('key_press_event', quit_figure)

    print("showing k_distance graph ...")

    plt.show()
