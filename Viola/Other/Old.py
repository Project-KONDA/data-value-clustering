import numpy as np

from Compression.Compression import compress
from Distance.WeightedLevenshteinDistance import is_lower_case, is_upper_case, is_digit, is_space, is_special, \
    to_lower_case
from Test.Test import run_example
from Util.ListOperations import remove_duplicates

np.set_printoptions(threshold=np.inf)


def distance(seq1, seq2):
    size_x = len(seq1) + 1
    size_y = len(seq2) + 1
    matrix = np.zeros((size_x, size_y))
    matrix[0, 0] = 0
    for x in range(1, size_x):
        matrix[x, 0] = matrix[x - 1, 0] + deletion_cost(seq1[x - 1])  # deletion
    for y in range(1, size_y):
        matrix[0, y] = matrix[0, y - 1] + insertion_cost(seq2[y - 1])  # insertion
    for x in range(1, size_x):
        for y in range(1, size_y):
            matrix[x, y] = min(
                matrix[x - 1, y] + deletion_cost(seq1[x - 1]),  # deletion
                matrix[x - 1, y - 1] + substitution_cost(seq1[x - 1], seq2[y - 1]),  # substitution
                matrix[x, y - 1] + insertion_cost(seq2[y - 1])  # insertion
            )
    # print(matrix)
    return matrix[size_x - 1, size_y - 1]


def substitution_cost(c1, c2):
    if c1 == c2:  # same character
        return 0
    else:  # different character
        if to_lower_case(c1) == to_lower_case(c2):
            return 0.1
        elif is_lower_case(c1) and is_lower_case(c2):
            return 0.25
        elif is_upper_case(c1) and is_upper_case(c2):
            return 0.25
        elif is_digit(c1) and is_digit(c2):
            return 0.25
        elif is_special(c1) and is_special(c2):
            return 1
        elif (is_lower_case(c1) and is_upper_case(c2)) or (
                is_lower_case(c2) and is_upper_case(
            c1)):
            return 0.375
        elif (is_digit(c1) and is_upper_case(c2)) or (
                is_digit(c2) and is_upper_case(c1)):
            return 0.75
        elif (is_lower_case(c1) and is_digit(c2)) or (
                is_lower_case(c2) and is_digit(c1)):
            return 0.75
        elif (is_special(c1) and is_upper_case(c2)) or (
                is_special(c2) and is_upper_case(c1)):
            return 2
        elif (is_lower_case(c1) and is_special(c2)) or (
                is_lower_case(c2) and is_special(c1)):
            return 2
        elif (is_digit(c1) and is_special(c2)) or (
                is_digit(c2) and not is_special(c1)):
            return 2
        else:
            # TODO
            return 1


def insertion_cost(c):
    if is_lower_case(c) or is_upper_case(c):
        return 0.25
    elif is_digit(c):
        return 0.5
    elif is_special(c):
        return 2
    else:
        return 1


def deletion_cost(c):
    if is_lower_case(c) or is_upper_case(c):
        return 0.25
    elif is_digit(c):
        return 0.5
    elif is_special(c):
        return 2
    else:
        return 1


#print(regex_from_compression("Aa 1"))





# distance(compression)
    # ... calculate_distance(): ... compression.insertion_cost(...)...
# cluster(values, distance, compression, clustering_algo)
    # ... compression.compress_list(values) ...
    # ... distance.calculate_distance_matrix(compression) ...


# runtime:

# matrix calculation for 100 values:
# - non-flattened: 0:00:03.143471
# - semi-flattened: 0:00:02.937821
# - flattened: 0:00:00.540556

# clustering 100 values without showing plot:
# - non-flattened: 0:00:03.495804
# - semi-flattened: 0:00:02.928830
# - flattened: 0:00:00.789223


# assertions:

assert remove_duplicates(["a", "b", "a", "c", "c"]) == ["a", "b", "c"]

