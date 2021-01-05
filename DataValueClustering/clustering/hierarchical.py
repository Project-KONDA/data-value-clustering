

def hierarchical_start(distance_function, values):
    # TODO: ask user for arguments
    #return hierarchical(...)
    pass


def hierarchical(distance_function, values, n_clusters, distance_threshold, method = 'single', criterion = 'inconsistent', depth = 2, monocrit = None):
    pass


def hierarchical_args(n_clusters, distance_threshold, method = 'single', criterion = 'inconsistent', depth = 2, monocrit = None):
    return lambda distance_function, values_compressed: hierarchical(distance_function, values_compressed,
                                                                            n_clusters, distance_threshold, method, criterion, depth, monocrit)