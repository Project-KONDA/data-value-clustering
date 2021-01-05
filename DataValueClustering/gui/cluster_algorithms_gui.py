from clustering.hierarchical import generate_linkage_matrix, hierarchical_lm
from clustering.kmedoids import kmedoids

from gui.dendrogram import show_dendrogram



def cluster_hierarchical(distance_function, values):
    # TODO: ask for 'method'
    method = 'single'

    # show dendrogram
    linkage_matrix = generate_linkage_matrix(distance_function, values, method)
    show_dendrogram(linkage_matrix, values)

    # TODO: ask for additional arguments: n_cluster, distance_threshold
    n_clusters = 2
    distance_threshold = 2
    criterion = 'distance'
    # criterion: 'maxclust', 'distance', 'inconsistent', 'monocrit', 'maxclust_monocrit'
    depth = 2
    monocrit = None

    return hierarchical_lm(linkage_matrix, values, n_clusters, distance_threshold, criterion, depth, monocrit)


def cluster_kmedoids(distance_function, values):
    # TODO: ask user for arguments - n_clusters, method, init, max_iter, random_state
    n_clusters = 2
    method = 'single'
    init = 'build'
    max_iter = None
    random_state = None

    return kmedoids(distance_function, values, n_clusters, method, init, max_iter, random_state)


def cluster_dbscan(distance_function, values):
    # TODO: ask user for arguments
    # return dbscan(...)
    pass


def cluster_optics(distance_function, values):
    # TODO: ask user for arguments
    # return optics(...)
    pass


def cluster_affinity(distance_function, values):
    # TODO: ask user for arguments
    # return affinity(...)
    pass


def cluster_spectral(distance_function, values):
    # TODO: ask user for arguments
    # return spectral.py(...)
    pass
