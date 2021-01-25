from centre.cluster_representation import fancy_cluster_representation
from clustering.clustering import get_clusters_original_values
from distance.distance_matrix import calculate_distance_matrix
from gui.DropdownInput import input_dropdown
from gui_clustering.cluster_algorithms_gui import cluster_algorithms
from gui_compression.compression_functions_gui import compression_functions
from gui_distances.distance_functions_gui import distance_functions
from data_extraction.read_file import get_sources_in_experiment_data_directory


class Main:

    def __init__(self, data_index=-1, compression_index=-1, distance_index=-1, cluster_index=-1, data=None,
                 compression_f=None, distance_f=None, cluster_f=None):

        self.l_data = get_sources_in_experiment_data_directory()
        self.l_compressions = compression_functions
        self.l_distances = distance_functions
        self.l_clusters = cluster_algorithms

        self.data_index = data_index
        self.compression_index = compression_index
        self.distance_index = distance_index
        self.cluster_index = cluster_index

        self.data = data
        self.compression_f = compression_f
        self.distance_f = distance_f
        self.cluster_f = cluster_f

        self.values_compressed = None
        self.compression_dict = None
        self.distance_matrix = None

        # Basic Configurations
        if ((data_index == -1 or data is None)
                and (compression_index == -1 or compression_f is None)
                and (distance_index == -1 or distance_f is None)
                and (cluster_index == -1 or cluster_f is None)):
            self.show_configuration_centre()

        # Specific Configurations
        # self.extract_configurations()
        if self.data_index != -1:
            self.extract_data()

        if self.compression_index != -1:
            self.compression_f, self.compression_answers = self.l_compressions[self.compression_index, 1]()
        if self.distance_index != -1:
            self.distance_f = self.l_distances[self.distance_index, 1]()  # compression configuration für blobs

        # EXECUTION

        print("Calculate compression ...")
        # COMPRESSION
        if self.values_compressed is None or self.compression_dict is None:
            self.values_compressed, self.compression_dict = self.compression_f(self.data)

        print("Calculate distance matrix ...")
        # DISTANCE
        if self.distance_matrix is None:
            self.distance_matrix = calculate_distance_matrix(self.distance_f, self.values_compressed)

        if self.cluster_index != -1:
            self.cluster_f = cluster_algorithms[self.cluster_index, 1]()  # distanzmatrix bereits berechnet

        print("Start clustering ...")
        # CLUSTERING
        clusters_compressed = self.cluster_f(self.distance_matrix, self.values_compressed)
        clusters = get_clusters_original_values(clusters_compressed, self.values_compressed, self.compression_f,
                                                self.data)

        # CLUSTER VISUALISATION
        fancy_cluster_representation(self.data, clusters)
        # TODO
        # print(cluster_list, noise)

        # CLUSTER VALIDATION
        # TODO

        # SUGGEST DATA ENHANCEMENTS
        # TODO

    def extract_data(self):
        self.data = self.l_data[self.data_index, 1]()
        if len(self.data) > 1000:
            self.data = self.data[0:1000]

    def show_configuration_centre(self):
        title = "Configuration Centre"
        labels = ["data", "compression", "distance", "cluster"]
        matrix = [
            list(self.l_data[:, 0]),
            list(self.l_compressions[:, 0]),
            list(self.l_distances[:, 0]),
            list(self.l_clusters[:, 0])
        ]
        current_indexes = [self.data_index, self.compression_index, self.distance_index, self.cluster_index]
        answers, answer_indexes = input_dropdown(title, labels, matrix, current_indexes)
        assert (len(answer_indexes) == 4)
        [self.data_index, self.compression_index, self.distance_index, self.cluster_index] = answer_indexes


if __name__ == '__main__':
    Main()