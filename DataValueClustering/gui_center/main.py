from datetime import datetime

from gui_center.cluster_representation import fancy_cluster_representation
from clustering.clustering import get_clusters_original_values, get_cluster_sizes
from gui_distances.blobinput_helper import get_blob_configuration
from distance.distance_matrix import calculate_distance_matrix_map
from gui_general.DropdownInput import input_dropdown
from gui_cluster_selection.clustering_choices import cluster_algorithms
from gui_compression.compression_choices import compression_functions
from gui_distances.distance_choices import distance_functions
from data_extraction.read_file import get_sources_in_experiment_data_directory
from gui_result import show_mds_scatter_plot
from validation.dunn_index import dunn_index
from validation.calinski_harabasz_index import calinski_harabasz_index, wb_index
from validation.intra_inter_cluster_distance import max_intra_cluster_distances, \
    average_intra_cluster_distances_per_cluster_per_value
import numpy as np

MAX_VALUES = 1000


class Main:

    def __init__(self, data_index=-1, compression_index=-1, distance_index=-1, cluster_index=-1, data=None,
                 compression_f=None, distance_f=None, cluster_f=None, scatter_plot_save_path=None):

        self.time_start = datetime.now()
        print("Initializing ...")

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
        if ((self.data_index == -1 and self.data is None)
                or (self.compression_index == -1 and self.compression_f is None)
                or (self.distance_index == -1 and self.distance_f is None)
                or (self.cluster_index == -1 and self.cluster_f is None)):
            print("Basic Configurations ...")
            self.show_configuration_centre()

        print("Data preprocessing ...")

        # Specific Configurations
        # self.extract_configurations()
        if self.data_index != -1:
            self.extract_data()


        if self.compression_index != -1:
            self.compression_f, self.compression_answers = self.l_compressions[self.compression_index, 1](self.data)

        if self.distance_index != -1:
            self.blob_configuration = get_blob_configuration(self.compression_answers)
            # [label, regex, resizable, info, x, y, size]
            self.distance_f, self.blob_configuration = self.l_distances[self.distance_index, 1](self.blob_configuration)


        self.num_data = len(self.data)

        # EXECUTION

        # COMPRESSION
        print("Calculate compression ...")
        self.time_compressing_start = datetime.now()
        if self.values_compressed is None or self.compression_dict is None:
            self.values_compressed, self.compression_dict = self.compression_f(self.data)
        self.time_compressing_end = datetime.now()

        self.num_compressed_data = len(self.values_compressed)
        self.compression_rate = self.num_data / self.num_compressed_data

        # DISTANCE
        print("Calculate distance matrix ...")
        if self.distance_matrix is None:
            self.time_distance_start = datetime.now()
            self.distance_matrix_map = calculate_distance_matrix_map(self.distance_f, self.values_compressed)
            self.time_distance_end = datetime.now()

        # CLUSTERING PARAMETER CONFIGURATION

        if self.cluster_index != -1 and self.cluster_f is None:
            self.cluster_answers, self.cluster_config_f = cluster_algorithms[self.cluster_index, 1]()
            if self.cluster_config_f is None:
                quit()

        if self.cluster_f is None:
            self.cluster_f = self.cluster_config_f(self.cluster_answers, self.distance_matrix_map, self.values_compressed)

        # CLUSTERING
        print("Start clustering ...")
        self.time_cluster_start = datetime.now()
        self.clusters_compressed = self.cluster_f(self.distance_matrix_map, self.values_compressed)
        self.clusters = get_clusters_original_values(self.clusters_compressed, self.values_compressed, self.compression_f,
                                                self.data)
        self.time_cluster_end = datetime.now()
        self.cluster_sizes, self.noise_size = get_cluster_sizes(self.clusters)
        self.cluster_sizes_compressed, self.noise_size_compressed = get_cluster_sizes(self.clusters_compressed)

        print("Finalizing ...")
        self.time_end = datetime.now()
        self.timedelta_total = self.time_end - self.time_start
        self.timedelta_compression = self.time_compressing_end - self.time_compressing_start
        self.timedelta_distance = self.time_distance_end - self.time_distance_start
        self.timedelta_cluster = self.time_cluster_end - self.time_cluster_start

        # CLUSTER VISUALISATION
        self.fancy_cluster_list, self.noise = fancy_cluster_representation(self.data, self.clusters)
        self.fancy_cluster_list_compressed, self.noise_compressed = fancy_cluster_representation(self.values_compressed, self.clusters_compressed)
        self.no_clusters = len(self.fancy_cluster_list)
        self.no_noise = len(self.noise)

        # TODO

        # MDS scatter plot
        show_mds_scatter_plot(self.values_compressed, self.distance_matrix_map["distance_matrix"], self.clusters_compressed, savepath=scatter_plot_save_path)
        # , "..\experiments\\result\here2")  # to instantly save the picture

        # CLUSTER VALIDATION
        noise_penalty = (self.num_data - self.no_noise)/self.num_data
        lines = np.where(self.clusters_compressed != -1)[0]
        distance_matrix_lines = self.distance_matrix_map['distance_matrix'][lines, :]
        filtered_distance_matrix = distance_matrix_lines[:, lines]
        index_parameters = self.clusters_compressed[self.clusters_compressed != -1], filtered_distance_matrix
        self.wb_index = noise_penalty * wb_index(*index_parameters)
        self.calinski_harabasz_index = noise_penalty * calinski_harabasz_index(*index_parameters)
        self.dunn_index = noise_penalty * dunn_index(*index_parameters)
        self.intra_cluster_distances = max_intra_cluster_distances(*index_parameters)
        self.average_intra_cluster_distances_per_cluster_per_value = average_intra_cluster_distances_per_cluster_per_value(*index_parameters)

        # TODO

        # SATISFACTION QUESTIONNAIRE
        # TODO

        # SUGGEST DATA ENHANCEMENTS
        # TODO

        self.print_result()

    def print_result(self):
        print("Clusters:")
        for i in range(len(self.fancy_cluster_list)):
            print("\t" + str(self.fancy_cluster_list[i]))
        print("]")
        print("Noise:", str(self.noise))

        print("Clusters compressed:")
        for i in range(len(self.fancy_cluster_list_compressed)):
            print("\t" + str(self.fancy_cluster_list_compressed[i]))
        print("]")
        print("Noise compressed:        ", self.noise_compressed)

        print("Data Values:             ", self.num_data)
        print("Compressed Data Values:  ", self.num_compressed_data)
        print("Compression:             ", self.compression_rate)
        print("Number of clusters:      ", self.no_clusters)
        print("Number of noisy values:  ", self.no_noise)
        print("Time Total:              ", self.timedelta_total)
        print("Time Compression:        ", self.timedelta_compression)
        print("Time Distance-Matrix:    ", self.timedelta_distance)
        print("Time Clustering:         ", self.timedelta_cluster)
        print("wb-Index:                ", self.wb_index)
        print("Calinski-Harabasz Index: ", self.calinski_harabasz_index)
        print("Dunn Index:              ", self.dunn_index)

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

    def extract_data(self):
        self.data = self.l_data[self.data_index, 1]()
        if len(self.data) > MAX_VALUES:
            self.data = self.data[:MAX_VALUES]


if __name__ == '__main__':
    Main()
    Main()
