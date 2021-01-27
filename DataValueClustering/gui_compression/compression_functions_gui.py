from compression.compression import *


# pass compression as compression_function to clustering.clustering.cluster
from gui_compression.compression_questionnaire import compression_configuration
from gui_compression.questions import question_array


def custom_dictionary():
    # TODO: let user specify compression
    pass


def custom_full():
    # TODO: let user specify compression
    pass

# name, [method() -> (   [method(vals)->(vals, dict)], answers)]

compression_functions = np.array([
    ["Manual Configuration", compression_configuration],

    ["No Compression", lambda: (lambda values: (values, {}), list(np.full(len(question_array), False)))],
    ["Maximum Compression", max_compression_function],

    ["letters, digits", char_compression_function],
    ["case-sensitive letters, digits", char_compression_case_sensitive_function],
    ["letter sequences and digit sequences", sequence_compression_function],
    ["case-sensitive letter sequences and digit sequences", sequence_compression_case_sensitive_function],
    ["letter sequences, digits", letter_sequence_compression_function],
    ["letters, number sequences", number_sequence_compression_function],
    ["words", word_compression_function],
    ["words and decimal", word_decimal_compression_function],
    ["sentence", word_sequence_compression_function],

    # ["Custom Dictionary", custom_dictionary],
    # ["Custom Full", custom_full]
])
