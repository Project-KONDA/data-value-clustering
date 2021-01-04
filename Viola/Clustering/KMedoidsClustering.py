from sklearn_extra.cluster import KMedoids
from Clustering.Clustering import use_unique_values_as_clusters


def kmedoids_clustering_args(n_clusters):
    return lambda original_values, compressed_values, unique_values, distance_matrix, cluster_original_values:\
        kmedoids_clustering(original_values, compressed_values, unique_values, n_clusters, distance_matrix, cluster_original_values)


def kmedoids_clustering(original_values, compressed_values, unique_values, n_clusters, distance_matrix,
                        cluster_original_values):
    if not (n_clusters is None) and len(unique_values) <= n_clusters:
        return use_unique_values_as_clusters(cluster_original_values, compressed_values, unique_values)[0]
    else:
        return perform_kmedoids_clustering(n_clusters, distance_matrix)


def perform_kmedoids_clustering(n_clusters, distance_matrix):
    assert not (n_clusters is None)
    clusters = KMedoids(n_clusters, 'precomputed').fit_predict(distance_matrix)
    # TODO: set initialization method via init
    # init : {‘random’, ‘heuristic’, ‘k-medoids++’, ‘build’}, optional, default: ‘build’
    return clusters


# def build_distance_metric(values, distance_matrix):
#     index_map = value_index_map(values)
#     print(index_map)
#     return lambda a, b: distance_metric(index_map, distance_matrix, a, b)
#
#
# def distance_metric(index_map, distance_matrix, a, b):
#     k = index_map[a]
#     l = index_map[b]
#     if l < k:
#         return distance_matrix[l, k]
#     else:
#         return distance_matrix[k, l]
#
#
# def value_index_map(values):
#     index_map = {}
#     for i in range(len(values)):
#         index_map[values[i]] = i
#     return index_map
