import numpy as np
from numpy.core.defchararray import lower
from pip._vendor.msgpack.fallback import xrange

weight_case = 1
weight_swap = 5
weight = np.array([
    #   ["", "a", "A", "1", " ", "."]
    # ""
    [0, 0, 2, 4, 4, 8],
    # "a"
    [1, 0, 0, 4, 4, 8],
    # "A"
    [2, 0, 0, 4, 4, 8],
    # "1"
    [4, 4, 4, 0, 4, 8],
    # " "
    [4, 4, 4, 4, 0, 8],
    # "."
    [8, 8, 8, 8, 8, 8]
])


def get_my_kind(c):
    if len(c) > 1:
        return 10000000000
    if c == "":
        return 0
    if "a" <= c <= "z":
        return 1
    if "A" <= c <= "Z":
        return 2
    if "0" <= c <= "9":
        return 3
    if " " == c:
        return 4
    return 5


def get_cost(c1, c2):
    if c1 == c2:
        return 0
    if lower(c1) == lower(c2):
        return weight_case
    return weight[get_my_kind(c1)][get_my_kind(c2)]


def levenshtein_distance(s1, s2):
    d = {}
    length1 = len(s1)
    length2 = len(s2)
    d[(-1, -1)] = 0

    for i in xrange(0, length1):
        d[(i, -1)] = d[(i - 1, -1)] + get_cost(s1[i], "")
    #    print(i, -1, d[(i, -1)])

    for j in xrange(0, length2):
        d[(-1, j)] = d[(-1, j - 1)] + get_cost("", s2[j])
    #    print(-1, j, d[(-1, j)])

    for i in xrange(0, length1):
        for j in xrange(0, length2):
            d[(i, j)] = min(
                d[(i - 1, j)] + get_cost(s1[i], ""),  # deletion
                d[(i, j - 1)] + get_cost("", s2[j]),  # insertion
                d[(i - 1, j - 1)] + get_cost(s1[i], s2[j]),  # substitution
            )
    #        print(i, j, d[(i, j)])
    #        if i and j and s1[i] == s2[j - 1] and s1[i - 1] == s2[j]:
    #            d[(i, j)] = min(d[(i, j)], d[i - 2, j - 2] + weight_swap)  # transposition

    return d[length1 - 1, length2 - 1]
