from Clustering.Clustering import cluster
from Util.ReadFile import read_data_values_from_file
from Compression.Compression import sequence_compression, char_compression, letter_sequence_compression, \
    word_decimal_compression, word_compression, word_sequence_compression
from Distance.WeightedLevenshteinDistance import weighted_levenshtein_distance_args
from Distance.LevenshteinDistance import levenshtein_distance
from Distance.LongestCommonSubsequenceDistance import longest_common_subsequence_distance
from Distance.DiceCoefficient import dice_coefficient_distance
from Clustering.HierarchicalClustering import hierarchical_clustering_args
from Clustering.KMedoidsClustering import kmedoids_clustering_args
from Clustering.DBSCANClustering import dbscan_clustering
from Clustering.OPTICSClustering import optics_clustering
from Clustering.AffinityPropagationClustering import affinity_propagation_clustering
from Clustering.SpectralClustering import spectral_clustering
import numpy as np

np.set_printoptions(threshold=np.inf)


def run_example(file_path, data_limit, compression, distance, clustering, use_original_values):
    example_values = read_data_values_from_file(file_path)
    example_values = example_values[0:data_limit]  # use subset
    # manually identified 7 clusters: year, um year, year/year, um year/year, um year?, year?, nach year

    cluster_matrix = cluster(example_values, compression, distance, clustering, use_original_values)

    print(cluster_matrix)
    print("Number of clusters = " + str(len(cluster_matrix)))


# main:

compression_algorithms = [char_compression,
                          sequence_compression,
                          letter_sequence_compression,
                          word_decimal_compression,
                          word_compression,
                          word_sequence_compression]

distance_algorithms = [levenshtein_distance,
                       weighted_levenshtein_distance_args(cost_matrix=None),
                       longest_common_subsequence_distance,
                       dice_coefficient_distance]

clustering_algorithms = [hierarchical_clustering_args(n_clusters=None, distance_threshold=None, linkage_criterion='single'),  # 'single', 'complete', 'average', 'weighted', 'centroid', 'median', 'ward'
                         kmedoids_clustering_args(n_clusters=7),
                         dbscan_clustering,
                         optics_clustering,
                         affinity_propagation_clustering,
                         spectral_clustering]


use_original_values = False  # e.g. has an influence on the distances between clusters for 'average', 'centroid' and 'ward' for hierarchical_clustering

run_example('../Data/dates.txt', 1000, compression_algorithms[1], distance_algorithms[1], clustering_algorithms[0], use_original_values)

# TODO: https://en.wikipedia.org/wiki/Determining_the_number_of_clusters_in_a_data_set
# TODO: check and compare "correctness" via https://scikit-learn.org/stable/modules/classes.html#module-sklearn.metrics
