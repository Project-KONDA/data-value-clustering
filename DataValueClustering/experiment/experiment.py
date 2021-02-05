import time
import numpy as np

from clustering.affinity_propagation_clustering import affinity_args
from clustering.dbscan_clustering import dbscan_args
from clustering.hierarchical_clustering import hierarchical_args
from clustering.kmedoids_clustering import kmedoids_args
from clustering.optics_clustering import optics_args
from clustering.spectral_clustering import spectral_args
from gui_center.main import Main
from compression.compression import sequence_compression_case_sensitive_function, word_sequence_compression_function
from distance.weighted_levenshtein_distance import get_cost_map, weighted_levenshtein_distance
from data_extraction.read_file import read_data_values_from_file

midas_dates = "../data/midas_dates.txt"
midas_artist_names = "../data/midas_artist_names.txt"
midas_measurements = "../data/midas_measurement.txt"

lido_titles = "../data/lido_titles.txt"
lido_attribution_qualifier = "../data/lido_attribution_qualifier.txt"
lido_measurement_unit = "../data/lido_measurement_unit.txt"


def run_clustering(file_path, data_limit, compression_f, distance_f, cluster_f):
    data = read_data_values_from_file(file_path)[0:data_limit]
    # print(data)

    start = time.time()
    main = Main(data=data, compression_f=compression_f, distance_f=distance_f, cluster_f=cluster_f)
    cluster_list, noise = main.fancy_cluster_list, main.noise
    end = time.time()
    print("Runtime = " + str(end - start))

    # print("Clusters = ")
    # for i in range(len(cluster_list)):
    #     print("\t" + str(cluster_list[i]))
    # print("]")
    # print("Noise = " + str(noise))
    # print("Number of clusters = " + str(len(cluster_list)))


def distance_configuration_1(dates):
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

    weights_titles = [
        [0, 1, 2, 4, 3, 3],
        [1, 0, 1, 4, 3, 3],
        [2, 1, 0, 4, 3, 3],
        [4, 4, 4, 0, 3, 3],
        [3, 3, 3, 3, 0, 3],
        [3, 3, 3, 3, 3, 3]
    ]
    weights_attribution = [
        [0, 1, 2, 4, 3, 3],
        [1, 0, 1, 4, 3, 3],
        [2, 1, 0, 4, 3, 3],
        [4, 4, 4, 0, 3, 3],
        [3, 3, 3, 3, 0, 3],
        [3, 3, 3, 3, 3, 3]
    ]
    weights_units = [
        [0, 1, 2, 4, 3, 3],
        [1, 0, 1, 4, 3, 3],
        [2, 1, 0, 4, 3, 3],
        [4, 4, 4, 0, 3, 3],
        [3, 3, 3, 3, 0, 3],
        [3, 3, 3, 3, 3, 3]
    ]

    # TODO: specify weight matrices for lido data

    if dates == 0:
        weights = weights_dates
    elif dates == 1:
        weights = weights_measurements
    elif dates == 2:
        weights = weights_artist_names
    elif dates == 3:
        weights = weights_titles
    elif dates == 4:
        weights = weights_attribution
    elif dates == 5:
        weights = weights_units
    else:
        raise ValueError('Data index out of range.')

    cost_map = get_cost_map(regex, weights, weight_case)

    return lambda s1, s2: weighted_levenshtein_distance(cost_map, s1, s2)


if __name__ == '__main__':
    algorithm_configurations = [
        hierarchical_args(method='single', n_clusters=7, distance_threshold=None, criterion='maxclust', depth=None, monocrit=None),
        kmedoids_args(n_clusters=7, init='heuristic', max_iter=200),
        dbscan_args(eps=3, min_samples=3, n_jobs=None),
        optics_args(min_samples=3, max_eps=np.inf, cluster_method='xi', eps=None, xi=0.05, predecessor_correction=True, min_cluster_size=None, n_jobs=None),
        affinity_args(damping=0.5, max_iter=200, convergence_iter=15, preference=None),
        spectral_args(n_clusters=7, eigen_solver=None, n_components=8, n_init=10, eigen_tol=0.0, assign_labels='kmeans')
    ]

    data_fields = [
        midas_dates,
        midas_measurements,
        midas_artist_names,
        lido_titles,
        lido_attribution_qualifier,
        lido_measurement_unit
    ]

    data_i = 0
    run_clustering(data_fields[data_i], 1000, word_sequence_compression_function()[0], distance_configuration_1(data_i), algorithm_configurations[3])
