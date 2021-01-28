import numpy as np

from gui_cluster_configuration.cluster_algorithms_gui import cluster_hierarchical, cluster_kmedoids, cluster_dbscan, \
    cluster_optics, cluster_affinity, cluster_spectral, clusters_from_compressed_values
from gui_cluster_selection.ClusteringQuestionnaireResultInput import cluster_suggest

cluster_algorithms = np.array([
    ["Suggest",
     cluster_suggest],
    ["Hierarchical",
     lambda: cluster_hierarchical],
    ["KMedoids",
     lambda: cluster_kmedoids],
    ["DBSCAN",
     lambda: cluster_dbscan],
    ["Optics",
     lambda: cluster_optics],
    ["Affinity Propagation",
     lambda: cluster_affinity],
    ["Spectral Clustering",
     lambda: cluster_spectral],
    ["None",
     lambda: clusters_from_compressed_values]
])