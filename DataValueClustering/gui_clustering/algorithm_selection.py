from gui_clustering.cluster_algorithms_gui import cluster_spectral, cluster_affinity, cluster_optics, cluster_dbscan, \
    cluster_kmedoids, cluster_hierarchical

algorithm_array = [
    # dependencies, not-dependencies, name
    # suggest value if none of the 'not-dependencies' questions were answered with True

    [[], [2],           "Hierarchical",            cluster_hierarchical],
    [[], [2, 4],        "KMedoids",                cluster_kmedoids],
    [[], [1,3],         "DBSCAN",                  cluster_dbscan],
    [[], [1],           "Optics",                  cluster_optics],
    [[], [0,1,2,4],     "Affinity Propagation",    cluster_affinity],
    [[], [0,1,2,5],     "Spectral Clustering",     cluster_spectral],

]
