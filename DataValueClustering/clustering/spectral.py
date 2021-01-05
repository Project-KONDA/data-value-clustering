from sklearn.cluster import SpectralClustering

from utility.distance_matrix import calculate_affinity_matrix


def spectral(distance_function, values, n_clusters=8, eigen_solver=None, n_components=8, random_state=None, n_init=10, gamma=1.0, eigen_tol=0.0, assign_labels='kmeans', verbose=False):
    affinity_matrix = calculate_affinity_matrix(distance_function, values)
    clusters = SpectralClustering(n_clusters=n_clusters, eigen_solver=eigen_solver, n_components=n_components, random_state=random_state, n_init=n_init, gamma=gamma, affinity='precomputed', eigen_tol=eigen_tol, assign_labels=assign_labels, verbose=verbose).fit_predict(affinity_matrix)
    return clusters
