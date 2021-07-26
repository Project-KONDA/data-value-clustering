'''Apply DBSCAN clustering algorithm.'''
from sklearn.cluster import DBSCAN
import numpy as np

from gui_center.cluster_representation import fancy_cluster_representation
# from gui_cluster_configuration.k_distance_graph import show_k_distance_graph

N_JOBS = "n_jobs"
LEAF_SIZE = "leaf_size"
ALGORITHM = "algorithm"
EPS = "eps"
MIN_SAMPLES = "min_samples"


def dbscan(distance_matrix, values, eps=0.5, min_samples=5, n_jobs=None):
    # show_k_distance_graph(distance_matrix, min_samples)
    clusters = DBSCAN(eps=eps, min_samples=min_samples, metric='precomputed', n_jobs=n_jobs).fit_predict(distance_matrix)
    return clusters


def dbscan_args(eps, min_samples, n_jobs):
    return lambda distance_matrix_map, values: dbscan(distance_matrix_map["distance_matrix"], values, eps, min_samples, n_jobs)


def dbscan_min_samples_config(no_values, answers):
    # int
    name = MIN_SAMPLES
    explanation = "Minimum number of samples per cluster. Higher values will yield less clusters and more noise. The larger or noiser the data, the larger the value should be."
    min_min_samples = max(1, min(3, no_values))
    max_min_samples = max(3, no_values-2)
    suggestion_value = min_min_samples

    # However, larger values are usually better for data sets with noise and will yield more significant clusters
    # increase if a) noisy , b) large data set set or c) data contains many duplicates

    return name, explanation, min_min_samples, max_min_samples, suggestion_value


def dbscan_eps_config(distance_matrix, min_distance, no_values):
    # float
    name = EPS
    explanation = "The maximum distance between two samples belonging to the same cluster." \
                  "In general, small values of eps are preferable. If chosen much too small, a large part of the data will not be clustered, thus be interpreted as " \
                  "noise. Whereas for a too high value, clusters will merge and the majority of objects will be in " \
                  "the same cluster."

    # as a rule of thumb, only a small fraction of points should be within this distance of each other

    max_eps = calculate_eps_max(distance_matrix, max(1, min(3, no_values)))  # 3 is min_min_samples
    min_eps = max(min_distance, 0.01)
    suggestion_value = min_eps
    resolution = 0.01
    return name, explanation, min_eps, max_eps, suggestion_value, resolution


def calculate_eps_max(distance_matrix, min_samples):
    k = min_samples
    distances = np.empty(len(distance_matrix), dtype=float)
    for i in range(len(distance_matrix)):
        d = distance_matrix[i, :]
        sorted = np.sort(d)
        distances[i] = sorted[k + 1]
    max_eps = max(distances)
    return float(max_eps)


# def dbscan_algorithm_config():
#     # enum
#     name = ALGORITHM  # TODO
#     explanation = ""  # TODO
#     options = np.array([['auto', ""],
#                         ['brute', ""],
#                         ['kd_tree', ""],
#                         ['ball_tree', ""]])  # TODO
#     suggestions = ['auto']  # TODO
#     deactivatable = False
#     return name, explanation, options, suggestions, deactivatable


def dbscan_leaf_size_config():
    # only activated if algorithm='ball_tree' or 'kd_tree'
    # int slider
    name = LEAF_SIZE  # TODO
    explanation = ""  # TODO
    mini = 0  # TODO
    maxi = 100  # TODO
    default = 30
    resolution = 1
    deactivatable = False
    return name, explanation, mini, maxi, default, resolution, deactivatable


def dbscan_n_jobs_config():
    # int slider
    name = N_JOBS  # TODO
    explanation = ""  # TODO
    mini = 0  # TODO
    maxi = 2  # TODO
    default = 1  # TODO
    resolution = 1  # TODO
    deactivatable = True  # TODO
    return name, explanation, mini, maxi, default, resolution, deactivatable


if __name__ == '__main__':
    v = [1, 1, 1, 3, 4, 5, 10, 100, 3]
    c = dbscan(lambda a, b: abs(a - b), v, eps=0.1, min_samples=2)
    # print(c)
    print(fancy_cluster_representation(v, c))
