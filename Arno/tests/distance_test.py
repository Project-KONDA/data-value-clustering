import numpy as np

from distance_functions.weighted_levenshtein_distance import levenshtein_distance

lt = np.array([
    ["", "", "", "a"],
    #["a", "ab", "a", "nc"],
    ["a", "c", "a", "1"],
    ["a", "A", "a", "1"],
    ["a", "B", "a", "1"],
    ["a", "b", "a", "1"],
    ["a", "A", "a", "1"],
    ["a", "1", "a", "."],
    ["a", ".", "a", ".."],
    ["a", "a", "!", "."],
    ["a", "b", "!", "."],
    ["a", "ab", "a", "a b"],
    ["a", "a b", "a", "A b"],
    ["", "", "", "a"]
])

eq = np.array([
    ["---", "---", "", ""],
    ["", "", "", ""],
    ["a", "b", "b", "a"],
    ["A", "a", "a", "c"],
    ["a", ".", ".", "a"],
    ["!", ".", ".", "!"],
    ["a", " ", " ", "a"],
    [".", " ", " ", "."],
    ["a", "1", "1", "a"],
    ["", "a", "", "b"],
    ["a", "", "", "b"],
    ["a", "b", "a", "c"],
    ["", "b", "", "a"],
    ["A", "1", "a", "1"],
    ["A", ".", "a", "."]
])

if __name__ == '__main__':
    for i in lt:
        if not (levenshtein_distance(i[0], i[1]) < levenshtein_distance(i[2], i[3])):
            print(i, levenshtein_distance(i[0], i[1]), levenshtein_distance(i[2], i[3]))
    for i in eq:
        assert levenshtein_distance(i[0], i[1]) == levenshtein_distance(i[2], i[3])
