import re
import numpy as np


def char_compression_function(values, unify_values=True):
    # ["[a-zA-Z]", "e"], ["[0-9]", "0"]
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
    # ["[a-zA-Z]+", "f"],  ["[0-9]+", "1"]
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
    # ["[a-z]+", "w"], ["[A-Z]+", "S"], ["[0-9]", "0"]
    return get_replacement_method(
        [True, False, True, True, False, True, False, False, False,
         True, False, False,
         False, False, False, False],
        unify_values)(values)


def number_sequence_compression_function(values, unify_values=True):
    # ["[a-z]", l"], ["[A-Z]", "L"], ["[0-9]+", "1"]
    return get_replacement_method(
        [True, False, True, False, False, False, False, False, False,
         True, True, False,
         False, False, False, False],
        unify_values)(values)


def word_compression_function(values, unify_values=True):
    # ["[a-z]", "l"], ["[A-Z]", "L"], ["l+", "w"], ["LL+", "M"], ["Lw", "W"], ["[0-9]+", "1"]
    return get_replacement_method(
        [True, False, True, True, False, True, True, False, False,
         True, True, False,
         False, False, False, False],
        unify_values)(values)


def word_decimal_compression_function(values, unify_values=True):
    # ["[a-z]", "l"], ["[A-Z]", "L"], ["l+", "w"], ["LL+", "M"], ["Lw", "W"], ["[0-9]+", "1"], ["1,1", "2"]
    return get_replacement_method(
        [True, False, True, True, False, True, True, False, False,
         True, True, True,
         False, False, False, False],
        unify_values)(values)


def word_sequence_compression_function(values, unify_values=True):
    # ["[a-z]", "l"], ["[A-Z]", "L"], ["l+", "w"], ["LL+", "M"], ["Lw", "W"], ["(w+ )+w+", "q"], ["(W+ )+W+", "U"], ["[qU]+", "V"], ["[0-9]+", "1"]
    return get_replacement_method(
        [True, False, True, True, False, True, True, True, False,
         True, True, False,
         False, False, False, False],
        unify_values)(values)


