midas_dates_10000_expectation = [

    # *** certain ***
    # -
    ["1875", "1750",
     "1977.10", "1846.04",
     "1732.08.14"],

    # *** uncertain ***
    # +
    ["1868?",
     "um 1725/1730?",
     "um 1620?",
     "1601/1700?",
     "nach 1864?",
     "1840-1855?"],

    # *** fuzzy ***
    # /
    ["um 1460", "um 845",
     "gegen 1907",  # !!! - new cluster?
     "um 560ante",
     "um 1634/1637",
     "um 1634-1636"],

    # *** imprecise ***
    # -
    ["1451/1475", "901/1000",
     "600ante/551ante",  # !
     "um 1728/um 1760"],  # !!!

    # imprecise one boundary
    # -
    ["nach 1594",
     "vor 1672",  # ! - new cluster?
     "nach 530ante",
     "vor 1876.02",  # ! -
     "nach 1415.02.23",
     "nach 1470-1484",
     "vor 1401/1500",  # ! -
     "nach 1895/1897"],

    # *** alternatives ***
    # -
    ["1471 / um 1505/1510",  # !
     "um 1508 / um 1510",
     "um 1651 / nach 1651",
     "um 1365/1370 / um 1380"],

    # *** intervals ***
    # -
    ["1853-1856", "1441-1447", "834-843",
     "1871.02.08-1871.03.23",  # !
     "1415-um 1425"],  # !!

    # interval one boundary
    ["ab 1445"],  # !

    # *** code ***
    # +
    ["---"],

]  # n = 9

midas_dates_10000_expectation_v2 = [

    # *** certain ***
    #
    ["1875", "1750",
     "1977.10", "1846.04",
     "1732.08.14"],

    # *** uncertain ***
    #
    ["1868?",
     "um 1725/1730?",
     "um 1620?",
     "1601/1700?",
     "nach 1864?",
     "1840-1855?"],

    # *** fuzzy ***
    #
    ["um 1460", "um 845",
     "um 560ante",
     "um 1634/1637",
     "um 1634-1636"],

    #
    ["gegen 1907"],

    # *** imprecise ***
    #
    ["1451/1475", "901/1000",
     "600ante/551ante",  # !
     "um 1728/um 1760"],  # !!!

    # imprecise one boundary
    #
    ["vor 1672",
     "vor 1876.02",
     "vor 1401/1500",
     ],

    #
    ["nach 1594",
     "nach 530ante",
     "nach 1415.02.23",
     "nach 1470-1484",
     "nach 1895/1897"
     ],

    # *** alternatives ***
    # -
    ["1471 / um 1505/1510",  # !
     "um 1508 / um 1510",
     "um 1651 / nach 1651",
     "um 1365/1370 / um 1380"],

    # *** intervals ***
    # -
    ["1853-1856", "1441-1447", "834-843",
     "1871.02.08-1871.03.23",  # !
     "1415-um 1425"],  # !!

    # interval one boundary
    ["ab 1445"],  # !

    # *** code ***
    # +
    ["---"],

]  # n = 11

midas_dates_10000_expectation_v3 = [

    ["vor 1672",
     "vor 1876.02",
     "vor 1401/1500"],

    ["nach 1594",
     "nach 1864?",
     "nach 1415.02.23",
     "nach 1470-1484",
     "nach 1895/1897"],

    ["nach 530ante"],

    ["ab 1445"],

    ["gegen 1907"],

    ["um 1460", "um 845",
     "um 1620?",
     "um 1634-1636",
     "um 1634/1637",
     "um 1725/1730?"],

    ["um 560ante"],

    ["1471 / um 1505/1510"],

    ["um 1651 / nach 1651"],

    ["um 1365/1370 / um 1380",
     "um 1508 / um 1510",
     "um 1728/um 1760"],

    ["1451/1475", "901/1000",
     "1601/1700?"],

    ["600ante/551ante"],

    ["1853-1856", "1441-1447", "834-843",
     "1871.02.08-1871.03.23",
     "1840-1855?"],

    ["1415-um 1425"],

    ["1875", "1750",
     "1977.10", "1846.04",
     "1732.08.14",
     "1868?"],

    ["---"],

]  # n = 16












