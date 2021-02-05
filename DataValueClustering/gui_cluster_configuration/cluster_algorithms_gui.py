from clustering import hierarchical_clustering, affinity_propagation_clustering, dbscan_clustering, optics_clustering, spectral_clustering, kmedoids_clustering
from clustering.hierarchical_clustering import *
from clustering.kmedoids_clustering import *
from clustering.dbscan_clustering import *
from clustering.optics_clustering import *
from clustering.affinity_propagation_clustering import *
from clustering.spectral_clustering import *
from gui_cluster_configuration import get_configuration_parameters
from gui_cluster_configuration.dendrogram import show_dendrogram
from gui_cluster_configuration.parameter_frames import create_enum_frame, create_slider_frame, create_boolean_frame


# pass method of this module as cluster_function to clustering.clustering.cluster
from gui_cluster_configuration.parameter_frames.ClusteringParameter import DEPENDENCY_ACTIVATION_ACTIVATION, \
    DEPENDENCY_ACTIVATION_ENUM, DEPENDENCY_ENUM_ACTIVATION, DEPENDENCY_VALUE_SLIDER_MAX


def cluster_hierarchical(cluster_answers, distance_matrix_map, values):
    if cluster_answers is None:
        cluster_answers = None
        # cluster_answers = not None
        # TODO: show questionnaire if not shown already
        # somewhat similar to:
        # answers, cluster_f = input_questionnaire_clustering(clustering_question_array, predefined_answers)

    # ask user for 'method' argument
    # method = 'single'
    method_info = hierarchical_method_config(cluster_answers)
    method_frame = create_enum_frame(*method_info)

    param_frames = [method_frame]
    method, = get_configuration_parameters(
        "Hierarchical Clustering Configuration Part 1/2", param_frames, [])

    linkage_matrix = generate_linkage_matrix(distance_matrix_map["condensed_distance_matrix"], values, method)
    show_dendrogram(linkage_matrix, values)

    # n_clusters = None  # TODO: support elbow method & Co.
    n_clusters_info = hierarchical_n_clusters_config(len(values))
    n_clusters_frame = create_slider_frame(*n_clusters_info)
    # https://towardsdatascience.com/10-tips-for-choosing-the-optimal-number-of-clusters-277e93d72d92
    # https://www.datanovia.com/en/lessons/determining-the-optimal-number-of-clusters-3-must-know-methods/

    # distance_threshold = 3.8  # 15  # 3.8  # depends on distances
    distance_threshold_info = hierarchical_distance_threshold_config(linkage_matrix,
                                                                     distance_matrix_map["min_distance"])
    distance_threshold_frame = create_slider_frame(*distance_threshold_info)

    # criterion = 'distance'
    criterion_info = hierarchical_criterion_config()
    criterion_frame = create_enum_frame(*criterion_info)
    # max number of clusters: 'maxclust', 'maxclust_monocrit'
    # threshold: 'distance', 'inconsistent', 'monocrit'

    # depth = 2
    depth_info = hierarchical_depth_config()
    depth_frame = create_slider_frame(*depth_info)

    # monocrit = None
    # monocrit_info = hierarchical_monocrit_config()
    # monocrit_frame = create_vector_input(*monocrit_info)

    frames = [n_clusters_frame, distance_threshold_frame, criterion_frame, depth_frame]
    dependencies2 = [
        [hierarchical_clustering.N_CLUSTERS, hierarchical_clustering.THRESHOLD, DEPENDENCY_ACTIVATION_ACTIVATION, False],
        [hierarchical_clustering.THRESHOLD, hierarchical_clustering.N_CLUSTERS, DEPENDENCY_ACTIVATION_ACTIVATION, False],
        [hierarchical_clustering.N_CLUSTERS, hierarchical_clustering.CRITERION, DEPENDENCY_ACTIVATION_ENUM, {True: ['maxclust', 'maxclust_monocrit'], False: ['distance', 'inconsistent', 'monocrit']}],
        [hierarchical_clustering.THRESHOLD, hierarchical_clustering.CRITERION, DEPENDENCY_ACTIVATION_ENUM, {True: ['distance', 'inconsistent', 'monocrit'], False: ['maxclust', 'maxclust_monocrit']}],
        [hierarchical_clustering.CRITERION, hierarchical_clustering.DEPTH, DEPENDENCY_ENUM_ACTIVATION, {'inconsistent': True, 'maxclust': False, 'maxclust_monocrit': False, 'distance': False, 'monocrit': False}],
        # [hierarchical.CRITERION, hierarchical.MONOCRIT, 'enum_value_activation', {'inconsistent': False, 'maxclust': False, 'maxclust_monocrit': True, 'distance': False, 'monocrit': True}]
    ]
    n_clusters, distance_threshold, criterion, depth = \
        get_configuration_parameters("", frames, dependencies2)

    return hierarchical_lm_args(linkage_matrix, n_clusters, distance_threshold, criterion, depth, None)