question_array = [
    # index, dependencies, not-dependencies, name, question, explanation, example
    [[],           [],   "lower_case",
     "Should all lower case letters be treated equally?",  # TODO: ask if there are exceptions
     "Choose yes if the concrete lower case letter present does not have a crucial impact on the meaning.",
     "'face' and 'tree' will be treated equally since both consist of four lower case letters"],  # 0
    [[],           [],   "to_lower",
     "Should an upper case letter be treated as its lower case variant?",
     "Choose yes if the capitalization does not have a crucial impact on the meaning.",
     "'Painting' and 'painting' will be treated equally since the only difference is the capitalization of 'p'"],  # 1
    [[],           [1],  "upper_case",
     "Should all upper case letters be treated equally?",  # TODO: ask if there are exceptions
     "Choose yes if the concrete upper case letter present does not have a crucial impact on the meaning.",
     "'USA' and 'DDR' will be treated equally since both consist of three upper case letters"],  # 2
    [[0],          [1],  "lower_sequence",
     "Should all lower case letter sequences (= lower case word) be treated equally?",
     "Choose yes if the length of lower case letter sequences does not have a crucial impact on the meaning or if you expect lower case letter sequences of heterogeneous length.",
     "'red' and 'architecture' will be treated equally since both consist of a sequence of lower case letters"],  # 3
    [[0, 1],       [],   "sequence",
     "Should all letter sequences be treated equally?",
     "Choose yes if the length of lower, upper or mixed case letter sequences does not have a crucial impact on the meaning or if you expect such letter sequences of heterogeneous length.",
     "'Portrait' and 'USA' will be treated equally since both consist of a sequence of lower, upper or mixed case letters"],  # 4
    [[2],          [1],  "upper_sequence",
     "Should all upper case letter sequences be treated equally?",
     "Choose yes if the length of upper case letter sequences does not have a crucial impact on the meaning or if you expect upper case letter sequences of heterogeneous length.",
     "'EU' and 'USA' will be treated equally since both consist of a sequence of upper case letters"],  # 5
    [[0, 3],       [1],  "words",
     "Should all lower and upper case words be treated equally?",
     "Choose yes if the capitalization of the first letter of a word does not have a crucial impact on the meaning.",
     "'Portrait' and 'child' will be treated equally since both are words"],  # 6
    [[0, 3, 6],    [1],  "word_sequence",
     "Should all sequences of lower or upper case words seperated by a blank space be treated equally?",
     "Choose yes if the length of sequences of lower or upper case words does not have a crucial impact on the meaning or if you expect sequences of lower or upper case words of heterogeneous length.",
     "'in Marburg' and 'brother or father' will be treated equally since both are sequences of words seperated by a blank space"],  # 7
    [[0, 1, 4],    [],   "sequence_sequence",
     "Should all sequences of lower, upper or mixed case letter sequences seperated by a blank space be treated equally?",
     "Choose yes if the length of sequences of lower, upper or mixed case letter sequences does not have a crucial impact on the meaning or if you expect sequences of lower, upper or mixed case letter sequences of heterogeneous length.",
     "'in USA' and 'around or in Marburg' will be treated equally since both are sequences of letter sequences seperated by a blank"],  # 8

    [[],           [],   "digits",
     "Should all digits be treated equally?",  # TODO: ask if there are exceptions
     "Choose yes if the concrete digit does not have a crucial impact on the meaning.",
     "'1' and '2' will be treated equally since both are digits"],  # 9
    [[9],          [],   "int",
     "Should all digit sequences be treated equally?",
     "Choose yes if the length of digit sequences does not have a crucial impact on the meaning or if you expect digit sequences of heterogeneous length.",
     "'1' and '1024' will be treated equally since both are digit sequences"],  # 10
    [[9, 10],      [],   "float",
     "Should all pairs of digit sequences separated by a comma be treated equally?",
     "Choose yes if the length of digit sequences preceding and following a comma does not have a crucial impact on the meaning or if you expect pairs of digit sequences separated by a comma of heterogeneous length.",
     "'118,43' and '0,5' will be treated equally since both consist of two digit sequences separated by a comma"],  # 11

    [[],           [],   "specials",
     "Should all characters that are not letters or digits be treated equally?",
     "Choose yes if the concrete character does not have a crucial impact on the meaning.",
     "'/' and '?' will be treated equally since both are neither a letter nor a digit"],  # 12
    [[],           [12], "punctuation",
     "Should all punctuation marks be treated equally?",
     "Choose yes if ...",
     "'.' and '?' will be treated equally"],  # 13
    [[],           [12], "brackets",
     "Should all bracket characters be treated equally?",
     "Choose yes if ...",
     "'{' and )'' will be treated equally"],  # 14
    [[], [12], "math_characters",
     "Should all mathematical operators be treated equally?",
     "Choose yes if ...",
     "'+' and '&' will be treated equally"],  # 15
    [[],           [12], "quotation_marks",
     "Should all quotation_marks be treated equally",
     "Choose yes if ...",
     "'\"'' and ''' will be treated equally"],  # 16
    [[],           [12], "special_rest",
     "Should all other special characters be treated equally?",
     "Choose yes if ...",
     "'$' and 'µ' will be treated equally"]   # 17
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

replacement_array = [
    # dependencies, not-dependencies, replacement(v), regex
    [[1],           [0],    lambda v: v.lower(),                                                                 "↓", "lower case"],  # 0
    [[0],           [1, 3], lambda v: re.sub("[a-zäöüß]", "l", v),                                               "l", "[a-zäöüß]"],  # 1
    [[0, 3],        [1, 6], lambda v: re.sub("[a-zäöüß]+", "s", v),                                              "s", "[a-zäöüß]+"],  # 2
    [[0, 3, 6],     [1, 7], lambda v: re.sub("[A-ZÄÖÜ]?[a-zäöüß]+", "w", v),                                     "w", "[A-ZÄÖÜ]?[a-zäöüß]+"],  # 3
    [[0, 3, 6, 7],  [1],    lambda v: re.sub("([A-ZÄÖÜ]?[a-zäöüß]+ )* [A-ZÄÖÜ]?[a-zäöüß]+", "q", v),             "q", "([A-ZÄÖÜ]?[a-zäöüß]+ )* [A-ZÄÖÜ]?[a-zäöüß]+"],  # 4
    [[0, 1],        [4],    lambda v: re.sub("[a-zäöüßA-ZÄÖÜ]", "a", v),                                         "a", "[a-zäöüßA-ZÄÖÜ]"],  # 5
    [[0, 1, 4],     [8],    lambda v: re.sub("[a-zäöüßA-ZÄÖÜ]+", "b", v),                                        "b", "[a-zäöüßA-ZÄÖÜ]+"],  # 6
    [[0, 1, 4, 8],  [],     lambda v: re.sub("([a-zäöüßA-ZÄÖÜ]+ )*[a-zäöüßA-ZÄÖÜ]+", "Q", v),                    "Q", "([a-zäöüßA-ZÄÖÜ]+ )*[a-zäöüßA-ZÄÖÜ]+"],  # 7
    [[2],           [1, 5], lambda v: re.sub("[A-ZÄÖÜ]", "L", v),                                                "L", "[A-ZÄÖÜ]"],  # 8
    [[2, 5],        [1],    lambda v: re.sub("[A-ZÄÖÜ]+", "S", v),                                               "S", "[A-ZÄÖÜ]+"],  # 9

    [[9],           [10],   lambda v: re.sub("[0-9]", "0", v),                                                   "0", "[0-9]"],  # 10
    [[9, 10],       [],     lambda v: re.sub("[0-9]+", "1", v),                                                  "1", "[0-9]+"],  # 11
    [[9, 10, 11],   [],     lambda v: re.sub("[0-9]+,[0-9]+", "2", v),                                           "2", "[0-9]+,[0-9]+"],  # 12

    [[13],          [12],   lambda v: re.sub("[\.,:;!\?]", ".", v),                                              ".", "[\.,:;!\?]"],  # 13
    [[14],          [12],   lambda v: re.sub("[\(\)\[\]\{\}]", "(", v),                                          "(", "[\(\)\[\]\{\}]"],  # 14
    [[15],          [12],   lambda v: re.sub("[\+\-\*/%=<>\&\|]", "+", v),                                       "+", "[\+\-\*/%=<>\&\|]"],  # 15
    [[16],          [12],   lambda v: re.sub("[\"`´']", "´", v),                                                 "`", "[\"`´']"],  # 16
    [[17],          [12],   lambda v: re.sub("[^a-zäöüßA-ZÄÖÜ0-9 \.,:;!\?\(\)\[\]\{\}\+\-\*/%=<>\&\|]", "_", v), "_", "[^a-zäöüßA-ZÄÖÜ0-9 \.,:;!\?\(\)\[\]\{\}\+\-\*/%=<>\&\|]"],  # 17
    [[12],          [],     lambda v: re.sub("[^a-zäöüßA-ZÄÖÜ0-9 ]", "$", v), '',                                "$", "[^a-zäöüßA-ZÄÖÜ0-9 ]"]  # 18
]


def get_replacement_method(answers, unify_values=True):
    def local_func(values, compressions_list, unique):
        for i in range(len(values)):
            for compr in compressions_list:
                values[i] = compr(values[i])
        if unique:
            values = np.array(list(set(values)))
        return values

    assert (len(answers) == len(question_array))
    compression_list = list()
    for replacement in replacement_array:
        apply = True
        for dep in replacement[0]:  # check positive dependencies
            apply = apply and answers[dep]
        for not_dep in replacement[1]:  # check negative dependencies
            apply = apply and not (answers[not_dep])
        if apply: compression_list.append(replacement[2])

    return lambda values: local_func(values, compression_list, unify_values)
