'''Basic choices for abstraction'''
from abstraction.abstractions import *


# pass abstraction as compression_function to clustering.clustering.cluster
from gui_abstraction.AbstractionQuestionnaireResultInput import abstraction_configuration
from gui_abstraction.abstraction_questions import abstraction_question_array


def custom_dictionary():
    # TODO: let user specify abstraction
    pass


def custom_full():
    # TODO: let user specify abstraction
    pass

# name, [method() -> (   [method(vals)->(vals, dict)], answers)]

abstraction_functions = np.array([
    ["Maximum Abstraction", lambda data: max_abstraction_function()],
    ["Manual Configuration", lambda data: abstraction_configuration (data)],

    ["No Compression", lambda data: (lambda values: (values, {}), list(np.full(len(abstraction_question_array), False)))],
    ["Duplicate Removal", lambda data: duplicate_removal_function()],

    ["letters, digits", lambda data: char_abstraction_function()],
    ["case-sensitive letters, digits", lambda data: char_abstraction_case_sensitive_function()],
    ["letter sequences and digit sequences", lambda data: sequence_abstraction_function()],
    ["case-sensitive letter sequences and digit sequences", lambda data: sequence_abstraction_case_sensitive_function()],
    ["letter sequences, digits", lambda data: letter_sequence_abstraction_function()],
    ["letters, number sequences", lambda data: number_sequence_abstraction_function()],
    ["words", lambda data: word_abstraction_function()],
    ["words and decimal", lambda data: word_decimal_abstraction_function()],
    ["sentence", lambda data: word_sequence_abstraction_function()],

    # ["Custom Dictionary", lambda data: custom_dictionary()],
    # ["Custom Full", lambda data: custom_full()]
])
