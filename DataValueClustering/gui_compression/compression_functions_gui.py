from compression.compression import *
from gui_compression.compression_questionaire import automatic

from gui_compression.compression_questions import compression_question_array


def custom_dictionary():
    # TODO: let user specify compression
    pass


def custom_full():
    # TODO: let user specify compression
    pass

# name, [method() -> (   [method(vals)->(vals, dict)], answers)]

compression_functions = np.array([
    ["max", lambda data: max_compression_function()],

    ["Atomatic", lambda data: automatic()],
    ["No Compression", lambda data: (lambda values: (values, {}), list(np.full(len(compression_question_array), False)))],

    ["letters, digits", lambda data: char_compression_function()],
    ["case-sensitive letters, digits", lambda data: char_compression_case_sensitive_function()],
    ["letter sequences and digit sequences", lambda data: sequence_compression_function()],
    ["case-sensitive letter sequences and digit sequences", lambda data: sequence_compression_case_sensitive_function()],
    ["letter sequences, digits", lambda data: letter_sequence_compression_function()],
    ["letters, number sequences", lambda data: number_sequence_compression_function()],
    ["words", lambda data: word_compression_function()],
    ["words and decimal", lambda data: word_decimal_compression_function()],
    ["sentence", lambda data: word_sequence_compression_function()],

    # ["Custom Dictionary", custom_dictionary],
    # ["Custom Full", custom_full]
])
