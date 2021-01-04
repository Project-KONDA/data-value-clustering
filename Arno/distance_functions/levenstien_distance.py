from pip._vendor.msgpack.fallback import xrange


# COPIED
# https://web.archive.org/web/20150302071013/http://www.guyrutenberg.com/2008/12/15/damerau-levenshtein-distance-in-python/comment-page-1/
from distance_functions.weighted_levenshtein_distance import get_cost


def damerau_levenshtein_distance_copied(s1, s2):
    d = {}
    lenstr1 = len(s1)
    lenstr2 = len(s2)
    for i in xrange(-1, lenstr1 + 1):
        d[(i, -1)] = i + 1
    for j in xrange(-1, lenstr2 + 1):
        d[(-1, j)] = j + 1

    for i in xrange(lenstr1):
        for j in xrange(lenstr2):
            if s1[i] == s2[j]:
                cost = 0
            else:
                cost = 1
            d[(i, j)] = min(
                d[(i - 1, j)] + 1,  # deletion
                d[(i, j - 1)] + 1,  # insertion
                d[(i - 1, j - 1)] + cost,  # substitution
            )
            if i and j and s1[i] == s2[j - 1] and s1[i - 1] == s2[j]:
                d[(i, j)] = min(d[(i, j)], d[i - 2, j - 2] + cost)  # transposition

    return d[lenstr1 - 1, lenstr2 - 1]


# NAIV RECURSIVE
def damerau_levenshtein_distance_naiv(st1, st2):
    st1length = len(st1)
    st2length = len(st2)

    if st1length == st2length == 0:
        return 0
    if st1length == 0:
        return get_cost("", st2[0]) + damerau_levenshtein_distance_naiv("", st2[1:])
    if st2length == 0:
        return get_cost(st1[0], "") + damerau_levenshtein_distance_naiv(st1[1:], "")
    return min(
        damerau_levenshtein_distance_naiv(st1[1:], st2[1:]) + get_cost(st1[0], st2[0]),
        damerau_levenshtein_distance_naiv(st1, st2[1:]) + get_cost("", st2[0]),
        damerau_levenshtein_distance_naiv(st1[1:], st2) + get_cost(st1[0], "")
    )


# newtry
def damerau_levenshtein_distance_self(s1, s2):
    d = {}
    length1 = len(s1)
    length2 = len(s2)
    d[(-1, -1)] = 0

    for i in xrange(0, length1):
        d[(i, -1)] = d[(i - 1, -1)] + get_cost(s1[i], "")
        print(i, -1, d[(i, -1)])

    for j in xrange(0, length2):
        d[(-1, j)] = d[(-1, j - 1)] + get_cost("", s2[j])
        print(-1, j, d[(-1, j)])

    for i in xrange(0, length1):
        for j in xrange(0, length2):
            d[(i, j)] = min(
                d[(i - 1, j)] + get_cost(s1[i], ""),  # deletion
                d[(i, j - 1)] + get_cost("", s2[j]),  # insertion
                d[(i - 1, j - 1)] + get_cost(s1[i], s2[j]),  # substitution
            )
            print(i, j, d[(i, j)])
    #        if i and j and s1[i] == s2[j - 1] and s1[i - 1] == s2[j]:
    #            d[(i, j)] = min(d[(i, j)], d[i - 2, j - 2] + weight_swap)  # transposition

    return d[length1 - 1, length2 - 1]