def cluster_kmedoids(cluster_answers, distance_matrix_map, values):
    # TODO: show questionnaire if not shown already

    # n_clusters = 7  # TODO: support elbow method
    n_clusters_info = kmedoids_n_clusters_config(len(values))
    n_clusters_frame = create_slider_frame(*n_clusters_info)

    # # method = 'alternate'  # TODO: unexpected keyword argument error
    # method_info = kmedoids_method_config(cluster_answers)
    # method_frame = create_enum_frame(*method_info)

    # init = 'heuristic'  # "if there are outliers in the dataset, use another initialization than build"
    init_info = kmedoids_init_config(cluster_answers)
    init_frame = create_enum_frame(*init_info)

    # max_iter = 300  # depends on efficiency vs. quality preference
    max_iter_info = kmedoids_max_iter_config()
    max_iter_frame = create_slider_frame(*max_iter_info)

    frames = [n_clusters_frame, init_frame, max_iter_frame]

    n_clusters, init, max_iter = \
        get_configuration_parameters("", frames, [])

    if not max_iter:
        max_iter = 200

    return kmedoids_args(n_clusters, init, max_iter)


def cluster_dbscan(cluster_answers, distance_matrix_map, values):
    # TODO: ask user for arguments
    # TODO: see 'Parameter Estimation' at https://www.kdnuggets.com/2020/04/dbscan-clustering-algorithm-machine-learning.html
    # TODO: and https://medium.com/@tarammullin/dbscan-parameter-estimation-ff8330e3a3bd
    n_values = len(values)
    # min_samples = 3  # depends on number of values
    min_samples_info = dbscan_min_samples_config(n_values, cluster_answers)
    min_samples_frame = create_slider_frame(*min_samples_info)

    # eps = 4.8  # depends on distances
    eps_info = dbscan_eps_config(distance_matrix_map["distance_matrix"], distance_matrix_map["min_distance"], n_values)
    eps_frame = create_slider_frame(*eps_info)
    # TODO: plot k_distance_graph

    # n_jobs = None
    n_jobs_info = dbscan_n_jobs_config()
    n_jobs_frame = create_slider_frame(*n_jobs_info)

    frames = [min_samples_frame, eps_frame, n_jobs_frame]
    dependencies = [
        [dbscan_clustering.MIN_SAMPLES, dbscan_clustering.EPS, DEPENDENCY_VALUE_SLIDER_MAX,
         lambda min_samples: calculate_eps_max(distance_matrix_map["distance_matrix"], min_samples)],
    ]
    min_samples, eps, n_jobs = get_configuration_parameters("", frames, dependencies)

    return dbscan_args(eps, min_samples, n_jobs)


def cluster_optics(cluster_answers, distance_matrix_map, values):
    # min_samples = 2
    min_samples_info = optics_min_samples_config(len(values), cluster_answers)
    min_samples_frame = create_slider_frame(*min_samples_info)

    # max_eps = np.inf
    max_eps_info = optics_max_eps_config()
    max_eps_frame = create_slider_frame(*max_eps_info)

    # cluster_method = 'xi'
    cluster_method_info = optics_cluster_method_config()
    cluster_method_frame = create_enum_frame(*cluster_method_info)

    # eps = None
    eps_info = optics_eps_config()
    eps_frame = create_slider_frame(*eps_info)

    # xi = 0.05
    xi_info = optics_xi_config()
    xi_frame = create_slider_frame(*xi_info)

    # predecessor_correction = True
    predecessor_correction_info = optics_predecessor_correction_config()
    predecessor_correction_frame = create_boolean_frame(*predecessor_correction_info)

    # min_cluster_size = None
    min_cluster_size_info = optics_min_cluster_size_config()
    min_cluster_size_frame = create_slider_frame(*min_cluster_size_info)

    # n_jobs = None
    n_jobs_info = optics_n_jobs_config()
    n_jobs_frame = create_slider_frame(*n_jobs_info)

    frames = [min_samples_frame, max_eps_frame, cluster_method_frame, eps_frame, xi_frame,
              predecessor_correction_frame, min_cluster_size_frame,
              n_jobs_frame]
    dependencies = [
        [optics_clustering.EPS, optics_clustering.CLUSTER_METHOD, DEPENDENCY_ENUM_ACTIVATION, {'dbscan': True, 'xi': False}],
        [optics_clustering.XI, optics_clustering.CLUSTER_METHOD, DEPENDENCY_ENUM_ACTIVATION, {'dbscan': False, 'xi': True}],
        [optics_clustering.PREDECESSOR_CORRECTION, optics_clustering.CLUSTER_METHOD, DEPENDENCY_ENUM_ACTIVATION, {'dbscan': False, 'xi': True}],
        [optics_clustering.MIN_CLUSTER_SIZE, optics_clustering.CLUSTER_METHOD, DEPENDENCY_ENUM_ACTIVATION, {'dbscan': False, 'xi': True}],
    ]
    min_samples, max_eps, cluster_method, eps, xi, predecessor_correction, min_cluster_size, \
    n_jobs \
        = get_configuration_parameters("", frames, dependencies)

    if not max_eps:
        max_eps = np.inf
    return optics_args(min_samples, max_eps, cluster_method,
                          eps, xi, predecessor_correction, min_cluster_size,
                          n_jobs)


