from tkinter import *
from clustering.clustering import cluster
from gui.cluster_algorithms_gui import cluster_algorithms
from gui.compression_functions_gui import compression_functions
from gui.distance_functions_gui import distance_functions


def execute(a, b, c, d):
    # CONFIGURATION
    # configuration compression?
    compression_f = compression_functions[compression_index, 1]

    # configuration distance
    distance_f = distance_functions[distance_index, 1]()

    # configuration cluster
    cluster_f = cluster_algorithms[cluster_index, 1]()

    # EXECUTION
    cluster_list, noise = cluster(data, compression_f, distance_f, cluster_f)

    # CLUSTER VISUALISATION
    # TODO
    print(cluster_list, noise)

    # CLUSTER VALIDATION
    # TODO
    # SUGGEST DATA ENHANCEMENTS
    # TODO


if __name__ == '__main__':
    # GUI
    root = Tk()
    root.title("Value Clustering")
    root.geometry("570x110")

    # INPUT
    # TODO
    # choose data -> query?
    data = ["a", "b", "0"]

    # choose compression
    compression_index = 0

    # choose distance function
    distance_index = 3

    # choose cluster algorithm
    cluster_index = 0

    button = Button(root, text='OK', width=75,
                    command=lambda: execute(data, compression_index, distance_index, cluster_index))
    button.grid(row=6, column=0, columnspan=5)

    # GUI
    root.mainloop()
