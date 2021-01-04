from sklearn.cluster import AffinityPropagation
from Util.DistanceMatrixHandling import negate


def affinity_propagation_clustering(original_values, compressed_values, unique_values, distance_matrix, cluster_original_values):
    affinity_matrix = negate(distance_matrix)
    clusters = AffinityPropagation(affinity='precomputed').fit_predict(affinity_matrix)
    # TODO: set damping, max_iter, convergence_iter, copy, preference, verbose
    return clusters
