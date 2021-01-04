import np as np
import numpy as np

from main import damerau_levenshtein_distance, get_my_kind, weight, get_cost

kind = np.array([
    ["", 0],
    ["a", 1],
    ["b", 1],
    ["A", 2],
    ["B", 2],
    ["1", 3],
    ["9", 3],
    [" ", 4],
    [".", 5],
    ["!", 5]
])

cost = np.array([
    ["", 0],
    ["a", 1],
    ["b", 1],
    ["A", 2],
    ["B", 2],
    ["1", 3],
    ["9", 3],
    [" ", 4],
    [".", 5],
    ["!", 5]
])

kinds = ["", "a", "B", "1", " ", "!"]

if __name__ == '__main__':
    print(damerau_levenshtein_distance("a", "B"))
    print(damerau_levenshtein_distance("a", "1"))
    print(damerau_levenshtein_distance("---", "---"))
    for i in kind:
        assert get_my_kind(i[0]) == int(i[1])

    for j in kinds:
        for k in kinds:
            assert get_cost(j, k) == weight[get_my_kind(j), get_my_kind(k)] or j == k and get_cost(j, k) == 0
