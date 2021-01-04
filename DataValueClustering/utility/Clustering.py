import numpy as np


def cluster(values, compression_function, distance_function, cluster_function):
    compressed_values = compression_function(values)  # may include removing duplicates
    clusters_compressed = cluster_function(distance_function, compressed_values)  # returns one dimensional array

    clusters = get_clusters_original_values(clusters_compressed, compressed_values, compression_function, values)

    # TODO: return fancy result


def get_clusters_original_values(clusters, compressed_values, compression_function, values):
    size = len(values)
    clusters_original_values = np.zeros(size, int)
    for x in range(size):
        i = compressed_values.index(compression_function([values[x]]))
        clusters_original_values[x] = clusters[i]
    assert max(clusters_original_values) == max(clusters)
    return clusters_original_values



