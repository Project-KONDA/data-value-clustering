from scipy.cluster.hierarchy import linkage, fcluster

from utility.distance_matrix import calculate_condensed_distance_matrix, plot_image

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
