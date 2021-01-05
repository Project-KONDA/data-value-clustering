from sklearn.cluster import DBSCAN

from gui.clustering import fancy_cluster_representation
from utility.distance_matrix import calculate_distance_matrix


def dbscan(distance_function, values, eps=0.5, min_samples=5, algorithm='auto', leaf_size=30, p=None, n_jobs=None):
    dm = calculate_distance_matrix(distance_function, values)
    clusters = DBSCAN(eps=eps, min_samples=min_samples, metric='precomputed', algorithm=algorithm, leaf_size=leaf_size, p=p, n_jobs=n_jobs).fit_predict(dm)
    return clusters


if __name__ == '__main__':
    v = [1, 1, 1, 3, 4, 5, 10, 100, 3]
    c = dbscan(lambda a, b: abs(a - b), v, eps=0.1, min_samples=2)
    # print(c)
    print(fancy_cluster_representation(v, c))
