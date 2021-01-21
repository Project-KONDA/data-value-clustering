import time

from sklearn.manifold import MDS
import numpy as np

from clustering.clustering import cluster
from clustering_algorithms.affinity_propagation import affinity
from clustering_algorithms.dbscan import dbscan
from clustering_algorithms.hierarchical import hierarchical_lm, generate_linkage_matrix
from clustering_algorithms.kmedoids import kmedoids
from clustering_algorithms.optics import optics
from clustering_algorithms.spectral import spectral
from compression.compression import char_compression_function, sequence_compression_function, \
    sequence_compression_case_sensitive_function
from distance.weighted_levenshtein_distance import get_cost_map, weighted_levenshtein_distance
from gui.cluster_algorithms_gui import cluster_hierarchical, cluster_dbscan, cluster_kmedoids, cluster_optics, \
    cluster_affinity, cluster_spectral
from gui.dendrogram import show_dendrogram
from utility.distance_matrix import calculate_distance_matrix, plot_image, min_distance, max_distance, avg_distance, \
    plot_at_y, plot_histogram, plot_box
from utility.read_file import read_data_values_from_file
from matplotlib import pyplot as plt, cm

midas_dates = "../experiment_data/midas_dates.txt"
midas_artist_names = "../experiment_data/midas_artist_names.txt"
midas_measurements = "../experiment_data/midas_measurement.txt"


def run_clustering(file_path, data_limit, compression_f, distance_f, cluster_f):
    data = read_data_values_from_file(file_path)[0:data_limit]
    # print(data)

    start = time.time()
    cluster_list, noise = cluster(data, compression_f, distance_f, cluster_f)
    end = time.time()
    print("Runtime = " + str(end - start))

    print("Clusters = ")
    for i in range(len(cluster_list)):
        print("\t" + str(cluster_list[i]))
    print("]")
    print("Noise = " + str(noise))
    print("Number of clusters = " + str(len(cluster_list)))


def distance_weighted_levenshtein():
    weight_case = 1
    regex = ["", "[a-zäöüßáàéèíìóòúù]", "[A-ZÄÖÜÁÀÉÈÍÌÓÒÚÙ]", "[0-9]", " ", "[^a-zäöüßáàéèíìóòúùA-ZÄÖÜÁÀÉÈÍÌÓÒÚÙ0-9 ]"]
    weights_dates = [
        [0, 2, 2, 1, 3, 3],
        [2, 0, 1, 3, 3, 3],
        [2, 1, 0, 3, 3, 3],
        [1, 3, 3, 0, 3, 3],
        [3, 3, 3, 3, 0, 3],
        [3, 3, 3, 3, 3, 3]
    ]
    weights_measurements = [
        [0, 3, 3, 2, 3, 4],
        [3, 0, 1, 4, 3, 4],
        [3, 1, 0, 4, 3, 4],
        [2, 4, 4, 0, 3, 4],
        [3, 3, 3, 3, 0, 3],
        [4, 4, 4, 4, 3, 4]
    ]
    weights_artist_names = [
        [0, 1, 2, 4, 3, 3],
        [1, 0, 1, 4, 3, 3],
        [2, 1, 0, 4, 3, 3],
        [4, 4, 4, 0, 3, 3],
        [3, 3, 3, 3, 0, 3],
        [3, 3, 3, 3, 3, 3]
    ]

    cost_map = get_cost_map(regex, weights_dates, weight_case)

    return lambda s1, s2: weighted_levenshtein_distance(cost_map, s1, s2)


if __name__ == '__main__':
    run_clustering(midas_dates, 1000, sequence_compression_case_sensitive_function, distance_weighted_levenshtein(), cluster_affinity())
