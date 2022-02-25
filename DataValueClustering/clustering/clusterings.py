'''Handle clusterings created by clustering algorithm.'''
import numpy as np

from clustering.affinity_propagation_clustering import affinity_args
from clustering.dbscan_clustering import dbscan_args
from clustering.hierarchical_clustering import hierarchical_args
from clustering.kmedoids_clustering import kmedoids_args
from clustering.optics_clustering import optics_args
from clustering.spectral_clustering import spectral_args


def get_clusters_original_values(clusters_compressed, values_compressed, compression_function, values):
    size = len(values)
    clusters_original_values = np.zeros(size, int)
    for k in range(size):
        compression_result, compression_dict = compression_function([values[k]])
        assert len(compression_result) == 1
        index = np.where(values_compressed == compression_result[0])[0][0]
        clusters_original_values[k] = clusters_compressed[index]
    assert max(clusters_original_values) == max(clusters_compressed)
    return clusters_original_values  # one dimensional array


def get_cluster_sizes(clusters):
    unique, counts = np.unique(clusters, return_counts=True)
    noise_size = 0
    cluster_sizes = counts
    if -1 in unique:
        noise_size = counts[0]
        cluster_sizes = counts[1:]
    return cluster_sizes.tolist(), int(noise_size)


clustering_args_functions = {
    "hierarchical": hierarchical_args,
    "kmedoids": kmedoids_args,
    "dbscan": dbscan_args,
    "optics": optics_args,
    "affinity": affinity_args,
    "spectral": spectral_args
}

