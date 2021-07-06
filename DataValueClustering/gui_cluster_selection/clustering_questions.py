'''Questionnaire configuration for suggesting clustering algorithms.'''
clustering_question_array = [
    # dependencies, not-dependencies, name, default, question, explanation

    [[], [],    "fast",             False,  "Is fast clustering desired?",
     "Choose yes if you prefer a fast execution over high quality (i.e. precise) clustering."],
    [[], [],    "deterministic",    False,  "Is deterministic clustering desired?",
     "Choose yes if you want each execution to return the exact same result.\n"
     + "Otherwise random initialization may be used."],
    [[], [],    "noise",            False,   "Do you expect noise in the data?",
     "Choose yes if you expect outliers that are very different from the other values\n"
     + "and thus do not belong to any of the clusters."],
    [[], [],    "density",          True,   "Do you expect clusters of varying density?",
     "Choose yes if you expect the ratio between the number of included samples and the\n"
     + "maximum distance between included samples to vary between clusters.\n"
     + "This is relevant for density-based clustering. In density-based clustering,\n"
     + "clusters are defined as areas of higher density than the remainder of the data set.\n"
     + "In case you are not sure, choose yes."],
    [[], [],    "shape",            True,   "Do you expect clusters of varying shape?",
     "Choose yes if you do not want to make assumptions concerning cluster shape.\n"
     + "Choose no if you expect only convex and sphere-shaped clusters with a high density\n"
     + "at the center and a decreasing density at the edge. In case you are not sure, choose yes."],
    [[], [],    "size",             True,   "Do you expect clusters of varying size?",
     "Choose yes if you expect varying numbers of values across clusters. In case you are not sure, choose yes."],

]