from centre.clustering import cluster
from gui.DropdownInput import input_dropdown
from gui_clustering.cluster_algorithms_gui import cluster_algorithms
from gui_compression.compression_functions_gui import compression_functions
from gui_distances.distance_functions_gui import distance_functions
from data_extraction.read_file import get_sources_in_experiment_data_directory


class Main:

    def __init__(self):

        self.l_data = get_sources_in_experiment_data_directory()
        self.l_compressions = compression_functions
        self.l_distances = distance_functions
        self.l_clusters = cluster_algorithms

        self.data_index = -1
        self.compression_index = -1
        self.distance_index = -1
        self.cluster_index = -1

        self.show_configuration_centre()

        self.execute()

    def execute(self):
        # DATA
        # TODO: choose data

        data, compression_f, distance_f, cluster_f = self.extract_configurations()

        print("Execute ... [", "Data:", self.l_data[self.data_index, 0],
              "Compression:", self.l_compressions[self.compression_index, 0],
              "Distance:", self.l_distances[self.distance_index, 0],
              "Cluster:", self.l_clusters[self.cluster_index, 0], "]")

        # EXECUTION
        cluster_list, noise = cluster(data, compression_f, distance_f, cluster_f)

        # CLUSTER VISUALISATION
        # TODO
        #print(cluster_list, noise)

        # CLUSTER VALIDATION
        # TODO

        # SUGGEST DATA ENHANCEMENTS
        # TODO

    def extract_configurations(self):
        data = self.extract_data()
        compression_f = self.l_compressions[self.compression_index, 1]()
        distance_f = self.l_distances[self.distance_index, 1]()
        cluster_f = cluster_algorithms[self.cluster_index, 1]()
        return data, compression_f, distance_f, cluster_f

    def extract_data(self):
        data = self.l_data[self.data_index, 1]()
        if len(data) > 1000:
            data = data[0:1000]
        return data

    def show_configuration_centre(self):
        title = "Configuration Centre"
        labels = ["data", "compression", "distance", "cluster"]
        matrix = [
            list(self.l_data[:, 0]),
            list(self.l_compressions[:, 0]),
            list(self.l_distances[:, 0]),
            list(self.l_clusters[:, 0])
        ]
        answers, answer_indexes = input_dropdown(title, labels, matrix)
        assert (len(answer_indexes) == 4)
        [self.data_index, self.compression_index, self.distance_index, self.cluster_index] = answer_indexes

