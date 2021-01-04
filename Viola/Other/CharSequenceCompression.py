class CharSequenceCompression:
    compression_matrix = [
        ["[a-z]+", "a"],  # lower-case letter sequence
        ["[A-Z]+", "A"],  # upper-case letter sequence
        ["[0-9]+", "1"],  # digit sequence
    ]

    def substitution_cost(c1, prev1, c2, prev2):
        if c1 == c2:  # same character
            return 0
        else:  # different character
            if is_special(c1) and is_special(c2):
                return 2
            elif (is_lower_case(c1) and is_upper_case(c2)) or (is_lower_case(c2) and is_upper_case(c1)):
                return 0.5
            elif (is_lower_case(c1) and is_digit(c2)) or (is_lower_case(c2) and is_digit(c1)):
                return 0.75
            elif (is_lower_case(c1) and is_space(c2)) or (is_lower_case(c2) and is_space(c1)):
                return 0.75
            elif (is_lower_case(c1) and is_special(c2)) or (is_lower_case(c2) and is_special(c1)):
                return 2
            elif (is_upper_case(c1) and is_digit(c2)) or (is_upper_case(c2) and is_digit(c1)):
                return 0.75
            elif (is_upper_case(c1) and is_space(c2)) or (is_upper_case(c2) and is_space(c1)):
                return 0.75
            elif (is_upper_case(c1) and is_special(c2)) or (is_upper_case(c2) and is_special(c1)):
                return 2
            elif (is_digit(c1) and is_space(c2)) or (is_digit(c2) and not is_space(c1)):
                return 0.75
            elif (is_digit(c1) and is_special(c2)) or (is_digit(c2) and not is_special(c1)):
                return 2
            else:
                # TODO
                return 1

    def insertion_cost(c, prev):
        if is_lower_case(c):
            if is_upper_case(prev) or is_space(prev):
                return 0.0625
            else:
                return 0.125
        elif is_upper_case(c):
            return 0.25
        elif is_digit(c):
            return 0.5
        elif is_space(c):
            return 0.75
        elif is_special(c):
            return 2
        else:
            return 1

    def deletion_cost(c, prev):
        return insertion_cost(c, prev)