import numpy as np


def cluster(values, compression_function, distance_function, cluster_function):
    values_compressed = compression_function(values)  # may include removing duplicates
    clusters_compressed = cluster_function(distance_function, values_compressed)  # returns one dimensional array
    clusters = get_clusters_original_values(clusters_compressed, values_compressed, compression_function, values)
    return fancy_cluster_representation(values, clusters)


def get_clusters_original_values(clusters_compressed, values_compressed, compression_function, values):
    size = len(values)
    clusters_original_values = np.zeros(size, int)
    for k in range(size):
        compression_result = compression_function([values[k]])
        assert len(compression_result) == 1
        index = values_compressed.index(compression_result[0])
        clusters_original_values[k] = clusters_compressed[index]
    assert max(clusters_original_values) == max(clusters_compressed)
    return clusters_original_values  # one dimensional array


def fancy_cluster_representation(values, clusters):
    no_clusters = max(clusters) + 1
    outer_list = list()
    noise = list()

    for i in range(no_clusters):
        outer_list.append(list())

    for j in range(len(values)):
        x = int(clusters[j])
        if x >=0:
            outer_list[x].append(values[j])
        else:
            noise.append(values[j])

    return outer_list, noise

