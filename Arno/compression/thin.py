import re

import numpy as np


def thin_string(s):

    s = re.sub('[a-zäöüß]+', 'a', s)
    s = re.sub('[A-Z´ÄÖÜ]+', 'B', s)
    s = re.sub('[0-9]+', '0', s)
    return s


def get_originals(s, thinfunction, values):
    result = list()
    for v in values:
        if thinfunction(v) == s:
            result.append(v)
    return result


def matches_thin_string(s, t):
    return thin_string(s) == t


def thin_array(a):
    for i in range(len(a)):
        a[i] = thin_string(a[i])
    return a


def super_thin_array(vals):
    return list(set(thin_array(vals)))


def count_x(x, a):
    n = 0
    for i in range(len(a)):
        if x == a[i]:
            n += 1
    return n


def super_thin_array_amounts(values):
    thin = thin_array(values)
    s_thin = super_thin_array(values)
    for i in range(len(s_thin)):
        s_thin[i] = [i, s_thin[i], count_x(s_thin[i], thin)]
    return np.array(s_thin)
