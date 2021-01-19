import re
import numpy as np


def char_compression_function(values, unify_values=True):
    # ["[a-zA-Z]", "e"], ["[0-9]", "0"]
    return get_compression_method(
        [True, True, False, False, False, False, False, False, False,
         True, False, False,
         False, False, False, False, False, False],
        unify_values)(values)


def char_compression_case_sensitive_function(values, unify_values=True):
    # ["[a-z]", "l"], ["[A-Z]", "L"], ["[0-9]", "0"]
    return get_compression_method(
        [True, False, True, False, False, False, False, False, False,
         True, False, False,
         False, False, False, False, False, False],
        unify_values)(values)


def sequence_compression_function(values, unify_values=True):
    # ["[a-zA-Z]+", "f"],  ["[0-9]+", "1"]
    return get_compression_method(
        [True, True, False, False, True, False, False, False, False,
         True, True, False,
         False, False, False, False, False, False],
        unify_values)(values)


def sequence_compression_case_sensitive_function(values, unify_values=True):
    # ["[a-z]+", "w"], ["[A-Z]+", "S"], ["[0-9]+", "1"]
    return get_compression_method(
        [True, False, True, True, False, True, False, False, False,
         True, True, False,
         False, False, False, False, False, False],
        unify_values)(values)


def letter_sequence_compression_function(values, unify_values=True):
    # ["[a-z]+", "w"], ["[A-Z]+", "S"], ["[0-9]", "0"]
    return get_compression_method(
        [True, False, True, True, False, True, False, False, False,
         True, False, False,
         False, False, False, False, False, False],
        unify_values)(values)


def number_sequence_compression_function(values, unify_values=True):
    # ["[a-z]", l"], ["[A-Z]", "L"], ["[0-9]+", "1"]
    return get_compression_method(
        [True, False, True, False, False, False, False, False, False,
         True, True, False,
         False, False, False, False, False, False],
        unify_values)(values)


def word_compression_function(values, unify_values=True):
    # ["[a-z]", "l"], ["[A-Z]", "L"], ["l+", "w"], ["LL+", "M"], ["Lw", "W"], ["[0-9]+", "1"]
    return get_compression_method(
        [True, False, True, True, False, True, True, False, False,
         True, True, False,
         False, False, False, False, False, False],
        unify_values)(values)


def word_decimal_compression_function(values, unify_values=True):
    # ["[a-z]", "l"], ["[A-Z]", "L"], ["l+", "w"], ["LL+", "M"], ["Lw", "W"], ["[0-9]+", "1"], ["1,1", "2"]
    return get_compression_method(
        [True, False, True, True, False, True, True, False, False,
         True, True, True,
         False, False, False, False, False, False],
        unify_values)(values)


def word_sequence_compression_function(values, unify_values=True):
    # ["[a-z]", "l"], ["[A-Z]", "L"], ["l+", "w"], ["LL+", "M"], ["Lw", "W"], ["(w+ )+w+", "q"], ["(W+ )+W+", "U"],
    # ["[qU]+", "V"], ["[0-9]+", "1"]
    return get_compression_method(
        [True, False, True, True, False, True, True, True, False,
         True, True, False,
         False, False, False, False, False, False],
        unify_values)(values)


