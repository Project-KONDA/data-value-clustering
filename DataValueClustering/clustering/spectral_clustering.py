'''Apply spectral clustering algorithm.'''
import numpy as np
from sklearn.cluster import SpectralClustering

from distance.distance_matrix import calculate_affinity_matrix, calculate_affinity_matrix_from_distance_matrix

ASSIGN_LABELS = "assign_labels"
EIGEN_TOL = "eigen_tol"
N_INIT = "n_init"
N_COMPONENTS = "n_components"
EIGEN_SOLVER = "eigen_solver"
N_CLUSTERS = "n_clusters"


def spectral(affinity_matrix, values, n_clusters=8, eigen_solver=None, n_components=8, n_init=10,
             eigen_tol=0.0, assign_labels='kmeans'):
    # affinity_matrix = calculate_affinity_matrix_from_distance_matrix(distance_matrix)
    clusters = SpectralClustering(n_clusters=n_clusters, eigen_solver=eigen_solver, n_components=n_components,
                                  n_init=n_init, affinity='precomputed',
                                  eigen_tol=eigen_tol, assign_labels=assign_labels).fit_predict(affinity_matrix)
    return clusters


def spectral_args(n_clusters, eigen_solver, n_components, n_init, eigen_tol, assign_labels):
    return lambda distance_matrix_map, values: spectral(distance_matrix_map["affinity_matrix"], values, n_clusters,
                                                        eigen_solver, n_components, n_init, eigen_tol, assign_labels)


def spectral_n_clusters_config(no_values):
    # int or range
    name = N_CLUSTERS
    explanation = "Maximum number of clusters created. Higher values will yield more clusters."
    min_n_clusters = 2
    max_n_clusters = no_values
    suggestion_value = min(7, no_values // 2)
    resolution = 1
    deactivatable = False
    return name, explanation, min_n_clusters, max_n_clusters, suggestion_value, resolution, deactivatable


def spectral_eigen_solver_config():
    # enum
    name = EIGEN_SOLVER  # TODO
    explanation = "Eigenvalue decomposition strategy."  # TODO
    options = np.array([
        ['arpack', "Default Value."],
        ['lobpcg', ""],
        ['amg', "Faster, but partially instable."]
    ], dtype=str)  # TODO
    suggestions = ['arpack']  # TODO
    deactivatable = False  # If None 'arpack' is used
    return name, explanation, options, suggestions, deactivatable


def spectral_n_components_config(no_values):
    # int
    name = N_COMPONENTS  # TODO
    explanation = ""  # TODO
    mini = 0  # TODO
    maxi = 2  # TODO
    default = min(7, no_values // 2)  # TODO : n.clusters
    resolution = 1  # TODO
    deactivatable = False
    return name, explanation, mini, maxi, default, resolution, deactivatable


def spectral_n_init_config(no_values):
    # int
    name = N_INIT  # TODO
    explanation = "Number of iterations of the algorithm."
    explanation += "The final result will be the best result of the single iterations."
    mini = 1
    maxi = no_values
    default = 10  # TODO
    resolution = 1  # TODO
    deactivatable = False
    return name, explanation, mini, maxi, default, resolution, deactivatable


def spectral_eigen_tol_config():
    # float
    # when eigen_solver='arpack' = default
    name = EIGEN_TOL  # TODO
    explanation = ""  # TODO
    mini = 0.  # TODO
    maxi = 2.  # TODO
    default = 1.  # TODO
    resolution = 0.01
    deactivatable = False
    return name, explanation, mini, maxi, default, resolution, deactivatable


def spectral_assign_labels_config():
    # enum
    #  k-means can be applied and is a popular choice. But it can also be sensitive to initialization.
    #  Discretization is another approach which is less sensitive to random initialization.
    name = ASSIGN_LABELS  # TODO
    explanation = "Strategy to use to assign labels in the embedding space."  # TODO

    options = np.array([
        ['kmeans', ""],
        ['discretize', ""]
    ], dtype=str)  # TODO
    suggestions = ['kmeans']  # TODO
    deactivatable = False
    return name, explanation, options, suggestions, deactivatable

