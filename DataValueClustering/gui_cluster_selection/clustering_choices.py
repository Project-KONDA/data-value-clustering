'''Collection of views for specifying the parameters of the clustering algorithm.'''
import numpy as np

from gui_cluster_configuration.cluster_algorithms_gui import cluster_hierarchical, cluster_kmedoids, cluster_dbscan, \
    cluster_optics, cluster_affinity, cluster_spectral, clusters_from_compressed_values
from gui_cluster_selection.ClusteringQuestionnaireResultInput import cluster_suggest

cluster_algorithms = np.array([
    ["Suggest",
     cluster_suggest],
    ["Hierarchical",
     lambda: (None, cluster_hierarchical)],
    ["KMedoids",
     lambda: (None, cluster_kmedoids)],
    ["DBSCAN",
     lambda: (None, cluster_dbscan)],
    ["Optics",
     lambda: (None, cluster_optics)],
    ["Affinity Propagation",
     lambda: (None, cluster_affinity)],
    ["Spectral Clustering",
     lambda: (None, cluster_spectral)],
    ["None",
     lambda: (None, clusters_from_compressed_values)]
])