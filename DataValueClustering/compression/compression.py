import re
import numpy as np

from gui_compression.questions import question_array
#from gui_distances.blobinput_helper import get_blob_configuration


def max_compression_function():
    answers = [False, False, False, False, False, False, False, False, False,
                 False, False, False,
                 True, False, False, False, False, False,
                 True]
    return get_compression_method(answers), answers


def char_compression_function():
    # ["[a-zA-Z]", "e"], ["[0-9]", "0"]
    answers = [True, True, False, False, False, False, False, False, False,
               True, False, False,
               False, False, False, False, False, False,
               True]
    return get_compression_method(answers), answers


def char_compression_case_sensitive_function():
    # ["[a-z]", "l"], ["[A-Z]", "L"], ["[0-9]", "0"]
    answers = [True, False, True, False, False, False, False, False, False,
               True, False, False,
               False, False, False, False, False, False,
               True]
    return get_compression_method(answers), answers


def sequence_compression_function():
    # ["[a-zA-Z]+", "f"],  ["[0-9]+", "1"]
    answers = [True, True, False, False, True, False, False, False, False,
               True, True, False,
               False, False, False, False, False, False,
               True]
    return get_compression_method(answers), answers


def sequence_compression_case_sensitive_function():
    # ["[a-z]+", "w"], ["[A-Z]+", "S"], ["[0-9]+", "1"]
    answers = [True, False, True, True, False, True, False, False, False,
               True, True, False,
               False, False, False, False, False, False,
               True]
    return get_compression_method(answers), answers


def letter_sequence_compression_function():
    # ["[a-z]+", "w"], ["[A-Z]+", "S"], ["[0-9]", "0"]
    answers = [True, False, True, True, False, True, False, False, False,
               True, False, False,
               False, False, False, False, False, False,
               True]
    return get_compression_method(answers), answers


def number_sequence_compression_function():
    # ["[a-z]", l"], ["[A-Z]", "L"], ["[0-9]+", "1"]
    answers = [True, False, True, False, False, False, False, False, False,
               True, True, False,
               False, False, False, False, False, False,
               True]
    return get_compression_method(answers), answers


def word_compression_function():
    # ["[a-z]", "l"], ["[A-Z]", "L"], ["l+", "w"], ["LL+", "M"], ["Lw", "W"], ["[0-9]+", "1"]
    answers = [True, False, True, True, False, True, True, False, False,
               True, True, False,
               False, False, False, False, False, False,
               True]
    return get_compression_method(answers), answers


def word_decimal_compression_function():
    # ["[a-z]", "l"], ["[A-Z]", "L"], ["l+", "w"], ["LL+", "M"], ["Lw", "W"], ["[0-9]+", "1"], ["1,1", "2"]
    answers = [True, False, True, True, False, True, True, False, False,
               True, True, True,
               False, False, False, False, False, False,
               True]
    return get_compression_method( answers), answers


def word_sequence_compression_function():
    # ["[a-z]", "l"], ["[A-Z]", "L"], ["l+", "w"], ["LL+", "M"], ["Lw", "W"], ["(w+ )+w+", "q"], ["(W+ )+W+", "U"],
    # ["[qU]+", "V"], ["[0-9]+", "1"]
    answers = [True, False, True, True, False, True, True, True, False,
               True, True, False,
               False, False, False, False, False, False,
               True]
    return get_compression_method(answers), answers


# dictionary = [
#     # term, definition
#     ["letter",                                          "[a-zäöüßA-ZÄÖÜ]"],
#     ["lower case letter",                               "[a-zäöüß]"],
#     ["upper case letter",                               "[A-ZÄÖÜ]"],
#     ["word",                                            "[A-ZÄÖÜ]?[a-zäöüß]+"],
#     ["lower case word (= lower case letter sequence)",  "[a-zäöüß]+"],
#     ["upper case word",                                 "[A-ZÄÖÜ][a-zäöüß]+"],
#     ["upper case letter sequence",                      "[A-ZÄÖÜ]+"],
#     ["letter sequence",                                 "[a-zäöüßA-ZÄÖÜ]+"],
# ]

