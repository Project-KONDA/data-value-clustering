from compression.compression import sequence_compression_case_sensitive_function
from distance.weighted_levenshtein_distance import get_cost_map
from experiments.ExecutionConfiguration import ExecutionConfigurationFromParams, load_ExecutionConfiguration
from experiments.experiment import midas_dates, lido_titles

if __name__ == '__main__':

    # specify parameters

    # compression
    compression_answers = "sentence"
    # [true, false, true, true, false, true, false, false, false, true, true, false, false, false, false, false, false, false, true]

    #distance
    weight_case = 1
    regex = ["", "abcdefghijklmnopqrstuvwxyzäöüßáàéèíìóòúù", "ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜÁÀÉÈÍÌÓÒÚÙ", "0123456789", " ", ".,:;!?()[]{}+-*/%=<>&|\"`´'"]
    weights = [
        [0, 1, 2, 4, 3, 24],
        [1, 0, 1, 4, 3, 24],
        [2, 1, 0, 4, 3, 24],
        [4, 4, 4, 0, 3, 24],
        [3, 3, 3, 3, 0, 24],
        [24, 24, 24, 24, 24, 24]
    ]
    costmap = get_cost_map(weight_case, regex, weights)

    # clustering
    algorithm = "spectral"
    algorithm_params = [["n_clusters", 3], ["eigen_solver", None], ["n_components", None], ["n_init", 10], ["eigen_tol", 0.0], ["assign_labels", 'kmeans']]

    # initialize
    object = ExecutionConfigurationFromParams(lido_titles, 1000, compression_answers, "distance_weighted_levenshtein", algorithm, algorithm_params, costmap)

    # execute
    object.execute()

    # save
    object.save("../data/examples/")

    # load
    # load = load_ExecutionConfiguration("../data/examples/midas_dates_hierarchical_20210215-133033")
    # load.execute()