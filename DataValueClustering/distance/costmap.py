import math
import re

import numpy as np
from numba import jit, prange
from pip._vendor.msgpack.fallback import xrange


def suggest_cost_map():
    # TODO: add parameters
    # TODO: suggest a (predefined or newly build) cost map based on user input
    pass


# TODO: predefined cost maps ?


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
def get_cost(cost_map_case, cost_map_weights, c1, index1, c2, index2):
    if c1 == c2:
        return 0
    if c1.lower() == c2.lower():
        return cost_map_case
    cost = cost_map_weights[index1, index2]
    return cost


# @jit(nopython=True, parallel=True)
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