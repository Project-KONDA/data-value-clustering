import numpy as np

from abstraction.abstraction import char_abstraction_case_sensitive_function, char_abstraction_function, \
    sequence_abstraction_case_sensitive_function, sequence_abstraction_function, word_abstraction_function, \
    word_decimal_abstraction_function, word_sequence_abstraction_function, max_abstraction_function
from gui_abstraction.abstraction_questions import abstraction_question_array

ABSTRACTION_OPTION_CUSTOM = "Custom Configuration"
ABSTRACTION_OPTION_CASE_LETTERS_DIGITS = "Case Letters & Digits"
ABSTRACTION_OPTION_LETTERS_DIGITS = "Letters & Digits"
ABSTRACTION_OPTION_CASE_LETTER_DIGIT_SEQ = "Case Letter Seq. & Digit Seq."
ABSTRACTION_OPTION_DEFAULT = "Letter Seq. & Digit Seq. (Default)"
ABSTRACTION_OPTION_WORDS_DIGIT_SEQ = "Words & Digit Seq."
ABSTRACTION_OPTION_WORDS_DECIMALS = "Words & Decimals"
ABSTRACTION_OPTION_SENTENCES_DIGIT_SEQ = "Sentences & Digit Seq."
ABSTRACTION_OPTION_MAX = "Maximum Abstraction"

preconfigured_abstraction_answers = np.array([
    [ABSTRACTION_OPTION_CUSTOM, list(np.full(len(abstraction_question_array), False))],
    # [DEFAULT_CONFIG, self.config[:, 3]],
    # ["Only Duplicate Removal", duplicate_removal_function()[1]],
    [ABSTRACTION_OPTION_CASE_LETTERS_DIGITS, char_abstraction_case_sensitive_function()[1]],
    [ABSTRACTION_OPTION_LETTERS_DIGITS, char_abstraction_function()[1]],
    # ["Letter Sequences & Digits", letter_sequence_abstraction_function()[1]],
    # ["Letters & Digit Sequences", number_sequence_abstraction_function()[1]],
    [ABSTRACTION_OPTION_CASE_LETTER_DIGIT_SEQ, sequence_abstraction_case_sensitive_function()[1]],
    [ABSTRACTION_OPTION_DEFAULT, sequence_abstraction_function()[1]],  # Letter Sequences & Digit Sequences
    [ABSTRACTION_OPTION_WORDS_DIGIT_SEQ, word_abstraction_function()[1]],
    [ABSTRACTION_OPTION_WORDS_DECIMALS, word_decimal_abstraction_function()[1]],
    [ABSTRACTION_OPTION_SENTENCES_DIGIT_SEQ, word_sequence_abstraction_function()[1]],
    [ABSTRACTION_OPTION_MAX, max_abstraction_function()[1]],

    # ["Custom Dictionary", lambda data: custom_dictionary()],
    # ["Custom Full", lambda data: custom_full()]
], dtype=object)


def get_predefined_option_from_answers(answer):
    for a in preconfigured_abstraction_answers:
        if a[1] == answer:
            return a[0]
    return ABSTRACTION_OPTION_CUSTOM