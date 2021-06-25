import numpy as np

from distance.weighted_levenshtein_distance import get_cost_map
from experiments.constants import evaluation_exports, lido_measurement_unit_randomized
from experiments.playground.lido_measurement_unit_expectation import lido_measurement_unit_100000_expectation
from export.ExecutionConfiguration import ExecutionConfigurationFromParams

if __name__ == '__main__':
    # specify parameters

    # compression
    compression_answers = [True, True, False, False, True, False, False, False, False,
               True, True, True,
               False, False, False, False, False, False,
               True]

    #distance
    weight_case = 1
    regex = ["", "abcdefghijklmnopqrstuvwxyzäöüßáàéèíìóòúù", "ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜÁÀÉÈÍÌÓÒÚÙ", "0123456789", " ", ".,:;!?()[]{}+-*/%=<>&|\"`´'" , "<rest>"]
    weights = [
        #         a      A      1      _      $     r
        [   0,   64,    64,    32,    16,    64,   64],  #
        [  64,    0,    64,    64,    32,   128,   64],  # a
        [  64,   64,     0,    64,    32,    64,   64],  # A
        [  32,   64,    64,     0,    32,    64,   64],  # 1
        [  16,   32,    32,    32,     0,    64,   64],  # _
        [  64,  128,    64,    64,    64,    64,   64],  # $
        [  64,   64,    64,    64,    64,    64,   64],  # r
    ]

    costmap = get_cost_map(weight_case, regex, weights)

    # clustering
    algorithm = "hierarchical"
    algorithm_params = [['method', 'complete'], ['n_clusters', None], ['distance_threshold', 35], ['criterion', 'distance']]

    # initialize
    object = ExecutionConfigurationFromParams(lido_measurement_unit_randomized, 0, 100000, compression_answers,
                                              "distance_weighted_levenshtein", algorithm, algorithm_params, costmap,
                                              lido_measurement_unit_100000_expectation)

    # execute
    object.execute()

    # save
    object.save(evaluation_exports)

    print("symmetric:", np.allclose(np.array(weights), np.array(weights).T))

    # load
    # load = load_ExecutionConfiguration("../data/examples/midas_dates_hierarchical_20210215-133033")
    # load.execute()