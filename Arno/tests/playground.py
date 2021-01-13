import json
import re

import numpy as np

from gui.gui_costmatrix import getcostmatrix
from tests.testdata import data_test


def a(n, m):
    return n + m


def b(f, v):
    return f(1) + v


def myescape2(s, debug=False):
    if debug: print('start: ' + s)
    s = re.escape(s)
    if debug: print('escaped: ' + s)
    regex = '(' + '[a-z]\\\-[a-z]' + '|' + '[A-Z]\\\-[A-Z]' + '|' + '[0-9]\\\-[0-9]' + ')'

    if debug: print(re.search(regex, s))
    while re.search(regex, s) != None:
        match = re.search(regex, s)
        if debug:
            print('match: ' + str(match))
            m = match.group()
            if debug: print('  ' + str(match) + ' ' + m)
            m2 = m.replace("\-", "-")
            if debug: print('  replace ' + m + ' with ' + str(m2))
            print('    from ' + s)
            s = s.replace(m, m2)
            print('    to   ' + s)
    if debug: print('result: ' + s)
    return s

    def myescape(s):
        s = re.escape(s)
        regex = '(' + '[a-z]\\\-[a-z]' + '|' + '[A-Z]\\\-[A-Z]' + '|' + '[0-9]\\\-[0-9]' + ')'
        match = re.search(regex, s)
        while match != None:
            m2 = match.group().replace("\-", "-")
            s = s.replace(match.group(), m2)
            match = re.search(regex, s)
        return s


if __name__ == '__main__':
    s = "\"`´'"
    print("[" + re.escape(s) + "]")
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
    # v = np.zeros((2, 2))
    # v[1,0] = 1
    # print(len(list(set(data_test[0:100]))))

    # start = "a-ba-dsd-f--+d-f-*/-"
    # goal = "a-ba-dsd-f\-\-\+d-f\-\*/\-"
    #
    # result = myescape(start)
    # print(result == goal)
