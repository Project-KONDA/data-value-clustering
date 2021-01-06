from clustering_algorithms.hierarchical import generate_linkage_matrix, hierarchical_lm
from clustering_algorithms.kmedoids import kmedoids
from clustering_algorithms.dbscan import *
from clustering_algorithms.optics import *
from clustering_algorithms.affinity_propagation import *
from clustering_algorithms.spectral import *

from gui.dendrogram import show_dendrogram


def cluster_hierarchical():
    # TODO: ask for 'method'
    method = 'single'

    return lambda distance_function, values: cluster_hierarchical_helper(distance_function, values, method)


def cluster_hierarchical_helper(distance_function, values, method):
    # show dendrogram
    linkage_matrix = generate_linkage_matrix(distance_function, values, method)
    show_dendrogram(linkage_matrix, values)

    # TODO: ask for additional arguments: n_cluster, distance_threshold etc.
    n_clusters = 2
    distance_threshold = 2
    criterion = 'distance'
    # criterion: 'maxclust', 'distance', 'inconsistent', 'monocrit', 'maxclust_monocrit'
    depth = 2
    monocrit = None

    return lambda distance_function, values: hierarchical_lm(linkage_matrix, values, n_clusters, distance_threshold,
                                                             criterion, depth, monocrit)


def cluster_kmedoids():
    # TODO: ask user for arguments - n_clusters, method, init, max_iter, random_state
    n_clusters = 2
    method = 'single'
    init = 'build'
    max_iter = None
    random_state = None

    return lambda distance_function, values: kmedoids(distance_function, values, n_clusters, method, init, max_iter, random_state)


def cluster_dbscan():
    # TODO: ask user for arguments
    eps = 0.5
    min_samples = 5
    algorithm = 'auto'
    leaf_size = 30
    p = None
    n_jobs = None

    return lambda distance_function, values: dbscan(distance_function, values, eps, min_samples,algorithm, leaf_size, p, n_jobs)


def cluster_optics():
    # TODO: ask user for arguments
    min_samples = 5
    max_eps = np.inf
    cluster_method = 'xi'
    eps = None
    xi = 0.05
    predecessor_correction = True
    min_cluster_size = None
    algorithm = 'auto'
    leaf_size = 30
    n_jobs = None

    return lambda distance_function, values: optics(distance_function, values, min_samples, max_eps, cluster_method, eps, xi, predecessor_correction, min_cluster_size, algorithm, leaf_size, n_jobs)


def cluster_affinity():
    # TODO: ask user for arguments
    damping = 0.5
    max_iter = 200
    convergence_iter = 15
    copy = True
    preference = None
    verbose = False
    random_state = None

    return lambda distance_function, values: affinity(distance_function, values, damping, max_iter, convergence_iter, copy, preference, verbose, random_state)


def cluster_spectral():
    # TODO: ask user for arguments
    n_clusters = 8
    eigen_solver = None
    n_components = 8
    random_state = None
    n_init = 10
    gamma = 1.0
    eigen_tol = 0.0
    assign_labels = 'kmeans'
    verbose = False

    return lambda distance_function, values: spectral(distance_function, values, n_clusters, eigen_solver, n_components, random_state, n_init, gamma, eigen_tol, assign_labels, verbose)


cluster_algorithms = np.array([
    ["Hierarchical",
     cluster_hierarchical],
    ["KMedoids",
     cluster_kmedoids],
    ["DBSCAN",
         cluster_dbscan],
    ["Optics",
         cluster_optics],
    ["Affinity Propagation",
         cluster_affinity],
    ["Spectral Clustering",
         cluster_spectral]
])