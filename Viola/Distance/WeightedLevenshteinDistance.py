import re

import numpy as np


def weighted_levenshtein_distance_args(cost_matrix):
    return lambda seq1, seq2: weighted_levenshtein_distance(seq1, seq2, cost_matrix)


def weighted_levenshtein_distance(seq1, seq2, cost_matrix):
    # TODO: use cost_matrix
    size_x = len(seq1) + 1
    size_y = len(seq2) + 1
    matrix = np.zeros((size_x, size_y))
    matrix[0, 0] = 0
    for x in range(1, size_x):
        matrix[x, 0] = matrix[x - 1, 0] + deletion_cost_compressed1(seq1[x - 1], seq1[x - 2])  # deletion
    for y in range(1, size_y):
        matrix[0, y] = matrix[0, y - 1] + insertion_cost_compressed1(seq2[y - 1], seq2[y - 2])  # insertion
    for x in range(1, size_x):
        for y in range(1, size_y):
            matrix[x, y] = min(
                matrix[x - 1, y] + deletion_cost_compressed1(seq1[x - 1], seq1[x - 2]),  # deletion
                matrix[x - 1, y - 1] + substitution_cost_compressed1(seq1[x - 1], seq1[x - 2], seq2[y - 1], seq2[y - 2]),  # substitution
                matrix[x, y - 1] + insertion_cost_compressed1(seq2[y - 1], seq2[y - 2])  # insertion
            )
    # print(matrix)
    return matrix[size_x - 1, size_y - 1]


# cost functions:

def substitution_cost_compressed1(c1, prev1, c2, prev2):
    if c1 == c2:  # same character
        return 0
    else:  # different character
        if is_special(c1) and is_special(c2):
            return 2
        elif (is_lower_case(c1) and is_upper_case(c2)) or (is_lower_case(c2) and is_upper_case(c1)):
            return 0.5
        elif (is_lower_case(c1) and is_digit(c2)) or (is_lower_case(c2) and is_digit(c1)):
            return 0.75
        elif (is_lower_case(c1) and is_space(c2)) or (is_lower_case(c2) and is_space(c1)):
            return 0.75
        elif (is_lower_case(c1) and is_special(c2)) or (is_lower_case(c2) and is_special(c1)):
            return 2
        elif (is_upper_case(c1) and is_digit(c2)) or (is_upper_case(c2) and is_digit(c1)):
            return 0.75
        elif (is_upper_case(c1) and is_space(c2)) or (is_upper_case(c2) and is_space(c1)):
            return 0.75
        elif (is_upper_case(c1) and is_special(c2)) or (is_upper_case(c2) and is_special(c1)):
            return 2
        elif (is_digit(c1) and is_space(c2)) or (is_digit(c2) and not is_space(c1)):
            return 0.75
        elif (is_digit(c1) and is_special(c2)) or (is_digit(c2) and not is_special(c1)):
            return 2
        else:
            # TODO
            return 1


def insertion_cost_compressed1(c, prev):
    if is_lower_case(c):
        if is_upper_case(prev) or is_space(prev):
            return 0.0625
        else:
            return 0.125
    elif is_upper_case(c):
        return 0.25
    elif is_digit(c):
        return 0.5
    elif is_space(c):
        return 0.75
    elif is_special(c):
        return 2
    else:
        return 1


def deletion_cost_compressed1(c, prev):
    return insertion_cost_compressed1(c, prev)


# def insertion_cost_compressed4(c, prev):
#     if is_lower_case(c):
#         if is_upper_case(prev) or is_space(prev):
#             return 0.0625
#         else:
#             return 0.125
#     elif is_upper_case(c):
#         return 0.25
#     elif is_digit(c):
#         return 0.5
#     elif is_space(c):
#         return 0.75
#     elif is_special(c):
#         return 2
#     else:
#         return 1


def is_lower_case(c):
    return re.search("^[a-z]$", c)


def is_upper_case(c):
    return re.search("^[A-Z]$", c)


def is_digit(c):
    return re.search("^[0-9]$", c)


def is_space(c):
    return re.search("^ $", c)


def is_special(c):
    escaped = re.escape(".!?-+*#/()&%[]=$~:; ")
    regex = "^[" + escaped + "]$"
    return re.search(regex, c)


def to_lower_case(c):
    return c.lower()