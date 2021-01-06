import re
import numpy as np


char_compression = [
    ["[a-z]", "l"],
    ["[A-Z]", "L"],
    ["[0-9]", "0"]
]

sequence_compression = [
    ["[a-z]+", "w"],
    ["[A-Z]+", "S"],
    ["[0-9]+", "1"]
]

letter_sequence_compression = [
    ["[a-z]+", "w"],
    ["[A-Z]+", "S"],
    ["[0-9]", "0"]
]

number_sequence_compression = [
    ["[a-z]", "l"],
    ["[A-Z]", "L"],
    ["[0-9]+", "1"]
]

lower_sequence_compression = [
    ["[a-z]+", "w"],
    ["[A-Z]", "L"],
    ["[0-9]", "0"]
]

upper_sequence_compression = [
    ["[a-z]", "l"],
    ["[A-Z]+", "S"],
    ["[0-9]", "0"]
]


word_compression = [
    ["[a-z]", "l"],
    ["[A-Z]", "L"],
    ["l+", "w"],
    ["LL+", "M"],
    ["Lw", "W"],
    ["[0-9]+", "1"]
]

word_decimal_compression = [
    ["[a-z]", "l"],
    ["[A-Z]", "L"],
    ["l+", "w"],
    ["LL+", "M"],
    ["Lw", "W"],
    ["[0-9]+", "1"],
    ["1,1", "2"]
]


word_sequence_compression = [
    ["[a-z]", "l"],
    ["[A-Z]", "L"],
    ["l+", "w"],
    ["LL+", "M"],
    ["Lw", "W"],
    ["(w+ )+w+", "q"],
    ["(W+ )+W+", "U"],
    ["[0-9]+", "1"]
]

sentence_compression = [
    ["[a-z]", "l"],
    ["[A-Z]", "L"],
    ["l+", "w"],
    ["LL+", "M"],
    ["Lw", "W"],
    ["(w+ )+w+", "q"],
    ["(W+ )+W+", "U"],
    ["(W )[qU]+", "T"],
    ["[0-9]+", "1"]
]


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

