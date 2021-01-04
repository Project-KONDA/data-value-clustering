import numpy as np
from scipy.spatial.distance import is_valid_y
from Compression.Compression import get_compression_from_value, compressed_value_index_map


def negate(distance_matrix):
    size_i = len(distance_matrix)
    size_j = len(distance_matrix[0])
    for i in range(size_i):
        for j in range(size_j):
            distance_matrix[i, j] = distance_matrix[i, j] * (-1)
    return distance_matrix


def calculate_complete_distance_matrix(triangular_distance_matrix):
    size_i = len(triangular_distance_matrix)
    size_j = len(triangular_distance_matrix[0])
    matrix = np.zeros((size_i, size_j))
    for j in range(size_j):
        for i in range(j):
            matrix[j,i] = triangular_distance_matrix[i,j]
            matrix[i, j] = triangular_distance_matrix[i, j]
    return matrix

def calculate_condensed_distance_matrix_original_values(original_values, compressed_values, unique_values, distance_matrix):
    distance_matrix_original_values = calculate_distance_matrix_original_values(original_values, compressed_values, unique_values, distance_matrix)
    return condense_distance_matrix(distance_matrix_original_values), distance_matrix_original_values


def calculate_distance_matrix_original_values(original_values, compressed_values, unique_values, distance_matrix):
    size = len(original_values)
    distance_matrix_original_values = np.zeros((size, size))
    index_map = compressed_value_index_map(unique_values)
    for j in range(size):
        for i in range(j):
            k = index_map[get_compression_from_value(compressed_values, i)]
            l = index_map[get_compression_from_value(compressed_values, j)]
            if l < k:
                distance_matrix_original_values[i, j] = distance_matrix[l, k]
            else:
                distance_matrix_original_values[i, j] = distance_matrix[k, l]
    return distance_matrix_original_values


def calculate_condensed_distance_matrix(values, distance_function):
    distance_matrix = calculate_distance_matrix(values, distance_function)
    return condense_distance_matrix(distance_matrix), distance_matrix


def condense_distance_matrix(distance_matrix):
    size_y = len(distance_matrix[0])
    condensed_distance_matrix = np.zeros(sum(range(size_y)))

    # transform two-dimensional matrix into one-dimensional array:
    for y in range(1, size_y):
        for x in range(y):
            i = y-1
            if x >= 1:
                i += size_y-y+y-x-1
            if x >= 2:
                for j in range(0, x - 1):
                    i += (size_y - (x - j))
            condensed_distance_matrix[i] = distance_matrix[x, y]

    if is_valid_y(condensed_distance_matrix):
        return condensed_distance_matrix
    else:
        return None, None


def calculate_distance_matrix(values, distance_function):
    # TODO: use cost_matrix
    size = len(values)
    distance_matrix = np.zeros((size, size))
    for y in range(size):
        for x in range(y):
            distance_matrix[x, y] = distance_function(values[x], values[y])
    # print(distance_matrix)
    # plot_matrix(distance_matrix)
    return distance_matrix
