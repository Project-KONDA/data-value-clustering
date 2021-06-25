import numpy as np

from distance.weighted_levenshtein_distance import get_cost_map
from experiments.constants import evaluation_exports, lido_titles
from experiments.playground.lido_titles_expectation import lido_titles_1000_expectation
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
    regex = ["", "abcdefghijklmnopqrstuvwxyzäöüßáàéèíìóòúù", "ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜÁÀÉÈÍÌÓÒÚÙ", "0123456789", " ", ",", "-", ".", "()", "?", ":", "/", ";![]{}+*%=<>&|\"`´'" , "<rest>"]
    weights = [
        #         a      A      1      _      ,      -      .      (      ?      :      /      $     r
        [   0,  256,   256,    16,    32,   900,   300,     8,   200,   512,     0,   256,     8,   64],  #
        [ 256,    0,   128,   256,    32,   900,   300,     8,   200,   512,     0,   256,     8,   64],  # a
        [ 256,  128,     0,   256,    32,   900,   300,     8,   200,   512,     0,   256,     8,   64],  # A
        [  16,  256,   256,     0,    32,   900,   300,     8,   200,   512,     0,   256,     8,   64],  # 1
        [  32,   32,    32,    32,     0,   900,   300,    32,   200,   512,     0,   256,     8,   64],  # _
        [ 900,  900,   900,   900,   900,     0,  1000,   900,  1000,  1000,     0,  1000,     8,  900],  # ,
        [ 300,  300,   300,   300,   300,  1000,     0,   300,  1000,  1000,     0,  1000,     8,  300],  # -
        [   8,    8,     8,     8,    32,   900,   300,     0,   200,   512,     0,   256,     8,   64],  # .
        [ 200,  200,   200,   200,   200,  1000,  1000,   200,     0,  1000,     0,  1000,     8,  200],  # (
        [ 512,  512,   512,   512,   512,  1000,  1000,   512,  1000,     0,     0,  1000,     8,  512],  # ?
        [   0,    0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,    0],  # :
        [ 256,  256,   256,   256,   256,  1000,  1000,   256,  1000,  1000,     0,     0,     8,  256],  # /
        [   8,    8,     8,     8,     8,     8,     8,     8,     8,     8,     0,     8,     8,    8],  # $
        [  64,   64,    64,    64,    64,   900,   300,    64,   200,   512,     0,   256,     8,   64],  # r
    ]

    costmap = get_cost_map(weight_case, regex, weights)

    # clustering
    algorithm = "hierarchical"
    algorithm_params = [['method', 'complete'], ['n_clusters', 17], ['distance_threshold', None], ['criterion', 'maxclust']]

    # initialize
    object = ExecutionConfigurationFromParams(lido_titles, 0, 1000, compression_answers,
                                              "distance_weighted_levenshtein", algorithm, algorithm_params, costmap,
                                              lido_titles_1000_expectation)

    # execute
    object.execute()

    # save
    object.save(evaluation_exports)

    print("symmetric:", np.allclose(np.array(weights), np.array(weights).T))

    # load
    # load = load_ExecutionConfiguration("../data/examples/midas_dates_hierarchical_20210215-133033")
    # load.execute()