from sklearn.cluster import AffinityPropagation

from clustering.clustering import fancy_cluster_representation
from utility.distance_matrix import calculate_affinity_matrix


def affinity(distance_function, values, damping=0.5, max_iter=200, convergence_iter=15, copy=True, preference=None,
             verbose=False, random_state=None):
    affinity_matrix = calculate_affinity_matrix(distance_function, values)
    clusters = AffinityPropagation(
        affinity='precomputed', damping=damping, max_iter=max_iter, convergence_iter=convergence_iter, copy=copy,
        preference=preference, verbose=verbose, random_state=random_state
    ).fit_predict(affinity_matrix)
    return clusters


def damping_config():
    min_damping = 0.5
    max_damping = 1
    pass


def preference_config():
    # it is advised to start with a preference equal to the median of the input similarities (= default)
    # if less clusters are desired: set the preference value lower
    pass


def max_iter_config(answers):
    # decrease for faster execution
    pass


def convergence_iter(answers):
    # decrease for faster execution
    pass


if __name__ == '__main__':
    v = [1, 1, 1, 3, 4, 5, 10, 100, 3]
    for i in range(10):
        c = affinity(lambda a, b: abs(a - b), v, convergence_iter=50, damping=0.9)
        # print(c)
        print(fancy_cluster_representation(v, c))
