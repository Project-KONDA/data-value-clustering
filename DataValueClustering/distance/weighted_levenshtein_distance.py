import re
import math

import numpy as np
from numba import jit
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


def get_cost(cost_map, c1, c2):
    if c1 == c2:
        return 0
    if lower(c1) == lower(c2):
        return cost_map[()]
    k1 = get_costmap_index(cost_map, c1)  # TODO: remove
    k2 = get_costmap_index(cost_map, c2)  # TODO: remove
    return cost_map[(k1, k2)]


def weighted_levenshtein_distance(cost_map, s1, s2):
    costmap_case, costmap_regex, costmap_weights = split_cost_map(cost_map)
    costmap_char_list = []  # TODO: use np array instead
    for regex in costmap_regex:
        if regex == "":
            costmap_char_list.append(("",))
        else:
            costmap_char_list.append(tuple(regex))
    costmap_char_list = tuple(costmap_char_list)
    costmap_weights = np.array(costmap_weights)
    s1 = tuple(s1)
    s2 = tuple(s2)
    return weighted_levenshtein_distance_jit(costmap_case, costmap_char_list, costmap_weights, s1, s2)


@jit(nopython=True)
def get_indices(costmap_regex, s):
    n = len(costmap_regex)
    indices = np.empty(len(s), dtype=np.int64)
    # print(costmap_regex)
    for i in range(len(s)):
        indices[i] = n-1
        for j in range(n):
            print(type(j))
            # regex = costmap_regex[j]
            regex = costmap_regex[j]
            n_regex = len(regex)
            for k in range(n_regex):
                if regex[k] == s[i]:
                    indices[i] = j
                    continue
    return indices


@jit(nopython=True)
def weighted_levenshtein_distance_jit(costmap_case, costmap_regex, costmap_weights, s1, s2):
    print(costmap_regex)
    i1 = get_indices(costmap_regex, s1)
    i2 = get_indices(costmap_regex, s2)

    # TODO: use i1 and i2

    l1 = len(s1)
    l2 = len(s2)

    d = np.empty((l1+1, l2+1), dtype=float)

    d[0, 0] = 0

    for i in xrange(1, l1+1):
        d[i, 0] = d[i - 1, 0] + get_cost(costmap_case, costmap_regex, costmap_weights, s1[i-1], "")
    #    print(i, -1, d[(i, -1)])

    for j in xrange(1, l2+1):
        d[0, j] = d[0, j - 1] + get_cost(costmap_case, costmap_regex, costmap_weights, "", s2[j-1])
    #    print(-1, j, d[(-1, j)])

    for i in xrange(1, l1+1):
        for j in xrange(1, l2+1):
            d[i, j] = min(
                d[i - 1, j] + get_cost(costmap_case, costmap_regex, costmap_weights, s1[i-1], ""),  # deletion
                d[i, j - 1] + get_cost(costmap_case, costmap_regex, costmap_weights, "", s2[j-1]),  # insertion
                d[i - 1, j - 1] + get_cost(costmap_case, costmap_regex, costmap_weights, s1[i-1], s2[j-1]),  # substitution
            )
    #        print(i, j, d[(i, j)])
    #        if i and j and s1[i] == s2[j - 1] and s1[i - 1] == s2[j]:
    #            d[(i, j)] = min(d[(i, j)], d[i - 2, j - 2] + weight_swap)  # transposition
    return d[l1 - 1, l2 - 1]


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
    weighted_levenshtein_distance(get_cost_map(),"haus","maus")
    # t = ('', ('[', 'a', '-', 'z', 'ä', 'ö', 'ü', 'ß', ']'), ('[', 'A', '-', 'Z', 'Ä', 'Ö', 'Ü', ']'), ('[', '0', '-', '9', ']'), (' ',), ('[', '\\', '$', '\\', '&', '\\', '+', ',', ':', ';', '=', '\\', '?', '@', '\\', '#', '\\', '|', "'", '<', '>', '\\', '.', '\\', '-', '\\', '^', '\\', '*', '\\', '(', '\\', ')', '%', '!', '/', ']'))
    # print(t[1])
