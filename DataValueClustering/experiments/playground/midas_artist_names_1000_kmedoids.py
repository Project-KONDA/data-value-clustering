from distance.weighted_levenshtein_distance import get_cost_map
from experiments.constants import playground_exports, midas_artist_names
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
        [0, 1, 1, 6, 2, 10],
        [1, 0, 1, 6, 2, 10],
        [1, 1, 0, 6, 2, 10],
        [6, 6, 6, 0, 6, 10],
        [2, 2, 2, 6, 0, 12],
        [12, 12, 12, 12, 12, 12]
    ]
    costmap = get_cost_map(weight_case, regex, weights)

    # clustering
    algorithm = "kmedoids"
    algorithm_params = [["n_clusters", 4], ["init", 'heuristic'], ["max_iter", 200]]

    # initialize
    object = ExecutionConfigurationFromParams(midas_artist_names, 0, 1000, compression_answers,
                                              "distance_weighted_levenshtein", algorithm, algorithm_params, costmap)

    # execute
    object.execute()

    # save
    object.save(playground_exports)

    # load
    # load = load_ExecutionConfiguration("../data/examples/midas_dates_hierarchical_20210215-133033")
    # load.execute()