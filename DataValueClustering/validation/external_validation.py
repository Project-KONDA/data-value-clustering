import numpy as np
from sklearn.metrics import adjusted_mutual_info_score

from abstraction.abstraction import abstraction_single_value
from gui_center.cluster_representation import fancy_cluster_representation


def get_true_and_pred_clusters_parts(compression_f, values_compressed, clusters_true_fancy, clusters_pred):
    clusters_true_part = get_clusters_true_from_fancy(compression_f, clusters_true_fancy, values_compressed)
    indices = np.array(clusters_true_part[2, :], dtype=int)
    clusters_pred_part = clusters_pred[indices]
    return clusters_true_part[1], clusters_pred_part


def compare_true_and_pred_clusters(score_f, compression_f, values_compressed, clusters_true_fancy, clusters_pred):
    clusters_true_part, clusters_pred_part = get_true_and_pred_clusters_parts(compression_f, values_compressed, clusters_true_fancy, clusters_pred)
    return score_f(clusters_true_part, clusters_pred_part)


def get_clusters_true_from_fancy(compression_f, clusters_true_fancy, values_compressed):
    clusters_true_fancy_compressed = get_clusters_compressed_fancy(clusters_true_fancy, compression_f)
    return get_clusters_true_from_fancy_compressed(clusters_true_fancy_compressed, values_compressed)


def get_clusters_compressed_fancy(clusters_true_fancy, compression_f):
    clusters_true_fancy_compressed = []
    for i, line in enumerate(clusters_true_fancy):
        clusters_true_fancy_compressed.append(compression_f(line)[0].tolist())
    return clusters_true_fancy_compressed


def filter_clusters_true_fancy(clusters_true_fancy, values_compressed, compression_f):
    clusters_true_fancy_compressed_filtered = []
    for x, l in enumerate(clusters_true_fancy):
        l_filtered = []
        for y, v in enumerate(l):
            if abstraction_single_value(v, compression_f) in values_compressed:
                l_filtered.append(v)
        clusters_true_fancy_compressed_filtered.append(l_filtered)
    return clusters_true_fancy_compressed_filtered


def get_clusters_true_from_fancy_compressed(clusters_true_fancy_compressed, values_compressed):
    no_compressed = sum(len(x) for x in clusters_true_fancy_compressed)
    clusters_true = np.empty((3, no_compressed), dtype=object)
    index = 0
    for i, l in enumerate(clusters_true_fancy_compressed):
        for j, v in enumerate(l):
            clusters_true[0, index] = v
            clusters_true[1, index] = i
            clusters_true[2, index] = np.where(values_compressed == v)[0][0]
            index += 1
    # print(compressed_true)
    return clusters_true


def get_pred_clustering_of_true_values(compression_f, clusters_true_fancy, values_compressed, clusters_pred):
    true_values = [item for sublist in clusters_true_fancy for item in sublist]
    pred_clusters_true_values = np.empty(len(true_values), dtype=int)
    for i, v in enumerate(true_values):
        index = np.where(values_compressed == compression_f([v])[0][0])[0][0]
        pred_clusters_true_values[i] = clusters_pred[index]
    return fancy_cluster_representation(true_values, pred_clusters_true_values)


def check_completeness_of_true_values(compression_f, clusters_true_fancy, values_compressed):
    true_values = [item for sublist in clusters_true_fancy for item in sublist]
    true_values_compressed, compression_dict = compression_f(true_values)
    true_values_compressed = set(true_values_compressed)
    values_compressed = set(values_compressed)
    return true_values_compressed == values_compressed, list(values_compressed - true_values_compressed), list(true_values_compressed - values_compressed)


if __name__ == "__main__":
    clusters = np.array([0, 1, 2, 3, 4, 5, 6, 7])
    cc = np.array(["e", "a", "f", "b", "x", "B", "A", "X"])
    f = [
        ["a", "A"],
        ["b", "B"]
    ]
    # print(get_compressed_true_from_fancy(f, cc))
    print(get_true_and_pred_clusters_parts(cc, f, clusters))

    print(compare_true_and_pred_clusters(adjusted_mutual_info_score, cc, f, clusters))


