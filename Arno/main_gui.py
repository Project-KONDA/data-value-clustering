from tkinter import *

import numpy as np

from cluster_algorithms.dendrogram import cluster_dendrogram_centroid, cluster_dendrogram_linkage
from compression.compressions import compression_simple, compress_array, compression_typed
from compression.thin import super_thin_array_amounts
from distance_functions.weighted_levenshtein_distance2 import get_cost_map, levenshtein_distance2
from gui.gui_costmatrix2 import Costmatrix
from tests.testdata import data_test
from distance_functions.weighted_levenshtein_distance import levenshtein_distance

# Data
# [ Name, () -> numpy-array of values ]
data = np.array([
            ["Data 100",
            np.array(data_test[0:100])],
            ["Data 1000",
            np.array(data_test[100:1100])],
            ["Data 10000",
            np.array(data_test[1100:11100])]
        ],
        dtype=object)

# Compression Methods
# [ Name, (array of values) -> array of values ]
comp = np.array([
    ["No Compression",
     lambda vals: vals],
    ["Simple",
     lambda vals: compress_array(vals, compression_simple)],
    ["Typed",
     lambda vals: compress_array(vals, compression_typed)],
    ["Tiny",
     lambda vals: super_thin_array_amounts(vals)[:, 1]]
])

# Distance Functions
# [ Name, (value, value) -> number ]
dist = np.array([
    ["LS1",
     levenshtein_distance],
    ["LS2",
     lambda s1, s2: levenshtein_distance2(get_cost_map(), s1, s2)],
    ["LS2 - c3",
     lambda s1, s2: levenshtein_distance2(Costmatrix.getcostmatrix(3), s1, s2)],
    ["LS2 - c4",
     lambda s1, s2: levenshtein_distance2(Costmatrix.getcostmatrix(4), s1, s2)],
    ["LS2 - c5",
     lambda s1, s2: levenshtein_distance2(Costmatrix.getcostmatrix(5), s1, s2)]

])

# Cluster Functions
# [ Name, (distance-function, values) -> dentrogram ]
clus = np.array([
    ["Linkage",
     cluster_dendrogram_linkage],
    ["Centroid",
     cluster_dendrogram_centroid]
])


def buildclusters(da, co, di, cl):
    c_data = comp[co, 1](data[da, 1])

    c_data = np.array(list(set(c_data)))

    cluster = clus[cl, 1](
        dist[di, 1],
        c_data
    )


def buildmyclusters():
    if i_data.get() != "" and i_comp.get() != "" and i_dist.get() != "" and i_clus.get() != "" and i_numb.get() != "":
        buildclusters(
            list(data[:, 0]).index(i_data.get()),
            list(comp[:, 0]).index(i_comp.get()),
            list(dist[:, 0]).index(i_dist.get()),
            list(clus[:, 0]).index(i_clus.get()))
        print()

def testVal(inStr, acttyp):
    if acttyp == '1':  # insert
        if not inStr.isdigit():
            return False
    return True


if __name__ == '__main__':

    root = Tk()
    root.title("Value Clustering")
    root.geometry("570x110")

    Label(root, text="Choose a cluster algorithm", justify=LEFT, width=15).grid(row=2, column=0, columnspan=4,
                                                                                sticky=W + E)

    i_data = StringVar(value=data[0, 0])
    Label(root, text="Data: ", justify=LEFT, width=15).grid(row=3, column=0, sticky=W + E)
    OptionMenu(root, i_data, *data[:, 0]).grid(row=4, column=0, sticky=W + E)

    i_comp = StringVar(value=comp[0, 0])
    Label(root, text="Compression: ", justify=LEFT, width=15).grid(row=3, column=1, sticky=W + E)
    OptionMenu(root, i_comp, *comp[:, 0]).grid(row=4, column=1, sticky=W + E)

    i_dist = StringVar(value=dist[0, 0])
    Label(root, text="Distance: ", justify=LEFT, width=15).grid(row=3, column=2, sticky=W + E)
    OptionMenu(root, i_dist, *dist[:, 0]).grid(row=4, column=2, sticky=W + E)

    i_clus = StringVar(value=clus[0, 0])
    Label(root, text="Cluster: ", justify=LEFT, width=15).grid(row=3, column=3, sticky=W + E)
    OptionMenu(root, i_clus, *clus[:, 0]).grid(row=4, column=3, sticky=W + E)

    i_numb = StringVar(value='2')
    Label(root, text="Amount: ", justify=LEFT, width=15).grid(row=3, column=4, sticky=W + E)
    e = Entry(root, validate="key", textvariable=i_numb, justify=CENTER)
    e['validatecommand'] = (e.register(testVal), '%P', '%d')
    e.grid(row=4, column=4, sticky=W + E)

    button = Button(root, text='OK', width=75, command=buildmyclusters)
    button.grid(row=6, column=0, columnspan=5)

    root.mainloop()

