import numpy as np
from sklearn.metrics import adjusted_mutual_info_score


def get_true_and_pred_clusters_parts(values_compressed, clusters_true_fancy, clusters_pred):
    clusters_true_part = get_clusters_true_from_fancy(clusters_true_fancy, values_compressed)
    indices = np.array(clusters_true_part[2, :], dtype=int)
    clusters_pred_part = clusters_pred[indices]
    return clusters_true_part[1], clusters_pred_part


def compare_true_and_pred_clusters(score_f, values_compressed, clusters_true_fancy, clusters_pred):
    clusters_true_part, clusters_pred_part = get_true_and_pred_clusters_parts(values_compressed, clusters_true_fancy, clusters_pred)
    return score_f(clusters_true_part, clusters_pred_part)


def get_clusters_true_from_fancy(clusters_true_fancy, values_compressed):
    no_compressed = sum(len(x) for x in clusters_true_fancy)
    clusters_true = np.empty((3, no_compressed), dtype=object)
    index = 0
    for i, l in enumerate(clusters_true_fancy):
        for j, v in enumerate(l):
            clusters_true[0, index] = v
            clusters_true[1, index] = i
            clusters_true[2, index] = np.where(values_compressed == v)[0][0]
            index += 1
    # print(compressed_true)
    return clusters_true


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

