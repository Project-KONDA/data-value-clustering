from distance.weighted_levenshtein_distance import get_cost_map
from experiments.constants import midas_measurements, evaluation_exports
from experiments.playground.midas_measurements_expectation import midas_measurement_expectation_10000
from export.ExecutionConfiguration import ExecutionConfigurationFromParams

if __name__ == '__main__':
    # specify parameters

    # compression
    compression_answers = "case-sensitive letter sequences and digit sequences"
    # [true, false, true, true, false, true, false, false, false, true, true, false, false, false, false, false, false, false, true]

    # distance
    weight_case = 1
    regex = ["",
             " abcdefghijklmnopqrstuvwxyzäöüßáàéèíìóòúùABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜÁÀÉÈÍÌÓÒÚÙ0123456789",
             ".,:;!?",
             "()[]{}",
             "<rest>"]
    weights = [
        [0, 1, 1, 16, 16],
        [1, 1, 1, 16, 16],
        [1, 1, 1, 16, 16],
        [16, 16, 16, 16, 16],
        [16, 16, 16, 16, 16]
    ]
    costmap = get_cost_map(weight_case, regex, weights)

    # clustering
    algorithm = "hierarchical"
    algorithm_params = [['method', 'single'], ['n_clusters', 10], ['distance_threshold', None], ['criterion', 'maxclust']]
    # algorithm_params = [["min_samples", 2], ["max_eps", 20], ["cluster_method", 'xi'], ["eps", None], ["xi", 0.05],
    #                     ["predecessor_correction", True], ["min_cluster_size", None], ["n_jobs", None]]
    #
    # algorithm_params = [["n_clusters", 10], ["eigen_solver", None], ["n_components", None], ["n_init", 10], ["eigen_tol", 0.0], ["assign_labels", 'kmeans']]

    # initialize
    object = ExecutionConfigurationFromParams(midas_measurements, 0, 10000, compression_answers,
                                              "distance_weighted_levenshtein", algorithm, algorithm_params, costmap,
                                              midas_measurement_expectation_10000)

    # execute
    object.execute()

    # save
    object.save(evaluation_exports)

    # load
    # load = load_ExecutionConfiguration("../data/examples/midas_dates_hierarchical_20210215-133033")
    # load.execute()
