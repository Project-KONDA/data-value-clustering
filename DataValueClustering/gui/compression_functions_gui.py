import numpy as np

from compression.compression import *


# pass compression as compression_function to clustering.clustering.cluster


def automatic():
    # TODO: ask user questions about the data

    answers = []  # TODO: save answers

    return get_compression_method(answers)  # TODO: add arguments


def custom_dictionary():
    # TODO: let user specify compression
    pass


def custom_full():
    # TODO: let user specify compression
    pass


compression_functions = np.array([
    ["No Compression", lambda vals: (vals, {})],

    ["letters, digits", char_compression_function],
    ["case-sensitive letters, digits", char_compression_case_sensitive_function],
    ["letter sequences and digit sequences", sequence_compression_function],
    ["case-sensitive letter sequences and digit sequences", sequence_compression_case_sensitive_function],
    ["letter sequences, digits", letter_sequence_compression_function],
    ["letters, number sequences", number_sequence_compression_function],
    ["words", word_compression_function],
    ["words and decimal", word_decimal_compression_function],
    ["sentence", word_sequence_compression_function],

    ["Atomatic", automatic]
    # ["Custom Dictionary", custom_dictionary],
    # ["Custom Full", custom_full]
])
