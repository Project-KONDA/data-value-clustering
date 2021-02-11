import re
import math
from datetime import datetime

import numpy as np
from numba import jit, njit, prange
import numba as nb
from numpy.core.defchararray import lower
from pip._vendor.msgpack.fallback import xrange


# TODO: predefined cost maps ?


def suggest_cost_map():
    # TODO: add parameters
    # TODO: suggest a (predefined or newly build) cost map based on user input
    pass


# example cost map components:
weight_case = 1
regex = ["", "abcdefghijklmnopqrstuvwxyzäöüß", "ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜ", "0123456789", " ", "\$\&\+,:;=\?@\#\|'<>\.\-\^\*\(\)%!/"]
weights = [
    [0, 1, 2, 4, 4, 8],
    [1, 0, 1, 4, 4, 8],
    [2, 1, 0, 4, 4, 8],
    [4, 4, 4, 0, 4, 8],
    [4, 4, 4, 4, 0, 8],
    [8, 8, 8, 8, 8, 8]]


def get_cost_map(weight_case_switch=weight_case, rgx=regex, w=weights):
    # def get_cost_map(regex, map, weight=1):
    assert len(rgx) == len(w) == len(w[0])
    d = {(()): weight_case_switch}
    for i in range(len(rgx)):
        d[(i)] = rgx[i]
    for i in range(len(rgx)):
        for j in range(len(rgx)):
            d[(i, j)] = w[i][j]
    return d


def split_cost_map(cost_map=get_cost_map()):
    n = get_costmap_num(cost_map)
    costmap_case = cost_map[()]

    costmap_regex = []
    for i in xrange(n):
        costmap_regex.append(cost_map[i])
    costmap_regex_len = len(costmap_regex)
    costmap_regex_max = max(map(len, costmap_regex))

    regex_np = np.full((costmap_regex_len, costmap_regex_max), '', dtype=str)
    for i, reg in enumerate(costmap_regex):
        for j, r in enumerate(reg):
            regex_np[i, j] = r

    costmap_weights = []

    for i in xrange(n):
        costmap_weights.append([])
        for j in xrange(n):
            costmap_weights[i].append(cost_map[(i, j)])

    costmap_weights = np.array(costmap_weights)

    return costmap_case, regex_np, costmap_weights


def regex_to_list(regex):
    n = len(regex)
    assert regex[0] == '^' and regex[n - 1] == '$'
    chars = []


def match(regex, string):
    return re.match("^" + regex + "$", string) is not None


def get_costmap_num(cost_map):
    return math.floor(math.sqrt(len(cost_map)))


@jit(nopython=True)
def get_costmap_index(cost_map, c):
    if not isinstance(cost_map, dict):
        return -1
    num = math.floor(math.sqrt(len(cost_map)))
    for i in range(num):
        for d in cost_map[i]:
            if c == d:
                return i
        # if match(cost_map[i], c):
        #     return i
    raise ValueError("Error when trying to identify: " + c)


@jit(nopython=True)
def get_cost(cost_map_case, cost_map_weights, c1, index1, c2, index2):
    if c1 == c2:
        return 0
    if c1.lower() == c2.lower():
        return cost_map_case
    cost = cost_map_weights[index1, index2]
    return cost


def get_weighted_levenshtein_distance(cost_map):
    case, regex, weight = split_cost_map(cost_map)

    @njit
    def distance_function(s1, s2):
        return weighted_levenshtein_distance(case, regex, weight, s1, s2)

    return distance_function


@jit(nopython=True, parallel=True)
def get_cost_map_indices(cost_map_regex, s):
    n = len(s)
    indices = np.empty(n, dtype=np.int64)
    n2 = len(cost_map_regex) - 1
    for i in prange(n):
        c = s[i]
        indices[i] = n2
        for j, row in enumerate(cost_map_regex):
            for r in row:
                if r == c:
                    indices[i] = j
                    break
            else:
                continue
            break
    # print(indices, s)
    return indices


@jit(nopython=True)
def weighted_levenshtein_distance_sequential(costmap_case, costmap_regex, costmap_weights, s1, s2):
    l1 = len(s1)
    l2 = len(s2)
    indices1 = get_cost_map_indices(costmap_regex, s1)
    indices2 = get_cost_map_indices(costmap_regex, s2)
    d = np.empty((l1 + 1, l2 + 1), dtype=np.float64)
    d[0, 0] = 0

    for i in xrange(1, l1 + 1):
        d[i, 0] = d[i - 1, 0] + get_cost(costmap_case, costmap_weights, s1[i - 1], indices1[i - 1], "", 0)

    for j in xrange(1, l2 + 1):
        d[0, j] = d[0, j - 1] + get_cost(costmap_case, costmap_weights, "", 0, s2[j - 1], indices2[j - 1])

    for i in xrange(1, l1 + 1):
        for j in xrange(1, l2 + 1):
            d[i, j] = min(
                d[i - 1, j] + get_cost(costmap_case, costmap_weights, s1[i - 1], indices1[i - 1], "", 0),  # deletion
                d[i, j - 1] + get_cost(costmap_case, costmap_weights, "", 0, s2[j - 1], indices2[j - 1]),  # insertion
                d[i - 1, j - 1] + get_cost(costmap_case, costmap_weights, s1[i - 1], indices1[i - 1], s2[j - 1],
                                           indices2[j - 1]),  # substitution
            )
    #        if i and j and s1[i] == s2[j - 1] and s1[i - 1] == s2[j]:
    #            d[(i, j)] = min(d[(i, j)], d[i - 2, j - 2] + weight_swap)  # transposition
    return d[l1, l2]


