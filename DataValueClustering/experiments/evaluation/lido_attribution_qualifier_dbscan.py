from distance.weighted_levenshtein_distance import get_cost_map
from experiments.constants import playground_exports, lido_attribution_qualifier
from experiments.evaluation.lido_attribution_qualifier_expectation import lido_attribution_qualifier_expecation
from export.ExecutionConfiguration import ExecutionConfigurationFromParams

if __name__ == '__main__':

    # specify parameters

    # compression
    compression_answers = "Duplicate Removal" #"letters, digits" #"case-sensitive letter sequences and digit sequences"
    # [true, false, true, true, false, true, false, false, false, true, true, false, false, false, false, false, false, false, true]

    #distance
    weight_case = 1
    regex = ["", "abcdefghijklmnopqrstuvwxyzäöüßáàéèíìóòúù", "ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜÁÀÉÈÍÌÓÒÚÙ", "0123456789", " ", ".,:;!?()[]{}+-*/%=<>&|\"`´'"]
    weights = [
        [0, 1, 2, 3, 12, 12],
        [1, 0, 2, 3, 12, 12],
        [2, 2, 0, 3, 12, 12],
        [3, 3, 3, 0, 12, 12],
        [12, 12, 12, 12, 12, 12],
        [12, 12, 12, 12, 12, 12]
    ]
    # weights = [
    #     [0, 1, 2, 5, 3, 4],
    #     [1, 0, 1, 5, 3, 4],
    #     [2, 1, 0, 5, 3, 4],
    #     [4, 4, 4, 0, 3, 4],
    #     [3, 3, 3, 3, 0, 4],
    #     [4, 4, 4, 4, 4, 12]
    # ]
    costmap = get_cost_map(weight_case, regex, weights)

    # clustering
    # algorithm = "affinity"
    # algorithm_params = [["damping", 0.5], ["max_iter", 200], ["convergence_iter", 15], ["preference", None]]
    algorithm = "dbscan"
    algorithm_params = [["eps", 10], ["min_samples", 3], ["n_jobs", None]]

    # initialize
    object = ExecutionConfigurationFromParams(
        lido_attribution_qualifier,
        1000000,
        compression_answers,
        "distance_weighted_levenshtein",
        algorithm,
        algorithm_params,
        costmap,
        lido_attribution_qualifier_expecation
    )

    # execute
    object.execute()

    # save
    object.save(playground_exports)

    # load
    # load = load_ExecutionConfiguration("../data/examples/midas_dates_hierarchical_20210215-133033")
    # load.execute()