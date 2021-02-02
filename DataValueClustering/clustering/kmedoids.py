from sklearn_extra.cluster import KMedoids

from clustering import hierarchical
from distance.distance_matrix import calculate_distance_matrix
from gui_cluster_selection.clustering_questions import clustering_question_array
from util.question_result_array_util import get_array_part

method_array = [ # not supported by KMedoids anymore
    # dependencies, not-dependencies, value
    # suggest value if none of the 'not-dependencies' questions were answered with True

    [[], [0], "pam"],
    [[], [], "alternate"],

]

initialization_array = [
    # dependencies, not-dependencies, value
    # suggest value if none of the 'not-dependencies' questions were answered with True

    [[], [1],   "random",       "Random selection of n_clusters points as medoids."],
    [[], [0],   "heuristic",    "Picks the n_clusters points with the smallest sum distance to every other point."],
    [[], [0, 1], "k-medoids++", "Gives initial medoids which are more separated than those generated by the other methods."],
    [[], [0],   "build",        "Greedy initialization of the medoids used in the original PAM algorithm. More effective but slower than other initializations. Very non-robust concerning outliers."],  # not supported by KMedoids anymore

]


def kmedoids(distance_matrix, values, n_clusters=8, method='alternate', init='build', max_iter=None,
             random_state=None):
    clusters = KMedoids(metric='precomputed', n_clusters=n_clusters, init=init, max_iter=max_iter,
                        random_state=random_state).fit_predict(distance_matrix)
    # TODO: method=method is unexpected keyword argument ...
    # method=method,
    return clusters


def kmedoids_args(n_clusters=8, method='alternate', init='build', max_iter=None,
                  random_state=None):
    return lambda distance_function, values_compressed: kmedoids(distance_function, values_compressed,
                                                                 n_clusters, method, init, max_iter,
                                                                 random_state)


def kmedoids_n_clusters_config(no_values):
    # int or range
    return hierarchical.hierarchical_n_clusters_config(no_values)


def kmedoids_method_config(answers):
    pass

def kmedoids_init_config(answers):
    # enum
    name = "heuristic"
    explanation = "Initialization method for medoids."
    values = initialization_array[:, 2]
    explanations = method_array[:, 3]
    suggestion_values = get_array_part(initialization_array, clustering_question_array, answers)

    return name, explanation, values, explanations, suggestion_values

def kmedoids_max_iter_config():
    pass