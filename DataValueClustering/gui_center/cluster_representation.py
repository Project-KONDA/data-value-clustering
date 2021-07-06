'''Convert between simple cluster representation output by clustering algorithms and more human readable fancy cluster representation.'''
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
