from math import sin, radians, cos, sqrt, floor

import numpy as np


# create n coordinates of equal distance to middlepoint x|y clockwise
from compression.compression import get_array_part
from gui_compression.compression_questions import compression_question_array


def create_coordinates(x, y, n):
    distance_to_center = min(x, y) / 1.5
    # array: [x, y]
    array = np.empty((n, 2), dtype=object)
    degree_delta = 360 / n

    for i in range(n):
        degree = i * degree_delta - 135
        g = sin(radians(degree)) * distance_to_center
        a = cos(radians(degree)) * distance_to_center
        array[i, 0] = x + a
        array[i, 1] = y + g
        # array[i, 2] = image_sizes

    return array


def create_coordinates_relative(n):
    x = 0.5
    y = 0.5
    size = 1
    distance_to_center = min(x, y) / 1.5
    # array: [x, y]
    array = np.empty((n, 3), dtype=object)
    degree_delta = 360 / n

    for i in range(n):
        degree = i * degree_delta - 135
        g = sin(radians(degree)) * distance_to_center
        a = cos(radians(degree)) * distance_to_center
        array[i, 0] = x + a
        array[i, 1] = y + g
        array[i, 2] = size

    return array


blob_configuration_array = [
    # dependencies, not-dependencies, name, regex, resizable, info
    [[],           [],                       "none",                        "^$",                                                        False,
     "info_none"],
    [[],           [],                       "space",                        "^ $",                                                        False,
     "info_space"],

    [[0],          [1, 3],                   "lower_case_letters",          "^l$",                                                       False,
     "info_lower_case_letters"],
    [[],           [0],                      "lower_case_letters",          "^[a-zäöüß]$",                                               True,
     "info_lower_case_letters"],
    [[0, 3],       [1, 6],                   "lower_case_words",            "^s$",                                                       False,
     "info_lower_case_words"],
    [[0, 3, 6],    [1, 7],                   "words",                       "^w$",                                                       False,
     "info_words"],
    [[0, 3, 6, 7], [1],                      "word_sequences",              "^q$",                                                       False,
     "info_word_sequences"],
    [[0, 1],       [4],                      "letters",                     "^a$",                                                       False,
     "info_letters"],
    [[0, 1, 4],    [8],                      "letter_sequences",            "^b$",                                                       False,
     "info_letter_sequences"],
    [[0, 1, 4, 8], [],                       "letter_sequence_sequences",   "^Q$",                                                       False,
     "info_letter_sequence_sequences"],
    [[2],          [1, 5],                   "upper_case_letters",          "^L$",                                                       False,
     "info_upper_case_letters"],
    [[],           [1, 2],                   "upper_case_letters",          "^[A-ZÄÖÜ]$",                                                True,
     "info_upper_case_letters"],
    [[2, 5],       [1],                      "upper_case_letter_sequences", "^S$",                                                       False,
     "info_upper_case_letter_sequences"],

    [[9],          [10],                     "digits",                      "^0$",                                                       False,
     "info_digits"],
    [[],           [9],                      "digits",                      "^[0-9]$",                                                   True,
     "info_digits"],
    [[9, 10],      [],                       "integers",                    "^1$",                                                       False,
     "info_integers"],
    [[9, 10, 11],  [],                       "floats",                      "^2$",                                                       False,
     "info_floats"],

    [[13],         [12],                     "punctuation_marks",           "^\.$",                                                      False,
     "info_punctuation_marks"],
    [[],           [12, 13],                 "punctuation_marks",           "^[\.,:;!\?]$",                                              True,
     "info_punctuation_marks"],
    [[14],         [12],                     "brackets",                    "^\($",                                                      False,
     "info_brackets"],
    [[],           [12, 14],                 "brackets",                    "^[\(\)\[\]\{\}]$",                                          True,
     "info_brackets"],
    [[15],         [12],                     "math_operators",              "^\+$",                                                      False,
     "info_math_operators"],
    [[],           [12, 15],                 "math_operators",              "^[\+\-\*/%=<>\&\|]$",                                       True,
     "info_math_operators"],
    [[16],         [12],                     "quotation_marks",             "^\"$",                                                      False,
     "info_quotation_marks"],
    [[],           [12, 16],                 "quotation_marks",             "^[\"`´']$",                                                 True,
     "info_quotation_marks"],
    [[17],         [12],                     "other_characters",            "^_$",                                                       False,
     "info_other_characters"],
    [[],           [12, 17],                 "other_characters",            "^[^a-zäöüßA-ZÄÖÜ0-9 \.,:;!\?\(\)\[\]\{\}\+\-\*/%=<>\&\|]$", True,
     "info_other_characters"],
    [[12],         [],                       "special_characters",          "^\$",                                                       False,
     "info_special_characters"],
    [[],           [12, 13, 14, 15, 16, 17], "special_characters",          "^[^a-zäöüßA-ZÄÖÜ0-9 ]$",                                    True,
     "info_special_characters"]
]


def get_blob_configuration(answers):
    blob_info = get_array_part(blob_configuration_array, compression_question_array, answers)  # [label, regex, resizable, info]
    n = len(blob_info)
    coordinates = create_coordinates_relative(n)  # [x, y, size]
    blob_info_t = np.transpose(blob_info)
    coordinates_t = np.transpose(coordinates)
    blob_configuration_t = np.concatenate((blob_info_t, coordinates_t))  # [label, regex, resizable, info, x, y, size]
    blob_configuration = np.transpose(blob_configuration_t)
    return blob_configuration


if __name__ == "__main__":
    m = np.full((5, 5), "a")
    n = np.full((5, 5), "b")
    print(m)
    print(n)

    m_t = np.transpose(m)
    n_t = np.transpose(n)
    result = np.concatenate((m_t, n_t))
    print(np.transpose(result))
