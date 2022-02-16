from math import sqrt

import numpy as np
from numpy import NaN

from abstraction.abstraction import sequence_abstraction_function
from distance.costmap import get_cost_map_indices, split_cost_map, get_cost_map


def get_weighted_uncommon_partstring(cost_map=get_cost_map()):
    if cost_map is None:
        cost_map = get_cost_map()
    case, regex, weight = split_cost_map(cost_map)

    def distance_function(s1, s2):
        return weighted_uncommon_partstring(regex, weight, s1, s2, end=True)

    return distance_function


def getWeight(string, costmap_regex, costmap_weights):
    if costmap_regex is None or costmap_weights is None:
        return len(string)
    res = 0
    index_array = get_cost_map_indices(costmap_regex, string)
    # print(index_array)
    weights0 = costmap_weights[0]
    for i in index_array:
        res += weights0[i]
    # print(res)
    return res


def weighted_uncommon_partstring(costmap_regex, costmap_weights, seq1, seq2, start=True, end=False):
    def common_start(seq1, seq2):
        res = 0
        max = min(len(seq1), len(seq2))
        while res < max and seq1[res] == seq2[res]:
            res += 1
        return res

    if start:
        startlen = common_start(seq1, seq2)
        seq1 = seq1[startlen:]
        seq2 = seq2[startlen:]

    if end:
        seq1 = seq1[::-1]
        seq2 = seq2[::-1]
        endlen = common_start(seq1, seq2)
        seq1 = seq1[endlen:]
        seq2 = seq2[endlen:]
        seq1 = seq1[::-1]
        seq2 = seq2[::-1]

    dn = getWeight(seq1, costmap_regex, costmap_weights)
    dm = getWeight(seq2, costmap_regex, costmap_weights)

    distance = dn + dm
    return distance


if __name__ == "__main__":

    regex = ["", "abcdefghijklmnopqrstuvwxyzäöüß", "ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜ", "0123456789", " ",
             "\$\&\+,:;=\?@\#\|'<>\.\-\^\*\(\)%!/"]
    weights = [
        [0, 1, 2, 4, 4, 8],
        [1, 0, 1, 4, 4, 8],
        [2, 1, 0, 4, 4, 8],
        [4, 4, 4, 0, 4, 8],
        [4, 4, 4, 4, 0, 8],
        [8, 8, 8, 8, 8, 8]]

    testvalues = [
        "", "a", "abcdefghijklmnopqrstuvwxyz", "0123456789", "abcdefghijklmnopqrstuvwxyz0123456789", "acdefgh", "abcde", "01234$abc",
        "Andrea Vannucci", "Monogrammist S (1519)"
]

    def get_abstracted(x):
        a = sequence_abstraction_function()[0]([x])[0][0]
        return a


    # n = len(testvalues)
    # for i in range(n):
    #     print(testvalues[i], get_abstracted(testvalues[i]))

    n = len(testvalues)
    values = [[0 for k in range(n)] for l in range(n)]

    for i in range(n):
        for j in range(n):
            dist = weighted_uncommon_partstring(
                    regex, weights,
                    get_abstracted(testvalues[i]),
                    get_abstracted(testvalues[j]),
                    start=True, end=True
                )
            values[i][j] = round(dist, 1)
    for i in range(n):
        print(values[i])


    # print(new_dissimilarity_measure(None, None, "abcdefghijklmn00100opqrstuvwxyz", "abcdefghijklmn00100opqrstuvwxyz"[::-1], start=False, end=False))