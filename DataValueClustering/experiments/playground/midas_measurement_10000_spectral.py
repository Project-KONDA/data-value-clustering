from distance.weighted_levenshtein_distance import get_cost_map
from experiments.constants import playground_exports
from export.ExecutionConfiguration import ExecutionConfigurationFromParams
from experiments.experiment import midas_measurements

if __name__ == '__main__':
    # specify parameters

    # compression
    compression_answers = "case-sensitive letter sequences and digit sequences"
    # [true, false, true, true, false, true, false, false, false, true, true, false, false, false, false, false, false, false, true]

    # distance
    weight_case = 1
    regex = ["", "abcdefghijklmnopqrstuvwxyzäöüßáàéèíìóòúù", "ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜÁÀÉÈÍÌÓÒÚÙ", "0123456789", " ", ".,:;!?()[]{}",  "<rest>"] # "+-*/%=<>&|",
    weights = [
        [0, 1, 1, 4, 4, 16, 32],
        [1, 0, 1, 4, 4, 16, 32],
        [1, 1, 0, 4, 4, 16, 32],
        [4, 4, 4, 0, 4, 16, 32],
        [4, 4, 4, 4, 4, 16, 32],
        [16, 16, 16, 16, 16, 16, 32],
        [32, 32, 32, 32, 32, 32, 32]
    ]
    costmap = get_cost_map(weight_case, regex, weights)

    # clustering
    algorithm = "spectral"
    # algorithm_params = [['method', 'single'], ['n_clusters', 11], ['distance_threshold', None], ['criterion', 'maxclust']]
    # algorithm_params = [["min_samples", 2], ["max_eps", 20], ["cluster_method", 'xi'], ["eps", None], ["xi", 0.05],
    #                     ["predecessor_correction", True], ["min_cluster_size", None], ["n_jobs", None]]

    algorithm_params = [["n_clusters", 7], ["eigen_solver", None], ["n_components", None], ["n_init", 10], ["eigen_tol", 0.0], ["assign_labels", 'kmeans']]

    # initialize
    object = ExecutionConfigurationFromParams(midas_measurements, 1000, compression_answers, "distance_weighted_levenshtein",
                                              algorithm, algorithm_params, costmap)

    # execute
    object.execute()

    # save
    object.save(playground_exports)

    # load
    # load = load_ExecutionConfiguration("../data/examples/midas_dates_hierarchical_20210215-133033")
    # load.execute()
