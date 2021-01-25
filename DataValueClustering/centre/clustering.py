import numpy as np


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


