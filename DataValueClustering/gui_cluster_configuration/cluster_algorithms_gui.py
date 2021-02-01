from clustering.hierarchical import generate_linkage_matrix, hierarchical_lm
from clustering.kmedoids import kmedoids
from clustering.dbscan import *
from clustering.optics import *
from clustering.affinity_propagation import *
from clustering.spectral import *

from gui_cluster_configuration.dendrogram import show_dendrogram


# pass method of this module as cluster_function to clustering.clustering.cluster

def cluster_hierarchical(cluster_answers, distance_matrix_map):
    # TODO: show questionnaire if not shown already
    # TODO: ask user for 'method' argument
    method = 'single'

    return lambda values: cluster_hierarchical_helper(distance_matrix_map["condensed_distance_matrix"], values, method)


def cluster_hierarchical_helper(condensed_distance_matrix, values, method):
    linkage_matrix = generate_linkage_matrix(condensed_distance_matrix, values, method)
    show_dendrogram(linkage_matrix, values)

    # TODO: ask user for additional arguments
    n_clusters = None  # TODO: support elbow method & Co.
    # https://towardsdatascience.com/10-tips-for-choosing-the-optimal-number-of-clusters-277e93d72d92
    # https://www.datanovia.com/en/lessons/determining-the-optimal-number-of-clusters-3-must-know-methods/
    distance_threshold = 3.8  # 15  # 3.8  # depends on distances
    criterion = 'distance'
    # max number of clusters: 'maxclust', 'maxclust_monocrit'
    # threshold: 'distance', 'inconsistent', 'monocrit'
    depth = 2
    monocrit = None

    return hierarchical_lm(linkage_matrix, values, n_clusters, distance_threshold, criterion, depth, monocrit)


def cluster_kmedoids(cluster_answers, distance_matrix_map):
    # TODO: show questionnaire if not shown already
    # TODO: ask user for arguments
    n_clusters = 7  # TODO: support elbow method
    method = 'alternate'  # TODO: unexpected keyword argument error
    init = 'heuristic'  # "if there are outliers in the dataset, use another initialization than build"
    max_iter = 300  # depends on efficiency vs. quality preference

    return lambda values: kmedoids(distance_matrix_map["distance_matrix"], values, n_clusters, method, init, max_iter,
                                                      random_state=None)


def cluster_dbscan(cluster_answers, distance_matrix_map):
    # TODO: ask user for arguments
    # TODO: see 'Parameter Estimation' at https://www.kdnuggets.com/2020/04/dbscan-clustering-algorithm-machine-learning.html
    # TODO: and https://medium.com/@tarammullin/dbscan-parameter-estimation-ff8330e3a3bd
    eps = 4.8  # depends on distances
    min_samples = 3  # depends on number of values
    algorithm = 'auto'
    leaf_size = 30
    n_jobs = None

    return lambda values: dbscan(distance_matrix_map["distance_matrix"], values, eps, min_samples, algorithm, leaf_size,
                                                    n_jobs)


def cluster_optics(cluster_answers, distance_matrix_map):
    # TODO: ask user for arguments
    min_samples = 2
    max_eps = np.inf
    cluster_method = 'xi'
    eps = None
    xi = 0.05
    predecessor_correction = True
    min_cluster_size = None
    algorithm = 'auto'
    leaf_size = 30
    n_jobs = None

    return lambda values: optics(distance_matrix_map["distance_matrix"], values, min_samples, max_eps, cluster_method,
                                                    eps, xi, predecessor_correction, min_cluster_size, algorithm,
                                                    leaf_size, n_jobs)


def cluster_affinity(cluster_answers, distance_matrix_map):
    # TODO: ask user for arguments
    damping = 0.99
    max_iter = 200
    convergence_iter = 15
    copy = True
    preference = None
    verbose = False

    return lambda values: affinity(distance_matrix_map["distance_matrix"], values, damping, max_iter, convergence_iter,
                                                      copy, preference, verbose, random_state=None)


def cluster_spectral(cluster_answers, distance_matrix_map):
    # TODO: ask user for arguments
    n_clusters = 5
    eigen_solver = None
    n_components = n_clusters
    random_state = None
    n_init = 10
    gamma = 1.0
    eigen_tol = 0.0
    assign_labels = 'kmeans'
    verbose = False

    return lambda values: spectral(distance_matrix_map["distance_matrix"], values, n_clusters, eigen_solver, n_components,
                                                      random_state, n_init, gamma, eigen_tol, assign_labels, verbose)


def clusters_from_compressed_values(cluster_answers, distance_matrix_map):
    return lambda values: list(range(0, len(values)))



