import numpy as np

from distance.weighted_levenshtein_distance import get_cost_map
from experiments.constants import midas_dates, evaluation_exports
from experiments.playground.midas_dates_expectation import midas_dates_10000_expectation_v3
from export.ExecutionConfiguration import ExecutionConfigurationFromParams

if __name__ == '__main__':
    # specify parameters

    # compression
    # compression_answers = "letters, number sequences"
    compression_answers = [False, False, True, False, False, False, False, False, False,
               True, True, False,
               False, False, False, False, False, False,
               True]
    # "letters, digits", "letter sequences and digit sequences", "case-sensitive letter sequences and digit sequences", "letter sequences, digits", "letters, number sequences"

    #distance
    weight_case = 1
    regex = ["", "abcdefghijklmnopqrstuvwxyzäöüßáàéèíìóòúù", "ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜÁÀÉÈÍÌÓÒÚÙ", "0123456789", " ", ".", ":,;!?[]{}()+-*/%=<>&|\"`´'" , "<rest>"]
    weights = [
        #         a      A      1      _    .      $     r
        [   0,   400,   400,   120,    50,  25,  400,   16],  #
        [ 400,   400,   400,   400,   400, 400,  400,  400],  # a
        [ 400,   400,   400,   400,   400, 400,  400,  400],  # A
        [ 120,   400,   400,     0,    50,  25,  400,  120],  # 1
        [  50,   400,   400,    50,     0,  25,  400,   50],  # _
        [  25,   400,   400,    25,    25,   0,  400,   25],  # .
        [ 400,   400,   400,   400,   400, 400,  500,  400],  # $
        [  16,   400,   400,   120,    50,  25,  400,   16],  # r
    ]

    # t = [
    #
    # ]
    # print(np.array(weights) - np.array(t))

    costmap = get_cost_map(weight_case, regex, weights)

    # clustering
    algorithm = "hierarchical"
    algorithm_params = [['method', 'complete'], ['n_clusters', None], ['distance_threshold', 900], ['criterion', 'distance']]  # complete, ward, average, weighted, centroid, median, single

    # initialize
    object = ExecutionConfigurationFromParams(midas_dates, 0, 10000, compression_answers,
                                              "distance_weighted_levenshtein", algorithm, algorithm_params, costmap,
                                              midas_dates_10000_expectation_v3)

    # execute
    object.execute()

    # save
    object.save(evaluation_exports)

    print("symmetric:", np.allclose(np.array(weights), np.array(weights).T))

    # load
    # load = load_ExecutionConfiguration("../data/examples/midas_dates_hierarchical_20210215-133033")
    # load.execute()