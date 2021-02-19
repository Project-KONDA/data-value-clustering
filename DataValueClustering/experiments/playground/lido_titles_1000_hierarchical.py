from distance.weighted_levenshtein_distance import get_cost_map
from experiments.constants import playground_exports, lido_titles
from export.ExecutionConfiguration import ExecutionConfigurationFromParams

if __name__ == '__main__':

    # specify parameters

    # compression
    compression_answers = "sentence"
    # [true, false, true, true, false, true, false, false, false, true, true, false, false, false, false, false, false, false, true]

    #distance
    weight_case = 1
    regex = ["", "abcdefghijklmnopqrstuvwxyzäöüßáàéèíìóòúù", "ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜÁÀÉÈÍÌÓÒÚÙ", "0123456789", " ", ".,:;!?()[]{}+-*/%=<>&|\"`´'"]
    weights = [
        [0, 1, 2, 4, 3, 12],
        [1, 0, 1, 4, 3, 12],
        [2, 1, 0, 4, 3, 12],
        [4, 4, 4, 0, 3, 12],
        [3, 3, 3, 3, 0, 12],
        [12, 12, 12, 12, 12, 24]
    ]
    costmap = get_cost_map(weight_case, regex, weights)

    # clustering
    algorithm = "hierarchical"
    algorithm_params = [['method', 'ward'], ['n_clusters', 4], ['distance_threshold', None], ['criterion', 'maxclust']]

    # initialize
    object = ExecutionConfigurationFromParams(lido_titles, 1000, compression_answers, "distance_weighted_levenshtein", algorithm, algorithm_params, costmap)

    # execute
    object.execute()

    # save
    object.save(playground_exports)

    # load
    # load = load_ExecutionConfiguration("../data/examples/midas_dates_hierarchical_20210215-133033")
    # load.execute()