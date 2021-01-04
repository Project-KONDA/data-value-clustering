import numpy as np
from scipy.cluster.hierarchy import dendrogram, linkage
from matplotlib import pyplot as plt
from sklearn.cluster import AgglomerativeClustering

import main
from compression.thin import super_thin_array_amounts, thin_array
from distance_functions.distance_matrix import calculate_distance_matrix
from distance_functions.weighted_levenshtein_distance import levenshtein_distance
from tests.testdata import data_test


def show_dendrogram(flattened_values, original_values):
    matrix = calculate_distance_matrix(flattened_values)
    # print(matrix)
    plot_matrix(matrix)
    linked = linkage(matrix)  # perform hierarchical clustering
    size = len(original_values)
    label_list = [""] * size
    for x in range(size):
        label_list[x] = original_values[x] + ' (' + flattened_values[x] + ')'

    plt.figure(figsize=(10, 7))
    dendrogram(linked,
               orientation='top',
               labels=label_list,
               distance_sort='descending',
               show_leaf_counts=True)
    plt.show()


def plot_matrix(matrix):
    plt.imshow(matrix)
    plt.colorbar()
    plt.show()


def cluster(values, n):
    matrix = calculate_distance_matrix(levenshtein_distance, values)
    clustering = AgglomerativeClustering(n_clusters=n, affinity='precomputed',
                                         linkage='single')  # alternativ zu n_clusters: distance_threshold
    clustering.fit_predict(matrix)
    return clustering


def cluster_result_matrix(clustering, values):
    size_x = clustering.n_clusters
    size_y = len(clustering.labels_)
    result = np.array([[""] * size_y for i in range(size_x)], dtype=object)
    counter = [0] * size_x
    for x in range(size_y):
        cluster_no = int(clustering.labels_[x])
        result[cluster_no, counter[cluster_no]] = values[x]
        counter[cluster_no] += 1
    return result


if __name__ == '__main__':
    # vals = thin_array(data_test[0:10000])
    values = super_thin_array_amounts(data_test[0:100000])
    # print(values)

    vals = values[:, 1]
    # print(vals)
    # show_dendrogram(vals, vals)
    cluster = cluster(vals, 10)
    matrix = cluster_result_matrix(cluster, vals)
    print(set(matrix[0]))
