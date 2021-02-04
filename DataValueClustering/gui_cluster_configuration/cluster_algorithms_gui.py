from clustering import hierarchical, affinity_propagation, dbscan, optics, spectral, kmedoids
from clustering.hierarchical import *
from clustering.kmedoids import *
from clustering.dbscan import *
from clustering.optics import *
from clustering.affinity_propagation import *
from clustering.spectral import *
from gui_cluster_configuration import get_configuration_parameters
from gui_cluster_configuration.dendrogram import show_dendrogram
from gui_cluster_configuration.parameter_frames import create_enum_frame, create_slider_frame, create_boolean_frame


# pass method of this module as cluster_function to clustering.clustering.cluster

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

    # TODO: ask user for additional arguments

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
        [hierarchical.N_CLUSTERS, hierarchical.THRESHOLD, 'activation_activation', False],
        [hierarchical.THRESHOLD, hierarchical.N_CLUSTERS, 'activation_activation', False],
        [hierarchical.N_CLUSTERS, hierarchical.CRITERION, 'activation_enum', {True: ['maxclust', 'maxclust_monocrit'], False: ['distance', 'inconsistent', 'monocrit']}],
        [hierarchical.THRESHOLD, hierarchical.CRITERION, 'activation_enum', {True: ['distance', 'inconsistent', 'monocrit'], False: ['maxclust', 'maxclust_monocrit']}],
        [hierarchical.CRITERION, hierarchical.DEPTH, 'enum_value_activation', {'inconsistent': True, 'maxclust': False, 'maxclust_monocrit': False, 'distance': False, 'monocrit': False}],
        # [hierarchical.CRITERION, hierarchical.MONOCRIT, 'enum_value_activation', {'inconsistent': False, 'maxclust': False, 'maxclust_monocrit': True, 'distance': False, 'monocrit': True}]
    ]
    n_clusters, distance_threshold, criterion, depth = \
        get_configuration_parameters("", frames, dependencies2)

    return hierarchical_lm_args(linkage_matrix, n_clusters, distance_threshold, criterion, depth, None)


def cluster_kmedoids(cluster_answers, distance_matrix_map, values):
    # TODO: show questionnaire if not shown already
    # TODO: ask user for arguments

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

    # min_samples = 3  # depends on number of values
    min_samples_info = dbscan_min_samples_config(len(values), cluster_answers)
    min_samples_frame = create_slider_frame(*min_samples_info)

    # eps = 4.8  # depends on distances
    eps_info = dbscan_eps_config(distance_matrix_map["distance_matrix"], distance_matrix_map["min_distance"])  # TODO: , min_samples)
    eps_frame = create_slider_frame(*eps_info)
    # TODO: plot k_distance_graph

    # algorithm = 'auto'
    algorithm_info = dbscan_algorithm_config()
    algorithm_frame = create_enum_frame(*algorithm_info)

    # leaf_size = 30
    leaf_size_info = dbscan_leaf_size_config()
    leaf_size_frame = create_slider_frame(*leaf_size_info)

    # n_jobs = None
    n_jobs_info = dbscan_n_jobs_config()
    n_jobs_frame = create_slider_frame(*n_jobs_info)

    frames = [min_samples_frame, eps_frame, algorithm_frame, leaf_size_frame, n_jobs_frame]
    dependencies = [
        [dbscan.ALGORITHM, dbscan.LEAF_SIZE, 'enum_value_activation', {'ball_tree': True, 'kd_tree': True, 'auto': False, 'brute': False}],
        [dbscan.MIN_SAMPLES, dbscan.EPS, 'slider_value_slider_max', lambda min_samples: calculate_eps_max(distance_matrix_map["distance_matrix"], min_samples)],
    ]
    min_samples, eps, algorithm, leaf_size, n_jobs = get_configuration_parameters("", frames, dependencies)

    return dbscan_args(eps, min_samples, algorithm, leaf_size, n_jobs)