question_array = [
    # dependencies, not-dependencies, name, question, default, explanation, example
    [[], [], "lower_case", True,
     "Should all lower case letters be treated equally?",  # TODO: ask if there are exceptions?
     "Choose yes if the concrete lower case letter present does not have a crucial impact on the meaning.\n" +
     "For example, 'face' and 'tree' will be treated equally since both consist of four lower case letters"],  # 0
    [[], [], "to_lower", True,
     "Should an upper case letter be treated as its lower case variant?",
     "Choose yes if the capitalization does not have a crucial impact on the meaning.\n" +
     "For example, 'Painting' and 'painting' will be treated equally since the only difference is the\n" +
     "capitalization of 'p'"],  # 1
    [[], [1], "upper_case", True,
     "Should all upper case letters be treated equally?",  # TODO: ask if there are exceptions?
     "Choose yes if the concrete upper case letter present does not have a crucial impact on the meaning.\n" +
     "For example, 'USA' and 'DDR' will be treated equally since both consist of three upper case letters"],  # 2
    [[0], [1], "lower_sequence", False,
     "Should all lower case letter sequences (= lower case word) be treated equally?",
     "Choose yes if the length of lower case letter sequences does not have a crucial impact on the meaning or if\n" +
     "you expect lower case letter sequences of heterogeneous length.\n" +
     "For example, 'red' and 'architecture' will be treated equally since both consist of a sequence of lower case\n" +
     "letters"],  # 3
    [[0, 1], [], "sequence", False,
     "Should all letter sequences be treated equally?",
     "Choose yes if the length of lower, upper or mixed case letter sequences does not have a crucial impact on the\n" +
     "meaning or if you expect such letter sequences of heterogeneous length.\n" +
     "For example, 'Portrait' and 'USA' will be treated equally since both consist of a sequence of lower, upper\n" +
     "or mixed case letters"],  # 4
    [[2], [1], "upper_sequence", False,
     "Should all upper case letter sequences be treated equally?",
     "Choose yes if the length of upper case letter sequences does not have a crucial impact on the meaning or if\n" +
     "you expect upper case letter sequences of heterogeneous length.\n" +
     "For example, 'EU' and 'USA' will be treated equally since both consist of a sequence of upper case letters"],  # 5
    [[0, 3], [1], "words", False,
     "Should all lower and upper case words be treated equally?",
     "Choose yes if the capitalization of the first letter of a word does not have a crucial impact on the meaning.\n" +
     "For example, 'Portrait' and 'child' will be treated equally since both are words"],  # 6
    [[0, 3, 6], [1], "word_sequence", False,
     "Should all sequences of lower or upper case words seperated by a blank space be treated equally?",
     "Choose yes if the length of sequences of lower or upper case words does not have a crucial impact on the\n" +
     "meaning or if you expect sequences of lower or upper case words of heterogeneous length.\n" +
     "For example, 'in Marburg' and 'brother or father' will be treated equally since both are sequences of words\n" +
     "seperated by a blank space"],  # 7
    [[0, 1, 4], [], "sequence_sequence", False,
     "Should all sequences of lower, upper or mixed case letter sequences seperated by a blank space be treated equally?",
     "Choose yes if the length of sequences of lower, upper or mixed case letter sequences does not have\n" +
     "a crucial impact on the meaning or if you expect sequences of lower, upper or mixed case letter sequences of\n" +
     "heterogeneous length.\n" +
     "For example, 'in USA' and 'around or in Marburg' will be treated equally since both are sequences of letter\n" +
     "sequences seperated by a blank"],  # 8

    [[], [], "digits", True,
     "Should all digits be treated equally?",  # TODO: ask if there are exceptions
     "Choose yes if the concrete digit does not have a crucial impact on the meaning.\n" +
     "For example, '1' and '2' will be treated equally since both are digits"],  # 9
    [[9], [], "int", False,
     "Should all digit sequences be treated equally?",
     "Choose yes if the length of digit sequences does not have a crucial impact on the meaning or if you expect\n" +
     "digit sequences of heterogeneous length.\n" +
     "For example, '1' and '1024' will be treated equally since both are digit sequences"],  # 10
    [[9, 10], [], "float", False,
     "Should all pairs of digit sequences separated by a comma be treated equally?",
     "Choose yes if the length of digit sequences preceding and following a comma does not have a crucial impact on\n" +
     "the meaning or if you expect pairs of digit sequences separated by a comma of heterogeneous length.\n" +
     "For example, '118,43' and '0,5' will be treated equally since both consist of two digit sequences separated\n" +
     "by a comma"],# 11

    [[], [], "specials", False,
     "Should all characters that are not letters or digits be treated equally?",
     "Choose yes if the concrete character does not have a crucial impact on the meaning.\n" +
     "For example, '/' and '?' will be treated equally since both are neither a letter nor a digit"],  # 12
    [[], [12], "punctuation", False,
     "Should all punctuation marks be treated equally?",
     "Choose yes if the concrete punctuation mark does not have a crucial impact on the meaning.\n" +
     "For example, '.' and '?' will be treated equally since both are punctuation marks"],  # 13
    [[], [12], "brackets", False,
     "Should all bracket characters be treated equally?",
     "Choose yes if the concrete bracket character does not have a crucial impact on the meaning.\n" +
     "For example, '{' and )'' will be treated equally since both are bracket characters"],  # 14
    [[], [12], "math_characters", False,
     "Should all mathematical characters (i.e. '+','-','*','/', '%', '=', '<', '>', '&', '|') be treated equally?",
     "Choose yes if the concrete mathematical character does not have a crucial impact on the meaning.\n" +
     "For example, '+' and '&' will be treated equally since both are mathematical characters"],  # 15
    [[], [12], "quotation_marks", False,
     "Should all quotation marks be treated equally?",
     "Choose yes if the concrete quotation mark does not have a crucial impact on the meaning.\n" +
     "For example, '\"'' and ''' will be treated equally since both are quotation marks"],  # 16
    [[], [12], "special_rest", False,
     "Should all other special characters be treated equally?",
     "Choose yes if the concrete specical character does not have a crucial impact on the meaning.\n" +
     "For example, '$' and 'µ' will be treated equally since both are specical characters"] # 17
]

