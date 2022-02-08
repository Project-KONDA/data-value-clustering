'''This script allows clustering the data values of the field MIDAS artist names with an example configuration used for the evaluation.'''
import numpy as np

from distance.costmap import get_cost_map
from experiments.constants import midas_artist_names_randomized, evaluation_exports, midas_aps_artist_names
from export.ExecutionConfiguration import ExecutionConfigurationFromParams

if __name__ == '__main__':
    # specify parameters

    # abstraction
    # "letter sequences, digits"
    abstraction_answers = [True, True, False, False, True, False, False, False, True,
                           True, False, False,
                           False, False, False, False, False, False,
                           True]
    #distance
    weight_case = 1
    regex = ["", "abcdefghijklmnopqrstuvwxyzäöüßáàéèíìóòúùABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜÁÀÉÈÍÌÓÒÚÙ", "0123456789", " ", "-'", ",", ".:;^?!()[]{}+*/%=<>&|\"`´" , "<rest>"]
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

    # weights = [
    #          #     a     1     _      -^     ,      $     r
    #     [    0,    1,   10,   10,     1,   200,   100,   90],  #
    #     [    1,    0,   10,   10,     1,   200,   100,   90],  # a
    #     [   10,   10,    0,   10,    10,   200,   100,   90],  # 1
    #     [   10,   10,   10,    0,    10,   200,   100,   90],  # _
    #     [    1,    1,   10,   10,     0,   200,   100,   90],  # -^
    #     [  200,  200,  200,  200,   200,     0,   200,  200],  # ,
    #     [  100,  100,  100,  100,   100,   200,   100,  100],  # $
    #     [   90,   90,   90,   90,    90,   200,   100,   90],  # r
    # ]

    # weights = [
    #          #     a     1     _      -     ,      $     r
    #     [    0,    1,   10,   10,     1,   200,   100,    1],  #
    #     [    1,    0,   10,   10,     1,   200,   100,    1],  # a
    #     [   10,   10,    0,   10,    10,   200,   100,   10],  # 1
    #     [   10,   10,   10,    0,    10,   200,   100,   10],  # _
    #     [    1,    1,   10,   10,     0,   200,   100,    1],  # -
    #     [  200,  200,  200,  200,   200,     0,   200,  200],  # ,
    #     [  100,  100,  100,  100,   100,   200,   100,  100],  # $
    #     [    1,    1,   10,   10,     1,   200,   100,    1],  # r
    # ]

    # weights = [
    #          #     a     1     _      -'     ,      $     r
    #     [    0,    1,   20,   15,     1,   200,   100,    1],  #
    #     [    1,    0,   20,   15,     1,   200,   100,    1],  # a
    #     [   20,   20,    0,   20,    20,   200,   100,   20],  # 1
    #     [   15,   15,   20,    0,    15,   200,   100,   15],  # _
    #     [    1,    1,   20,   15,     0,   200,   100,    1],  # -'
    #     [  200,  200,  200,  200,   200,     0,   200,  200],  # ,
    #     [  100,  100,  100,  100,   100,   200,   100,  100],  # $
    #     [    1,    1,   20,   15,     1,   200,   100,    1],  # r
    # ]

    # weights = [
    #          #     a     1     _      -'     ,      $     r
    #     [    0,    1,   10,   15,     1,   100,   100,    1],  #
    #     [    1,    0,   10,   15,     1,   100,   100,    1],  # a
    #     [   10,   10,    0,   15,    10,   100,   100,   10],  # 1
    #     [   15,   15,   10,    0,    15,   100,   100,   15],  # _
    #     [    1,    1,   10,   15,     0,   100,   100,    1],  # -'
    #     [  100,  100,  100,  100,   100,     0,   100,  100],  # ,
    #     [  100,  100,  100,  100,   100,   100,   100,  100],  # $
    #     [    1,    1,   10,   15,     1,   100,   100,    1],  # r
    # ]

    # weights = [
    #          #     a     1     _      -'     ,      $     r
    #     [    0,    1,   10,   15,     1,   100,   100,    1],  #
    #     [    1,    0,   11,   16,     2,   101,   101,    2],  # a
    #     [   10,   11,    0,   25,    11,   110,   110,   11],  # 1
    #     [   15,   16,   25,    0,    16,   115,   115,   16],  # _
    #     [    1,    2,   11,   16,     0,   101,   101,    2],  # -'
    #     [  100,  101,  110,  115,   101,     0,   200,  101],  # ,
    #     [  100,  101,  110,  115,   101,   200,   200,  101],  # $
    #     [    1,    2,   11,   16,     2,   101,   101,    2],  # r
    # ]    weights = [
    #              #     a     1     _      -^     ,      $     r
    #         [    0,    1,   10,   10,     1,   200,   100,   90],  #
    #         [    1,    0,   10,   10,     1,   200,   100,   90],  # a
    #         [   10,   10,    0,   10,    10,   200,   100,   90],  # 1
    #         [   10,   10,   10,    0,    10,   200,   100,   90],  # _
    #         [    1,    1,   10,   10,     0,   200,   100,   90],  # -^
    #         [  200,  200,  200,  200,   200,     0,   200,  200],  # ,
    #         [  100,  100,  100,  100,   100,   200,   100,  100],  # $
    #         [   90,   90,   90,   90,    90,   200,   100,   90],  # r
    #     ]

    weights = [
             #     a     1     _      -'     ,      $     r
        [    0,    1,   10,   15,     1,   200,   100,    1],  #
        [    1,    0,   11,   16,     2,   201,   101,    2],  # a
        [   10,   11,    0,   25,    11,   210,   110,   11],  # 1
        [   15,   16,   25,    0,    16,   215,   115,   16],  # _
        [    1,    2,   11,   16,     0,   201,   101,    2],  # -'
        [  200,  201,  210,  215,   201,     0,   300,  201],  # ,
        [  100,  101,  110,  115,   101,   300,   200,  101],  # $
        [    1,    2,   11,   16,     2,   201,   101,    2],  # r
    ]

    print("symmetric:", np.allclose(np.array(weights), np.array(weights).T))


    costmap = get_cost_map(weight_case, regex, weights)

    # clustering
    algorithm = "hierarchical"
    algorithm_params = [['method', 'complete'], ['n_clusters', None], ['distance_threshold', 700], ['criterion', 'distance']]  # complete, ward, average, weighted, centroid, median, single

    # initialize
    object = ExecutionConfigurationFromParams(midas_aps_artist_names, 0, 1000000, abstraction_answers,
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