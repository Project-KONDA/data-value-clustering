import numpy as np
from scipy.spatial.distance import is_valid_y


def calculate_distance_matrix(distance_function, values):
    size = len(values)
    matrix = np.zeros((size, size))
    for y in range(size):
        for x in range(y):
            matrix[x, y] = distance_function(values[x], values[y])
    return matrix


def calculate_condensed_distance_matrix(distance_function, values):
    size_y = sum(range(len(values)))
    condensed_distance_matrix = np.zeros(size_y)

    i = 0
    for y in range(len(values)):
        for x in range(y+1, len(values)):
            condensed_distance_matrix[i] = distance_function(values[x], values[y])
            i += 1
    assert (i == len(condensed_distance_matrix))

    if is_valid_y(condensed_distance_matrix):
        return condensed_distance_matrix
    else:
        return None

