from scipy.cluster.hierarchy import cophenet


def cophenetic_distance(linkage_matrix, condensed_distance_matrix):
    cophentic_correlation_distance, condensed_cophenetic_distance_matrix = cophenet(linkage_matrix, condensed_distance_matrix)