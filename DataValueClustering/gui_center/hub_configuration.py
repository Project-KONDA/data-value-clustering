from datetime import datetime

from clustering.clustering import get_clusters_original_values, get_cluster_sizes
from data_extraction import read_data_values_from_file
from distance import calculate_distance_matrix_map
from export.ExecutionConfiguration import load_ExecutionConfiguration
from gui_center.cluster_representation import fancy_cluster_representation


class HubConfiguration():

    def __init__(self):

        "Initialisation of parameters"

        self.data = None
        self.data_path = None
        self.data_lower_limit = None
        self.data_upper_limit = None
        self.num_data = None

        self.abstraction_answers = None
        self.abstraction_f = None
        self.values_abstracted = None
        self.abstraction_dict = None
        self.num_abstracted_data = None
        self.abstraction_rate = None
        self.timedelta_abstraction = None

        self.distance_f = None
        self.distance_matrix_map = None
        self.timedelta_distance = None

        self.cluster_answers = None
        self.cluster_config_f = None
        self.cluster_f = None
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
        self.values_abstracted, self.abstraction_dict = self.abstraction_f(self.data)
        time_abstraction_end = datetime.now()
        self.timedelta_abstraction = time_abstraction_end - time_abstraction_start
        self.num_abstracted_data = len(self.values_abstracted)
        self.abstraction_rate = self.num_data / self.num_abstracted_data

    def execute_distance(self):
        time_distance_start = datetime.now()
        self.distance_matrix_map = calculate_distance_matrix_map(self.distance_f, self.values_abstracted)
        time_distance_end = datetime.now()
        self.timedelta_distance = time_distance_end - time_distance_start

    def execute_clustering(self):
        time_cluster_start = datetime.now()
        self.clusters_abstracted = self.cluster_f(self.distance_matrix_map, self.values_abstracted)
        time_cluster_end = datetime.now()
        self.clusters = get_clusters_original_values(self.clusters_abstracted, self.values_abstracted, self.abstraction_f, self.data)
        self.timedelta_cluster = time_cluster_end - time_cluster_start
        self.cluster_sizes, self.noise_size = get_cluster_sizes(self.clusters)
        self.cluster_sizes_abstracted, self.noise_size_abstracted = get_cluster_sizes(self.clusters_abstracted)
        self.fancy_cluster_list, self.noise = fancy_cluster_representation(self.data, self.clusters)
        self.fancy_cluster_list_abstracted, self.noise_abstracted = fancy_cluster_representation(self.values_abstracted, self.clusters_abstracted)
        self.no_clusters = len(self.fancy_cluster_list)
        self.no_noise = len(self.noise)

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
        self.abstraction_f = configuration.get_abstraction()
        self.distance_f = configuration.distance_functions[configuration.distance_func](configuration.get_costmap())
        self.cluster_f = configuration.clustering_args_functions[configuration.algorithm](**configuration.params_to_dict())

        # load results:



    "Test configuration validity"
    def data_configuration_valid(self):
        return not self.data is None

    def abstraction_configuration_valid(self):
        return not self.abstraction_f is None

    def distance_configuration_valid(self):
        return not self.distance_f is None

    def clustering_configuration_valid(self):
        return not self.cluster_f is None


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

    def get_abstraction_configuration(self):
        pass

    def get_distance_configuration(self):
        pass

    def get_clustering_configuration(self):
        pass

    # def get_abstraction_configuration(self):
    #     pass

    "Set configuration"
    def set_abstraction_configuration(self):
        pass

    def set_distance_configuration(self):
        pass

    def set_clustering_configuration(self):
        pass

    # def set_abstraction_configuration(self):
    #     pass