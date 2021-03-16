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
    # regex = ["", "abcdefghijklmnopqrstuvwxyzäöüßáàéèíìóòúù", "ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜÁÀÉÈÍÌÓÒÚÙ", "0123456789", " ", ".,:;!?()[]{}+-*/%=<>&|"]
    regex = ["", "abcdefghijklmnopqrstuvwxyzäöüßáàéèíìóòúù", "ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜÁÀÉÈÍÌÓÒÚÙ", "0123456789", " ", ".,:;!?()[]{}\"`´'",  "<rest>"] # "+-*/%=<>&|",

    weights = [
        [0, 1, 1, 4, 4, 16, 32],
        [1, 0, 1, 4, 4, 16, 32],
        [1, 1, 0, 4, 4, 16, 32],
        [4, 4, 4, 0, 4, 16, 32],
        [4, 4, 4, 4, 4, 16, 32],
        [16, 16, 16, 16, 16, 16, 32],
        [32, 32, 32, 32, 32, 32, 32]
    ]
    # weights = [
    #     [0, 2, 2, 1, 3, 3],
    #     [2, 0, 1, 3, 3, 3],
    #     [2, 1, 0, 3, 3, 3],
    #     [1, 3, 3, 0, 3, 3],
    #     [3, 3, 3, 3, 0, 3],
    #     [3, 3, 3, 3, 3, 3]
    # ]
    costmap = get_cost_map(weight_case, regex, weights)

    # clustering
    algorithm = "spectral"
    algorithm_params = [["n_clusters", 12], ["eigen_solver", None], ["n_components", None], ["n_init", 10], ["eigen_tol", 0.0], ["assign_labels", 'kmeans']]

    # initialize
    object = ExecutionConfigurationFromParams(midas_dates, 0, 100000, compression_answers,
                                              "distance_weighted_levenshtein", algorithm, algorithm_params, costmap)

    # execute
    object.execute()

    # save
    object.save(playground_exports)

    # load
    # load = load_ExecutionConfiguration("../data/examples/midas_dates_hierarchical_20210215-133033")
    # load.execute()