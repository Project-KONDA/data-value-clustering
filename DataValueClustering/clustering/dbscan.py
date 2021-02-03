from sklearn.cluster import DBSCAN
import numpy as np
from matplotlib import pyplot as plt

from gui_center.cluster_representation import fancy_cluster_representation
from distance.distance_matrix import calculate_distance_matrix, get_condensed


def dbscan(distance_matrix, values, eps=0.5, min_samples=5, algorithm='auto', leaf_size=30, n_jobs=None):
    k_distance_graph(distance_matrix, min_samples)
    clusters = DBSCAN(eps=eps, min_samples=min_samples, metric='precomputed', algorithm=algorithm, leaf_size=leaf_size, n_jobs=n_jobs).fit_predict(distance_matrix)
    return clusters


def dbscan_args(eps, min_samples, algorithm, leaf_size, n_jobs):
    return lambda distance_matrix_map, values: dbscan(distance_matrix_map["distance_matrix"], values, eps, min_samples, algorithm, leaf_size, n_jobs)


def dbscan_min_samples_config(no_values, answers):
    # int
    name = "dbscan_min_samples"
    explanation = "Minimum number of samples per cluster. Higher values will yield less clusters and more noise. The larger or noiser the data, the larger the value should be."
    min_min_samples = 3
    max_min_samples = no_values
    suggestion_value = min_min_samples

    # However, larger values are usually better for data sets with noise and will yield more significant clusters
    # increase if a) noisy , b) large data set set or c) data contains many duplicates

    return name, explanation, min_min_samples, max_min_samples, suggestion_value


def dbscan_eps_config(distance_matrix, no_values, min_samples=None): # TODO: min_samples
    # float
    name = "dbscan_eps"
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
    resolution = 0.01
    return name, explanation, min_eps, max_eps, suggestion_value, resolution


def dbscan_algorithm_config():
    # enum
    name = "dbscan_algorithm"  # TODO
    explanation = ""  # TODO
    options = np.array([['auto', ""],
                        ['brute', ""],
                        ['kd_tree', ""],
                        ['ball_tree', ""]])  # TODO
    suggestions = ['auto']  # TODO
    deactivatable = False
    return name, explanation, options, suggestions, deactivatable


def dbscan_leaf_size_config():
    # only activated if algorithm='ball_tree' or 'kd_tree'
    # int slider
    name = "dbscan_leaf_size"  # TODO
    explanation = ""  # TODO
    mini = 0  # TODO
    maxi = 2  # TODO
    default = 30
    resolution = 1  # TODO
    deactivatable = True  # TODO
    return name, explanation, mini, maxi, default, resolution, deactivatable


def dbscan_n_jobs_config():
    # int slider
    name = "dbscan_n_jobs"  # TODO
    explanation = ""  # TODO
    mini = 0  # TODO
    maxi = 2  # TODO
    default = 1  # TODO
    resolution = 1  # TODO
    deactivatable = True  # TODO
    return name, explanation, mini, maxi, default, resolution, deactivatable


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
