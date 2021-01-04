from sklearn.cluster import OPTICS
from Util.ClusterHandling import increase_by_one


def optics_clustering(original_values, compressed_values, unique_values, distance_matrix, cluster_original_values):
    clusters = OPTICS(min_samples=2, metric='precomputed').fit_predict(distance_matrix)
    # TODO: set min_samples, max_eps, cluster_method, eps, xi, predecessor_correction, min_cluster_size, algorithm,
    #  leaf_size, n_jobs
    return clusters
