import numpy as np
from matplotlib import pyplot as plt

from scipy.spatial.distance import is_valid_y


def plot_box(condensed_matrix):
    plt.boxplot(condensed_matrix)
    plt.show()


def plot_histogram(condensed_matrix):
    n_bins = len(np.array(list(set(condensed_matrix))))
    plt.hist(condensed_matrix, bins=n_bins)
    plt.show()


def plot_image(matrix):
    plt.imshow(matrix)
    plt.colorbar()
    plt.show()


def plot_at_y(condensed_matrix):
    plt.plot(condensed_matrix, np.zeros_like(condensed_matrix), '.',)
    plt.show()


def get_condensed(matrix):
    size = len(matrix)
    condensed = np.zeros(sum(range(1, size)))
    i = 0
    for y in range(size):
        for x in range(y):
            condensed[i] = matrix[x, y]
            i += 1
    return condensed


def avg_distance(condensed_matrix):
    n = len(condensed_matrix)
    return sum(condensed_matrix)/n


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


def calculate_affinity_matrix(distance_function, values):
    distance_matrix = calculate_distance_matrix(distance_function, values)
    affinity_matrix = 1 - (distance_matrix / max(distance_matrix))
    assert max(affinity_matrix) <= 1
    assert min(affinity_matrix) >= 0
    return affinity_matrix


if __name__ == "__main__":
    distance_matrix = np.array([
        [0, 1,  2,   1.5],
        [0, 0,  1.5, 1.3],
        [0, 0,  0.5, 1.1],
        [0, 0,  0,   0]
    ])

    condensed_matrix = get_condensed(distance_matrix)

    print(min_distance(condensed_matrix))
    print(max_distance(condensed_matrix))
    print(avg_distance(condensed_matrix))

    plot_image(distance_matrix)

    plot_box(condensed_matrix)
    plot_histogram(condensed_matrix)
    plot_at_y(condensed_matrix)