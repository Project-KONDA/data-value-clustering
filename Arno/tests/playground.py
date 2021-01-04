import json
import re

import numpy as np

from gui.gui_costmatrix import getcostmatrix
from tests.testdata import data_test


def a(n, m):
    return n + m


def b(f, v):
    return f(1) + v


if __name__ == '__main__':
    # d = {}
    # for i in range(-1, 2):
    #    for j in range(-1, 2):
    #        d[i,j] = str(i) + " " + str(j)
    # print(d)
    # print(b(lambda x: a(1, x), 1))
    # print( re.match("^$", "s") == None)
    # s = "a"
    # if True:
    #     s = "a" + s
    # print(s)
    # print(list("abc"))

    # a = np.array([[0, 1], [2, 3]])
    # print(a[:, 1])

    # d = {(()): 0, 1: 1}
    # print(d)
    # print(str(d))
    # print(json.loads(str(d)))
    # print(getcostmatrix())
    # list = []
    # print(not list)
    # list.append(2)
    # print(not list)
    v = np.zeros((2, 2))
    v[1,0] = 1
    print(len(list(set(data_test[0:100]))))
