from compression.compression import sequence_compression_case_sensitive_function
from distance.weighted_levenshtein_distance import get_cost_map
from experiments.ExecutionConfiguration import ExecutionConfigurationFromParams, load_ExecutionConfiguration
from experiments.experiment import midas_dates, lido_titles, lido_attribution_qualifier

if __name__ == '__main__':

    # specify parameters

    # compression
    compression_answers = "case-sensitive letter sequences and digit sequences"
    # [true, false, true, true, false, true, false, false, false, true, true, false, false, false, false, false, false, false, true]

    #distance
    weight_case = 1
    regex = ["", "abcdefghijklmnopqrstuvwxyzäöüßáàéèíìóòúù", "ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜÁÀÉÈÍÌÓÒÚÙ", "0123456789", " ", ".,:;!?()[]{}+-*/%=<>&|"]
    weights = [
        [0, 1, 2, 5, 3, 4],
        [1, 0, 1, 5, 3, 4],
        [2, 1, 0, 5, 3, 4],
        [4, 4, 4, 0, 3, 4],
        [3, 3, 3, 3, 0, 4],
        [4, 4, 4, 4, 4, 4]
    ]
    costmap = get_cost_map(weight_case, regex, weights)

    # clustering
    algorithm = "affinity"
    algorithm_params = [["damping", 0.5], ["max_iter", 200], ["convergence_iter", 15], ["preference", None]]

    # initialize
    object = ExecutionConfigurationFromParams(lido_attribution_qualifier, 10000, compression_answers, "distance_weighted_levenshtein", algorithm, algorithm_params, costmap)

    # execute
    object.execute()

    # save
    object.save("../data/examples/")

    # load
    # load = load_ExecutionConfiguration("../data/examples/midas_dates_hierarchical_20210215-133033")
    # load.execute()