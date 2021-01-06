import re
import numpy as np


# TODO: dictionary ?

# TODO: predefined compression matrices ?
compression_simple = None


def suggest_compression():
    # TODO: add parameters
    # TODO: suggest a (predefined or newly build) compression function based on user input
    pass


def compress_array(values, compression_matrix, unique):
    for i in range(len(values)):
        for compression in compression_matrix:
            values[i] = re.sub(compression[0], compression[1], values[i])

    if unique:
        return np.array(list(set(values)))  # remove duplicates
    else:
        return values


# def validate_compression_matrix(compression_matrix):
#     for i in range(len(compression_matrix)):
#         assert len(compression_matrix[i]) == 2

