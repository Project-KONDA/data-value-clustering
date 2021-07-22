'''Manage cost map input.'''
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


def groups_to_enumerations(s):
    s = s.replace("-", "\-")
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    alphabet_capitalized = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    digits = "0123456789"
    regex_alphabet = '[a-z]\\\-[a-z]'
    regex_alphabet_capitalized = '[A-Z]\\\-[A-Z]'
    regex_digits = '[0-9]\\\-[0-9]'
    s = replace_interval_by_enumeration(alphabet, regex_alphabet, s)
    s = replace_interval_by_enumeration(alphabet_capitalized, regex_alphabet_capitalized, s)
    s = replace_interval_by_enumeration(digits, regex_digits, s)
    return s


def replace_interval_by_enumeration(alphabet, regex_alphabet, s):
    match_object = re.search(regex_alphabet, s)
    while match_object is not None:
        match = match_object.group()
        match_split = match.split("\-")
        start = match_split[0]
        end = match_split[1]
        start_index = alphabet.index(start)
        end_index = alphabet.index(end) + 1
        if start_index < end_index:
            enumeration = alphabet[start_index: end_index]
            s = s.replace(match, enumeration)
        else:
            match_unescaped = match.replace("\-", "-")
            s = s.replace(match, match_unescaped)
        match_object = re.search(regex_alphabet, s)
    return s


def get_n_from_map(map):
    return int(floor(sqrt(len(map))))


def get_regexes_from_map(map):
    n = get_n_from_map(map)
    result = list()
    for i in range(n):
        result.append(map[i])
    return result


def costmap_is_valid(map, n=None):
    if type(map) is not type({}):
        raise ValueError
    if n is None:
        n = int(floor(sqrt(len(map))))
    else:
        if not n == int(floor(sqrt(len(map)))):
            raise ValueError

    if not len(map) == n * n + n + 1:
        raise ValueError
    # test Values - () is number
    if () not in map:
        raise ValueError
    if not isinstance(map[()], float) and not isinstance(map[()], int):
        raise ValueError
    # test Values - (i) is single-character regex
    for i in range(n):
        if i not in map:
            raise ValueError
        if not isinstance(map[i], str):
            raise ValueError
    # test Values - (i,j) is number
    for i in range(n):
        for j in range(n):
            if (i, j) not in map:
                raise ValueError
            if not isinstance(map[(i, j)], float) and not isinstance(map[(i, j)], int):
                raise ValueError
    return True


def print_cost_map(map):
    if not costmap_is_valid(map):
        print("{}")
        return
    n = int(floor(sqrt(len(map))))
    s = "{"
    # s += "(): "
    s += str(map[()])
    # s += ","
    print(s)
    s = ""
    for i in range(n):
        # s += str(i) + ": "
        s += map[i] + "  "
    print(s)
    # print()
    for i in range(n):
        s = ""
        for j in range(n):
            # s += "(" + str(i) + ", " + str(j) + "): "
            s += str(map[(j, i)]) + "  "
        print(s)

    print("}")


def preprocess_regexes(regexlist):
    # assert (regexlist[0] == "^$")
    # for i, regex in enumerate(regexlist):
    #     assert type(regex) is str
    #     assert regex[0] == '^' and regex[len(regex) - 1] == "$"
    #
    #     r_len = len(regex)
    #     if r_len > 2 and regex[1] == "[" and regex[r_len-2] == "]":
    #         regexlist[i] = regex[2:r_len - 2]
    #     else:
    #         regexlist[i] = regex[1:r_len - 1]
    return list(regexlist)


def example_costmap():
    example_map = {(()): 1, 0: "^$", 1: "^a-f$", 2: "^A-F$", 3: "^0-2$", 4: "^.$"}
    for i in range(5):
        for j in range(5):
            example_map[(i, j)] = float(int(i != j) + 1)
    return example_map

if __name__ == "__main__":
    print_cost_map(example_costmap())
    print(costmap_is_valid(example_costmap()))
    print(len(example_costmap()))

    print(groups_to_enumerations(""))
    print("1\\3"[1] == "\\")