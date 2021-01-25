from sklearn.cluster import DBSCAN
import numpy as np
from matplotlib import pyplot as plt

from main.clustering import fancy_cluster_representation
from distance.distance_matrix import calculate_distance_matrix, get_condensed


def dbscan(distance_function, values, eps=0.5, min_samples=5, algorithm='auto', leaf_size=30, n_jobs=None):
    dm = calculate_distance_matrix(distance_function, values)
    k_distance_graph(dm, min_samples)
    clusters = DBSCAN(eps=eps, min_samples=min_samples, metric='precomputed', algorithm=algorithm, leaf_size=leaf_size, n_jobs=n_jobs).fit_predict(dm)
    return clusters


def min_samples_config(no_values, answers):
    name = "min_samples"
    explanation = "Minimum number of samples per cluster. Higher values will yield less clusters and more noise. The larger or noiser the data, the larger the value should be. "
    min_min_samples = 3
    max_min_samples = no_values
    suggestion_value = min_min_samples

    # However, larger values are usually better for data sets with noise and will yield more significant clusters
    # increase if a) noisy , b) large data set set or c) data contains many duplicates

    return name, explanation, min_min_samples, max_min_samples, suggestion_value


def eps_config(distance_matrix, no_values, min_samples):
    name = "eps"
    explanation = "The maximum distance between two samples belonging to the same cluster." \
                  "In general, small values of eps are preferable. If chosen much too small, a large part of the data will not be clustered, thus be interpreted as " \
                  "noise. Whereas for a too high value, clusters will merge and the majority of objects will be in " \
                  "the same cluster "

    # as a rule of thumb, only a small fraction of points should be within this distance of each other

    if not (min_samples is None):
        k = min_samples
        distances = np.empty(len(distance_matrix), dtype=float)
        for i in range(len(distance_matrix)):
            d = distance_matrix[i, :]
            sorted = np.sort(d)
            distances[i] = sorted[k + 1]
        max_eps = max(distances)
    else:
        max_eps = np.amax(distance_matrix)

    min_eps = min(get_condensed(distance_matrix))
    suggestion_value = min_eps

    return name, explanation, min_eps, max_eps, suggestion_value


def k_distance_graph(distance_matrix, k):
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



if __name__ == '__main__':
    v = [1, 1, 1, 3, 4, 5, 10, 100, 3]
    c = dbscan(lambda a, b: abs(a - b), v, eps=0.1, min_samples=2)
    # print(c)
    print(fancy_cluster_representation(v, c))
