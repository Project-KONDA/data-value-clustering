'''calculation of the calinsky harabasz index including helper functions'''
import numpy as np


from validation.intra_inter_cluster_distance import filter_distance_matrix


def get_medoid_index(cluster_distance_matrix):
    index, dist = -1, np.inf
    for i, line in enumerate(cluster_distance_matrix):
        s = np.sum(line)
        if dist > s:
            index, dist = i, s
    return index


def get_cluster_medoid_squared_distance(cluster, clusters, distance_matrix):
    cluster_distance_matrix = filter_distance_matrix(cluster, cluster, clusters, distance_matrix)
    index = get_medoid_index(cluster_distance_matrix)

    distances = cluster_distance_matrix[index, :]

    sum = 0
    for i, value in enumerate(distances):
        sum += value * value
    return sum


def get_total_medoid_squared_distance(distance_matrix):
    index = get_medoid_index(distance_matrix)
    distances = distance_matrix[index]
    sum = 0
    for i, value in enumerate(distances):
        sum += value * value
    return sum


def total_within_sum_of_squares(clusters, distance_matrix):
    sum = 0
    clusterset = set(clusters)
    for i, k in enumerate(clusterset):
        sum += get_cluster_medoid_squared_distance(k, clusters, distance_matrix)
    return sum


def calinski_harabasz_index(clusters, distance_matrix):
    n = len(clusters)
    k = len(set(clusters))

    SSw = total_within_sum_of_squares(clusters, distance_matrix)
    SSb = get_total_medoid_squared_distance(distance_matrix) - SSw

    return (n-k) * SSb / ((k-1) * SSw)


def wb_index(clusters, distance_matrix):
    n = len(clusters)
    k = len(set(clusters))

    SSw = total_within_sum_of_squares(clusters, distance_matrix)
    SSb = get_total_medoid_squared_distance(distance_matrix) - SSw

    return k * SSw / SSb
