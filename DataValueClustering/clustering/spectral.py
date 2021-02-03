from sklearn.cluster import SpectralClustering

from distance.distance_matrix import calculate_affinity_matrix, calculate_affinity_matrix_from_distance_matrix


def spectral(affinity_matrix, values, n_clusters=8, eigen_solver=None, n_components=8, n_init=10,
             gamma=1.0, eigen_tol=0.0, assign_labels='kmeans'):
    # affinity_matrix = calculate_affinity_matrix_from_distance_matrix(distance_matrix)
    clusters = SpectralClustering(n_clusters=n_clusters, eigen_solver=eigen_solver, n_components=n_components,
                                  n_init=n_init, gamma=gamma, affinity='precomputed',
                                  eigen_tol=eigen_tol, assign_labels=assign_labels).fit_predict(affinity_matrix)
    return clusters


def spectral_args(n_clusters, eigen_solver, n_components, n_init, gamma, eigen_tol, assign_labels):
    return lambda distance_matrix_map, values: spectral(distance_matrix_map["affinity_matrix"], values, n_clusters, eigen_solver,
                            n_components, n_init, gamma, eigen_tol, assign_labels)


def spectral_n_clusters_config(no_values):
    # int or range
    name = " spectral_n_clusters"
    explanation = "Maximum number of clusters created. Higher values will yield more clusters."
    min_n_clusters = 2
    max_n_clusters = no_values
    suggestion_value = min(7, no_values / 2)
    return name, explanation, min_n_clusters, max_n_clusters, suggestion_value


def spectral_eigen_solver_config():
    # enum
    name = "spectral_eigen_solver"  # TODO
    explanation = ""  # TODO
    options = [["", ""]]  # TODO
    suggestions = [""]  # TODO
    deactivatable = True
    return name, explanation, options, suggestions, deactivatable


def spectral_n_components_config():
    # int
    name = "spectral_n_components"  # TODO
    explanation = ""  # TODO
    mini = 0  # TODO
    maxi = 2  # TODO
    default = 1  # TODO
    resolution = 1  # TODO
    deactivatable = True
    return name, explanation, mini, maxi, default, resolution, deactivatable


def spectral_n_init_config():
    # int
    name = "spectral_n_init"  # TODO
    explanation = ""  # TODO
    mini = 0  # TODO
    maxi = 2  # TODO
    default = 1  # TODO
    resolution = 1  # TODO
    deactivatable = True
    return name, explanation, mini, maxi, default, resolution, deactivatable


def spectral_gamma_config():
    # float
    # TODO: remove?
    name = "spectral_gamma"  # TODO
    explanation = ""  # TODO
    mini = 0.  # TODO
    maxi = 2.  # TODO
    default = 1.  # TODO
    resolution = 0.01  # TODO
    deactivatable = True  # TODO
    return name, explanation, mini, maxi, default, resolution, deactivatable


def spectral_eigen_tol_config():
    # float
    # when eigen_solver='arpack'
    name = "spectral_eigen_tol"  # TODO
    explanation = ""  # TODO
    mini = 0.  # TODO
    maxi = 2.  # TODO
    default = 1.  # TODO
    resolution = 0.01
    deactivatable = True
    return name, explanation, mini, maxi, default, resolution, deactivatable


def spectral_assign_labels_config():
    # enum
    #  k-means can be applied and is a popular choice. But it can also be sensitive to initialization.
    #  Discretization is another approach which is less sensitive to random initialization.
    name = "spectral_assign_labels"  # TODO
    explanation = ""  # TODO
    options = [["", ""]]  # TODO
    suggestions = [""]  # TODO
    deactivatable = True
    return name, explanation, options, suggestions, deactivatable
