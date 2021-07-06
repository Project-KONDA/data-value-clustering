'''Configuration array for for abstraction questionaire'''
abstraction_question_array = [
    # dependencies, not-dependencies, name, default, question, explanation, example
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
     "Should all sequences of lower or upper case words separated by a blank space be treated equally?",
     "Choose yes if the length of sequences of lower or upper case words does not have a crucial impact on the\n" +
     "meaning or if you expect sequences of lower or upper case words of heterogeneous length.\n" +
     "For example, 'in Marburg' and 'brother or father' will be treated equally since both are sequences of words\n" +
     "seperated by a blank space"],  # 7
    [[0, 1, 4], [], "sequence_sequence", False,
     "Should all sequences of lower, upper or mixed case letter sequences separated by a blank space be treated equally?",
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
     "by a comma"],  # 11

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
     "For example, '$' and 'µ' will be treated equally since both are specical characters"],  # 17

    [[], [], "unify", True,
     "Should duplicates be removed?",
     "Choose yes if ....\n" +  # TODO: influence on clusters
     "For example, ..."]  # 18
]