dictionary = [
    # term, definition
    ["letter",                                          "[a-zäöüßA-ZÄÖÜ]"],
    ["lower case letter",                               "[a-zäöüß]"],
    ["upper case letter",                               "[A-ZÄÖÜ]"],
    ["word",                                            "[A-ZÄÖÜ]?[a-zäöüß]+"],
    ["lower case word (= lower case letter sequence)",  "[a-zäöüß]+"],
    ["upper case word",                                 "[A-ZÄÖÜ][a-zäöüß]+"],
    ["upper case letter sequence",                      "[A-ZÄÖÜ]+"],
    ["letter sequence",                                 "[a-zäöüßA-ZÄÖÜ]+"],
]

compression_configuration_array = [
    # dependencies, not-dependencies, replacement function, replacement char, label, regex
    [[1],          [0],    lambda v: v.lower(),                                                                 ],  # "↓",  "",                            "lower_case"],  # 0
    [[0],          [1, 3], lambda v: re.sub("[a-zäöüß]", "l", v),                                               ],  # "l",  "lower_case_letters",          "[a-zäöüß]"],  # 1
    [[0, 3],       [1, 6], lambda v: re.sub("[a-zäöüß]+", "s", v),                                              ],  # "s",  "lower_case_words",            "[a-zäöüß]+"],  # 2
    [[0, 3, 6],    [1, 7], lambda v: re.sub("[A-ZÄÖÜ]?[a-zäöüß]+", "w", v),                                     ],  # "w",  "words",                       "[A-ZÄÖÜ]?[a-zäöüß]+"],  # 3
    [[0, 3, 6, 7], [1],    lambda v: re.sub("([A-ZÄÖÜ]?[a-zäöüß]+ )* [A-ZÄÖÜ]?[a-zäöüß]+", "q", v),             ],  # "q",  "word_sequences",              "([A-ZÄÖÜ]?[a-zäöüß]+ )* [A-ZÄÖÜ]?[a-zäöüß]+"],  # 4
    [[0, 1],       [4],    lambda v: re.sub("[a-zäöüßA-ZÄÖÜ]", "a", v),                                         ],  # "a",  "letters",                     "[a-zäöüßA-ZÄÖÜ]"],  # 5
    [[0, 1, 4],    [8],    lambda v: re.sub("[a-zäöüßA-ZÄÖÜ]+", "b", v),                                        ],  # "b",  "letter_sequences",            "[a-zäöüßA-ZÄÖÜ]+"],  # 6
    [[0, 1, 4, 8], [],     lambda v: re.sub("([a-zäöüßA-ZÄÖÜ]+ )*[a-zäöüßA-ZÄÖÜ]+", "Q", v),                    ],  # "Q",  "letter_sequence_sequences",   "([a-zäöüßA-ZÄÖÜ]+ )*[a-zäöüßA-ZÄÖÜ]+"],  # 7
    [[2],          [1, 5], lambda v: re.sub("[A-ZÄÖÜ]", "L", v),                                                ],  # "L",  "upper_case_letters",          "[A-ZÄÖÜ]"],  # 8
    [[2, 5],       [1],    lambda v: re.sub("[A-ZÄÖÜ]+", "S", v),                                               ],  # "S",  "upper_case_letter_sequences", "[A-ZÄÖÜ]+"],  # 9

    [[9],          [10],   lambda v: re.sub("[0-9]", "0", v),                                                   ],  # "0",  "digits",                      "[0-9]"],  # 10
    [[9, 10],      [],     lambda v: re.sub("[0-9]+", "1", v),                                                  ],  # "1",  "integers",                    "[0-9]+"],  # 11
    [[9, 10, 11],  [],     lambda v: re.sub("[0-9]+,[0-9]+", "2", v),                                           ],  # "2",  "floats",                      "[0-9]+,[0-9]+"],  # 12

    [[13],         [12],   lambda v: re.sub("[\.,:;!\?]", ".", v),                                              ],  # "\.", "punctuation_marks",           "[\.,:;!\?]"],  # 13
    [[14],         [12],   lambda v: re.sub("[\(\)\[\]\{\}]", "(", v),                                          ],  # "\(", "brackets",                    "[\(\)\[\]\{\}]"],  # 14
    [[15],         [12],   lambda v: re.sub("[\+\-\*/%=<>\&\|]", "+", v),                                       ],  # "\+", "math_operators",              "[\+\-\*/%=<>\&\|]"],  # 15
    [[16],         [12],   lambda v: re.sub("[\"`´']", "\"", v),                                                ],  # "\"", "quotation_marks",             "[\"`´']"],  # 16
    [[17],         [12],   lambda v: re.sub("[^a-zäöüßA-ZÄÖÜ0-9 \.,:;!\?\(\)\[\]\{\}\+\-\*/%=<>\&\|]", "_", v), ],  # "_",  "other_characters",            "[^a-zäöüßA-ZÄÖÜ0-9 \.,:;!\?\(\)\[\]\{\}\+\-\*/%=<>\&\|]"],  # 17
    [[12],         [],     lambda v: re.sub("[^a-zäöüßA-ZÄÖÜ0-9 ]", "$", v),                                    ],  # "\$", "special_characters",          "[^a-zäöüßA-ZÄÖÜ0-9 ]"]  # 18
]

