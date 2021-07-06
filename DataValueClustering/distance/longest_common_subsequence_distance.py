'''Apply longest common subsequence distance.'''
import numpy as np


def longest_common_subsequence_distance(seq1, seq2):
    lcss = longest_common_subsequence(seq1, seq2)
    # return (len(seq1)-lcss) + (len(seq2)-lcss)
    return 1 - lcss/min(len(seq1), len(seq2))


def longest_common_subsequence(seq1, seq2):
    # TODO: cost!?
    size_x = len(seq1) + 1
    size_y = len(seq2) + 1
    matrix = np.zeros((size_x, size_y))
    matrix[0, 0] = 0
    for x in range(1, size_x):
        matrix[x, 0] = 0
    for y in range(1, size_y):
        matrix[0, y] = 0
    for x in range(1, size_x):
        for y in range(1, size_y):
            if seq1[x-1] == seq2[y-1]:
                matrix[x,y] = matrix[x-1,y-1] + 1
            else:
                matrix[x, y] = max(matrix[x-1,y], matrix[x,y-1])


    #print(matrix)
    return matrix[size_x - 1, size_y - 1]
