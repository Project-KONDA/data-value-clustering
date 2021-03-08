import numpy as np

from distance.weighted_levenshtein_distance import get_cost_map
from experiments.constants import midas_dates, evaluation_exports, lido_measurement_unit, lido_titles
from experiments.evaluation.lido_measurement_unit_expectation import lido_measurement_unit_100000_expectation
from experiments.evaluation.lido_titles_expectation import lido_titles_1000_expectation
from experiments.evaluation.midas_dates_expectation import midas_dates_10000_expectation
from export.ExecutionConfiguration import ExecutionConfigurationFromParams

if __name__ == '__main__':
    # specify parameters

    # compression
    compression_answers = [True, True, False, False, True, False, False, False, True,
                             True, False, False,
                             False, False, False, False, False, False,
                             True]

    #distance
    weight_case = 1
    regex = ["", "abcdefghijklmnopqrstuvwxyzäöüßáàéèíìóòúù", "ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜÁÀÉÈÍÌÓÒÚÙ", "0123456789", " ", ":,.;!?[]{}()+-*/%=<>&|\"`´'" , "<rest>"]
    weights = [
        #         a      A      1      _      $     r
        [   0,   256,   256,   400,   500,  1000,   16],  #
        [ 256,     0,   128,   400,   500,  1000,  256],  # a
        [ 256,   128,     0,   400,   500,  1000,  256],  # A
        [ 400,   400,   400,     0,   500,  1000,  400],  # 1
        [ 500,   500,   500,   500,     0,  1000,  500],  # _
        [1000,  1000,  1000,  1000,  1000,  2500, 1000],  # $
        [  16,   256,   256,   400,   500,  1000,   16],  # r
    ]

    costmap = get_cost_map(weight_case, regex, weights)

    # clustering
    algorithm = "hierarchical"
    algorithm_params = [['method', 'complete'], ['n_clusters', 17], ['distance_threshold', None], ['criterion', 'maxclust']]

    # initialize
    object = ExecutionConfigurationFromParams(lido_titles, 1000, compression_answers, "distance_weighted_levenshtein", algorithm, algorithm_params, costmap,
                                              lido_titles_1000_expectation)

    # execute
    object.execute()

    # save
    object.save(evaluation_exports)

    print("symmetric:", np.allclose(np.array(weights), np.array(weights).T))

    # load
    # load = load_ExecutionConfiguration("../data/examples/midas_dates_hierarchical_20210215-133033")
    # load.execute()