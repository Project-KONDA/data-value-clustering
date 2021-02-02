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
    return dbscan.dbscan_min_samples_config(no_values, answers)


def optics_max_eps_config():
    # default value of np.inf will identify clusters across all scales
    # reducing max_eps will result in shorter run times

    # see DBSCAN

    pass

def optics_cluster_method_config():
    pass


def optics_eps_config():
    pass


def optics_xi_config():
    pass


def optics_predecessor_correction_config():
    pass


def optics_min_cluster_size_config():
    pass


def optics_algorithm_config():
    pass


def optics_leaf_size_config():
    pass


def optics_n_jobs_config():
    pass


if __name__ == '__main__':
    v = [1, 1, 1, 3, 4, 5, 10, 100, 3]
    c = optics(lambda a, b: abs(a - b), v, min_samples=2)
    # print(c)
    print(fancy_cluster_representation(v, c))