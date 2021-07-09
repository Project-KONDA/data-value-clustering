from datetime import datetime
import numpy as np

from abstraction.abstraction import get_abstraction_method
from clustering.clustering import get_clusters_original_values, get_cluster_sizes, clustering_args_functions
from data_extraction import read_data_values_from_file
from distance import calculate_distance_matrix_map
from distance.weighted_levenshtein_distance import get_weighted_levenshtein_distance
from export.ExecutionConfiguration import load_ExecutionConfiguration
from gui_center.cluster_representation import fancy_cluster_representation
from gui_cluster_selection.algorithm_selection import algorithm_array


class HubConfiguration():

    def __init__(self):

        "Initialisation of parameters"

        self.data = None
        self.data_path = None
        self.data_lower_limit = None
        self.data_upper_limit = None
        self.num_data = None

        self.abstraction_answers = None
        # self.abstraction_f = None
        self.values_abstracted = None
        self.abstraction_dict = None
        self.num_abstracted_data = None
        self.abstraction_rate = None
        self.timedelta_abstraction = None

        # self.distance_f = None
        # self.distance_algorithm = None # string
        self.cost_map = None # dict
        self.distance_matrix_map = None
        self.timedelta_distance = None

        self.clustering_algorithm = None # string
        self.clustering_parameters = None # dict
        self.clustering_answers = None
        # self.cluster_config_f = None
        # self.cluster_f = None
        self.cluster_sizes = None
        self.noise_size = None
        self.cluster_sizes_abstracted = None
        self.noise_size_abstracted = None
        self.fancy_cluster_list = None
        self.noise = None
        self.fancy_cluster_list_abstracted = None
        self.noise_abstracted = None
        self.no_clusters = None
        self.no_noise = None
        self.timedelta_cluster = None

        self.clusters_abstracted = None
        self.clusters = None

    def execute_data(self):
        self.data = read_data_values_from_file(self.data_path)[self.data_lower_limit:self.data_upper_limit]
        self.num_data = len(self.data)

    def execute_abstraction(self):
        time_abstraction_start = datetime.now()
        abstraction_f = self.get_abstraction_function()
        self.values_abstracted, self.abstraction_dict = abstraction_f(self.data)
        time_abstraction_end = datetime.now()
        self.timedelta_abstraction = time_abstraction_end - time_abstraction_start
        self.num_abstracted_data = len(self.values_abstracted)
        self.abstraction_rate = self.num_data / self.num_abstracted_data

    def execute_distance(self):
        time_distance_start = datetime.now()
        distance_f = self.get_distance_function()
        self.distance_matrix_map = calculate_distance_matrix_map(distance_f, self.values_abstracted)
        time_distance_end = datetime.now()
        self.timedelta_distance = time_distance_end - time_distance_start

    def execute_clustering(self):
        time_cluster_start = datetime.now()
        cluster_f = self.get_clustering_function()
        self.clusters_abstracted = cluster_f(self.distance_matrix_map, self.values_abstracted)
        time_cluster_end = datetime.now()
        self.clusters = get_clusters_original_values(self.clusters_abstracted, self.values_abstracted, self.get_abstraction_function(), self.data)
        self.timedelta_cluster = time_cluster_end - time_cluster_start
        self.cluster_sizes, self.noise_size = get_cluster_sizes(self.clusters)
        self.cluster_sizes_abstracted, self.noise_size_abstracted = get_cluster_sizes(self.clusters_abstracted)
        self.fancy_cluster_list, self.noise = fancy_cluster_representation(self.data, self.clusters)
        self.fancy_cluster_list_abstracted, self.noise_abstracted = fancy_cluster_representation(self.values_abstracted, self.clusters_abstracted)
        self.no_clusters = len(self.fancy_cluster_list)
        self.no_noise = len(self.noise)

    def get_abstraction_function(self):
        return get_abstraction_method(self.abstraction_answers)

    def get_distance_function(self):
        return get_weighted_levenshtein_distance(self.cost_map)

    def get_clustering_function(self):
        algorithms = np.array(algorithm_array, dtype=object)
        clustering_function_parameterized = algorithms[np.where(algorithms[:, 2] == self.clustering_algorithm)][:, 4][0]
        return clustering_function_parameterized(**self.clustering_parameters)

    def save(self, path):
        # TODO: translate fields into distance_func, algorithm, algorithm_params, costmap
        # ExecutionConfigurationFromParams(self.data_path, self.lower_limit, self.upper_limit, self.abstraction_answers ...).save()
        pass

    def load(self, path):
        configuration = load_ExecutionConfiguration(path)
        # see ExecutionConfiguration.execute()

        # load configuration:
        self.data_path = configuration.data_path
        self.data_lower_limit = configuration.lower_limit
        self.data_upper_limit = configuration.upper_limit
        # self.abstraction_f = configuration.get_abstraction()
        # self.distance_f = configuration.distance_functions[configuration.distance_func](configuration.get_costmap())
        # self.cluster_f = configuration.clustering_args_functions[configuration.algorithm](**configuration.params_to_dict())

        # load results:



    "Test configuration validity"
    def data_configuration_valid(self):
        return not self.data is None

    def abstraction_configuration_valid(self):
        # return not self.abstraction_f is None
        pass

    def distance_configuration_valid(self):
        # return not self.distance_f is None
        pass

    def clustering_configuration_valid(self):
        # return not self.cluster_f is None
        pass

    "Test if ready for configuration"
    def abstraction_configuration_possible(self):
        return self.data_configuration_valid()

    def distance_configuration_possible(self):
        return self.abstraction_configuration_possible() \
            and self.abstraction_configuration_valid()

    def clustering_configuration_possible(self):
        return self.distance_configuration_possible() \
            and self.distance_configuration_valid()

    def execute_possible(self):
        return self.clustering_configuration_possible() \
            and self.clustering_configuration_valid()

    "Get configuration"

    def get_data_configuration(self):
        return self.data_path, self.data_lower_limit, self.data_upper_limit

    def get_abstraction_configuration(self):
        return self.abstraction_answers

    def get_distance_configuration(self):
        return self.cost_map

    def get_clustering_selection(self):
        return self.clustering_algorithm, self.clustering_answers

    def get_clustering_configuration(self):
        return self.clustering_parameters

    "Set configuration"
    def set_data_configuration(self, data_path, data_lower_limit=None, data_upper_limit=None):
        if not self.data_path == data_path or not self.data_lower_limit == data_lower_limit or not self.data_upper_limit == data_upper_limit:
            self.data_path = data_path
            self.data_lower_limit = data_lower_limit
            self.data_upper_limit = data_upper_limit
            self.data = None

    def set_abstraction_configuration(self, abstraction_answers):
        if not self.abstraction_answers == abstraction_answers:
            self.abstraction_answers = abstraction_answers
            self.values_abstracted = None
            self.abstraction_dict = None
            self.num_abstracted_data = None
            self.abstraction_rate = None
            self.timedelta_abstraction = None

    def set_distance_configuration(self, cost_map):
        if not self.cost_map == cost_map:
            self.cost_map = cost_map
            self.distance_matrix_map = None
            self.timedelta_distance = None

    def set_clustering_selection(self, clustering_algorithm, clustering_answers=None):
        if not self.clustering_algorithm == clustering_algorithm or not self.clustering_answers == clustering_answers:
            self.clustering_algorithm = clustering_algorithm
            self.clustering_answers = clustering_answers
            self.cluster_sizes = None
            self.noise_size = None
            self.cluster_sizes_abstracted = None
            self.noise_size_abstracted = None
            self.fancy_cluster_list = None
            self.noise = None
            self.fancy_cluster_list_abstracted = None
            self.noise_abstracted = None
            self.no_clusters = None
            self.no_noise = None
            self.timedelta_cluster = None

    def set_clustering_configuration(self, clustering_parameters):
        if not self.clustering_parameters == clustering_parameters:
            self.clustering_parameters = clustering_parameters
            self.cluster_sizes = None
            self.noise_size = None
            self.cluster_sizes_abstracted = None
            self.noise_size_abstracted = None
            self.fancy_cluster_list = None
            self.noise = None
            self.fancy_cluster_list_abstracted = None
            self.noise_abstracted = None
            self.no_clusters = None
            self.no_noise = None
            self.timedelta_cluster = None


    "Get functions"

    def get_abstraction_f(self):
        return get_abstraction_method(self.abstraction_answers)

    def get_distance_f(self):
        pass

    def get_clustering_f(self):
        pass