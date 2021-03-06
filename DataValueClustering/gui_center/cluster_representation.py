'''Convert between simple cluster representation output by clustering algorithms and more human readable fancy cluster representation.'''


def fancy_cluster_representation(values, clusters):
    outer_list, noise = _fancy_cluster_representation_unsorted(values, clusters)
    cluster_sizes = list(map(len, outer_list))
    sorted_outer_list, order = sort_clusters_counts(outer_list, cluster_sizes)
    return sorted_outer_list, noise


def _fancy_cluster_representation_unsorted(values, clusters):
    n_clusters = max(clusters) + 1
    outer_list = list()
    noise = list()
    for i in range(n_clusters):
        outer_list.append(list())
    for j in range(len(values)):
        x = int(clusters[j])
        if x >= 0:
            outer_list[x].append(values[j])
        else:
            noise.append(values[j])
    return outer_list, noise


def fancy_cluster_representation_abstracted(values_abstracted, clusters_abstracted, values, clusters):
    outer_list_abstracted, noise_abstracted = _fancy_cluster_representation_unsorted(values_abstracted, clusters_abstracted)
    outer_list, noise = _fancy_cluster_representation_unsorted(values, clusters)
    cluster_sizes = list(map(len, outer_list))
    sorted_outer_list_abstracted, order = sort_clusters_counts(outer_list_abstracted, cluster_sizes)
    order = invert_order_list(order)
    return sorted_outer_list_abstracted, noise_abstracted, order


def invert_order_list(order):
    turned = [None] * (max(order)+1)
    for new, old in enumerate(order):
        assert isinstance(old, int)
        turned[old] = new
    return turned


def sort_clusters_counts(clusters, counts):
    if not clusters or not counts:
        return [], []
    order = range(0,len(clusters))
    res = list(zip(*sorted(zip(counts, clusters, order), reverse=True)))
    return list(res[1]), list(res[2])


def fancy_cluster_representation_reverse(values, fancy):
    clusters = list()
    b = False
    for i,v in enumerate(values):
        b = False
        for j,k in enumerate(fancy):
            print(v)
            print(k)
            if v in k:
                clusters.append(j)
                b = True
        if not b:
            raise Exception("problem")
    return clusters
