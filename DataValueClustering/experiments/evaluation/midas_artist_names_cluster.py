from distance.weighted_levenshtein_distance import get_cost_map
from experiments.constants import playground_exports, lido_attribution_qualifier, midas_artist_names, midas_artist_names_randomized
from experiments.evaluation.lido_attribution_qualifier_expectation import lido_attribution_qualifier_expecation
from experiments.evaluation.midas_artist_names_expectation import midas_artist_names_expecation_10000
from export.ExecutionConfiguration import ExecutionConfigurationFromParams

if __name__ == '__main__':
    # specify parameters

    # compression
    compression_answers = "letters, digits"  # "case-sensitive letter sequences and digit sequences" #

    # distance
    weight_case = 1
    regex = ["", ",()?", "<rest>"]

    weights = [
        [1, 20, 1],
        [20, 20, 20],
        [1, 20, 1]
    ]

    costmap = get_cost_map(weight_case, regex, weights)

    # clustering
    algorithm = "hierarchical"
    algorithm_params = [['method', 'single'], ['n_clusters', 25], ['distance_threshold', None], ['criterion', 'maxclust']]
    # algorithm = "optics"
    # algorithm_params = [["eps", 15], ["min_samples", 5], ["max_eps", 100], ["cluster_method", 'xi'], ["xi", 0.5], ["predecessor_correction", 3], ["min_cluster_size", 3], ["n_jobs", 3]]
    # algorithm = "affinity"
    # algorithm_params = [["damping", 0.75], ["max_iter", 200], ["convergence_iter", 15], ["preference", None]]#, ['random_state', 0]]
    # algorithm = "dbscan"
    # algorithm_params = [["eps", 3], ["min_samples", 3], ["n_jobs", None]]

    # initialize
    object = ExecutionConfigurationFromParams(midas_artist_names_randomized, 0, 10000, compression_answers,
                                              "distance_weighted_levenshtein", algorithm, algorithm_params, costmap,
                                              midas_artist_names_expecation_10000)

    object.execute()
    object.save(playground_exports)