blob_configuration_array = [
    # dependencies, not-dependencies, name, resizable, regex
    [[],           [],                       "none",                        "^$",                                                        False],

    [[0],          [1, 3],                   "lower_case_letters",          "^l$",                                                       False],
    [[],           [0],                      "lower_case_letters",          "^[a-zäöüß]$",                                               True],
    [[0, 3],       [1, 6],                   "lower_case_words",            "^s$",                                                       False],
    [[0, 3, 6],    [1, 7],                   "words",                       "^w$",                                                       False],
    [[0, 3, 6, 7], [1],                      "word_sequences",              "^q$",                                                       False],
    [[0, 1],       [4],                      "letters",                     "^a$",                                                       False],
    [[0, 1, 4],    [8],                      "letter_sequences",            "^b$",                                                       False],
    [[0, 1, 4, 8], [],                       "letter_sequence_sequences",   "^Q$",                                                       False],
    [[2],          [1, 5],                   "upper_case_letters",          "^L$",                                                       False],
    [[],           [1, 2],                   "upper_case_letters",          "^[A-ZÄÖÜ]$",                                                True],
    [[2, 5],       [1],                      "upper_case_letter_sequences", "^S$",                                                       False],

    [[9],          [10],                     "digits",                      "^0$",                                                       False],
    [[],           [9],                      "digits",                      "^[0-9]$",                                                   True],
    [[9, 10],      [],                       "integers",                    "^1$",                                                       False],
    [[9, 10, 11],  [],                       "floats",                      "^2$",                                                       False],

    [[13],         [12],                     "punctuation_marks",           "^\.$",                                                      False],
    [[],           [12, 13],                 "punctuation_marks",           "^[\.,:;!\?]$",                                              True],
    [[14],         [12],                     "brackets",                    "^\($",                                                      False],
    [[],           [12, 14],                 "brackets",                    "^[\(\)\[\]\{\}]$",                                          True],
    [[15],         [12],                     "math_operators",              "^\+$",                                                      False],
    [[],           [12, 15],                 "math_operators",              "^[\+\-\*/%=<>\&\|]$",                                       True],
    [[16],         [12],                     "quotation_marks",             "^\"$",                                                      False],
    [[],           [12, 16],                 "quotation_marks",             "^[\"`´']$",                                                 True],
    [[17],         [12],                     "other_characters",            "^_$",                                                       False],
    [[],           [12, 17],                 "other_characters",            "^[^a-zäöüßA-ZÄÖÜ0-9 \.,:;!\?\(\)\[\]\{\}\+\-\*/%=<>\&\|]$", True],
    [[12],         [],                       "special_characters",          "^\$",                                                       False],
    [[],           [12, 13, 14, 15, 16, 17], "special_characters",          "^[^a-zäöüßA-ZÄÖÜ0-9 ]$",                                    True]
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


def get_blob_configuration(answers):
    return get_array_part(blob_configuration_array, answers)


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


def get_compression_method(answers, unify_values=True):
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

    compressions = get_compression_configuration(answers=answers)

    return lambda values: local_func(values, compressions, unify_values)


if __name__ == '__main__':
    min = [True, True, False, False, False, False, False, False, False,
        True, True, False,
        True, False, False, False, False, False]
    min_compression = get_compression_configuration(answers=min)
    print(min_compression)

    max = [True, False, True, True, True, True, True, True, True,
        True, True, True,
        False, True, True, True, True, True]
    max_compression = get_blob_configuration(answers=min)
    print(max_compression)
