from sklearn.cluster import DBSCAN

from clustering.clustering import fancy_cluster_representation
from utility.distance_matrix import calculate_distance_matrix, get_condensed, min_distance, max_distance, avg_distance


def dbscan(distance_function, values, eps=0.5, min_samples=5, algorithm='auto', leaf_size=30, n_jobs=None):
    dm = calculate_distance_matrix(distance_function, values)
    clusters = DBSCAN(eps=eps, min_samples=min_samples, metric='precomputed', algorithm=algorithm, leaf_size=leaf_size, n_jobs=n_jobs).fit_predict(dm)
    return clusters


def min_samples_config(no_values, answers):
    name = "min_samples"
    explanation = "Higher values will yield less clusters."
    min_min_samples = 3
    max_min_samples = no_values

    # TODO:
    noise_factor = 1
    noisy = False  # TODO: extract from answers
    if(noisy):
        noise_factor = 1.5  # TODO: experiment
    suggestion_min = max(no_values/2000 * noise_factor, min_min_samples)  # TODO: experiment
    suggestion_max = min(no_values/50 * noise_factor, max_min_samples)  # TODO: experiment
    suggestion_value = suggestion_min  # TODO: experiment

    # increase if a) noisy , b) big data set or c) data contains many duplicates

    return name, explanation, min_min_samples, max_min_samples, suggestion_min, suggestion_max, suggestion_value


def eps_config(distance_matrix, no_values):
    name = "eps"
    explanation = "Higher values will yield less clusters."

    # min_eps = min(distances_to_k_nearest) # TODO
    # max_eps = max_value_distance or max(distances_to_k_nearest) # TODO

    # if eps is chosen much too small, a large part of the data will not be clustered
    # whereas for a too high value of eps, clusters will merge and the majority of objects will be in the same cluster

    # The value for eps can then be chosen by using a k-distance graph,
    # plotting the distance to the k = minPts-1 nearest neighbor ordered from the largest to the smallest value
    # good values of eps are where this plot shows an “elbow”
    # TODO: calculate graph and plot

    # In general, small values of eps are preferable
    # as a rule of thumb, only a small fraction of points should be within this distance of each other
    pass

    # return name, explanation, min_min_samples, max_min_samples, suggestion_min, suggestion_max, suggestion_value


if __name__ == '__main__':
    v = [1, 1, 1, 3, 4, 5, 10, 100, 3]
    c = dbscan(lambda a, b: abs(a - b), v, eps=0.1, min_samples=2)
    # print(c)
    print(fancy_cluster_representation(v, c))