def cluster_optics(cluster_answers, distance_matrix_map, values):
    # TODO: ask user for arguments
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

    # algorithm = 'auto'
    algorithm_info = optics_algorithm_config()
    algorithm_frame = create_enum_frame(*algorithm_info)

    # leaf_size = 30
    leaf_size_info = optics_leaf_size_config()
    leaf_size_frame = create_slider_frame(*leaf_size_info)

    # n_jobs = None
    n_jobs_info = optics_n_jobs_config()
    n_jobs_frame = create_slider_frame(*n_jobs_info)

    frames = [min_samples_frame, max_eps_frame, cluster_method_frame, eps_frame, xi_frame,
              predecessor_correction_frame, min_cluster_size_frame, algorithm_frame, leaf_size_frame,
              n_jobs_frame]
    dependencies = [
        [dbscan.ALGORITHM, dbscan.LEAF_SIZE, 'enum_value_activation', {'ball_tree': True, 'kd_tree': True, 'auto': False, 'brute': False}],
        [optics.EPS, optics.CLUSTER_METHOD, 'enum_value_activation', {'dbscan': True, 'xi': False}],
        [optics.XI, optics.CLUSTER_METHOD, 'enum_value_activation', {'dbscan': False, 'xi': True}],
        [optics.PREDECESSOR_CORRECTION, optics.CLUSTER_METHOD, 'enum_value_activation', {'dbscan': False, 'xi': True}],
        [optics.MIN_CLUSTER_SIZE, optics.CLUSTER_METHOD, 'enum_value_activation', {'dbscan': False, 'xi': True}],
    ]
    min_samples, max_eps, cluster_method, eps, xi, predecessor_correction, min_cluster_size, \
    algorithm, leaf_size, n_jobs \
        = get_configuration_parameters("", frames, dependencies)

    if not max_eps:
        max_eps = np.inf
    return optics_args(min_samples, max_eps, cluster_method,
                          eps, xi, predecessor_correction, min_cluster_size, algorithm,
                          leaf_size, n_jobs)


def cluster_affinity(cluster_answers, distance_matrix_map, values):
    # TODO: ask user for arguments

    # damping = 0.99
    damping_info = affinity_damping_config()
    damping_frame = create_slider_frame(*damping_info)

    # max_iter = 200
    max_iter_info = affinity_max_iter_config(cluster_answers)
    max_iter_frames = create_slider_frame(*max_iter_info)

    # convergence_iter = 15
    convergence_iter_info = affinity_convergence_iter_config()
    convergence_iter_frame = create_slider_frame(*convergence_iter_info)

    # copy = True
    copy_info = affinity_copy_config()
    copy_frame = create_boolean_frame(*copy_info)

    # preference = None
    preference_info = affinity_preference_config(distance_matrix_map["affinity_matrix"])
    preference_frame = create_slider_frame(*preference_info)

    frames = [damping_frame, max_iter_frames, convergence_iter_frame, copy_frame, preference_frame]
    dependencies = [
        [affinity_propagation.MAX_ITER, affinity_propagation.CONVERGENCE_ITER, 'slider_value_slider_max', lambda new_max_iter: new_max_iter],
    ]
    damping, max_iter, convergence_iter, copy, preference = get_configuration_parameters("", frames, dependencies)

    if not max_iter:
        max_iter = 200

    if not convergence_iter:
        convergence_iter = 15

    return affinity_args(damping, max_iter, convergence_iter, copy, preference)


def cluster_spectral(cluster_answers, distance_matrix_map, values):
    # TODO: ask user for arguments
    # n_clusters = 5
    n_clusters_info = spectral_n_clusters_config(len(values))
    n_clusters_frame = create_slider_frame(*n_clusters_info)

    # eigen_solver = None
    eigen_solver_info = spectral_eigen_solver_config()
    eigen_solver_frame = create_enum_frame(*eigen_solver_info)

    # n_components = n_clusters
    n_components_info = spectral_n_components_config()
    n_components_frame = create_slider_frame(*n_components_info)

    # n_init = 10
    n_init_info = spectral_n_init_config()
    n_init_frame = create_slider_frame(*n_init_info)

    # gamma = 1.0
    gamma_info = spectral_gamma_config()
    gamma_frame = create_slider_frame(*gamma_info)

    # eigen_tol = 0.0
    eigen_tol_info = spectral_eigen_tol_config()
    eigen_tol_frame = create_slider_frame(*eigen_tol_info)

    # assign_labels = 'kmeans'
    assign_labels_info = spectral_assign_labels_config()
    assign_labels_frame = create_enum_frame(*assign_labels_info)

    frames = [n_clusters_frame, eigen_solver_frame, n_components_frame, n_init_frame, gamma_frame,
              eigen_tol_frame, assign_labels_frame]
    dependencies = [
        [spectral.EIGEN_SOLVER, spectral.EIGEN_TOL, 'enum_value_activation', {'lobpcg': False, 'amg': False, 'arpack': True}],
    ]
    n_clusters, eigen_solver, n_components, n_init, gamma, eigen_tol, assign_labels \
        = get_configuration_parameters("", frames, dependencies)

    if not n_components:
        n_components = n_clusters

    return spectral(values, n_clusters, eigen_solver, n_components, n_init, gamma, eigen_tol, assign_labels)


def clusters_from_compressed_values(cluster_answers, distance_matrix_map, values):
    return lambda distance_matrix_map, values: list(range(0, len(values)))