compression_configuration_array = [
    # dependencies, not-dependencies, replacement function, replacement char, label, regex
    [[1],          [0],    lambda v: v.lower(),                                                                 ],  # "↓",  "",                            "lower_case"],  # 0
    [[0],          [1, 3], lambda v: re.sub("[a-zäöüßáàéèíìóòúù]", "l", v),                                               ],  # "l",  "lower_case_letters",          "[a-zäöüß]"],  # 1
    [[0, 3],       [1, 6], lambda v: re.sub("[a-zäöüßáàéèíìóòúù]+", "s", v),                                              ],  # "s",  "lower_case_words",            "[a-zäöüß]+"],  # 2
    [[0, 3, 6],    [1, 7], lambda v: re.sub("[A-ZÄÖÜÁÀÉÈÍÌÓÒÚÙ]?[a-zäöüßáàéèíìóòúù]+", "w", v),                                     ],  # "w",  "words",                       "[A-ZÄÖÜ]?[a-zäöüß]+"],  # 3
    [[0, 3, 6, 7], [1],    lambda v: re.sub("([A-ZÄÖÜÁÀÉÈÍÌÓÒÚÙ]?[a-zäöüßáàéèíìóòúù]+ )* [A-ZÄÖÜÁÀÉÈÍÌÓÒÚÙ]?[a-zäöüßáàéèíìóòúù]+", "q", v),             ],  # "q",  "word_sequences",              "([A-ZÄÖÜ]?[a-zäöüß]+ )* [A-ZÄÖÜ]?[a-zäöüß]+"],  # 4
    [[0, 1],       [4],    lambda v: re.sub("[a-zäöüßáàéèíìóòúùA-ZÄÖÜÁÀÉÈÍÌÓÒÚÙ]", "a", v),                                         ],  # "a",  "letters",                     "[a-zäöüßA-ZÄÖÜ]"],  # 5
    [[0, 1, 4],    [8],    lambda v: re.sub("[a-zäöüßáàéèíìóòúùA-ZÄÖÜÁÀÉÈÍÌÓÒÚÙ]+", "b", v),                                        ],  # "b",  "letter_sequences",            "[a-zäöüßA-ZÄÖÜ]+"],  # 6
    [[0, 1, 4, 8], [],     lambda v: re.sub("([a-zäöüßáàéèíìóòúùA-ZÄÖÜÁÀÉÈÍÌÓÒÚÙ]+ )*[a-zäöüßáàéèíìóòúùA-ZÄÖÜÁÀÉÈÍÌÓÒÚÙ]+", "Q", v),                    ],  # "Q",  "letter_sequence_sequences",   "([a-zäöüßA-ZÄÖÜ]+ )*[a-zäöüßA-ZÄÖÜ]+"],  # 7
    [[2],          [1, 5], lambda v: re.sub("[A-ZÄÖÜÁÀÉÈÍÌÓÒÚÙ]", "L", v),                                                ],  # "L",  "upper_case_letters",          "[A-ZÄÖÜ]"],  # 8
    [[2, 5],       [1],    lambda v: re.sub("[A-ZÄÖÜÁÀÉÈÍÌÓÒÚÙ]+", "S", v),                                               ],  # "S",  "upper_case_letter_sequences", "[A-ZÄÖÜ]+"],  # 9

    [[9],          [10],   lambda v: re.sub("[0-9]", "0", v),                                                   ],  # "0",  "digits",                      "[0-9]"],  # 10
    [[9, 10],      [],     lambda v: re.sub("[0-9]+", "1", v),                                                  ],  # "1",  "integers",                    "[0-9]+"],  # 11
    [[9, 10, 11],  [],     lambda v: re.sub("[0-9]+,[0-9]+", "2", v),                                           ],  # "2",  "floats",                      "[0-9]+,[0-9]+"],  # 12

    [[13],         [12],   lambda v: re.sub("[\.,:;!\?]", ".", v),                                              ],  # "\.", "punctuation_marks",           "[\.,:;!\?]"],  # 13
    [[14],         [12],   lambda v: re.sub("[\(\)\[\]\{\}]", "(", v),                                          ],  # "\(", "brackets",                    "[\(\)\[\]\{\}]"],  # 14
    [[15],         [12],   lambda v: re.sub("[\+\-\*/%=<>\&\|]", "+", v),                                       ],  # "\+", "math_operators",              "[\+\-\*/%=<>\&\|]"],  # 15
    [[16],         [12],   lambda v: re.sub("[\"`´']", "\"", v),                                                ],  # "\"", "quotation_marks",             "[\"`´']"],  # 16
    [[17],         [12],   lambda v: re.sub("[^a-zäöüßáàéèíìóòúùA-ZÄÖÜÁÀÉÈÍÌÓÒÚÙ0-9 \.,:;!\?\(\)\[\]\{\}\+\-\*/%=<>\&\|]", "_", v), ],  # "_",  "other_characters",            "[^a-zäöüßA-ZÄÖÜ0-9 \.,:;!\?\(\)\[\]\{\}\+\-\*/%=<>\&\|]"],  # 17
    [[12],         [],     lambda v: re.sub("[^a-zäöüßáàéèíìóòúùA-ZÄÖÜÁÀÉÈÍÌÓÒÚÙ0-9 ]", "$", v),                                    ],  # "\$", "special_characters",          "[^a-zäöüßA-ZÄÖÜ0-9 ]"]  # 18
]


