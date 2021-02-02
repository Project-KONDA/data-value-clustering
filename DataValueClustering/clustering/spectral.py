from sklearn.cluster import SpectralClustering

from distance.distance_matrix import calculate_affinity_matrix, calculate_affinity_matrix_from_distance_matrix


def spectral(affinity_matrix, values, n_clusters=8, eigen_solver=None, n_components=8, random_state=None, n_init=10, gamma=1.0, eigen_tol=0.0, assign_labels='kmeans'):
    # affinity_matrix = calculate_affinity_matrix_from_distance_matrix(distance_matrix)
    clusters = SpectralClustering(n_clusters=n_clusters, eigen_solver=eigen_solver, n_components=n_components,
                                  random_state=random_state, n_init=n_init, gamma=gamma, affinity='precomputed',
                                  eigen_tol=eigen_tol, assign_labels=assign_labels).fit_predict(affinity_matrix)
    return clusters


def spectral_n_clusters_config(no_values):
    # int or range
    name = "n_clusters"
    explanation = "Maximum number of clusters created. Higher values will yield more clusters."
    min_n_clusters = 2
    max_n_clusters = no_values
    suggestion_value = min(7, no_values / 2)
    return name, explanation, min_n_clusters, max_n_clusters, suggestion_value


def spectral_eigen_solver_config():
    # enum
    deactivatable = True
    # return name, explanation, options, suggestion_values
    pass


def spectral_n_components_config():
    # int
    deactivatable = True
    # return name, explanation, min_n_clusters, max_n_clusters, suggestion_value, deactivatable
    pass


def spectral_n_init_config():
    # int
    # return name, explanation, min_n_clusters, max_n_clusters, suggestion_value
    pass


def spectral_gamma_config():
    # float
    # TODO: remove?
    pass


def spectral_eigen_tol_config():
    # float
    # when eigen_solver='arpack'
    deactivatable = True
    resolution = 0.01
    # return name, explanation, min_distance_threshold, max_distance_threshold, suggestion_value, resolution, deactivatable
    pass


def spectral_assign_labels_config():
    # enum
    #  k-means can be applied and is a popular choice. But it can also be sensitive to initialization.
    #  Discretization is another approach which is less sensitive to random initialization.
    deactivatable = True
    # return name, explanation, options, suggestion_values
    pass

