from compression.compression import *


# pass compression as compression_function to clustering.clustering.cluster
from gui_compression.CompressionQuestionnaireResultInput import compression_configuration
from gui_compression.compression_questions import compression_question_array


def custom_dictionary():
    # TODO: let user specify compression
    pass


def custom_full():
    # TODO: let user specify compression
    pass

# name, [method() -> (   [method(vals)->(vals, dict)], answers)]

compression_functions = np.array([
    ["Manual Configuration", lambda data: compression_configuration (data)],

    ["No Compression", lambda data: (lambda values: (values, {}), list(np.full(len(compression_question_array), False)))],
    ["Maximum Compression", lambda data: max_compression_function()],

    ["letters, digits", lambda data: char_compression_function()],
    ["case-sensitive letters, digits", lambda data: char_compression_case_sensitive_function()],
    ["letter sequences and digit sequences", lambda data: sequence_compression_function()],
    ["case-sensitive letter sequences and digit sequences", lambda data: sequence_compression_case_sensitive_function()],
    ["letter sequences, digits", lambda data: letter_sequence_compression_function()],
    ["letters, number sequences", lambda data: number_sequence_compression_function()],
    ["words", lambda data: word_compression_function()],
    ["words and decimal", lambda data: word_decimal_compression_function()],
    ["sentence", lambda data: word_sequence_compression_function()],

    # ["Custom Dictionary", lambda data: custom_dictionary()],
    # ["Custom Full", lambda data: custom_full()]
])
