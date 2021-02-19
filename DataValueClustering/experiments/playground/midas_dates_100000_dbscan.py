from distance.weighted_levenshtein_distance import get_cost_map
from experiments.constants import playground_exports, midas_dates
from export.ExecutionConfiguration import ExecutionConfigurationFromParams

if __name__ == '__main__':

    # specify parameters

    # compression
    compression_answers = "case-sensitive letter sequences and digit sequences"
    # [true, false, true, true, false, true, false, false, false, true, true, false, false, false, false, false, false, false, true]

    #distance
    weight_case = 1
    regex = ["", "abcdefghijklmnopqrstuvwxyzäöüßáàéèíìóòúù", "ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜÁÀÉÈÍÌÓÒÚÙ", "0123456789", " ", ".,:;!?()[]{}+-*/%=<>&|\"`´'"]
    weights = [
        [0, 2, 2, 1, 3, 3],
        [2, 0, 1, 3, 3, 3],
        [2, 1, 0, 3, 3, 3],
        [1, 3, 3, 0, 3, 3],
        [3, 3, 3, 3, 0, 3],
        [3, 3, 3, 3, 3, 3]
    ]
    # weights = [
    #     [0, 2, 2, 1, 2, 6],
    #     [2, 0, 1, 2, 2, 6],
    #     [2, 1, 0, 2, 2, 6],
    #     [1, 2, 2, 0, 2, 6],
    #     [2, 2, 2, 2, 0, 6],
    #     [6, 6, 6, 6, 6, 12]
    # ]
    costmap = get_cost_map(weight_case, regex, weights)

    # clustering
    algorithm = "dbscan"
    algorithm_params = [["eps", 3], ["min_samples", 3], ["n_jobs", None]]

    # initialize
    object = ExecutionConfigurationFromParams(midas_dates, 100000, compression_answers, "distance_weighted_levenshtein", algorithm, algorithm_params, costmap)

    # execute
    object.execute()

    # save
    object.save(playground_exports)

    # load
    # load = load_ExecutionConfiguration("../data/examples/midas_dates_hierarchical_20210215-133033")
    # load.execute()