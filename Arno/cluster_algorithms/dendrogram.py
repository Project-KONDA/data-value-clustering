import numpy as np
from scipy.cluster.hierarchy import linkage, dendrogram, centroid, fcluster
from matplotlib import pyplot as plt

from distance_functions.distance_matrix import calculate_distance_matrix, calculate_condensed_distance_matrix, \
    calculate_condensed_distance_matrix2


def form_flat_clusters(linkage_matrix, n_clusters, distance_threshold):
    if not (n_clusters is None):
        return fcluster(linkage_matrix, n_clusters, 'maxclust')
    elif not (distance_threshold is None):
        return fcluster(linkage_matrix, distance_threshold, 'distance')
    # criteria: 'maxclust', 'distance', 'inconsistent', 'monocrit', 'maxclust_monocrit'


def show_dendrogram(clusters, labelList=[]):
    plt.figure(figsize=(10, 7))
    if not labelList:
        dendrogram(clusters,
                   orientation='right',
                   # labels=labelList,
                   distance_sort='descending',
                   show_leaf_counts=True)

    else:
        dendrogram(clusters,
                   orientation='right',
                   labels=labelList,
                   distance_sort='descending',
                   show_leaf_counts=True)
    print("showing dendrogram ...")
    plt.show()


def cluster_dendrogram(cluster_function, distance_function, value_list):
    matrix = np.zeros(0)
    cluster = np.zeros(0)
    matrix = calculate_condensed_distance_matrix2(distance_function, value_list)
    #matrix = calculate_distance_matrix(distance_function, value_list)
    cluster = cluster_function(matrix)
    show_dendrogram(cluster)


def cluster_dendrogram_linkage(distance_function, value_list):
    cluster_dendrogram(linkage, distance_function, value_list)


def cluster_dendrogram_centroid(distance_function, value_list):
    cluster_dendrogram(centroid, distance_function, value_list)