def get_array_part(selectables, answers):
    assert (len(answers) == len(question_array))
    result = list()
    for line in selectables:
        apply = True
        for dep in line[0]:  # check positive dependencies
            apply = apply and answers[dep]
        for not_dep in line[1]:  # check negative dependencies
            apply = apply and not (answers[not_dep])
        if apply:
            result.append(line[2:])
    return np.array(result, dtype=object)


def get_compression_configuration(answers):
    array = get_array_part(compression_configuration_array, answers)
    return array[:, 0]


# def get_applicable_replacements(answers):
#     assert (len(answers) == len(question_array))
#     result = list()
#     for replacement in compression_configuration_array:
#         apply = True
#         for dep in replacement[0]:  # check positive dependencies
#             apply = apply and answers[dep]
#         for not_dep in replacement[1]:  # check negative dependencies
#             apply = apply and not (answers[not_dep])
#         if apply:
#             result.append(replacement[2:])
#     return np.array(result, dtype=object)


def get_compression_method(answers):
    def local_func(values, compressions_list, unique):
        values_compressed = values.copy()
        compression_dict = {}
        assert len(values_compressed) == len(values)
        for i in range(len(values_compressed)):
            # apply all compressions:
            for compression in compressions_list:
                values_compressed[i] = compression(values_compressed[i])
            # add dict entry:
            if values_compressed[i] in compression_dict:
                compression_dict[values_compressed[i]].append(values[i])
            else:
                compression_dict[values_compressed[i]] = [values[i]]
        if unique:
            # remove redundancy:
            values_compressed = np.array(list(set(values_compressed)))  # order differs across multiple runs
        return values_compressed, compression_dict

    n = len(answers)

    compressions = get_compression_configuration(answers=answers)

    return lambda values: local_func(values, compressions, answers[n-1])


if __name__ == '__main__':
    min = [True, True, False, False, False, False, False, False, False,
        True, True, False,
        True, False, False, False, False, False,
        True]
    min_compression = get_compression_configuration(answers=min)
    print(min_compression)

    # max = [True, False, True, True, True, True, True, True, True,
    #     True, True, True,
    #     False, True, True, True, True, True,
    #     True]
    #max_compression = get_blob_configuration(answers=min)
    #print(max_compression)

