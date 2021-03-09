import numpy as np

from distance.weighted_levenshtein_distance import get_cost_map
from experiments.constants import midas_dates, evaluation_exports, lido_measurement_unit, lido_titles, \
    lido_repository_names
from experiments.evaluation.lido_measurement_unit_expectation import lido_measurement_unit_100000_expectation
from experiments.evaluation.lido_repository_names_expectation import lido_repository_names_expectation
from experiments.evaluation.lido_titles_expectation import lido_titles_1000_expectation, lido_titles_1000_expectation_v2
from experiments.evaluation.midas_dates_expectation import midas_dates_10000_expectation
from export.ExecutionConfiguration import ExecutionConfigurationFromParams




if __name__ == '__main__':
    # specify parameters

    # compression
    compression_answers = [True, True, False, False, True, False, False, False, True,
                             True, True, False,
                             False, False, False, False, False, False,
                             True]

    #distance
    weight_case = 1
    regex = ["", "abcdefghijklmnopqrstuvwxyzäöüßáàéèíìóòúù", "ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜÁÀÉÈÍÌÓÒÚÙ", "0123456789", " ", ".-", ":,;!?[]{}()+—*/%=<>&|\"`´'" , "<rest>"]
    weights = [
        #         a      A      1      _     .-       $       r
        [   0,   500,   500,   170,   600,   150,   1501,    16],  #
        [ 500,     0,   128,   500,   600,   500,   1501,   500],  # a
        [ 500,   128,     0,   500,   600,   500,   1501,   500],  # A
        [ 170,   500,   500,     0,   600,   170,   1501,   170],  # 1
        [ 600,   600,   600,   600,     0,   600,   1501,   600],  # _
        [ 150,   500,   500,   170,   600,   150,   2401,   150],  # .-
        [1501,  1501,  1501,  1501,  1501,  2401,   2651,  1501],  # $
        [  16,   500,   500,   170,   600,   150,   1501,    16],  # r
    ]

    costmap = get_cost_map(weight_case, regex, weights)

    # clustering
    algorithm = "hierarchical"
    algorithm_params = [['method', 'complete'], ['n_clusters', 32], ['distance_threshold', None], ['criterion', 'maxclust']]

    # initialize
    object = ExecutionConfigurationFromParams(lido_repository_names, 1000, compression_answers, "distance_weighted_levenshtein", algorithm, algorithm_params, costmap,
                                              lido_repository_names_expectation)

    # execute
    object.execute()

    # save
    object.save(evaluation_exports)

    print("symmetric:", np.allclose(np.array(weights), np.array(weights).T))

    # load
    # load = load_ExecutionConfiguration("../data/examples/midas_dates_hierarchical_20210215-133033")
    # load.execute()