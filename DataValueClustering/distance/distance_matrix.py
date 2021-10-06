'''Calculate distance matrix containing pairwise distances between abstracted data values.'''
import time
from datetime import datetime

import numpy as np
from numba import njit

def get_condensed(matrix):
    size = len(matrix)
    condensed = np.zeros(sum(range(1, size)))
    i = 0
    for y in range(size):
        for x in range(y+1, size):
            condensed[i] = matrix[x, y]
            i += 1
    return condensed


def avg_distance(condensed_matrix):
    n = len(condensed_matrix)
    return sum(condensed_matrix) / n


def min_distance(condensed_matrix):
    return min(condensed_matrix)


def max_distance(condensed_matrix):
    return max(condensed_matrix)


def get_symmetric(matrix):
    symmetric_matrix = matrix.copy()
    for i in range(len(symmetric_matrix)):
        for j in range(i):
            symmetric_matrix[i, j] = matrix[j, i]
    return symmetric_matrix


def calculate_distance_matrix_map(distance_function, values, duplicates_removed):
    start = time.time()
    if duplicates_removed:
        map = calculate_distance_matrix_map_without_duplicates(distance_function, values)
    else:
        map = calculate_distance_matrix_map_with_duplicates(distance_function, values)
    end = time.time()
    print(end - start)
    return map


@njit
def calculate_distance_matrix_map_jit(distance_function, values, matrix, condensed_matrix):
    min_distance = np.inf
    max_distance = 0.
    condensed_index = 0
    size = len(values)
    for y in range(size):
        matrix[y, y] = 0
        for x in range(y + 1, size):
            vx = str(values[x])  # numba needs str
            vy = str(values[y])  # numba needs str
            distance_x_y = distance_function(vx, vy)

            if x != y and distance_x_y < min_distance:
                min_distance = float(distance_x_y)
            if distance_x_y > max_distance:
                max_distance = distance_x_y

            matrix[x, y] = distance_x_y
            matrix[y, x] = distance_x_y
            # if x >= y + 1:
            condensed_matrix[condensed_index] = distance_x_y
            condensed_index += 1

        print("...", round((y + 1) / size * 100, 1), "%")

    assert (condensed_index == len(condensed_matrix))
    # if not is_valid_y(condensed_matrix):
    #     condensed_matrix = None

    affinity_matrix = calculate_affinity_matrix_from_distance_matrix(matrix)

    return matrix, condensed_matrix, affinity_matrix, min_distance, max_distance


def calculate_distance_matrix(distance_function, values):
    size = len(values)
    matrix = np.zeros((size, size))
    for y in range(size):
        for x in range(size):  # y?
            matrix[x, y] = distance_function(values[x], values[y])
    return matrix


def calculate_affinity_matrix(distance_function, values):
    distance_matrix = calculate_distance_matrix(distance_function, values)
    return calculate_affinity_matrix_from_distance_matrix(distance_matrix)


@njit
def calculate_affinity_matrix_from_distance_matrix(distance_matrix):
    affinity_matrix = 1 - (distance_matrix / np.amax(distance_matrix))

    assert np.amax(affinity_matrix) <= 1
    assert np.amin(affinity_matrix) >= 0
    return affinity_matrix


def upscale_dm_cdm(distance_matrix, abstracted_values, original_values):
    n = len(original_values)
    n_a = len(abstracted_values)
    abstracted = list(abstracted_values)
    if n_a == n:
        return distance_matrix
    index = list()
    for v in original_values:
        index.append(abstracted.index(v))
    dm = np.full((n, n), -1)
    for i, a in enumerate(index):
        for j, b in enumerate(index):
            dm[i, j] = \
                distance_matrix[(a, b)]
    cdm = get_condensed(dm)
    return dm, cdm


def calculate_distance_matrix_map_without_duplicates(distance_function, values):
    size = len(values)
    matrix = np.full((size, size), -1.0, dtype=np.float32)
    condensed_matrix = np.zeros(sum(range(1, size)), dtype=np.float32)

    dm, cdm, am, mi, ma = calculate_distance_matrix_map_jit(distance_function, values, matrix, condensed_matrix)
    return {"distance_matrix": dm,
            "condensed_distance_matrix": cdm,
            "affinity_matrix": am,
            "min_distance": mi,
            "max_distance": ma}


def calculate_distance_matrix_map_with_duplicates(distance_function, values):
    unique_values = np.array(list(set(values)), dtype=np.str)
    size = len(values)
    size_unique = len(unique_values)

    if (float(size_unique) // float(size)) < 0.8:
        matrix = np.full((size_unique, size_unique), -1.0, dtype=np.float32)
        condensed_matrix = np.zeros(sum(range(1, size_unique)), dtype=np.float32)

        dm, cdm, am, mi, ma = calculate_distance_matrix_map_jit(distance_function, unique_values, matrix, condensed_matrix)
        dm, cdm = upscale_dm_cdm(dm, unique_values, values)
        am = calculate_affinity_matrix_from_distance_matrix(dm)
        return {"distance_matrix": dm,
                "condensed_distance_matrix": cdm,
                "affinity_matrix": am,
                "min_distance": mi,
                "max_distance": ma}
    else:
        return calculate_distance_matrix_map_without_duplicates(distance_function, values)


if __name__ == "__main__":
    # from gui_distances.matrix_plots import plot_box, plot_histogram, plot_image, plot_at_y
    #
    # distance_matrix = np.array([
    #     [0, 1, 2, 1.5],
    #     [0, 0, 1.5, 1.3],
    #     [0, 0, 0.5, 1.1],
    #     [0, 0, 0, 0]
    # ])
    #
    # condensed_matrix = get_condensed(distance_matrix)
    #
    # print(min_distance(condensed_matrix))
    # print(max_distance(condensed_matrix))
    # print(avg_distance(condensed_matrix))
    #
    # plot_image(distance_matrix)
    #
    # plot_box(condensed_matrix)
    # plot_histogram(condensed_matrix)
    # plot_at_y(condensed_matrix)

    from weighted_levenshtein_distance import get_weighted_levenshtein_distance, get_cost_map

    distance_function = get_weighted_levenshtein_distance(
        get_cost_map()
    )

    values = np.array(["a", "1", "Test007", "JamesBond007", "Hallo"], dtype=np.str)

    start = datetime.now()
    x = calculate_distance_matrix_map(
        distance_function,
        values,
        True
    )
    print("Compile:", datetime.now() - start, ":", x)
    # print(type(b))
    start = datetime.now()
    x = calculate_distance_matrix_map(
        distance_function,
        values,
        True
    )
    print("Normal:", datetime.now() - start, ":", x)
