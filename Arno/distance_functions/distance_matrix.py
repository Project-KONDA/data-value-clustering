import numpy as np

from distance_functions.weighted_levenshtein_distance import levenshtein_distance
from tests.testdata import data_test
from scipy.spatial.distance import is_valid_y

from compression.thin import super_thin_array_amounts


def calculate_distance_matrix(distance_function, values):
    size = len(values)
    matrix = np.zeros((size, size))
    for y in range(size):
        for x in range(y):
            matrix[x, y] = distance_function(values[x], values[y])
    return matrix


def calculate_condensed_distance_matrix(distance_function, values):
    distance_matrix = calculate_distance_matrix(distance_function, values)
    size_y = len(distance_matrix[0])
    condensed_distance_matrix = np.zeros(sum(range(size_y)))

    # transform two-dimensional matrix into one-dimensional array:
    for y in range(1, size_y):
        for x in range(y):
            i = y - 1
            if x >= 1:
                i += size_y - x - 1  # -y+y
            if x >= 2:
                for j in range(0, x - 1):
                    i += (size_y - (x - j))
            condensed_distance_matrix[i] = distance_matrix[x, y]

    if is_valid_y(condensed_distance_matrix):
        return condensed_distance_matrix
    else:
        return None


def calculate_condensed_distance_matrix2(distance_function, values):
    size_y = sum(range(len(values)))
    condensed_distance_matrix = np.zeros(size_y)
    # print(sum(range(size_y)))
    # print(condensed_distance_matrix)

    i = 0
    for y in range(len(values)):
        for x in range(y+1, len(values)):
            condensed_distance_matrix[i] = distance_function(values[x], values[y])
            i += 1
    assert (i == len(condensed_distance_matrix))

    if is_valid_y(condensed_distance_matrix):
        print(list(condensed_distance_matrix))
        return condensed_distance_matrix
    else:
        return None


if __name__ == "__main__":
    1
    # lambda vals: super_thin_array_amounts(vals)[:, 1]
    # data_test[0:10000]
    # print(calculate_condensed_distance_matrix(levenshtein_distance, data_test[0:10]))
