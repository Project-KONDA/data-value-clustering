from distance.weighted_levenshtein_distance import get_cost_map
from experiments.constants import playground_exports, lido_titles
from export.ExecutionConfiguration import ExecutionConfigurationFromParams

if __name__ == '__main__':

    # specify parameters

    # compression
    compression_answers = "words"
    # [true, false, true, true, false, true, false, false, false, true, true, false, false, false, false, false, false, false, true]

    #distance
    weight_case = 1
    regex = ["", "abcdefghijklmnopqrstuvwxyzäöüßáàéèíìóòúù", "ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜÁÀÉÈÍÌÓÒÚÙ", "0123456789", " ", ".,:;!?()[]{}+-*/%=<>&|"]
    weights = [
        [ 0,  2,  2,  2,  1, 10],
        [ 2,  0,  1,  2,  1, 10],
        [ 2,  2,  0,  2,  1, 10],
        [ 2,  2,  2,  1,  2, 10],
        [ 1,  1,  1,  2,  0, 10],
        [10, 10, 10, 10, 10,  5]
    ]
    costmap = get_cost_map(weight_case, regex, weights)

    # clustering
    algorithm = "hierarchical"
    # algorithm_params = [["n_clusters", 10], ["eigen_solver", None], ["n_components", 8], ["n_init", 10], ["eigen_tol", 0.0], ["assign_labels", 'kmeans']]
    algorithm_params = [['method', 'single'], ['n_clusters', 9], ['distance_threshold', None], ['criterion', 'maxclust']]

    # initialize
    object = ExecutionConfigurationFromParams(lido_titles, 0, 4000, compression_answers,
                                              "distance_weighted_levenshtein", algorithm, algorithm_params, costmap)

    # execute
    object.execute()

    # save
    object.save(playground_exports)

    # load
    # load = load_ExecutionConfiguration("../data/examples/midas_dates_hierarchical_20210215-133033")
    # load.execute()