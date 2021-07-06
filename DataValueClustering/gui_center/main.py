'''This script allows starting the GUI.'''
from datetime import datetime

from data_extraction.representants import get_repr_cluster, get_repr_list
from gui_center.cluster_representation import fancy_cluster_representation
from clustering.clustering import get_clusters_original_values, get_cluster_sizes
from gui_distances.blobinput_helper import get_blob_configuration
from distance.distance_matrix import calculate_distance_matrix_map
from gui_general.DropdownInput import input_dropdown
from gui_cluster_selection.clustering_choices import cluster_algorithms
from gui_abstraction.abstraction_choices import abstraction_functions
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
    """
    Central class that realises the workflow of the clustering approach and controls the data flows between the other components.
    Allows data value clustering via an API or via the GUI.
    """

    def __init__(self, data_index=-1, abstraction_index=-1, distance_index=-1, cluster_index=-1, data=None,
                 abstraction_f=None, distance_f=None, cluster_f=None, scatter_plot_save_path=None):
        """
        :param data_index: int
            index of the data (default is -1)
            data corresponds to files in the 'data' folder, order alphabetically
        :param abstraction_index: int
            index of the abstraction function (default is -1)
            functions specified in 'gui_abstraction/abstraction_choices.py'
        :param distance_index: int
            index of the distance function (default is -1)
            functions specified in 'gui_distance/distance_choices.py'
        :param cluster_index: int
            index of the cluster algorithm (default is -1)
            algorithms specified in 'gui_cluster_selection/clustering_choices.py'
        :param data: list[str]
            specify the data (default is None)
        :param abstraction_f:  (list[str]) -> ?
            specify the abstraction function (default is None)
        :param distance_f: (str, str) -> float
            specify the distance function (default is None)
        :param cluster_f: ({str: ndarray}, list[str]) -> ndarray[float, float]
            specify the clustering function (default is None)
        :param scatter_plot_save_path: str
            path where the scatter plot is saved as image
            will not be saved if None (default is None)
        """

        self.time_start = datetime.now()
        print("Initializing ...")

        self.l_data = get_sources_in_experiment_data_directory()
        self.l_abstractions = abstraction_functions
        self.l_distances = distance_functions
        self.l_clusters = cluster_algorithms

        self.data_index = data_index
        self.abstraction_index = abstraction_index
        self.distance_index = distance_index
        self.cluster_index = cluster_index

        self.data = data
        self.abstraction_f = abstraction_f
        self.distance_f = distance_f
        self.cluster_f = cluster_f

        self.values_abstracted = None
        self.abstraction_dict = None
        self.distance_matrix = None

        # Basic Configurations
        if ((self.data_index == -1 and self.data is None)
                or (self.abstraction_index == -1 and self.abstraction_f is None)
                or (self.distance_index == -1 and self.distance_f is None)
                or (self.cluster_index == -1 and self.cluster_f is None)):
            print("Basic Configurations ...")
            self.show_configuration_centre()

        print("Data preprocessing ...")

        # Specific Configurations
        # self.extract_configurations()
        if self.data_index != -1:
            self.extract_data()


        if self.abstraction_index != -1:
            self.abstraction_f, self.abstraction_answers = self.l_abstractions[self.abstraction_index, 1](self.data)

        if self.distance_index != -1:
            self.blob_configuration = get_blob_configuration(self.abstraction_answers)
            # [label, regex, resizable, info, x, y, size]
            self.distance_f, self.blob_configuration = self.l_distances[self.distance_index, 1](self.blob_configuration)


        self.num_data = len(self.data)

        # EXECUTION

        # COMPRESSION
        print("Calculate abstraction ...")
        self.time_abstraction_start = datetime.now()
        if self.values_abstracted is None or self.abstraction_dict is None:
            self.values_abstracted, self.abstraction_dict = self.abstraction_f(self.data)
        self.time_abstraction_end = datetime.now()

        self.num_abstracted_data = len(self.values_abstracted)
        self.abstraction_rate = self.num_data / self.num_abstracted_data

        # DISTANCE
        print("Calculate distance matrix ...")
        if self.distance_matrix is None:
            self.time_distance_start = datetime.now()
            self.distance_matrix_map = calculate_distance_matrix_map(self.distance_f, self.values_abstracted)
            self.time_distance_end = datetime.now()

        # CLUSTERING PARAMETER CONFIGURATION

        if self.cluster_index != -1 and self.cluster_f is None:
            self.cluster_answers, self.cluster_config_f = cluster_algorithms[self.cluster_index, 1]()
            if self.cluster_config_f is None:
                quit()

        if self.cluster_f is None:
            self.cluster_f = self.cluster_config_f(self.cluster_answers, self.distance_matrix_map, self.values_abstracted)

        # CLUSTERING
        print("Start clustering ...")
        self.time_cluster_start = datetime.now()
        self.clusters_abstracted = self.cluster_f(self.distance_matrix_map, self.values_abstracted)
        self.clusters = get_clusters_original_values(self.clusters_abstracted, self.values_abstracted, self.abstraction_f,
                                                     self.data)
        self.time_cluster_end = datetime.now()
        self.cluster_sizes, self.noise_size = get_cluster_sizes(self.clusters)
        self.cluster_sizes_abstracted, self.noise_size_abstracted = get_cluster_sizes(self.clusters_abstracted)

        print("Finalizing ...")
        self.time_end = datetime.now()
        self.timedelta_total = self.time_end - self.time_start
        self.timedelta_abstraction = self.time_abstraction_end - self.time_abstraction_start
        self.timedelta_distance = self.time_distance_end - self.time_distance_start
        self.timedelta_cluster = self.time_cluster_end - self.time_cluster_start

        # CLUSTER VISUALISATION
        self.fancy_cluster_list, self.noise = fancy_cluster_representation(self.data, self.clusters)
        self.fancy_cluster_list_abstracted, self.noise_abstracted = fancy_cluster_representation(self.values_abstracted, self.clusters_abstracted)
        self.no_clusters = len(self.fancy_cluster_list)
        self.no_noise = len(self.noise)

        # TODO
        # MDS scatter plot
        values_representants = get_repr_list(self.values_abstracted, self.abstraction_dict)
        show_mds_scatter_plot(values_representants, self.distance_matrix_map["distance_matrix"], self.clusters_abstracted, savepath=scatter_plot_save_path)
        # , "..\experiments\\result\here2")  # to instantly save the picture

        # CLUSTER VALIDATION
        noise_penalty = (self.num_data - self.no_noise)/self.num_data
        lines = np.where(self.clusters_abstracted != -1)[0]
        distance_matrix_lines = self.distance_matrix_map['distance_matrix'][lines, :]
        filtered_distance_matrix = distance_matrix_lines[:, lines]
        index_parameters = self.clusters_abstracted[self.clusters_abstracted != -1], filtered_distance_matrix
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

        print("Clusters abstracted:")
        for i in range(len(self.fancy_cluster_list_abstracted)):
            print("\t" + str(self.fancy_cluster_list_abstracted[i]))
        print("]")
        print("Noise abstracted:        ", self.noise_abstracted)

        print("Data Values:             ", self.num_data)
        print("Abstracted Data Values:  ", self.num_abstracted_data)
        print("Abstraction:             ", self.abstraction_rate)
        print("Number of clusters:      ", self.no_clusters)
        print("Number of noisy values:  ", self.no_noise)
        print("Time Total:              ", self.timedelta_total)
        print("Time Abstraction:        ", self.timedelta_abstraction)
        print("Time Distance-Matrix:    ", self.timedelta_distance)
        print("Time Clustering:         ", self.timedelta_cluster)
        print("wb-Index:                ", self.wb_index)
        print("Calinski-Harabasz Index: ", self.calinski_harabasz_index)
        print("Dunn Index:              ", self.dunn_index)

    def show_configuration_centre(self):
        title = "Configuration Centre"
        labels = ["data", "abstraction", "distance", "cluster"]
        matrix = [
            list(self.l_data[:, 0]),
            list(self.l_abstractions[:, 0]),
            list(self.l_distances[:, 0]),
            list(self.l_clusters[:, 0])
        ]
        current_indexes = [self.data_index, self.abstraction_index, self.distance_index, self.cluster_index]
        answers, answer_indexes = input_dropdown(title, labels, matrix, current_indexes)
        assert (len(answer_indexes) == 4)
        [self.data_index, self.abstraction_index, self.distance_index, self.cluster_index] = answer_indexes

    def extract_data(self):
        self.data = self.l_data[self.data_index, 1]()
        if len(self.data) > MAX_VALUES:
            self.data = self.data[:MAX_VALUES]


if __name__ == '__main__':
    Main()
    Main()
