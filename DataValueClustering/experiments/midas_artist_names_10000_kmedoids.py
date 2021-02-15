from compression.compression import sequence_compression_case_sensitive_function
from distance.weighted_levenshtein_distance import get_cost_map
from experiments.ExecutionConfiguration import ExecutionConfigurationFromParams, load_ExecutionConfiguration
from experiments.experiment import midas_dates, midas_artist_names

if __name__ == '__main__':

    # specify parameters

    # compression
    compression_answers = "case-sensitive letter sequences and digit sequences"
    # [true, false, true, true, false, true, false, false, false, true, true, false, false, false, false, false, false, false, true]

    #distance
    weight_case = 1
    regex = ["", "[a-zäöüßáàéèíìóòúù]", "[A-ZÄÖÜÁÀÉÈÍÌÓÒÚÙ]", "[0-9]", " ", "[^a-zäöüßáàéèíìóòúùA-ZÄÖÜÁÀÉÈÍÌÓÒÚÙ0-9 ]"]
    weights = [
        [0, 1, 2, 4, 3, 3],
        [1, 0, 1, 4, 3, 3],
        [2, 1, 0, 4, 3, 3],
        [4, 4, 4, 0, 3, 3],
        [3, 3, 3, 3, 0, 3],
        [3, 3, 3, 3, 3, 3]
    ]
    costmap = get_cost_map(weight_case, regex, weights)

    # clustering
    algorithm = "kmedoids"
    algorithm_params = [["n_clusters", 7], ["init", 'heuristic'], ["max_iter", 200]]

    # initialize
    object = ExecutionConfigurationFromParams(midas_artist_names, 10000, compression_answers, "distance_weighted_levenshtein", algorithm, algorithm_params, costmap)

    # execute
    object.execute()

    # save
    object.save("../data/examples/")

    # load
    # load = load_ExecutionConfiguration("../data/examples/midas_dates_hierarchical_20210215-133033")
    # load.execute()