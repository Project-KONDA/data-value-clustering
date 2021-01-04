from cluster_algorithms.dendrogram import cluster_dendrogram_centroid, cluster_dendrogram_linkage
from compression.compressions import compression_simple, compress_array, compression_typed
from compression.thin import super_thin_array_amounts
from distance_functions.weighted_levenshtein_distance2 import get_cost_map, levenshtein_distance2
from tests.testdata import data_test
from distance_functions.weighted_levenshtein_distance import levenshtein_distance

# () -> array of values
data = [
    data_test[0:100]
]

# (array of values) -> array of values
compressions = [
    lambda vals: vals,
    lambda vals: compress_array(compression_simple, vals),
    lambda vals: compress_array(compression_typed, vals),
    lambda vals: super_thin_array_amounts(vals)[:, 1]
]


# (value, value) -> number
distances = [
    levenshtein_distance,
    lambda s1, s2: levenshtein_distance2(get_cost_map(), s1, s2)
]

# (distance-function, values) -> dentrogram
clusters = [
    cluster_dendrogram_linkage,
    cluster_dendrogram_centroid
]


def buildclusters(da, co, di, cl):
    compressed_data = compressions[co](data[da])
    clusters[cl] (distances[di], compressed_data)


if __name__ == '__main__':
    i_data = 0
    i_comp = 0
    i_dist = 1
    i_clus = 0

    print(compressions[i_comp](data[i_data]))

    buildclusters(i_data, i_comp, i_dist, i_clus)
