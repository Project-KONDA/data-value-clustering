import re

# dictionary:
lower_letter = ["[a-z]", "l"]
upper_letter = ["[A-Z]", "L"]
digit = ["[0-9]", "1"]

lower_letter_seq = ["[a-z]+", "a"]
upper_letter_seq = ["[A-Z]+", "A"]
digit_seq = ["[0-9]+", "0"]

lower_word_seq = ["(w )+w", "s"]
upper_word_seq = ["W (w )+w", "S"]

decimal_comma = ["0,0", "2"]

lower_word = ["l+", "w"]
upper_word = ["Ll+", "W"]


# pre-defined matrices:
char_compression = [
    lower_letter,  # lower-case letter
    upper_letter,  # upper-case letter
    digit,  # digit
]
sequence_compression = [
    lower_letter_seq,  # lower-case letter sequence
    upper_letter_seq,  # upper-case letter sequence
    digit_seq,  # digit sequence
]
letter_sequence_compression = [
    lower_letter_seq,  # lower-case letter sequence
    upper_letter_seq,  # upper-case letter sequence
    digit,  # digit
]
word_decimal_compression = [  # TODO: cost functions
    lower_letter,  # lower-case letter
    upper_letter,  # upper-case letter
    upper_word,  # upper-case word
    lower_word,  # lower-case word
    digit_seq,  # digit sequence
    decimal_comma,  # decimal
]
word_compression = [  # TODO: cost functions
    lower_letter,  # lower-case letter
    upper_letter,  # upper-case letter
    upper_word,  # Word
    lower_word,  # word
    digit_seq,  # digit sequence
]
word_sequence_compression = [  # TODO: cost functions
    lower_letter,  # lower-case letter
    upper_letter,  # upper-case letter
    upper_word,  # upper-case word
    lower_word,  # lower-case word
    upper_word_seq,  # upper-case word sequence
    lower_word_seq,  # lower-case word sequence
    digit_seq,  # digit sequence
]



def compress(seq, compression_matrix):
    for x in range(len(compression_matrix)):
        seq = re.sub(compression_matrix[x][0], compression_matrix[x][1], seq)
    return seq


def compress_list(values, compression_matrix):
    validate_compression_matrix(compression_matrix)
    compressed_values = values.copy()
    assert len(compressed_values) == len(values)
    for i in range(len(compressed_values)):
        compressed_values[i] = compress(compressed_values[i], compression_matrix)
    return compressed_values


def get_compression_from_value(compressed_values, i):
    return compressed_values[i]


def compressed_value_index_map(unique_values):
    index_map = {}
    for i in range(len(unique_values)):
        index_map[unique_values[i]] = i
    return index_map


def regex_from_compression(seq, compression_matrix):
    for x in range(len(compression_matrix)):
        seq = re.sub(compression_matrix[x][1], compression_matrix[x][0], seq)
    return seq


def validate_compression_matrix(compression_matrix):
    length = len(compression_matrix[0])
    for i in range(len(compression_matrix)):
        assert len(compression_matrix[i]) == length
