import numpy as np

from compression.compression import compress_array, suggest_compression, compression_simple


# pass compression as compression_function to clustering.clustering.cluster


def automatic():
    # TODO: ask user questions about the data

    return suggest_compression  # TODO: add arguments


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

