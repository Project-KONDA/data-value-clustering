from scipy.cluster.hierarchy import linkage, fcluster

from utility.distance_matrix import calculate_condensed_distance_matrix, plot_image, get_condensed, min_distance

# def hierarchical(distance_function, values, n_clusters, distance_threshold, method='single', criterion='inconsistent',
#                  depth=2, monocrit=None):
#     pass
#
#
# def hierarchical_args(n_clusters, distance_threshold, method='single', criterion='inconsistent', depth=2,
#                       monocrit=None):
#     return lambda distance_function, values_compressed: hierarchical(distance_function, values_compressed,
#                                                                      n_clusters, distance_threshold, method, criterion,
#                                                                      depth, monocrit)


method_array = [
    # dependencies, not-dependencies, value
    # suggest value if none of the 'not-dependencies' questions were answered with True

    [[], [], "single"],
    [[], [4], "complete"],
    [[], [4,5], "ward"],
    [[], [], "average"],
    [[], [], "weighted"],  # 4
    [[], [], "centroid"],
    [[], [], "median"],  # 4

]


def generate_linkage_matrix(distance_function, values, method):
    cdm = calculate_condensed_distance_matrix(distance_function, values)
    # c, coph_dists = cophenet(linkage_matrix, condensed_distance_matrix)
    return linkage(cdm, method)


def hierarchical_lm(linkage_matrix, values, n_clusters, distance_threshold, criterion, depth, monocrit):
    if not (n_clusters is None):
        return decrease_by_one(fcluster(linkage_matrix, n_clusters, criterion, depth, None, monocrit))
    elif not (distance_threshold is None):
        return decrease_by_one(fcluster(linkage_matrix, distance_threshold, criterion, depth, None, monocrit))


def decrease_by_one(clusters):
    for i in range(len(clusters)):
        clusters[i] = clusters[i] - 1
    return clusters


def method_config(answers):
    name = "method"
    explanation = "Method for calculating the distance between clusters."
    values = method_array[:, 2]
    suggestion_values = ""  # TODO: calculate from answers and method_array

    return name, explanation, values, suggestion_values


def n_clusters_config(no_values):
    name = "n_clusters"
    explanation = "Maximum number of clusters created. Higher values will yield more clusters."
    min_n_clusters = 2
    max_n_clusters = no_values
    suggestion_value = min(7, no_values/2)
    return name, explanation, min_n_clusters, max_n_clusters, suggestion_value


def distance_threshold_config(linkage_matrix, distance_matrix):  # or pass condensed_distance_matrix instead?
    name = "distance_threshold"
    explanation = "Threshold for distances of values in the same cluster. Higher values will yield less clusters."
    condensed = get_condensed(distance_matrix)
    min_n_clusters = min_distance(condensed)
    max_n_clusters = linkage_matrix[len(linkage_matrix)-1, 2] - 0.01
    suggestion_value = (max_n_clusters-min_n_clusters)/2
    return name, explanation, min_n_clusters, max_n_clusters, suggestion_value
