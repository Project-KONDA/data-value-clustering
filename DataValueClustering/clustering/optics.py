import numpy as np
from sklearn.cluster import OPTICS

from gui_center.cluster_representation import fancy_cluster_representation
from clustering import dbscan
from distance.distance_matrix import calculate_distance_matrix


def optics(distance_matrix, values,
           min_samples=5, max_eps=np.inf, cluster_method='xi', eps=None,
           xi=0.05, predecessor_correction=True, min_cluster_size=None, algorithm='auto', leaf_size=30, n_jobs=None):
    clusters = OPTICS(
        min_samples=min_samples, metric='precomputed', max_eps=max_eps, cluster_method=cluster_method, eps=eps,
        xi=xi, predecessor_correction=predecessor_correction, min_cluster_size=min_cluster_size, algorithm=algorithm,
        leaf_size=leaf_size, n_jobs=n_jobs).fit_predict(distance_matrix)
    return clusters


def optics_min_samples_config(no_values, answers):
    # int
    return dbscan.dbscan_min_samples_config(no_values, answers)


def optics_max_eps_config():
    # float or inf
    # "default value of np.inf will identify clusters across all scales"
    # "reducing max_eps will result in shorter run times"

    # see DBSCAN
    # return ??
    pass

def optics_cluster_method_config():
    # enum
    # return name, explanation, options, suggestion_values
    pass


def optics_eps_config():
    # float
    # Used only when cluster_method='dbscan'
    resolution = 0.01
    deactivatable = True
    # return name, explanation, min_eps, max_eps, suggestion_value, resolution, deactivatable
    pass


def optics_xi_config():
    # float
    # Used only when cluster_method='xi'
    deactivatable = True
    # return name, explanation, min_eps, max_eps, suggestion_value, resolution, deactivatable
    pass


def optics_predecessor_correction_config():
    # bool
    # This parameter has minimal effect on most datasets. Used only when cluster_method='xi'.
    # return name, explanation, default
    pass


def optics_min_cluster_size_config():
    # int
    # Used only when cluster_method='xi'.
    # return name, explanation, min_min_samples, max_min_samples, suggestion_value
    pass


def optics_algorithm_config():
    # enum
    return dbscan.dbscan_algorithm_config()


def optics_leaf_size_config():
    # int
    return dbscan.dbscan_leaf_size_config()


def optics_n_jobs_config():
    # int
    return dbscan.dbscan_n_jobs_config()


if __name__ == '__main__':
    v = [1, 1, 1, 3, 4, 5, 10, 100, 3]
    c = optics(lambda a, b: abs(a - b), v, min_samples=2)
    # print(c)
    print(fancy_cluster_representation(v, c))