# clustering_true = [  # first try
#     ["1875", "1750"],  # year
#     ["1977.10", "1846.04", "1732.08.14"],  # year.month.day
#     ["1868?"],  # year uncertain
#     ["um 1460", "um 1620?", "um 1634/1637", "um 1634-1636", "gegen 1907", "um 845", "um 560ante"],  # fuzzy
#     ["1451/1475", "nach 1594", "vor 1672", "1601/1700?", "nach 1864?", "901/1000", "600ante/551ante", "nach 1470-1484"],  # point in interval
#     ["1471 / um 1505/1510", "um 1508 / um 1510", "um 1651 / nach 1651"],  # alternatives
#     ["1853-1856", "1441-1447", "834-843", "ab 1445"],  # interval
#     ["---"],  # other
# ]

# clustering_true = [  # fine-grained
#
#     # *** certain ***
#     ["1875", "1750"],  # year
#     ["1977.10", "1846.04"],  # year.month
#     ["1732.08.14"],  # year.month.day
#
#     # *** uncertain ***
#     ["1868?"],  # year uncertain
#
#     # *** fuzzy ***
#     ["um 1460", "gegen 1907", "um 845", "um 560ante"],  # fuzzy year
#
#     ["um 1620?"],  # fuzzy year uncertain
#
#     ["um 1634/1637"],  # fuzzy point in interval
#     ["um 1728/um 1760"],  # point in interval with fuzzy boundaries
#
#     ["um 1725/1730?"],  # fuzzy uncertain point in interval
#
#     # *** imprecise ***
#     ["1451/1475", "901/1000", "600ante/551ante"],  # point in interval with two year boundaries
#
#     ["nach 1594", "vor 1672"],  # point in interval with one year boundary
#     ["vor 1876.02"],  # point in interval with one year.month boundary
#     ["nach 1415.02.23"],  # point in interval with one year.month.day boundary
#
#     ["1601/1700?"],  # uncertain point in interval with two boundaries
#     ["nach 1864?"],  # uncertain point in interval with one boundary
#
#     ["vor 1401/1500", "nach 1895/1897"],  # point in interval with one point in interval boundary
#
#     # *** alternatives ***
#     ["1471 / um 1505/1510"],  # alternatives: one normal, one fuzzy point in interval
#     ["um 1508 / um 1510"],  # alternatives: two fuzzy points in intervals
#     ["um 1651 / nach 1651"],  # alternatives: one fuzzy point in interval, one interval with one year boundary
#
#     # *** intervals ***
#     ["1853-1856", "1441-1447", "834-843"],  # interval with two year boundaries
#     ["1871.02.08-1871.03.23"],  # interval with two year.month.day boundaries
#
#     ["ab 1445"],  # interval with one year boundary
#
#     ["1840-1855?"],  # uncertain interval with two year boundaries
#
#     ["um 1634-1636"],  # fuzzy interval
#     ["1415-um 1425"],  # interval with one fuzzy boundary
#
#     ["nach 1470-1484"],  # point in interval with one interval boundary
#
#     # *** code ***
#     ["---"],  # other
# ]

# clustering_true = [
#
#     # *** certain ***
#     ["1875", "1750",
#      "1977.10", "1846.04",
#      "1732.08.14"],  # year.month.day
#
#     # *** uncertain ***
#     ["1868?"],  # year uncertain
#
#     # fuzzy uncertain
#     ["um 1725/1730?",
#      "um 1620?"],
#
#     # imprecise uncertain
#     ["1601/1700?"],  # uncertain point in interval with two boundaries
#     ["nach 1864?"],  # uncertain point in interval with one boundary
#
#     # interval uncertain
#     ["1840-1855?"],  # uncertain interval with two year boundaries
#
#     # *** fuzzy ***
#     ["um 1460", "gegen 1907", "um 845", "um 560ante"],
#
#     ["um 1634/1637"],
#
#     ["um 1634-1636"],
#
#     # *** imprecise ***
#     ["1451/1475", "901/1000", "600ante/551ante"],  # point in interval with two year boundaries
#
#     ["um 1728/um 1760"],
#
#     # imprecise one boundary
#     ["nach 1594", "vor 1672",
#      "vor 1876.02",
#      "nach 1415.02.23"],
#
#     ["nach 1470-1484"],
#
#     ["vor 1401/1500", "nach 1895/1897"],
#
#     # *** alternatives ***
#     ["1471 / um 1505/1510"],
#     ["um 1508 / um 1510"],
#     ["um 1651 / nach 1651"],
#
#     # *** intervals ***
#     ["1853-1856", "1441-1447", "834-843",
#      "1871.02.08-1871.03.23"],
#     ["1415-um 1425"],
#
#     # interval one boundary
#     ["ab 1445"],  # interval with one year boundary
#
#     # *** code ***
#     ["---"],  # other
#
# ]  # n = 14