def cluster_affinity(cluster_answers, distance_matrix_map, values):
    # damping = 0.99
    damping_info = affinity_damping_config()
    damping_frame = create_slider_frame(*damping_info)

    # max_iter = 200
    max_iter_info = affinity_max_iter_config(cluster_answers)
    max_iter_frames = create_slider_frame(*max_iter_info)

    # convergence_iter = 15
    convergence_iter_info = affinity_convergence_iter_config()
    convergence_iter_frame = create_slider_frame(*convergence_iter_info)

    # preference = None
    preference_info = affinity_preference_config(distance_matrix_map["affinity_matrix"])
    preference_frame = create_slider_frame(*preference_info)

    frames = [damping_frame, max_iter_frames, convergence_iter_frame, preference_frame]
    dependencies = [
        [affinity_propagation_clustering.MAX_ITER, affinity_propagation_clustering.CONVERGENCE_ITER, DEPENDENCY_VALUE_SLIDER_MAX, lambda new_max_iter: new_max_iter],
    ]
    damping, max_iter, convergence_iter, preference = get_configuration_parameters("", frames, dependencies)

    if not max_iter:
        max_iter = 200

    if not convergence_iter:
        convergence_iter = 15

    return affinity_args(damping=damping, max_iter=max_iter, convergence_iter=convergence_iter, preference=preference)


def cluster_spectral(cluster_answers, distance_matrix_map, values):
    num_values = len(values)
    # n_clusters = 5
    n_clusters_info = spectral_n_clusters_config(num_values)
    n_clusters_frame = create_slider_frame(*n_clusters_info)

    # eigen_solver = None
    eigen_solver_info = spectral_eigen_solver_config()
    eigen_solver_frame = create_enum_frame(*eigen_solver_info)

    # n_components = n_clusters
    n_components_info = spectral_n_components_config(num_values)
    n_components_frame = create_slider_frame(*n_components_info)

    # n_init = 10
    n_init_info = spectral_n_init_config(num_values)
    n_init_frame = create_slider_frame(*n_init_info)

    # eigen_tol = 0.0
    eigen_tol_info = spectral_eigen_tol_config()
    eigen_tol_frame = create_slider_frame(*eigen_tol_info)

    # assign_labels = 'kmeans'
    assign_labels_info = spectral_assign_labels_config()
    assign_labels_frame = create_enum_frame(*assign_labels_info)

    frames = [n_clusters_frame, eigen_solver_frame, n_components_frame, n_init_frame,
              eigen_tol_frame, assign_labels_frame]
    dependencies = [
        [spectral_clustering.EIGEN_SOLVER, spectral_clustering.EIGEN_TOL, DEPENDENCY_ENUM_ACTIVATION, {'lobpcg': False, 'amg': False, 'arpack': True}],
    ]
    n_clusters, eigen_solver, n_components, n_init, eigen_tol, assign_labels \
        = get_configuration_parameters("", frames, dependencies)

    if not n_components:
        n_components = n_clusters

    return spectral_args(n_clusters, eigen_solver, n_components, n_init, eigen_tol, assign_labels)


def clusters_from_compressed_values(cluster_answers, distance_matrix_map, values):
    return lambda distance_matrix_map, values: list(range(0, len(values)))