# # assert: insertion cost = deletion cost
# assert distance("", "1") == distance("1", "")
# assert distance("", "a") == distance("a", "")
# assert distance("", "A") == distance("A", "")
# assert distance("", ".") == distance(".", "")
#
# # assert: insertion cost is independent from previous
# assert distance("a", "a.") == distance("", ".")
# assert distance("a", "a.") == distance("A", "A.")
# assert distance("a", "a.") == distance("1", "1.")
# assert distance("a", "a.") == distance(".", "..")
# assert distance("a", "aa") == distance("", "a")
# assert distance("a", "aa") == distance("A", "Aa")
# assert distance("a", "aa") == distance("1", "1a")
# assert distance("a", "aa") == distance(".", ".a")
# assert distance("a", "aA") == distance("", "A")
# assert distance("a", "aA") == distance("A", "AA")
# assert distance("a", "aA") == distance("1", "1A")
# assert distance("a", "aA") == distance(".", ".A")
# assert distance("a", "a1") == distance("", "1")
# assert distance("a", "a1") == distance("A", "A1")
# assert distance("a", "a1") == distance("1", "11")
# assert distance("a", "a1") == distance(".", ".1")
#
# # assert: deletion cost is independent from previous
# assert distance("a.", "a") == distance(".", "")
# assert distance("a.", "a") == distance("A.", "A")
# assert distance("a.", "a") == distance("1.", "1")
# assert distance("a.", "a") == distance("..", ".")
# assert distance("aa", "a") == distance("a", "")
# assert distance("aa", "a") == distance("Aa", "A")
# assert distance("aa", "a") == distance("1a", "1")
# assert distance("aa", "a") == distance(".a", ".")
# assert distance("aA", "a") == distance("A", "")
# assert distance("aA", "a") == distance("AA", "A")
# assert distance("aA", "a") == distance("1A", "1")
# assert distance("aA", "a") == distance(".A", ".")
# assert distance("a1", "a") == distance("1", "")
# assert distance("a1", "a") == distance("A1", "A")
# assert distance("a1", "a") == distance("11", "1")
# assert distance("a1", "a") == distance(".1", ".")
#
# # assert: substitution cost is independent from previous
# # TODO
#
# # assert: replace upper case, lower case or digit by other of same type has equal cost
# assert distance("A", "B") == distance("a", "b")
# assert distance("1", "2") == distance("a", "b")
#
# # assert: replacing upper case by digit or special has equal cost as replacing lower case by digit or special
# assert distance("A", "1") == distance("a", "1")
# assert distance("A", ".") == distance("a", ".")
#
# # assert: upper case are more similar to each other than to lower case and vice versa
# assert distance("A", "b") > distance("a", "b")
# assert distance("a", "B") > distance("a", "b")
# assert distance("A", "B") == distance("a", "b")
# assert distance("A", "b") > distance("A", "B")
# assert distance("a", "B") > distance("A", "B")
#
# # assert: replacing by dot has equal cost for upper, lower and digit
# assert distance("1", ".") == distance("a", ".")  # ?
# assert distance("A", ".") == distance("a", ".")
#
# # assert: costs for deletion, insertion and substitution are > 0
# assert distance("a", "") > distance("", "")
# assert distance("", "a") > distance("", "")
# assert distance("a", "b") > distance("a", "a")
#
# # assert: different lower/upper case are less similar than equal lower/upper case
# assert distance("A", "B") > distance("A", "A")
# assert distance("a", "b") > distance("a", "a")
#
# # assert: distance between equal/different lower case is equal to distance between equal/different upper case
# assert distance("A", "A") == distance("a", "a")
# assert distance("A", "B") == distance("a", "b")
#
# # assert: distance between different special is greater than distance between different lower/upper
# assert distance("!", ".") > distance("a", "b")
# assert distance("!", ".") > distance("A", "B")
#
# # assert: lower and upper case more similar than lower/upper and other lower/upper
# assert distance("a", "b") > distance("A", "a")
# assert distance("a", "b") > distance("a", "A")
# assert distance("a", "1") > distance("a", "A")
# assert distance("a", "1") > distance("a", "c")  # ?
#
# # assert: replacing lower/upper case by dot has greater cost than by lower, upper or digit
# assert distance("a", ".") > distance("a", "A")
# assert distance("a", ".") > distance("a", "B")
# assert distance("a", ".") > distance("a", "a")
# assert distance("a", ".") > distance("a", "b")
# assert distance("a", ".") > distance("a", "1")  # == ?
# assert distance("A", ".") > distance("A", "a")
# assert distance("A", ".") > distance("A", "b")
# assert distance("A", ".") > distance("A", "A")
# assert distance("A", ".") > distance("A", "B")
# assert distance("A", ".") > distance("A", "1")  # == ?
#
# # assert: replacing special by special has greater cost than replacing lower/upper/digit by lower/upper/digit
# assert distance("!", ".") > distance("a", "b")  # ?
# assert distance("!", ".") > distance("A", "B")  # ?
# assert distance("!", ".") > distance("1", "2")  # ?
#
# # old assertions:
# # assert my_distance("a", "bc") > my_distance("a", "ab")
# # assert my_distance("a", "bc") > my_distance("a", "AB") # !!
# # assert my_distance("a", "a b") > my_distance("a", "ab")
# # assert my_distance("a", "A b") > my_distance("a", "a b")
#
assert is_lower_case("a")
assert is_upper_case("A")
assert is_digit("1")
assert is_special(".")
assert is_special("!")
assert is_special("?")
assert is_special("-")
assert is_special("+")
assert is_special("*")
assert is_special("#")
assert is_special("/")
assert is_special("(")
assert is_special(")")
assert is_special("&")
assert is_special("%")
assert is_special("[")
assert is_special("]")
assert is_special("=")
assert is_special(")")
assert is_special("$")
assert is_special("~")
assert is_special(":")
assert is_special(";")
assert is_special(" ")

assert is_space(" ")

assert to_lower_case("ABC") == "abc"

assert compress("abc abc") == "a a"


