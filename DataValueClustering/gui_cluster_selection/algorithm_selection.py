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

    [[], [2],       HIERARCHICAL,           cluster_hierarchical,   hierarchical_args,  "Recommended. Easy parameter configuration."],
    [[], [2, 4],    K_MEDOIDS,              cluster_kmedoids,       kmedoids_args,      "Easy parameter configuration."],
    [[], [1],       OPTICS,                 cluster_optics,         optics_args,        "Advanced parameter configuration. Typically interprets a lot of values as noise.\nSimilar to DBSCAN but can find clusters of varying density."],
    [[], [1,3],     DBSCAN,                 cluster_dbscan,         dbscan_args,        "Expert parameter configuration. Typically interprets a lot of values as noise. \nSimilar to OPTICS but tends to find clusters of similar density. Prefer OPTICS."],
    [[], [0,1,2,4], AFFINITY_PROPAGATION,   cluster_affinity,       affinity_args,      "Expert parameter configuration. Tends to find clusters of globular shape."],
    [[], [0,1,2,5], SPECTRAL_CLUSTERING,    cluster_spectral,       spectral_args,      "Expert parameter configuration. Tends to find clusters of similar size."],

]
