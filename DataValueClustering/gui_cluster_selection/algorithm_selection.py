'''Suggest clusterings algorithms based on answers to questionnaire.'''
from gui_cluster_configuration.cluster_algorithms_gui import cluster_spectral, cluster_affinity, cluster_optics, cluster_dbscan, \
    cluster_kmedoids, cluster_hierarchical
from clustering.affinity_propagation_clustering import affinity_args
from clustering.dbscan_clustering import dbscan_args
from clustering.hierarchical_clustering import hierarchical_args
from clustering.kmedoids_clustering import kmedoids_args
from clustering.optics_clustering import optics_args
from clustering.spectral_clustering import spectral_args

SPECTRAL_CLUSTERING = "Spectral Clustering"
AFFINITY_PROPAGATION = "Affinity Propagation"
OPTICS = "Optics"
DBSCAN = "DBSCAN"
K_MEDOIDS = "KMedoids"
HIERARCHICAL = "Hierarchical"

algorithm_array = [
    # dependencies, not-dependencies, name, configuration view function, clustering function accepting parameters as arguments
    # suggest value if none of the 'not-dependencies' questions were answered with True

    [[], [2],       HIERARCHICAL,           cluster_hierarchical,   hierarchical_args,  "Recommended choice if you do not expect noise in the data."],
    [[], [2, 4],    K_MEDOIDS,              cluster_kmedoids,       kmedoids_args,      "..."],
    [[], [1,3],     DBSCAN,                 cluster_dbscan,         dbscan_args,        "Appropriate if you expect noise in the data. OPTICS may achieve better results."],
    [[], [1],       OPTICS,                 cluster_optics,         optics_args,        "Recommended choice if you expect noise in the data."],
    [[], [0,1,2,4], AFFINITY_PROPAGATION,   cluster_affinity,       affinity_args,      "..."],
    [[], [0,1,2,5], SPECTRAL_CLUSTERING,    cluster_spectral,       spectral_args,      "..."],

]
