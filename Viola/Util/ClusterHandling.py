import numpy as np
from Compression.Compression import compressed_value_index_map


def map_compressed_values_to_unique_clusters(compressed_values, unique_values, clusters_unique_values):
    size = len(compressed_values)
    clusters_compressed_values = np.zeros(size, int)
    index_map = compressed_value_index_map(unique_values)
    for x in range(size):
        i = index_map[compressed_values[x]]
        clusters_compressed_values[x] = clusters_unique_values[i]
    assert max(clusters_compressed_values) == max(clusters_unique_values)
    return clusters_compressed_values


def build_cluster_matrix(clusters, values):
    size_x = max(clusters) + 1  # number of clusters
    size_y = len(clusters)  # overall number of values
    cluster_matrix = np.array([[""] * size_y for i in range(size_x)], dtype=object)  # array containing empty strings
    empty_column = [0] * size_x  # first empty empty_column per cluster
    for x in range(size_y):
        cluster_no = int(clusters[x])  # cluster that the current value is assigned to (between 0 and n_clusters)
        cluster_matrix[cluster_no, empty_column[cluster_no]] = values[
            x]  # write current value in row representing cluster
        empty_column[cluster_no] += 1
    return cluster_matrix


def build_cluster_matrix_zero(clustering, n_clusters, values):
    size_x = n_clusters  # number of clusters
    size_y = len(clustering)  # overall number of values
    cluster_matrix = np.array([[""] * size_y for i in range(size_x)], dtype=object)  # array containing empty strings
    empty_column = [0] * size_x  # first empty empty_column per cluster
    for x in range(size_y):
        cluster_no = int(clustering[x])  # cluster that the current value is assigned to (between 0 and n_clusters-1)
        cluster_matrix[cluster_no, empty_column[cluster_no]] = values[
            x]  # write current value in row representing cluster
        empty_column[cluster_no] += 1
    return cluster_matrix


def increase_by_one(clusters):
    for i in range(len(clusters)):
        clusters[i] = clusters[i] + 1
    return clusters


def decrease_by_one(clusters):
    for i in range(len(clusters)):
        clusters[i] = clusters[i] - 1
    return clusters