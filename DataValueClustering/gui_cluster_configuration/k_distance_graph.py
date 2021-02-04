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
    plt.show()