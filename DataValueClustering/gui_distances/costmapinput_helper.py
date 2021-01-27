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
        return False
    if n is None:
        n = int(floor(sqrt(len(map))))
    else:
        if not n == int(floor(sqrt(len(map)))):
            return False

    if not len(map) == n * n + n + 1:
        return False
    # test Values - () is number
    if () not in map:
        return False
    if not isinstance(map[()], float):
        return False
    # test Values - (i) is single-character regex
    for i in range(n):
        if i not in map:
            return False
        if not isinstance(map[i], str):
            return False
    # test Values - (i,j) is number
    for i in range(n):
        for j in range(n):
            if (i, j) not in map:
                return False
            if not isinstance(map[(i, j)], float):
                return False
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
    assert (regexlist[0] == "^$")
    for i, regex in enumerate(regexlist):
        assert type(regex) is str
        assert regex[0] == '^' and regex[len(regex) - 1] == "$"

        r_len = len(regex)
        print(regex)
        if re.search(regex, "^\^\[.*\]\$$") is not None:
            regexlist[i] = regex[2:r_len - 2]
        else:
            regexlist[i] = regex[1:r_len - 1]
    return list(regexlist)


def example_costmap():
    example_map = {(()): 1, 0: "^$", 1: "^a-f$", 2: "^A-F$", 3: "^0-2$", 4: "^.$"}
    for i in range(5):
        for j in range(5):
            example_map[(i, j)] = float(int(i != j) + 1)
    return example_map
