import numpy as np

from distance.weighted_levenshtein_distance import get_cost_map
from experiments.constants import evaluation_exports, lido_measurement_unit
from export.ExecutionConfiguration import ExecutionConfigurationFromParams

if __name__ == '__main__':
    # specify parameters

    # compression
    # compression_answers = "letters, number sequences"
    compression_answers = [False, False, False, False, False, False, False, False, False,
               True, True, False,
               False, False, False, False, False, False,
               True]

    #distance
    weight_case = 1
    regex = ["", "0123456789", "abcdefghijklmnopqrstuvwxyzäöüßáàéèíìóòúùABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜÁÀÉÈÍÌÓÒÚÙ", "-+ ", "<rest>"]
    weights = [
        [0, 1, 1, 1, 2],  #
        [1, 0, 2, 1, 2],  # 1
        [1, 2, 1, 1, 2],  # aA
        [1, 1, 1, 1, 2],  # +-_
        [2, 2, 2, 2, 2],  # <rest>
    ]

    costmap = get_cost_map(weight_case, regex, weights)

    # clustering
    algorithm = "hierarchical"
    algorithm_params = [['method', 'complete'], ['n_clusters', None], ['distance_threshold', 1.5], ['criterion', 'distance']]  # complete, ward, average, weighted, centroid, median, single

    # algorithm = "dbscan"
    # algorithm_params = [["eps", 1.5], ["min_samples", 2], ["n_jobs", None]]


    # initialize
    object = ExecutionConfigurationFromParams(lido_measurement_unit, 0, 1000000, compression_answers,
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