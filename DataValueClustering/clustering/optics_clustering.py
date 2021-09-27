'''Apply OPTICS clustering algorithm.'''
import numpy as np
from sklearn.cluster import OPTICS

from clustering.dbscan_clustering import calculate_eps_max
from gui_center.cluster_representation import fancy_cluster_representation
from clustering import dbscan_clustering
from distance.distance_matrix import calculate_distance_matrix

MIN_CLUSTER_SIZE = "min_cluster_size"
PREDECESSOR_CORRECTION = "predecessor_correction"
XI = "xi"
EPS = "eps"
CLUSTER_METHOD = "cluster_method"
MAX_EPS = "max_eps"


def optics(distance_matrix, values,
           min_samples=5, max_eps=np.inf, cluster_method='xi', eps=None,
           xi=0.05, predecessor_correction=True, min_cluster_size=None, n_jobs=None):
    clusters = OPTICS(
        min_samples=min_samples, metric='precomputed', max_eps=max_eps, cluster_method=cluster_method, eps=eps,
        xi=xi, predecessor_correction=predecessor_correction, min_cluster_size=min_cluster_size,
        n_jobs=n_jobs).fit_predict(distance_matrix)
    return clusters


def optics_args(min_samples, max_eps, cluster_method, eps, xi, predecessor_correction, min_cluster_size,
                          n_jobs):
    return lambda distance_matrix_map, values: optics(distance_matrix_map["distance_matrix"], values, min_samples, max_eps, cluster_method,
                          eps, xi, predecessor_correction, min_cluster_size, n_jobs)


def optics_min_samples_config(no_values):
    # int
    return dbscan_clustering.dbscan_min_samples_config(no_values)


def optics_max_eps_config(distance_matrix, min_distance, no_values):
    # float or inf
    # expert
    # "default value of np.inf will identify clusters across all scales"
    # "reducing max_eps will result in shorter run times"
    # TODO: does optics correspond to dbscan if max_eps is not np.inf?

    # see DBSCAN
    name = MAX_EPS
    explanation = "If deactivated, clusters across all scales will be identified. Reducing max_eps will result in shorter run times." \
                  "Lower values will result in more clusters but shorter run times."
    max_eps = calculate_eps_max(distance_matrix, max(1, min(3, no_values)))  # default min_samples, updated dynamically
    min_eps = max(min_distance, 0.01)
    suggestion_value = min_eps
    resolution = 0.01
    deactivatable = True  # handles infinity
    return name, explanation, min_eps, max_eps, suggestion_value, resolution, deactivatable


# def optics_cluster_method_config():
#     # enum
#     name = CLUSTER_METHOD
#     explanation = "Method for cluster extraction."
#     options = np.array([["dbscan", "Extraction method similar to DBSCAN."],
#                         ["xi", "Extraction method proposed by Ankerst et al. 1999: "
#                                "'OPTICS: ordering points to identify the clustering structure."]])
#     suggestions = ["xi"]
#     deactivatable = False
#     return name, explanation, options, suggestions, deactivatable


# def optics_eps_config(distance_matrix):
#     # float
#     # Used only when cluster_method='dbscan'
#     name = EPS
#     explanation = "Similar to max_eps defines maximum distance for data points to be considered as neighbour."
#     mini = float(distance_matrix.min())
#     maxi = (float(distance_matrix.max())-mini)/2 + mini
#     default = maxi  # default same value as max_eps
#     resolution = 0.01
#     deactivatable = False
#     return name, explanation, mini, maxi, default, resolution, deactivatable


def optics_xi_config():
    # float
    # Used only when cluster_method='xi'
    # expert
    name = XI
    explanation = "Determines the minimum steepness on the reachability plot that constitutes a cluster boundary."
    mini = 0.
    maxi = 1.
    default = 0.05
    resolution = 0.01
    deactivatable = False
    return name, explanation, mini, maxi, default, resolution, deactivatable


def optics_predecessor_correction_config():
    # bool
    # expert
    # This parameter has minimal effect on most datasets.
    # Used only when cluster_method='xi'.
    name = PREDECESSOR_CORRECTION
    explanation = "Correct clusters according to the predecessors calculated. This parameter has minimal effect on most datasets."
    default = True
    deactivatable = False
    return name, explanation, default, deactivatable


def optics_min_cluster_size_config(no_values):
    # int
    # expert
    # Used only when cluster_method='xi'.
    # If None, the value of min_samples is used instead
    name = MIN_CLUSTER_SIZE
    explanation = "Minimum number of samples in an OPTICS cluster. If deactivated, the value of " + dbscan_clustering.MIN_SAMPLES + " is used instead."
    mini = 2
    maxi = no_values-1
    default = 10 if no_values >= 50 else round(no_values*0.1)
    resolution = 1
    deactivatable = True
    return name, explanation, mini, maxi, default, resolution, deactivatable


# def optics_algorithm_config():
#     # enum
#     return dbscan_clustering.dbscan_algorithm_config()


# def optics_leaf_size_config():
#     # int
#     return dbscan_clustering.dbscan_leaf_size_config()
#
#
# def optics_n_jobs_config():
#     # int
#     return dbscan_clustering.dbscan_n_jobs_config()


if __name__ == '__main__':
    v = [1, 1, 1, 3, 4, 5, 10, 100, 3]
    c = optics(lambda a, b: abs(a - b), v, min_samples=2)
    # print(c)
    print(fancy_cluster_representation(v, c))
