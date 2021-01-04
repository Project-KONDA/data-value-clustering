import numpy as np
import re

np.set_printoptions(threshold=np.inf)


class Compression:
    # https://en.wikipedia.org/wiki/Strategy_pattern
    # https://en.wikipedia.org/wiki/Template_method_pattern

    compression_matrix = [["", ""]]  # contains lists of pairs containing regex and result

    def compress_list(self, l):
        f = l.copy()
        for i in range(len(f)):
            f[i] = self.compress(self, f[i])
        return f

    def compress(self, seq):
        for x in range(len(self.compression_matrix)):
            seq = re.sub(self.compression_matrix[x][0], self.compression_matrix[x][1], seq)
        return seq

    def regex_from_compression(self, seq):
        for x in range(len(self.compression_matrix)):
            seq = re.sub(self.compression_matrix[x][1], self.compression_matrix[x][0], seq)
        return seq

    def insertion_cost(self, char, prev):
        pass

    def deletion_cost(self, char, prev):
        pass

    def distance(self, seq1, seq2):
        size_x = len(seq1) + 1
        size_y = len(seq2) + 1
        matrix = np.zeros((size_x, size_y))
        matrix[0, 0] = 0
        for x in range(1, size_x):
            matrix[x, 0] = matrix[x - 1, 0] + self.deletion_cost(seq1[x - 1], seq1[x - 2])  # deletion
        for y in range(1, size_y):
            matrix[0, y] = matrix[0, y - 1] + self.insertion_cost(seq2[y - 1], seq2[y - 2])  # insertion
        for x in range(1, size_x):
            for y in range(1, size_y):
                matrix[x, y] = min(
                    matrix[x - 1, y] + self.deletion_cost(seq1[x - 1], seq1[x - 2]),  # deletion
                    matrix[x - 1, y - 1] + self.substitution_cost(seq1[x - 1], seq1[x - 2], seq2[y - 1],
                                                                  seq2[y - 2]),  # substitution
                    matrix[x, y - 1] + self.insertion_cost(seq2[y - 1], seq2[y - 2])  # insertion
                )
        # print(matrix)
        return matrix[size_x - 1, size_y - 1]
