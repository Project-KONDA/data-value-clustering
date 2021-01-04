

def levenshtein_distance(seq1, seq2):
    size_x = len(seq1) + 1
    size_y = len(seq2) + 1
    matrix = np.zeros((size_x, size_y))
    for x in range(size_x):
        matrix[x, 0] = x  # delete every character of source prefix
    for y in range(size_y):
        matrix[0, y] = y  # insert every character of target prefix

    for x in range(1, size_x):
        for y in range(1, size_y):
            if seq1[x - 1] == seq2[y - 1]:  # same character
                matrix[x, y] = min(
                    matrix[x - 1, y] + 1,  # deletion with cost 1
                    matrix[x - 1, y - 1],  # substitution with cost 0
                    matrix[x, y - 1] + 1  # insertion with cost 1
                )
            else:  # different character
                matrix[x, y] = min(
                    matrix[x - 1, y] + 1,  # deletion with cost 1
                    matrix[x - 1, y - 1] + 1,  # substitution with cost 1
                    matrix[x, y - 1] + 1  # insertion with cost 1
                )
    print(matrix)
    return matrix[size_x - 1, size_y - 1]