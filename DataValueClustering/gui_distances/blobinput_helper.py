from math import sin, radians, cos, sqrt, floor

import numpy as np


# create n coordinates of equal distance to middlepoint x|y clockwise
def create_coordinates(x, y, labels):
    distance_to_center = min(x, y) / 1.5
    # array: [label, x, y, size]
    array = np.empty((len(labels), 2), dtype=object)
    degree_delta = 360 / len(labels)

    for i, l in enumerate(labels):
        degree = i * degree_delta - 135
        g = sin(radians(degree)) * distance_to_center
        a = cos(radians(degree)) * distance_to_center
        array[i, 0] = x + a
        array[i, 1] = y + g
        # array[i, 2] = image_sizes

    return array


def matrix_is_valid(matrix, n=-1):
    if type(matrix) is not type({}):
        return False
    if n < 0:
        n = int(floor(sqrt(len(matrix))))
    else:
        if not n == int(floor(sqrt(len(matrix)))):
            return False

    if not len(matrix) == n * n + n + 1:
        return False
    # test Values - () is number
    if () not in matrix:
        return False
    if not isinstance(matrix[()], float):
        return False
    # test Values - (i) is single-character regex
    for i in range(n):
        if i not in matrix:
            return False
        if not isinstance(matrix[i], str):
            return False
    # test Values - (i,j) is number
    for i in range(n):
        for j in range(n):
            if (i, j) not in matrix:
                return False
            if not isinstance(matrix[(i, j)], float):
                return False
    return True


def print_cost_matrix(matrix):
    n = int(floor(sqrt(len(matrix))))
    if not matrix_is_valid(matrix):
        print("{}")
        return
    s = "{"
    s += str(matrix[()])
    print(s)
    s = f'{"": <15}'
    for i in range(n):
        s += f'{str(matrix[i]): <10}  '
    print(s)
    for i in range(n):
        s = f'{matrix[i] + ":": <15}'
        for j in range(n):
            s += f'{str(matrix[(j, i)]): <10}  '
        print(s)
    print("}")
