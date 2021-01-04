import re

import numpy as np

from tests.testdata import data_test

compression_simple = [
    # regex , replacement
    ["[a-z]+", "a"],
    ["[A-Z]+", "A"],
    ["[0-9]+", "0"]
]

compression_ = [
    # regex , replacement
    ["[A-Z][a-z]+", "W"],  # Word
    ["[a-z]+", "w"],  # word
    # ["[0-9]+.[0-9]+", "d"],  # decimal english
    ["[0-9]+,[0-9]+", "e"],  # decimal german
    ["[0-9]+", "i"]  # int
]

compression_typed = [
    ["[a-z]", "c"],  # char
    ["[A-Z]", "C"],  # Char
    ["Cc+", "W"],  # Word
    ["cc+", "w"],  # Word
    ["[0-9]+", "1"],  # int
    ["1,1", "2"]  # decimal
]


def compress_array(strings, replacements):
    for s in range(len(strings)):
        for i in replacements:
            strings[s] = re.sub(i[0], i[1], strings[s])
    return np.array(list(set(strings)))


if __name__ == '__main__':
    print(6)
