from scipy.cluster.hierarchy import linkage, fcluster
from gui_cluster_selection.clustering_questions import clustering_question_array
from util.question_result_array_util import get_array_part

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

    [[], [], "single", "The minimum distance between contained samples. Will yield long chain-like clusters."],
    [[], [4], "complete", "The minimum distance between contained samples. Will yield small globular clusters."],
    [[], [4, 5], "ward",
     "The sum of squared deviations from samples to centroids. Will yield globular clusters of similar size."],
    [[], [], "average",
     "The average distance between contained samples. Will yield globular clusters of similar variance."],
    [[], [], "weighted", "The arithmetic mean of the average distances between contained samples."],  # 4
    [[], [], "centroid", "The distance between centroids."],
    [[], [], "median", "The distance between centroids calculated as the average of the old centroids."],  # 4

]


def generate_linkage_matrix(condensed_distance_matrix, values, method):
    # c, coph_dists = cophenet(linkage_matrix, condensed_distance_matrix)
    return linkage(condensed_distance_matrix, method)


def hierarchical_lm(linkage_matrix, values, n_clusters, distance_threshold, criterion, depth, monocrit):
    if not (n_clusters is None):
        return decrease_by_one(fcluster(linkage_matrix, n_clusters, criterion, depth, None, monocrit))
    elif not (distance_threshold is None):
        return decrease_by_one(fcluster(linkage_matrix, distance_threshold, criterion, depth, None, monocrit))


def decrease_by_one(clusters):
    for i in range(len(clusters)):
        clusters[i] = clusters[i] - 1
    return clusters


def hierarchical_method_config(answers):
    # enum
    name = "method"
    explanation = "Method for calculating the distance between clusters."
    options = method_array[:, (2, 3)]
    suggestion_values = get_array_part(method_array, clustering_question_array, answers)
    return name, explanation, options, suggestion_values


def hierarchical_n_clusters_config(no_values):
    # int or range
    name = "n_clusters"
    explanation = "Maximum number of clusters created. Higher values will yield more clusters."
    min_n_clusters = 2
    max_n_clusters = no_values
    suggestion_value = min(7, no_values / 2)
    deactivatable = True
    return name, explanation, min_n_clusters, max_n_clusters, suggestion_value, deactivatable


def hierarchical_distance_threshold_config(linkage_matrix, min_distance):
    # float
    name = "distance_threshold"
    explanation = "Threshold for distances of values in the same cluster. Higher values will yield less clusters."
    min_distance_threshold = min_distance
    max_distance_threshold = linkage_matrix[len(linkage_matrix) - 1, 2] - 0.01
    suggestion_value = (max_distance_threshold - min_distance_threshold) / 2
    resolution = 0.01
    deactivatable = True
    return name, explanation, min_distance_threshold, max_distance_threshold, suggestion_value, resolution, deactivatable


def hierarchical_criterion_config():
    # enum
    # return name, explanation, min_distance_threshold, max_distance_threshold, suggestion_value, resolution
    pass


def hierarchical_depth_config():
    # only activated if criterion = 'inconsistent'
    # int slider
    deactivatable = True
    # return name, explanation, min_distance_threshold, max_distance_threshold, suggestion_value, deactivatable
    pass


def hierarchical_monocrit_config():
    # vector
    # return ??
    pass


if __name__ == '__main__':
    res = hierarchical_n_clusters_config(2)
    print(res)
    print(type(res))
    print(res[0])
