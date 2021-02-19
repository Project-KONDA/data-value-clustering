
from distance.weighted_levenshtein_distance import get_cost_map
from experiments.constants import playground_exports, midas_dates, evaluation_exports
from export.ExecutionConfiguration import ExecutionConfigurationFromParams

if __name__ == '__main__':

    clustering_true = [
        ["1875", "1750"],  # year
        ["1977.10", "1846.04", "1732.08.14"],  # year.month.day
        ["1868?"],  # year uncertain
        ["um 1460", "um 1620?", "um 1634/1637", "um 1634-1636", "gegen 1907", "um 845", "um 560ante"],  # fuzzy
        ["1451/1475", "nach 1594", "vor 1672", "1601/1700?", "nach 1864?", "901/1000", "600ante/551ante", "nach 1470-1484"],  # point in interval
        ["1471 / um 1505/1510", "um 1508 / um 1510", "um 1651 / nach 1651"],  # alternatives
        ["1853-1856", "1441-1447", "834-843", "ab 1445"],  # interval
        ["---"],  # other
    ]

    # specify parameters

    # compression
    compression_answers = "case-sensitive letter sequences and digit sequences"
    # "letters, digits", "letter sequences and digit sequences", "case-sensitive letter sequences and digit sequences", "letter sequences, digits", "letters, number sequences"

    #distance
    weight_case = 1
    regex = ["", "abcdefghijklmnopqrstuvwxyzäöüßáàéèíìóòúù", "ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜÁÀÉÈÍÌÓÒÚÙ", "0123456789", " ", ".,:;!?()[]{}+-*/%=<>&|\"`´'" , "<rest>"]
    weights = [  # "case-sensitive letter sequences and digit sequences"
        [0,   32,  32,  24,  32,  24,  24],
        [32,  0,   1,   24,  32,  32,  32],
        [32,  1,   0,   24,  32,  32,  32],
        [24,  24,  24,  0,   32,  32,  32],
        [32,  32,  32,  32,  0,   32,  32],
        [24,  32,  32,  32,  32,  32,  32],
        [24,  32,  32,  32,  32,  32,  32],
    ]
    costmap = get_cost_map(weight_case, regex, weights)

    # clustering
    algorithm = "hierarchical"
    algorithm_params = [['method', 'single'], ['n_clusters', 8], ['distance_threshold', None], ['criterion', 'maxclust']]

    # initialize
    object = ExecutionConfigurationFromParams(midas_dates, 10000, compression_answers, "distance_weighted_levenshtein", algorithm, algorithm_params, costmap, clustering_true)

    # execute
    object.execute()

    # save
    object.save(evaluation_exports)

    # load
    # load = load_ExecutionConfiguration("../data/examples/midas_dates_hierarchical_20210215-133033")
    # load.execute()