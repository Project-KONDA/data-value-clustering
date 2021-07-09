'''Suggest clusterings algorithms based on answers to questionnaire.'''
from gui_cluster_configuration.cluster_algorithms_gui import cluster_spectral, cluster_affinity, cluster_optics, cluster_dbscan, \
    cluster_kmedoids, cluster_hierarchical
from clustering.affinity_propagation_clustering import affinity_args
from clustering.dbscan_clustering import dbscan_args
from clustering.hierarchical_clustering import hierarchical_args
from clustering.kmedoids_clustering import kmedoids_args
from clustering.optics_clustering import optics_args
from clustering.spectral_clustering import spectral_args

algorithm_array = [
    # dependencies, not-dependencies, name, configuration view function, clustering function accepting parameters as arguments
    # suggest value if none of the 'not-dependencies' questions were answered with True

    [[], [2],           "Hierarchical",            cluster_hierarchical,    hierarchical_args],
    [[], [2, 4],        "KMedoids",                cluster_kmedoids,        kmedoids_args],
    [[], [1,3],         "DBSCAN",                  cluster_dbscan,          dbscan_args],
    [[], [1],           "Optics",                  cluster_optics,          optics_args],
    [[], [0,1,2,4],     "Affinity Propagation",    cluster_affinity,        affinity_args],
    [[], [0,1,2,5],     "Spectral Clustering",     cluster_spectral,        spectral_args],

]
