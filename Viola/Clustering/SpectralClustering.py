from sklearn.cluster import SpectralClustering
from Util.DistanceMatrixHandling import negate


def spectral_clustering(original_values, compressed_values, unique_values, distance_matrix, cluster_original_values):
    affinity_matrix = negate(distance_matrix)
    clusters = SpectralClustering(affinity='precomputed').fit_predict(affinity_matrix)
    # TODO: set n_clusters, eigen_solver, n_components, n_init, gamma, eigen_tol, assign_labels, verbose
    return clusters
