from Compression.Compression import compress_list
from Util.ClusterHandling import map_compressed_values_to_unique_clusters, build_cluster_matrix
from Util.DistanceMatrixHandling import calculate_distance_matrix, calculate_distance_matrix_original_values, calculate_complete_distance_matrix
from Util.ListOperations import remove_duplicates
from Validation.SilhouetteCoefficient import silhouette_score_mean_validation, plot_silhouette_analysis


def cluster(original_values, compression_matrix, distance_function, cluster_function, use_original_values):
    if compression_matrix is None:
        compressed_values = original_values
    else:
        compressed_values = compress_list(original_values, compression_matrix)
    unique_values = remove_duplicates(compressed_values)

    # print("original_values = " + str(original_values))
    # print("compressed_values = " + str(compressed_values))
    print("unique_values = " + str(unique_values))
    # print("len(unique_values) = " + str(len(unique_values)))

    # create distance matrix
    distance_matrix = calculate_distance_matrix(unique_values, distance_function)

    if use_original_values:
        # create distance matrix for original_values via distance matrix for unique_values
        distance_matrix = calculate_distance_matrix_original_values(
            original_values, compressed_values, unique_values, distance_matrix)

    # print("distance_matrix = ")
    # print(distance_matrix)

    # perform clustering
    clusters = cluster_function(original_values, compressed_values, unique_values, distance_matrix, use_original_values)
    # print("clusters = " + str(clusters))

    print_silhouette_score_unique_values(clusters, unique_values, distance_matrix)

    # map compressed_values to clusters:
    if not use_original_values:
        clusters = map_compressed_values_to_unique_clusters(compressed_values, unique_values, clusters)
        #print(clusters)

    print_silhouette_score_original_values(clusters, distance_matrix, original_values, compressed_values, unique_values,
                                           use_original_values)


    return build_cluster_matrix(clusters, original_values)


def print_silhouette_score_original_values(clusters, distance_matrix, original_values, compressed_values, unique_values,
                                           use_original_values):
    if not use_original_values:
        distance_matrix_original_values = calculate_distance_matrix_original_values(original_values, compressed_values,
                                                                                    unique_values, distance_matrix)
    else:
        distance_matrix_original_values = distance_matrix
    complete_distance_matrix = calculate_complete_distance_matrix(distance_matrix_original_values)
    print(
        "silhouette score of original values = " + str(silhouette_score_mean_validation(complete_distance_matrix, clusters)))
    plot_silhouette_analysis(original_values, complete_distance_matrix, max(clusters)+1, clusters)


def print_silhouette_score_unique_values(clusters, unique_values, distance_matrix):
    complete_distance_matrix = calculate_complete_distance_matrix(distance_matrix)
    print("silhouette score of compressed unique values = " + str(
        silhouette_score_mean_validation(complete_distance_matrix, clusters)))
    plot_silhouette_analysis(unique_values, complete_distance_matrix, max(clusters) + 1, clusters)


def use_unique_values_as_clusters(cluster_original_values, compressed_values, unique_values):
    n_clusters = len(unique_values)
    clusters = list(range(0, n_clusters))  # name clusters as 0..n_clusters
    if cluster_original_values:
        clusters = map_compressed_values_to_unique_clusters(compressed_values, unique_values, clusters)
    return clusters, n_clusters


def user_config(n_clusters, distance_threshold):
    while n_clusters is None and distance_threshold is None:
        # request configuration via console
        try:
            input1 = str(
                input("Do you want to specify the number of clusters or the distance threshold? Type 'c' or 't' ... "))
            if input1 == "c":
                n_clusters = user_config_n_clusters(n_clusters)
            elif input1 == "t":
                distance_threshold = user_config_distance_threshold(distance_threshold)
            else:
                pass
        except ValueError:
            pass
    assert not (n_clusters is None and distance_threshold is None)
    return n_clusters, distance_threshold


def user_config_distance_threshold(distance_threshold):
    while distance_threshold is None:
        try:
            input2 = float(input("Please enter the desired distance threshold ... "))
            distance_threshold = input2
        except ValueError:
            pass
    assert not (distance_threshold is None)
    return distance_threshold


def user_config_n_clusters(n_clusters):
    while n_clusters is None:
        try:
            input2 = int(input("Please enter the desired number of clusters ... "))
            n_clusters = input2
        except ValueError:
            pass
    assert not (n_clusters is None)
    return n_clusters
