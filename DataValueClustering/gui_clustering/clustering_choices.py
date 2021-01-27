import numpy as np

from gui_clustering.cluster_algorithms_gui import cluster_hierarchical, cluster_kmedoids, cluster_dbscan, \
    cluster_optics, cluster_affinity, cluster_spectral, clusters_from_compressed_values
from gui_clustering.clustering_questionnaire import cluster_suggest

cluster_algorithms = np.array([
    ["Suggest",
     cluster_suggest],
    ["Hierarchical",
     cluster_hierarchical],
    ["KMedoids",
     cluster_kmedoids],
    ["DBSCAN",
     cluster_dbscan],
    ["Optics",
     cluster_optics],
    ["Affinity Propagation",
     cluster_affinity],
    ["Spectral Clustering",
     cluster_spectral],
    ["None", lambda: clusters_from_compressed_values]
])