from gui_clustering.cluster_algorithms_gui import cluster_algorithms
from gui_compression.compression_functions_gui import compression_functions
from gui_distances.distance_functions_gui import distance_functions
from gui.DropdownInput import input_dropdown
from data_extraction.read_file import get_sources_in_experiment_data_directory
from centre.main import cluster

l_data = get_sources_in_experiment_data_directory()
l_compressions = compression_functions
l_distances = distance_functions
l_clusters = cluster_algorithms


def execute(data_i, compression_i, distance_i, cluster_i):


    # DATA
    # TODO: choose data
    data = l_data[data_i, 1]()
    if len(data) > 1000:
        data = data[0:1000]

    # CONFIGURATION
    # configuration compression?
    compression_f = l_compressions[compression_i, 1]

    # configuration distance
    distance_f = l_distances[distance_i, 1]()

    # configuration cluster
    cluster_f = cluster_algorithms[cluster_i, 1]()

    print("Execute ... [", "Data:", l_data[data_i, 0],
          "Compression:", l_compressions[compression_i, 0],
          "Distance:", l_distances[distance_i, 0],
          "Cluster:", cluster_algorithms[cluster_i, 0], "]")

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
    title = "Hello"
    labels = ["data", "compression", "distance", "cluster"]
    matrix = [
        list(l_data[:, 0]),
        list(l_compressions[:, 0]),
        list(l_distances[:, 0]),
        list(l_clusters[:, 0])
    ]
    answers, answer_indexes = input_dropdown(title, labels, matrix)
    assert (len(answer_indexes) == 4)
    [data_index, compression_index, distance_index, cluster_index] = answer_indexes

    execute(data_index, compression_index, distance_index, cluster_index)
