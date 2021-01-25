import numpy as np

from centre.cluster_representation import fancy_cluster_representation


def cluster(values, compression_function, distance_function, cluster_function):
    values_compressed, compression_dict = compression_function(values)  # may include removing duplicates
    print(len(values_compressed))
    clusters_compressed = cluster_function(distance_function, values_compressed)  # returns one dimensional array
    clusters = get_clusters_original_values(clusters_compressed, values_compressed, compression_function, values)
    return fancy_cluster_representation(values, clusters)


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


