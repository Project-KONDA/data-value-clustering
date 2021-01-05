import numpy as np


def cluster(values, compression_function, distance_function, cluster_function):
    values_compressed = compression_function(values)  # may include removing duplicates
    clusters_compressed = cluster_function(distance_function, values_compressed)  # returns one dimensional array
    clusters = get_clusters_original_values(clusters_compressed, values_compressed, compression_function, values)
    return fancy_cluster_representation(values, clusters)

    # TODO: return fancy result


def get_clusters_original_values(clusters, compressed_values, compression_function, values):
    size = len(values)
    clusters_original_values = np.zeros(size, int)
    for x in range(size):
        i = compressed_values.index(compression_function([values[x]]))
        clusters_original_values[x] = clusters[i]
    assert max(clusters_original_values) == max(clusters)
    return clusters_original_values


def fancy_cluster_representation(values, clusters):
    no_clusters = max(clusters) + 1
    outer_list = list()
    for i in range(no_clusters):
        outer_list.append(list())
    for j in range(len(values)):
        outer_list[int(clusters[j])].append(values[j])
    return outer_list

