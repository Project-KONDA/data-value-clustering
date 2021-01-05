import numpy as np
from sklearn.cluster import OPTICS

from gui.clustering import fancy_cluster_representation
from utility.distance_matrix import calculate_distance_matrix


def optics(distance_function, values,
           min_samples=5, max_eps=np.inf, cluster_method='xi', eps=None,
           xi=0.05, predecessor_correction=True, min_cluster_size=None, algorithm='auto', leaf_size=30, n_jobs=None):
    dm = calculate_distance_matrix(distance_function, values)
    clusters = OPTICS(
        min_samples=min_samples, metric='precomputed', max_eps=max_eps, cluster_method=cluster_method, eps=eps,
        xi=xi, predecessor_correction=predecessor_correction, min_cluster_size=min_cluster_size, algorithm=algorithm,
        leaf_size=leaf_size, n_jobs=n_jobs).fit_predict(dm)
    return clusters


if __name__ == '__main__':
    v = [1, 1, 1, 3, 4, 5, 10, 100, 3]
    c = optics(lambda a, b: abs(a - b), v, min_samples=2)
    # print(c)
    print(fancy_cluster_representation(v, c))
