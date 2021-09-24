'''Apply affinity propagation clustering algorithm.'''
from sklearn.cluster import AffinityPropagation

from gui_center.cluster_representation import fancy_cluster_representation
from distance.distance_matrix import calculate_affinity_matrix, calculate_affinity_matrix_from_distance_matrix
import numpy as np

COPY = "copy"
CONVERGENCE_ITER = "convergence_iter"
MAX_ITER = "max_iter"
PREFERENCE = "preference"
DAMPING = "damping"


def affinity(affinity_matrix, values, damping=0.5, max_iter=200, convergence_iter=15, preference=None):
    # affinity_matrix = calculate_affinity_matrix_from_distance_matrix(distance_matrix)
    clusters = AffinityPropagation(
        affinity='precomputed', damping=damping, max_iter=max_iter, convergence_iter=convergence_iter,
        preference=preference, random_state=None).fit_predict(affinity_matrix)
    return clusters


def affinity_args(damping, max_iter, convergence_iter, preference):
    return lambda distance_matrix_map, values: affinity(distance_matrix_map["affinity_matrix"], values, damping,
                                                        max_iter, convergence_iter, preference)


def affinity_damping_config():
    # float
    # expert
    name = DAMPING
    explanation = "Extent to which the current value is maintained relative to incoming values. Higher values will yield less clusters."
    min_damping = 0.5
    max_damping = 0.99
    suggestion_value = 0.5
    resolution = 0.01
    deactivatable = False
    return name, explanation, min_damping, max_damping, suggestion_value, resolution, deactivatable


def affinity_preference_config(affinity_matrix):
    # float
    # expert
    # it is advised to start with a preference equal to the median of the input similarities (= default)
    # If the preferences are not passed as arguments, they will be set to the median of the input similarities
    # Wikipedia: When it is set to the same value for all inputs, it controls how many classes the algorithm produces.
    # ...A value close to the minimum possible similarity produces fewer classes, while a value close to or larger than the maximum possible similarity produces many classes.
    name = PREFERENCE
    explanation = "Controls the number of clusters. Lower values will yield less clusters. If deactivated, the default value, which is automatically calculated and " \
                  "should be appropriate in most cases, is used."
    min_preference = 0.0
    max_preference = 100.0
    suggestion_value = float(np.median(affinity_matrix))
    resolution = 0.01
    deactivatable = True
    return name, explanation, min_preference, max_preference, suggestion_value, resolution, deactivatable


def affinity_max_iter_config(answers):
    # int
    # expert
    name = MAX_ITER
    explanation = "The algorithm runs multiple times and improves with every iteration. " \
                  "This parameter determines the maximum number of iterations the algorithm will perform."
    mini = 1
    maxi = 500
    default = 200
    resolution = 1
    deactivatable = False
    return name, explanation, mini, maxi, default, resolution, deactivatable


def affinity_convergence_iter_config():
    # int
    # expert
    # increase for more clusters?
    name = CONVERGENCE_ITER
    explanation = "Terminate the algorithm if for the given amount of iterations there is no difference between the results."
    mini = 2
    maxi = 100
    default = 15
    resolution = 1
    deactivatable = False
    return name, explanation, mini, maxi, default, resolution, deactivatable


if __name__ == '__main__':
    v = [1, 1, 1, 3, 4, 5, 10, 100, 3]
    for i in range(10):
        c = affinity(lambda a, b: abs(a - b), v, convergence_iter=50, damping=0.9)
        # print(c)
        print(fancy_cluster_representation(v, c))

