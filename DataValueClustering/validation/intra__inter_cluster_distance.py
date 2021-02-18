import numpy as np


def filter_distance_matrix(cluster1, cluster2, clusters, distance_matrix):
    # cluster : int
    # clusters = [4 0 3 5 ...]
    lines = np.where(clusters == cluster1)[0]
    columns = np.where(clusters == cluster2)[0]
    return distance_matrix[lines, columns]


def max_intra_cluster_distance(cluster, clusters, distance_matrix):
    filtered_distance_matrix = filter_distance_matrix(cluster, cluster, clusters, distance_matrix)
    return np.amax(filtered_distance_matrix)


def min_inter_cluster_distance(cluster1, cluster2, clusters, distance_matrix):
    filtered_distance_matrix = filter_distance_matrix(cluster1, cluster2, clusters, distance_matrix)
    return np.amin(filtered_distance_matrix)


def max_intra_cluster_distances(clusters, distance_matrix):
    clusters_unique = np.array(list(set(clusters)))
    clusters_unique_sorted = np.sort(clusters_unique)
    distances = np.full(len(clusters_unique_sorted), 0.0)
    for i in clusters_unique_sorted:
        distances[i] = max_intra_cluster_distance(i, clusters, distance_matrix)
    return distances


def max_inter_cluster_distances(clusters, distance_matrix):
    clusters_unique = np.array(list(set(clusters)))
    clusters_unique_sorted = np.sort(clusters_unique)
    n = len(clusters_unique_sorted)
    distances = np.full((n, n), 0.0)
    for i in clusters_unique_sorted:
        for j in clusters_unique_sorted:
            if i != j:
                distances[i, j] = min_inter_cluster_distance(i, j, clusters, distance_matrix)
    return distances


if __name__ == "__main__":
    # c1 = 0
    # c2 = 1
    clusters = np.array([1, 1, 0])
    dm = np.array([
        [1,2,3],
        [2,5,6],
        [3,6,9],
    ])
    # print(filter_distance_matrix(c1, c2, clusters, dm))
    # print(max_intra_cluster_distances(clusters, dm))
    print(max_inter_cluster_distances(clusters, dm))