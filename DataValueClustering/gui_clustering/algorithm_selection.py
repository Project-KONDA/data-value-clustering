from gui_clustering.cluster_algorithms_gui import cluster_spectral, cluster_affinity, cluster_optics, cluster_dbscan, \
    cluster_kmedoids, cluster_hierarchical

question_array = [
    # dependencies, not-dependencies, name, default, question, explanation

    [[], [],    "fast",             False,  "Is fast clustering desired?",
     "Choose yes if you prefer a fast execution over high quality (i.e. precise) clustering."],
    [[], [],    "deterministic",    False,  "Is deterministic clustering desired?",
     "Choose yes if you want each execution to return the exact same result. Otherwise random initialization may be used."],
    [[], [],    "noise",            True,   "Do you expect noise in the data?",
     "Choose yes if you expect outliers that are very different from the other values and thus do not belong to any of the clusters."],
    [[], [],    "density",          True,   "Do you expect clusters of varying density?",
     "Choose yes if you expect the ratio between the number of included samples and the maximum distance between included samples to vary between clusters. This is relevant for density-based clustering. In density-based clustering, clusters are defined as areas of higher density than the remainder of the data set. In case you are not sure, choose yes."],
    [[], [],    "shape",            True,   "Do you expect clusters of varying shape?",
     "Choose yes if you do not want to make assumptions concerning cluster shape. Choose no if you expect only convex and sphere-shaped clusters with a high density at the center and a decreasing density at the edge. In case you are not sure, choose yes."],
    [[], [],    "size",             True,   "Do you expect clusters of varying size?",
     "Choose yes if you expect varying numbers of values across clusters. In case you are not sure, choose yes."],

]

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
