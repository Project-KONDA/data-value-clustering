from sklearn_extra.cluster import KMedoids

from utility.distance_matrix import calculate_distance_matrix


method_array = [
    # dependencies, not-dependencies, value
    # suggest value if none of the 'not-dependencies' questions were answered with True

    [[], [0], "pam"],
    [[], [], "alternate"],

]

initialization_array = [
    # dependencies, not-dependencies, value
    # suggest value if none of the 'not-dependencies' questions were answered with True

    [[], [1],   "random"],
    [[], [0],   "heuristic"],
    [[], [0,1], "k-medoids++"],
    [[], [0],   "build"],

]


def kmedoids(distance_function, values, n_clusters=8, method='alternate', init='build', max_iter=None,
             random_state=None):
    distance_matrix = calculate_distance_matrix(distance_function, values)
    clusters = KMedoids(metric='precomputed', n_clusters=n_clusters, method=method, init=init, max_iter=max_iter,
                        random_state=random_state).fit_predict(distance_matrix)
    return clusters


def kmedoids_args(n_clusters=8, method='alternate', init='build', max_iter=None,
                  random_state=None):
    return lambda distance_function, values_compressed: kmedoids(distance_function, values_compressed,
                                                                 n_clusters, method, init, max_iter,
                                                                 random_state)


def n_clusters_config(no_values):
    # min_n_clusters = 2
    # max_n_clusters = no_values

    # if only compression but no clustering is desired: n_clusters = max_n_clusters

    pass
