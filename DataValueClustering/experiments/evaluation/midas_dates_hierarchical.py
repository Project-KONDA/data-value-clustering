import numpy as np

from distance.weighted_levenshtein_distance import get_cost_map
from experiments.constants import midas_dates, evaluation_exports
from experiments.evaluation.midas_dates_expectation import midas_dates_10000_expectation
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
    regex = ["", "abcdefghijklmnopqrstuvwxyzäöüßáàéèíìóòúù", "ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜÁÀÉÈÍÌÓÒÚÙ", "0123456789", " ", ".", "?", ",:;!()[]{}+-*/%=<>&|\"`´'" , "<rest>"]
    weights = [  # "case-sensitive letter sequences and digit sequences"
        #           a      A        1      _      .      ?      $      r
        [    0,   128,    128,     32,    128,    32,  1024,   512,    32],  #
        [  128,   256,    256,    256,    256,   256,  1024,   256,   256],  # a
        [  128,   256,    256,    256,    256,   256,  1024,   256,   256],  # A
        [   32,   256,    256,      0,    256,    32,  1024,   512,    32],  # 1
        [  128,   256,    256,    256,      0,   256,  1024,   256,   256],  # _
        [   32,   256,    256,     32,    256,     0,  1024,   512,    32],  # .
        [ 1024,  1024,   1024,   1024,   1024,  1024,    0,   1024,  1024],  # ?
        [  512,   256,    256,    512,    256,   512,  1024,   512,   128],  # $
        [   32,   256,    256,     32,    256,    32,  1024,   128,    32],  # r
    ]

    # t = [
    #     [0, 128, 128, 32, 128, 32, 1024, 512, 32],
    #     [128, 256, 256, 256, 256, 256, 1024, 256, 256],
    #     [128, 256, 256, 256, 256, 256, 1024, 256, 256],
    #     [32, 256, 256, 0, 256, 32, 1024, 512, 32],
    #     [128, 256, 256, 256, 0, 256, 1024, 256, 256],
    #     [32, 256, 256, 32, 256, 0, 1024, 512, 32],
    #     [1024, 1024, 1024, 1024, 1024, 1024, 0, 1024, 1024],
    #     [512, 256, 256, 512, 256, 512, 1024, 512, 128],
    #     [32, 256, 256, 32, 256, 32, 1024, 128, 32],
    # ]
    # print(np.array(weights) - np.array(t))

    costmap = get_cost_map(weight_case, regex, weights)

    # clustering
    algorithm = "hierarchical"
    algorithm_params = [['method', 'complete'], ['n_clusters', 9], ['distance_threshold', None], ['criterion', 'maxclust']]  # complete, ward, average, weighted, centroid, median, single

    # initialize
    object = ExecutionConfigurationFromParams(midas_dates, 10000, compression_answers, "distance_weighted_levenshtein", algorithm, algorithm_params, costmap,
                                              midas_dates_10000_expectation)

    # execute
    object.execute()

    # save
    object.save(evaluation_exports)

    print("symmetric:", np.allclose(np.array(weights), np.array(weights).T))

    # load
    # load = load_ExecutionConfiguration("../data/examples/midas_dates_hierarchical_20210215-133033")
    # load.execute()