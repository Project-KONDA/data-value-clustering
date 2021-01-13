from math import floor, sqrt
import re


def is_number(string):
    try:
        float(string)
        return True
    except ValueError:
        return False


def validate_input_float(string):
    if string == "" or is_number(string) and float(string) >= 0.:
        return True
    return False


def validate_input_int(string):
    return string.isdigit()


def character_escape(s):
    if s == "":
        return ".^"
    s = re.escape(s)
    regex = '(' + '[a-z]\\\-[a-z]' + '|' + '[A-Z]\\\-[A-Z]' + '|' + '[0-9]\\\-[0-9]' + ')'
    match = re.search(regex, s)
    while match is not None:
        m2 = match.group().replace("\-", "-")
        s = s.replace(match.group(), m2)
        match = re.search(regex, s)
    return '^[' + s + ']$'


def matrix_is_valid(matrix, n=-1):
    if n < 0:
        n = int(floor(sqrt(len(matrix))))
    else:
        if not n == int(floor(sqrt(len(matrix)))):
            return False

    if not len(matrix) == n * n + n + 1:
        return False
    # test Values - () is number
    if () not in matrix:
        return False
    if not isinstance(matrix[()], float):
        return False
    # test Values - (i) is single-character regex
    for i in range(n):
        if i not in matrix:
            return False
        if not isinstance(matrix[i], str):
            return False
    # test Values - (i,j) is number
    for i in range(n):
        for j in range(n):
            if (i, j) not in matrix:
                return False
            if not isinstance(matrix[(i, j)], float):
                return False
    return True


def print_cost_matrix(matrix):
    if not matrix_is_valid(matrix):
        print("{}")
        return
    n = int(floor(sqrt(len(matrix))))
    s = "{"
    # s += "(): "
    s += str(matrix[()])
    # s += ","
    print(s)
    s = ""
    for i in range(n):
        # s += str(i) + ": "
        s += matrix[i] + "  "
    print(s)
    # print()
    for i in range(n):
        s = ""
        for j in range(n):
            # s += "(" + str(i) + ", " + str(j) + "): "
            s += str(matrix[(j, i)]) + "  "
        print(s)

    print("}")