@jit(nopython=True, parallel=True)
def weighted_levenshtein_distance(costmap_case, costmap_regex, costmap_weights, s1, s2):
    l1 = len(s1)
    l2 = len(s2)
    indices1 = get_cost_map_indices(costmap_regex, s1)
    indices2 = get_cost_map_indices(costmap_regex, s2)

    d = np.empty((l1 + 1, l2 + 1), dtype=np.float64)
    d[0, 0] = 0

    n_diagonale = l1 + l2 + 1
    for diag in xrange(1, n_diagonale):

        # order from left to right: x,y in [(0|dia), (dia|0)]
        minx = 0 if diag < l2 else diag - l2
        maxx = l1 + 1 if diag > l1 else diag + 1

        for x in prange(minx, maxx):  # loop over all matrix-fields in diagonale
            y = diag - x

            if x == 0:  # initialize top row
                d[0, y] = d[0, y - 1] + get_cost(costmap_case, costmap_weights, "", 0, s2[y - 1], indices2[y - 1])

            elif y == 0:  # initialize left column
                d[x, 0] = d[x - 1, 0] + get_cost(costmap_case, costmap_weights, s1[x - 1], indices1[x - 1], "", 0)

            else:
                delete = d[x - 1, y] + get_cost(costmap_case, costmap_weights, s1[x - 1], indices1[x - 1], "", 0)
                insert = d[x, y - 1] + get_cost(costmap_case, costmap_weights, "", 0, s2[y - 1], indices2[y - 1])
                substitute = d[x - 1, y - 1] + get_cost(costmap_case, costmap_weights, s1[x - 1], indices1[x - 1],
                                                        s2[y - 1], indices2[y - 1])
                d[x, y] = min(delete, insert, substitute)

                # if x and y and s1[x] == s2[y - 1] and s1[x - 1] == s2[y]:
                #     d[x, y] = min(d[x, y], d[y - 2, y - 2] + weight_swap)  # transposition

    return d[l1, l2]


if __name__ == "__main__":
    # map = get_cost_map()
    # # print(match(" ", " "))
    # #      != None)
    # print(get_costmap_index(map, ""))
    # print(get_costmap_index(map, "a"))
    # print(get_costmap_index(map, "A"))
    # print(get_costmap_index(map, "1"))
    # print(get_costmap_index(map, " "))
    # print(get_costmap_index(map, "-"))
    #
    # print(map)

    # print(regex_to_list("^A-Z$"))
    # print(list(""))
    # c = ''
    # print(type([""]))
    #
    # l = ["a"]
    # l.append(["b", "c"])
    # print(l)
    #
    # costmap_char_list = tuple(["a", "b", tuple("cd")])
    # print(costmap_char_list)
    #
    # weights = [
    #     [0, 1, 2, 4, 4, 8],
    #     [1, 0, 1, 4, 4, 8],
    #     [2, 1, 0, 4, 4, 8],
    #     [4, 4, 4, 0, 4, 8],
    #     [4, 4, 4, 4, 0, 8],
    #     [8, 8, 8, 8, 8, 8]]
    # print(np.array(weights))
    # t = ("a", "b")
    # print(t[0])

    function = get_weighted_levenshtein_distance(get_cost_map())

    start = datetime.now()
    x = function("aax", "a1")
    print("Compile:", datetime.now() - start, ":", x)

    teststrings = ["a", "1", "Test00pü2ü9386h%%!Test00pü2ü9386h%%!7", "JamesBond007", "X Æ A-XII"]

    for i in teststrings:
        for j in teststrings:
            start = datetime.now()
            x = function(i, j)
            print(datetime.now() - start, i, "to", j, ":", x)

    # function("Jame", "01a!")

    # t = ('', ('[', 'a', '-', 'z', 'ä', 'ö', 'ü', 'ß', ']'), ('[', 'A', '-', 'Z', 'Ä', 'Ö', 'Ü', ']'), ('[', '0', '-', '9', ']'), (' ',), ('[', '\\', '$', '\\', '&', '\\', '+', ',', ':', ';', '=', '\\', '?', '@', '\\', '#', '\\', '|', "'", '<', '>', '\\', '.', '\\', '-', '\\', '^', '\\', '*', '\\', '(', '\\', ')', '%', '!', '/', ']'))
    # print(t[1])
#