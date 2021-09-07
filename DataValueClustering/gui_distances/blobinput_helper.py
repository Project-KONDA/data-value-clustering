'''Mange blobs.'''
from math import sin, radians, cos, sqrt, floor

import numpy as np


# create n coordinates of equal distance to middlepoint x|y clockwise
from util.question_result_array_util import get_array_part
from gui_abstraction.abstraction_questions import abstraction_question_array


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
    [[],           [],                       "none",                        "",                                                        False,  # TODO: handle "nothing"
     ""],
    [[],           [],                       "space",                        " ",                                                        False,
     "' ' represents a blank space."],

    [[0],          [1, 3],                   "lower_case_letters",          "l",                                                       False,
     "'l' represents all lower case letters, e.g. 'a', 'b' and 'c'."],
    [[],           [0],                      "lower_case_letters",          "abcdefghijklmnopqrstuvwxyzäöüß",                                               True,
     "info_lower_case_letters"],
    [[0, 3],       [1, 6],                   "lower_case_words",            "s",                                                       False,
     "'s' represents all lower case letter sequences, i.e. lower case words, e.g. 'red' and 'to'."],
    [[0, 3, 6],    [1, 7],                   "words",                       "w",                                                       False,
     "'w' represents all words starting with a lower or upper case letter, e.g. 'red' and 'Portrait'."],
    [[0, 3, 6, 7], [1],                      "word_sequences",              "q",                                                       False,
     "'q' represents all sequences of words starting with a lower or upper case letter separated by a blank space, e.g. 'in Marburg'."],
    [[0, 1],       [4],                      "letters",                     "a",                                                       False,
     "'a' represents all lower and upper case letters, e.g. 'a' and 'A'."],
    [[0, 1, 4],    [8],                      "letter_sequences",            "b",                                                       False,
     "'b' represents all sequences of lower and upper case letters, e.g. 'Portrait', 'red' and 'USA'."],
    [[0, 1, 4, 8], [],                       "sequences_of_letter_sequences",   "Q",                                                       False,
     "'Q' represents all sequences of sequences of lower and upper case letters separated by a blank space, e.g. 'in USA' and 'around or in Marburg'."],
    [[2],          [1, 5],                   "upper_case_letters",          "L",                                                       False,
     "'L' represents all upper case letters, e.g. 'A', 'B' and 'C'."],
    [[],           [1, 2],                   "upper_case_letters",          "ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜ",                                                True,
     "info_upper_case_letters"],
    [[2, 5],       [1],                      "upper_case_letter_sequences", "S",                                                       False,
     "'S' represents all sequences of upper case letters, e.g. 'USA' and 'EU'."],

    [[9],          [10],                     "digits",                      "0",                                                       False,
     "'0' represents all digits, e.g. '1', '2' and '3'."],
    [[],           [9],                      "digits",                      "0123456789",                                                   True,
     "info_digits"],
    [[9, 10],      [],                       "integers",                    "1",                                                       False,
     "'1' represents all sequences of digits, i.e. integers, e.g. '1' and '1024'."],
    [[9, 10, 11],  [],                       "floats",                      "2",                                                       False,
     "'2' represents all pairs of sequences of digits separated by a comma, e.g. '118,43' and '0,5'."],

    [[13],         [12],                     "punctuation_marks",           ".",                                                      False,
     "'.' represents all punctuation marks, i.e. '.', ',', ':', ';', '!', and '?'."],
    [[],           [12, 13],                 "punctuation_marks",           ".,:;!?",                                              True,
     "info_punctuation_marks"],
    [[14],         [12],                     "brackets",                    "(",                                                      False,
     "'(' represents all brackets, i.e. '(', '[', '{' and the corresponding opposites."],
    [[],           [12, 14],                 "brackets",                    "()[]{}",                                          True,
     "info_brackets"],
    [[15],         [12],                     "math_operators",              "+",                                                      False,
     "'+' represents all math operators, i.e. '+', '-', '*', '/', '%', '=', '<', '>', '&', and '|'."],
    [[],           [12, 15],                 "math_operators",              "+-*/%=<>&|",                                       True,
     "info_math_operators"],
    [[16],         [12],                     "quotation_marks",             '"',                                                      False,
     '\'"\' represents all quotation marks, i.e. \'"\', \'`\', \'´\' and \'\'\'.'],
    [[],           [12, 16],                 "quotation_marks",             "\"`´'",                                                 True,
     "info_quotation_marks"],
    [[17],         [12],                     "other_characters",            "_",                                                       False,
     "'_' represents all characters that are not letters, digits, punctuation marks, brackets, math operators or quotation marks. "],
    [[],           [12, 17],                 "other_characters",            "^", True,  # TODO: handle rest
     "'^' represents all other characters."],
    [[12],         [],                       "other_characters",            "§",                                                       False,
     "'$' represents all characters that are not letters or digits."]
]


def get_blob_configuration(answers):
    if answers == None:
        return None
    blob_info = get_array_part(blob_configuration_array, abstraction_question_array, answers)  # [label, regex, resizable, info]
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
