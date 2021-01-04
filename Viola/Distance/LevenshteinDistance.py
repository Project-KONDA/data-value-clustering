import numpy as np


def levenshtein_distance(seq1, seq2):
    size_x = len(seq1) + 1
    size_y = len(seq2) + 1
    matrix = np.zeros((size_x, size_y))
    matrix[0, 0] = 0
    for x in range(1, size_x):
        matrix[x, 0] = x  # deletion
    for y in range(1, size_y):
        matrix[0, y] = y  # insertion
    for x in range(1, size_x):
        for y in range(1, size_y):
            if seq1[x-1] == seq2[y-1]:
                substitution_cost = 0
            else:
                substitution_cost = 1
            matrix[x, y] = min(
                matrix[x - 1, y] + 1,  # deletion
                matrix[x - 1, y - 1] + substitution_cost,  # substitution
                matrix[x, y - 1] + 1  # insertion
            )
    # print(matrix)
    return matrix[size_x - 1, size_y - 1]