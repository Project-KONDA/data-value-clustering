import numpy as np

from compression.compression import compress_array, suggest_compression, compression_simple


# pass compression as compression_function to clustering.clustering.cluster


def automatic():
    # TODO: ask user questions about the data

    questions = [
        "Should all lower case letters be treated equally?",
        "Should all upper case letters be treated equally?",
        "Should an upper case letter be treated as its lower case variant?",  # note: if true and previous two are also true then all letters are treated equally
        "Should all digits be treated equally?",

        "Should all lower and upper case letter sequences be treated equally?",
        "Should all lower case letter sequences (= lower case word) be treated equally?",
        "Should all upper case letter sequences be treated equally?",
        "Should all letter sequences beginning with an upper case letter followed by a sequence of lower case letters (= upper case word) be treated equally?",

        "Should all sequences of lower or upper case words be treated equally?",
        "Should all sequences of lower case words be treated equally?",
        "Should all sequences of upper case words be treated equally?",
        "Should all sequences of words starting with an upper case word being followed by lower or upper case words be treated equally?"

        "Should all digit sequences that contain a comma be treated equally?",
        "Should all digit sequences be treated equally?",

    ]

    answers = []  # TODO: save answers

    return suggest_compression(answers)  # TODO: add arguments


def custom_dictionary():
    # TODO: let user specify compression
    pass


def custom_full():
    # TODO: let user specify compression
    pass


compression_functions = np.array([
    ["No Compression",
     lambda vals: vals],
    ["Compression Simple",
    lambda values: compress_array(values, compression_simple)],
    # TODO: add more predefined compressions
    ["Atomatic",
     automatic],
    ["Custom Dictionary",
     custom_dictionary],
    ["Custom Full",
     custom_full]
    # TODO: add compressions in the form lambda values: compress_array(values, compression_simple)]
])

