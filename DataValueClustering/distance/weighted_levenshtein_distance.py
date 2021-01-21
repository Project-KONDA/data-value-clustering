import re
import math

import numpy as np
from numpy.core.defchararray import lower
from pip._vendor.msgpack.fallback import xrange


# TODO: predefined cost maps ?


def suggest_cost_map():
    # TODO: add parameters
    # TODO: suggest a (predefined or newly build) cost map based on user input
    pass


# example cost map components:
weight_case = 1
regex = ["", "[a-zäöüß]", "[A-ZÄÖÜ]", "[0-9]", " ", "[\$\&\+,:;=\?@\#\|'<>\.\-\^\*\(\)%!/]"]
weights = [
    [0, 1, 2, 4, 4, 8],
    [1, 0, 1, 4, 4, 8],
    [2, 1, 0, 4, 4, 8],
    [4, 4, 4, 0, 4, 8],
    [4, 4, 4, 4, 0, 8],
    [8, 8, 8, 8, 8, 8]]


def get_cost_map(rgx=regex, w=weights, weight_case_switch=weight_case):
    # def get_cost_map(regex, matrix, weight=1):
    assert len(rgx) == len(w) == len(w[0])
    d = {}
    d[()] = weight_case_switch
    for i in range(len(rgx)):
        d[(i)] = rgx[i]
    for i in range(len(rgx)):
        for j in range(len(rgx)):
            d[(i, j)] = w[i][j]
    return d


def match(regex, string):
    return re.match("^" + regex + "$", string) is not None


def get_costmap_index(cost_map, c):
    if not isinstance(cost_map, dict):
        return -1
    num = math.floor(math.sqrt(len(cost_map)))
    for i in range(num):
        if match (cost_map[i], c):
            return i
    print("Error when trying to identify: " + c)
    return AssertionError


def get_cost(cost_map, c1, c2):
    if c1 == c2:
        return 0
    if lower(c1) == lower(c2):
        return cost_map[()]
    k1 = get_costmap_index(cost_map, c1)
    k2 = get_costmap_index(cost_map, c2)
    return cost_map[(k1, k2)]


def weighted_levenshtein_distance(cost_map, s1, s2):
    d = {}
    l1 = len(s1)
    l2 = len(s2)
    d[(-1, -1)] = 0

    for i in xrange(0, l1):
        d[(i, -1)] = d[(i - 1, -1)] + get_cost(cost_map, s1[i], "")
    #    print(i, -1, d[(i, -1)])

    for j in xrange(0, l2):
        d[(-1, j)] = d[(-1, j - 1)] + get_cost(cost_map, "", s2[j])
    #    print(-1, j, d[(-1, j)])

    for i in xrange(0, l1):
        for j in xrange(0, l2):
            d[(i, j)] = min(
                d[(i - 1, j)] + get_cost(cost_map, s1[i], ""),  # deletion
                d[(i, j - 1)] + get_cost(cost_map, "", s2[j]),  # insertion
                d[(i - 1, j - 1)] + get_cost(cost_map, s1[i], s2[j]),  # substitution
            )
    #        print(i, j, d[(i, j)])
    #        if i and j and s1[i] == s2[j - 1] and s1[i - 1] == s2[j]:
    #            d[(i, j)] = min(d[(i, j)], d[i - 2, j - 2] + weight_swap)  # transposition
    return d[l1 - 1, l2 - 1]


if __name__ == "__main__":
    map = get_cost_map()
    #print(match(" ", " "))
    #      != None)
    print(get_costmap_index(map, ""))
    print(get_costmap_index(map, "a"))
    print(get_costmap_index(map, "A"))
    print(get_costmap_index(map, "1"))
    print(get_costmap_index(map, " "))
    print(get_costmap_index(map, "-"))

    print(map)


