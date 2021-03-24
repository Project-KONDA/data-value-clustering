import numpy as np


def filter_distance_matrix(cluster1, cluster2, clusters, distance_matrix):
    lines = np.where(clusters == cluster1)[0]
    columns = np.where(clusters == cluster2)[0]

    distance_matrix_lines = distance_matrix[lines, :]
    return distance_matrix_lines[:, columns]


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


def min_inter_cluster_distances(clusters, distance_matrix):
    clusters_unique = np.array(list(set(clusters)))
    clusters_unique_sorted = np.sort(clusters_unique)
    n = len(clusters_unique_sorted)
    distances = np.full((n, n), 0.0)
    for i in clusters_unique_sorted:
        for j in clusters_unique_sorted:
            if i != j:
                distances[i, j] = min_inter_cluster_distance(i, j, clusters, distance_matrix)
    return distances


def min_of_min_inter_cluster_distances(clusters, distance_matrix):
    matrix = min_inter_cluster_distances(clusters, distance_matrix)
    m = len(matrix)
    mini = np.inf
    for i in range(m):
        # for j in range(m):
        # if i != j:
        for j in range(i+1, m):
            mini = min(matrix[i, j], mini)
    return mini


def average_intra_cluster_distance_per_value(cluster, clusters, distance_matrix):
    filtered_distance_matrix = filter_distance_matrix(cluster, cluster, clusters, distance_matrix)
    length = len(filtered_distance_matrix)
    distances = np.full(length, 0.0)
    for i in range(length):
        no_other_values = len(filtered_distance_matrix[i, :]) - 1
        if no_other_values > 0:
            distances[i] = (sum(filtered_distance_matrix[i,:]) - filtered_distance_matrix[i,i]) / no_other_values
        else:
            distances[i] = 0.0
    return distances


def average_intra_cluster_distances_per_cluster_per_value(clusters, distance_matrix):
    clusters_unique = np.array(list(set(clusters)))
    clusters_unique_sorted = np.sort(clusters_unique)
    distances_per_cluster = []
    for i in clusters_unique_sorted:
        distances_per_cluster.append(average_intra_cluster_distance_per_value(i, clusters, distance_matrix).tolist())
    return distances_per_cluster

if __name__ == "__main__":
    # c1 = 0
    # c2 = 1
    clusters = np.array([1, 1, 0])
    dm = np.array([
        [1, 2, 3],
        [2, 5, 6],
        [3, 6, 9],
    ])
    # print(filter_distance_matrix(c1, c2, clusters, dm))
    # print(max_intra_cluster_distances(clusters, dm))
    # print(min_inter_cluster_distances(clusters, dm))
    print(average_intra_cluster_distances_per_cluster_per_value(clusters, dm))