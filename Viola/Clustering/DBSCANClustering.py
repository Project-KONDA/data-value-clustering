from sklearn.cluster import DBSCAN
from Util.ClusterHandling import increase_by_one


def dbscan_clustering(original_values, compressed_values, unique_values, distance_matrix, cluster_original_values):
    clusters = DBSCAN(eps=0.1, min_samples=4, metric='precomputed').fit_predict(distance_matrix)
    # TODO: set eps, min_samples, algorithm, leaf_size, p, n_jobs
    return clusters
