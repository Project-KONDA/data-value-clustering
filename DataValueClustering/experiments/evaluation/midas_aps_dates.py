import numpy as np

from distance.weighted_levenshtein_distance import get_cost_map
from experiments.constants import midas_aps_dates, evaluation_exports
from export.ExecutionConfiguration import ExecutionConfigurationFromParams

if __name__ == '__main__':
    # specify parameters



    # compression
    # compression_answers = "letters, number sequences"
    compression_answers = [False, True, False, False, False, False, False, False, False,
               True, True, False,
               False, False, False, False, False, False,
               True]



    #distance
    weight_case = 1
    # regex = ["", "0123456789", "abcdefghijklmnopqrstuvwxyzäöüßáàéèíìóòúùABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜÁÀÉÈÍÌÓÒÚÙ", "<rest>"]
    # weights = [
    #     # a    r
    #     [ 0,  1,  6, 4],  #
    #     [ 1,  0,  6, 4],  # 1
    #     [ 6,  6, 10, 4],  # aA$
    #     [ 4,  4,  4, 4],  # rest
    # ]

    regex = ["", "0123456789", "<rest>"]
    weights = [
        # a    r
        [ 0,  1,  4],  #
        [ 1,  1,  4],  # ante0-9
        [ 4,  4,  4],  # rest
    ]

    costmap = get_cost_map(weight_case, regex, weights)



    # clustering
    algorithm = "hierarchical"
    # algorithm_params = [['method', 'complete'], ['n_clusters', 20], ['distance_threshold', None], ['criterion', 'maxclust']]  # complete, ward, average, weighted, centroid, median, single
    algorithm_params = [['method', 'complete'], ['n_clusters', 25], ['distance_threshold', None], ['criterion', 'maxclust']]  # complete, ward, average, weighted, centroid, median, single

    # algorithm = "dbscan"
    # algorithm_params = [["eps", 10], ["min_samples", 2], ["n_jobs", None]]








    # initialize
    object = ExecutionConfigurationFromParams(midas_aps_dates, 0, 1000000, compression_answers,
                                              "distance_weighted_levenshtein", algorithm, algorithm_params, costmap)

    # execute
    object.execute()

    # save
    object.save(evaluation_exports)
    object.export_to_excel(evaluation_exports)

    print("symmetric:", np.allclose(np.array(weights), np.array(weights).T))

    # load
    # load = load_ExecutionConfiguration("../data/examples/midas_dates_hierarchical_20210215-133033")
    # load.execute()