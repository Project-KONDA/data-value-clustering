import re
import numpy as np


def char_compression_function(values, unify_values=True):
    # ["[a-zA-Z]", "e"], ["[0-9]",    "0"]
    return get_replacement_method(
        [True, True, False, False, False, False, False, False, False,
         True, False, False,
         False, False, False, False],
        unify_values)(values)


def char_compression_case_sensitive_function(values, unify_values=True):
    # ["[a-z]", "l"], ["[A-Z]", "L"], ["[0-9]", "0"]
    return get_replacement_method(
        [True, False, True, False, False, False, False, False, False,
         True, False, False,
         False, False, False, False],
        unify_values)(values)


def sequence_compression_function(values, unify_values=True):
    # ["[a-zA-Z]+", "f"],  ["[0-9]+",    "1"]
    return get_replacement_method(
        [True, True, False, False, True, False, False, False, False,
         True, True, False,
         False, False, False, False],
        unify_values)(values)


def sequence_compression_case_sensitive_function(values, unify_values=True):
    # ["[a-z]+", "w"], ["[A-Z]+", "S"], ["[0-9]+", "1"]
    return get_replacement_method(
        [True, False, True, True, False, True, False, False, False,
         True, True, False,
         False, False, False, False],
        unify_values)(values)


def letter_sequence_compression_function(values, unify_values=True):
    # ["[a-z]+", "w"], ["[A-Z]+", "S"], ["[0-9]",  "0"]
    return get_replacement_method(
        [True, False, True, True, False, True, False, False, False,
         True, False, False,
         False, False, False, False],
        unify_values)(values)


def number_sequence_compression_function(values, unify_values=True):
    # ["[a-z]",  "l"], ["[A-Z]",  "L"], ["[0-9]+", "1"]
    return get_replacement_method(
        [True, False, True, False, False, False, False, False, False,
         True, True, False,
         False, False, False, False],
        unify_values)(values)


def word_compression_function(values, unify_values=True):
    # ["[a-z]",  "l"], ["[A-Z]",  "L"], ["l+",     "w"], ["LL+",    "M"], ["Lw",     "W"], ["[0-9]+", "1"]
    return get_replacement_method(
        [True, False, True, True, False, True, True, False, False,
         True, True, False,
         False, False, False, False],
        unify_values)(values)


def word_decimal_compression_function(values, unify_values=True):
    # ["[a-z]",  "l"], ["[A-Z]",  "L"], ["l+",     "w"], ["LL+",    "M"], ["Lw",     "W"], ["[0-9]+", "1"], ["1,1",    "2"]
    return get_replacement_method(
        [True, False, True, True, False, True, True, False, False,
         True, True, True,
         False, False, False, False],
        unify_values)(values)


def word_sequence_compression_function(values, unify_values=True):
    # ["[a-z]",    "l"], ["[A-Z]",    "L"], ["l+",       "w"], ["LL+",      "M"], ["Lw",       "W"], ["(w+ )+w+", "q"], ["(W+ )+W+", "U"], ["[qU]+",    "V"], ["[0-9]+",   "1"]
    return get_replacement_method(
        [True, False, True, True, False, True, True, True, False,
         True, True, False,
         False, False, False, False],
        unify_values)(values)


