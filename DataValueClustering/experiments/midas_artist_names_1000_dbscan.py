from compression.compression import sequence_compression_case_sensitive_function
from distance.weighted_levenshtein_distance import get_cost_map
from experiments.ExecutionConfiguration import ExecutionConfigurationFromParams, load_ExecutionConfiguration
from experiments.experiment import midas_dates, midas_artist_names

if __name__ == '__main__':

    # specify parameters

    # compression
    compression_answers = "letter sequences and digit sequences"
    # [true, false, true, true, false, true, false, false, false, true, true, false, false, false, false, false, false, false, true]

    #distance
    weight_case = 1
    regex = ["", "abcdefghijklmnopqrstuvwxyzäöüßáàéèíìóòúù", "ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜÁÀÉÈÍÌÓÒÚÙ", "0123456789", " ", ".,:;!?()[]{}+-*/%=<>&|\"`´'"]
    weights = [
        [0, 1, 1, 6, 2, 10],
        [1, 0, 1, 6, 2, 10],
        [1, 1, 0, 6, 2, 10],
        [6, 6, 6, 0, 6, 10],
        [2, 2, 2, 6, 0, 12],
        [12, 12, 12, 12, 12, 12]
    ]
    costmap = get_cost_map(weight_case, regex, weights)

    # clustering
    algorithm = "dbscan"
    algorithm_params = [["eps", 3], ["min_samples", 3], ["n_jobs", None]]

    # initialize
    object = ExecutionConfigurationFromParams(midas_artist_names, 1000, compression_answers, "distance_weighted_levenshtein", algorithm, algorithm_params, costmap)

    # execute
    object.execute()

    # save
    object.save("../data/examples/")

    # load
    # load = load_ExecutionConfiguration("../data/examples/midas_dates_hierarchical_20210215-133033")
    # load.execute()