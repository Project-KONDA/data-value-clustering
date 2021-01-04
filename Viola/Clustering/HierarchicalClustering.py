from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster, cophenet
from Clustering.Clustering import use_unique_values_as_clusters, user_config
from Util.DistanceMatrixHandling import condense_distance_matrix
from Util.ClusterHandling import decrease_by_one


def hierarchical_clustering_args(n_clusters, distance_threshold, linkage_criterion):
    return lambda original_values, compressed_values, unique_values, distance_matrix, cluster_original_values:\
        hierarchical_clustering(original_values, compressed_values, unique_values, n_clusters, distance_threshold, distance_matrix, linkage_criterion, cluster_original_values)


def hierarchical_clustering(original_values, compressed_values, unique_values, n_clusters, distance_threshold,
                            distance_matrix,
                            linkage_criterion, cluster_original_values):
    if (not (n_clusters is None) and len(unique_values) <= n_clusters) or (
            not (distance_threshold is None) and distance_threshold == 0):
        return use_unique_values_as_clusters(cluster_original_values, compressed_values, unique_values)[0]

    if cluster_original_values:
        values = original_values
    else:
        values = unique_values

    linkage_matrix = perform_hierarchical_clustering(values, distance_matrix, linkage_criterion)

    if n_clusters is None and distance_threshold is None:
        n_clusters, distance_threshold = user_config(n_clusters, distance_threshold)

    if (not (n_clusters is None) and len(unique_values) <= n_clusters) or (
            not (distance_threshold is None) and distance_threshold == 0):
        return use_unique_values_as_clusters(cluster_original_values, compressed_values, unique_values)[0]
    else:
        return form_flat_clusters(linkage_matrix, n_clusters, distance_threshold)


def perform_hierarchical_clustering(values, distance_matrix, linkage_criterion):
    assert linkage_criterion in ['single', 'complete', 'average', 'weighted', 'centroid', 'median', 'ward']
    condensed_distance_matrix = condense_distance_matrix(distance_matrix)
    linkage_matrix = linkage(condensed_distance_matrix,
                             linkage_criterion)
    print("linkage_matrix = ")
    print(linkage_matrix)
    c, coph_dists = cophenet(linkage_matrix, condensed_distance_matrix)
    print("cophentic correlation distance of dendrogram = " + str(c))
    show_dendrogram(linkage_matrix, values)
    return linkage_matrix


def form_flat_clusters(linkage_matrix, n_clusters, distance_threshold):
    if not (n_clusters is None):
        return decrease_by_one(fcluster(linkage_matrix, n_clusters, 'maxclust'))
    elif not (distance_threshold is None):
        return decrease_by_one(fcluster(linkage_matrix, distance_threshold, 'distance'))
    # other criteria: 'inconsistent', 'monocrit', 'maxclust_monocrit'


def show_dendrogram(linkage_matrix, values):
    plt.figure(figsize=(10, 7))
    dendrogram(linkage_matrix,
               orientation='top',
               labels=values,
               distance_sort='descending',
               show_leaf_counts=True)
    plt.show()


# def calculate_clusters(distance_matrix, n_clusters, distance_threshold, linkage_criterion):
#     #print("distance_matrix: " + str(distance_matrix))
#     if not (n_clusters is None):
#         clustering = AgglomerativeClustering(n_clusters=n_clusters, affinity='precomputed',
#                                              linkage=linkage_criterion)
#     elif not (distance_threshold is None):
#         clustering = AgglomerativeClustering(n_clusters=None, affinity='precomputed',
#                                              linkage=linkage_criterion, distance_threshold=distance_threshold,
#                                              compute_full_tree=True)
#     else:
#         return None
#
#     clustering.fit_predict(distance_matrix)
#     return clustering
