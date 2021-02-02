from sklearn.cluster import AffinityPropagation

from gui_center.cluster_representation import fancy_cluster_representation
from distance.distance_matrix import calculate_affinity_matrix, calculate_affinity_matrix_from_distance_matrix
import numpy as np


def affinity(affinity_matrix, values, damping=0.5, max_iter=200, convergence_iter=15, copy=True, preference=None,
             verbose=False, random_state=None):
    # affinity_matrix = calculate_affinity_matrix_from_distance_matrix(distance_matrix)
    clusters = AffinityPropagation(
        affinity='precomputed', damping=damping, max_iter=max_iter, convergence_iter=convergence_iter, copy=copy,
        preference=preference, verbose=verbose, random_state=random_state
    ).fit_predict(affinity_matrix)
    return clusters


def affinity_damping_config():
    name = "damping"
    explanation = "Higher values will yield less clusters."
    min_damping = 0.5
    max_damping = 0.99
    suggestion_value = 0.5
    return name, explanation, min_damping, max_damping, suggestion_value


def affinity_preference_config(affinity_matrix):
    # it is advised to start with a preference equal to the median of the input similarities (= default)
    name = "preference"
    explanation = "Lower values will yield less clusters."
    min_preference = 0  # TODO
    max_preference = np.inf  # TODO
    suggestion_value = np.median(affinity_matrix)  # = default
    return name, explanation, min_preference, max_preference, suggestion_value


def affinity_max_iter_config(answers):
    pass


def affinity_convergence_iter_config():
    # increase for more clusters?
    pass


def affinity_copy_config():
    pass


def affinity_verbose_config():
    pass


if __name__ == '__main__':
    v = [1, 1, 1, 3, 4, 5, 10, 100, 3]
    for i in range(10):
        c = affinity(lambda a, b: abs(a - b), v, convergence_iter=50, damping=0.9)
        # print(c)
        print(fancy_cluster_representation(v, c))

