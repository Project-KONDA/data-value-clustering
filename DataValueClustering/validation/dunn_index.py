import numpy as np
from validation.intra_inter_cluster_distance import max_intra_cluster_distances, \
    min_of_min_inter_cluster_distances


def dunn_index(clusters, distance_matrix):
    min_inter = min_of_min_inter_cluster_distances(clusters, distance_matrix)
    max_intra = np.amax(max_intra_cluster_distances(clusters, distance_matrix))
    return min_inter/max_intra
