import numpy as np

from distance.weighted_levenshtein_distance import get_cost_map
from experiments.constants import midas_artist_names_randomized, evaluation_exports
from export.ExecutionConfiguration import ExecutionConfigurationFromParams

if __name__ == '__main__':
    # specify parameters

    # compression
    # "letter sequences, digits"
    compression_answers = [True, True, False, False, True, False, False, False, True,
         True, False, False,
         False, False, False, False, False, False,
         True]
    #distance
    weight_case = 1
    regex = ["", "abcdefghijklmnopqrstuvwxyzäöüßáàéèíìóòúùABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜÁÀÉÈÍÌÓÒÚÙ", "0123456789", " ", "-^", ",", ".:;?!()[]{}+*/%=<>&|\"'`´" , "<rest>"]
    # weights = [
    #          #    a     1     _      $      r
    #     [    0,    1,   10,    1,   100,   90],  #
    #     [    1,    0,   10,    1,   100,   90],  # a
    #     [   10,   10,    0,   10,   100,   90],  # 1
    #     [    1,    1,   10,    0,   100,   90],  # _
    #     [  100,  100,  100,  100,   100,  100],  # $
    #     [   90,   90,   90,   90,   100,   90],  # r
    # ]

    # weights = [
    #          #     a     1     _      -      $     r
    #     [    0,    1,   10,    1,     1,   100,   90],  #
    #     [    1,    0,   10,    1,     1,   100,   90],  # a
    #     [   10,   10,    0,   10,    10,   100,   90],  # 1
    #     [    1,    1,   10,    0,     1,   100,   90],  # _
    #     [    1,    1,   10,    1,     0,   100,   90],  # -
    #     [  100,  100,  100,  100,   100,   100,  100],  # $
    #     [   90,   90,   90,   90,    90,   100,   90],  # r
    # ]

    # weights = [
    #          #     a     1     _      -      $     r
    #     [    0,    1,   20,   10,     1,   100,   90],  #
    #     [    1,    0,   20,   10,     1,   100,   90],  # a
    #     [   20,   20,    0,   20,    20,   100,   90],  # 1
    #     [   10,   10,   20,    0,    10,   100,   90],  # _
    #     [    1,    1,   20,   10,     0,   100,   90],  # -
    #     [  100,  100,  100,  100,   100,   100,  100],  # $
    #     [   90,   90,   90,   90,    90,   100,   90],  # r
    # ]

    # weights = [
    #          #     a     1     _      -^     ,      $     r
    #     [    0,    1,   20,   10,     1,   200,   100,   90],  #
    #     [    1,    0,   20,   10,     1,   200,   100,   90],  # a
    #     [   20,   20,    0,   20,    20,   200,   100,   90],  # 1
    #     [   10,   10,   20,    0,    10,   200,   100,   90],  # _
    #     [    1,    1,   20,   10,     0,   200,   100,   90],  # -^
    #     [  200,  200,  200,  200,   200,     0,   200,  200],  # ,
    #     [  100,  100,  100,  100,   100,   200,   100,  100],  # $
    #     [   90,   90,   90,   90,    90,   200,   100,   90],  # r
    # ]

    weights = [
             #     a     1     _      -^     ,      $     r
        [    0,    1,   10,   10,     1,   200,   100,   90],  #
        [    1,    0,   10,   10,     1,   200,   100,   90],  # a
        [   10,   10,    0,   10,    10,   200,   100,   90],  # 1
        [   10,   10,   10,    0,    10,   200,   100,   90],  # _
        [    1,    1,   10,   10,     0,   200,   100,   90],  # -^
        [  200,  200,  200,  200,   200,     0,   200,  200],  # ,
        [  100,  100,  100,  100,   100,   200,   100,  100],  # $
        [   90,   90,   90,   90,    90,   200,   100,   90],  # r
    ]

    print("symmetric:", np.allclose(np.array(weights), np.array(weights).T))


    costmap = get_cost_map(weight_case, regex, weights)

    # clustering
    algorithm = "hierarchical"
    algorithm_params = [['method', 'complete'], ['n_clusters', None], ['distance_threshold', 500], ['criterion', 'distance']]  # complete, ward, average, weighted, centroid, median, single

    # initialize
    object = ExecutionConfigurationFromParams(midas_artist_names_randomized, 0, 1000000, compression_answers,
                                              "distance_weighted_levenshtein", algorithm, algorithm_params, costmap)

    # execute
    object.execute()

    # save
    object.save(evaluation_exports)

    # export
    object.export_to_excel(evaluation_exports)

    # load
    # load = load_ExecutionConfiguration("../data/examples/midas_dates_hierarchical_20210215-133033")
    # load.execute()