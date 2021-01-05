from sklearn_extra.cluster import KMedoids
from utility.distance_matrix import calculate_distance_matrix


def kmedoids_clustering(distance_function, values, n_clusters=8, method='alternate', init='build', max_iter=None,
                        random_state=None):
    distance_matrix = calculate_distance_matrix(distance_function, values)
    clusters = KMedoids(metric='precomputed', n_clusters=n_clusters, method=method, init=init, max_iter=max_iter,
                        random_state=random_state).fit_predict(distance_matrix)
    return clusters


def kmedoids_clustering_args(no_clusters, method, init, max_iter, random_state):
    return lambda distance_function, values_compressed: kmedoids_clustering(distance_function, values_compressed,
                                                                            no_clusters, method, init, max_iter,
                                                                            random_state)
