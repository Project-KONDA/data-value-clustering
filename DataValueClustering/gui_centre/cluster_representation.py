def fancy_cluster_representation(values, clusters):
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