question_array = [
    # index, dependencies, not-dependencies, name, question
    [[],           [],   "lower_case",        "Should all lower case letters be treated equally?"],  # 0
    [[],           [],   "to_lower",          "Should an upper case letter be treated as its lower case variant?"],  # 1
    [[],           [1],  "upper_case",        "Should all upper case letters be treated equally?"],  # 2
    [[0],          [1],  "lower_sequence",    "Should all lower case letter sequences (= lower case word) be treated equally?"],  # 3
    [[0, 1],       [],   "sequence",          "Should all letter sequences be treated equally?"],  # 4
    [[2],          [1],  "upper_sequence",    "Should all upper case letter sequences be treated equally?"],  # 5
    [[0, 3],       [1],  "words",             "Should all sequences of upper case words be treated equally?"],  # 6
    [[0, 3, 6],    [1],  "word_sequence",     "Should all sequences of words be treated equally?"],  # 7
    [[0, 1, 4],    [],   "sequence_sequence", "Should all sequences of words be treated equally?"],  # 8

    [[],           [],   "digits",            "Should all digits be treated equally?"],  # 9
    [[9],          [],   "int",               "Should all digit sequences be treated equally?"],  # 10
    [[9, 10],      [],   "float",             "Should all digit sequences that contain a comma be treated equally?"],  # 11

    [[],           [],   "specials",          "Should all special characters be treated equally?"],  # 12
    [[],           [12], "punctuation",       "Should all punctuation marks be treated equally?"],  # 13
    [[],           [12], "brackets",          "Should all bracket characters be treated equally?"],  # 14
    [[],           [12], "special_rest",      "Should all other special characters be treated equally?"]   # 15
]

replacement_array = [
    # dependencies, not-dependencies, replacement(v)
    [[1],             [0],   lambda v: v.lower()],
    [[0],             [1, 3], lambda v: re.sub("[a-zäöüß]",                                   "l", v)],
    [[0,3],           [1,6],  lambda v: re.sub("[a-zäöüß]+",                                  "s", v)],
    [[0, 3, 6],       [1, 7], lambda v: re.sub("[A-ZÄÖÜ]?[a-zäöüß]+",                         "w", v)],
    [[0, 3, 6, 7],    [1],    lambda v: re.sub("([A-ZÄÖÜ]?[a-zäöüß]+ )* [A-ZÄÖÜ]?[a-zäöüß]+", "q", v)],
    [[0, 1],          [4],    lambda v: re.sub("[a-zäöüßA-ZÄÖÜ]",                             "a", v)],
    [[0, 1, 4],       [8],    lambda v: re.sub("[a-zäöüßA-ZÄÖÜ]+",                            "a", v)],
    [[0, 1, 4, 8],    [],     lambda v: re.sub("([a-zäöüßA-ZÄÖÜ]+ )*[a-zäöüßA-ZÄÖÜ]+",        "Q", v)],
    [[2],             [1, 5], lambda v: re.sub("[A-ZÄÖÜ]",                                    "L", v)],
    [[2, 5],          [1],    lambda v: re.sub("[A-ZÄÖÜ]+",                                   "S", v)],

    [[9],             [10],   lambda v: re.sub("[0-9]",                                       "0", v)],
    [[9, 10],         [11],   lambda v: re.sub("[0-9]+",                                      "0", v)],
    [[9, 10, 11],     [],     lambda v: re.sub("[0-9]+,[0-9]+",                               "1", v)],

    [[13],            [12],   lambda v: re.sub("[\.,:;!\?]",                                  ".", v)],
    [[14],            [12],   lambda v: re.sub("[\(\)\[\]\{\}<>]",                            "(", v)],
    [[15],            [12],   lambda v: re.sub("[^a-zäöüßA-ZÄÖÜ0-9 \.,:;!\?\(\)\[\]\{\}<>]",  "$", v)],
    [[12],            [],     lambda v: re.sub("[^a-zäöüßA-ZÄÖÜ0-9 ]",                        "$", v)]
]


def get_replacement_method(answers, unify_values=True):

    def local_func(values, compressions_list, unique):
        for i in range(len(values)):
            for compr in compressions_list:
                values[i] = compr(values[i])
        if unique: values = np.array(list(set(values)))
        return values

    assert(len(answers) == len(question_array))
    compression_list = list()
    for replacement in replacement_array:
        apply = True
        for dep in replacement[0]:  # check positive dependencies
            apply = apply and answers[dep]
        for not_dep in replacement[1]:  # check negative dependencies
            apply = apply and not(answers[not_dep])
        if apply: compression_list.append(replacement[2])

    return lambda values: local_func(values, compression_list, unify_values)
