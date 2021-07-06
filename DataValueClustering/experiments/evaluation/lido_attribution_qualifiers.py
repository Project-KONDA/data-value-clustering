'''This script allows clustering the data values of the field LIDO attribution qualifiers with an example configuration used for the evaluation.'''
import numpy as np

from distance.weighted_levenshtein_distance import get_cost_map
from experiments.constants import lido_attribution_qualifier_randomized, evaluation_exports
from export.ExecutionConfiguration import ExecutionConfigurationFromParams

if __name__ == '__main__':
    # specify parameters

    # abstraction
    abstraction_answers = "letters, digits"

    #distance
    weight_case = 1
    regex = ["", "abcdefghijklmnopqrstuvwxyzäöüßáàéèíìóòúù", "ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜÁÀÉÈÍÌÓÒÚÙ", "0123456789", " ", ".,:;?!()[]{}+-*/%=<>&|\"`´'" , "<rest>"]
    weights = [
             #    a      A     1     _      $      r
        [    0,    1,    2,   30,   20,   100,   90],  #
        [    1,    0,    2,   30,   20,   100,   90],  # a
        [    2,    2,    0,   30,   20,   100,   90],  # A
        [   30,   30,   30,    0,   30,   100,   90],  # 1
        [   20,   20,   20,   30,    0,   100,   90],  # _
        [  100,  100,  100,  100,  100,   100,  100],  # $
        [   90,   90,   90,   90,   90,   100,   90],  # r
    ]
    print("symmetric:", np.allclose(np.array(weights), np.array(weights).T))


    costmap = get_cost_map(weight_case, regex, weights)

    # clustering
    algorithm = "hierarchical"
    algorithm_params = [['method', 'complete'], ['n_clusters', None], ['distance_threshold', 100], ['criterion', 'distance']]  # complete, ward, average, weighted, centroid, median, single

    # initialize
    object = ExecutionConfigurationFromParams(lido_attribution_qualifier_randomized, 0, 1000000, abstraction_answers,
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