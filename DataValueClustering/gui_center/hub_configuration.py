import datetime as dt
from datetime import datetime
import json

import jsbeautifier
import numpy
import numpy as np

from abstraction.abstraction import get_abstraction_method
from clustering.clustering import get_clusters_original_values, get_cluster_sizes
from data_extraction import read_data_values_from_file
from distance import calculate_distance_matrix_map
from distance.weighted_levenshtein_distance import get_weighted_levenshtein_distance, split_cost_map, get_cost_map
from gui_center.cluster_representation import fancy_cluster_representation
from gui_cluster_selection.algorithm_selection import algorithm_array
from gui_distances.blobinput_helper import get_blob_configuration


def load_hub_configuration(path):
    text = open(path, "r")
    json_data = json.load(text)
    hub = create_hub_configuration_from_dict(json_data)
    return hub


def create_hub_configuration_from_dict(dict):
    hub = HubConfiguration()
    hub.fill_hub_configuration_from_dict(dict)
    return hub


class HubConfiguration():

    def fill_hub_configuration_from_dict(self, dic):
        for key, value in dic.items():
            if key == "timedelta_abstraction" or key == "timedelta_distance" or key == "timedelta_cluster":
                value_split = value.split(":")
                value_adapted = dt.timedelta(hours=float(value_split[0]), minutes=float(value_split[1]), seconds=float(value_split[2]))
                setattr(self, key, value_adapted)
            elif key == "values_abstracted" or key == "clusters_abstracted" or key == "clusters":
                value_adapted = np.array(value)
                setattr(self, key, value_adapted)
            elif key == "distance_matrix_map":
                value_adapted = {"distance_matrix": np.array(value["distance_matrix"]), "condensed_distance_matrix": np.array(value["condensed_distance_matrix"]), "affinity_matrix": np.array(value["affinity_matrix"]), "min_distance": value["min_distance"], "max_distance": value["max_distance"]}
                setattr(self, key, value_adapted)
            elif key == "cost_map":
                value_adapted = get_cost_map(value["weight_case_switch"], value["rgx"], value["w"])
                setattr(self, key, value_adapted)
            else:
                setattr(self, key, value)

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
        self.blob_configuration = None
        self.cost_map = None # dict
        self.distance_matrix_map = None
        self.timedelta_distance = None

        self.clustering_algorithm = None # string
        self.clustering_parameters = None # dict
        self.clustering_answers = None
        # self.cluster_config_f = None
        # self.cluster_f = None
        self.clusters_abstracted = None
        self.clusters = None
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

        self.excel_path = None
        self.timedelta_total = None

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
        self.timedelta_total = self.timedelta_cluster + self.timedelta_distance + self.timedelta_abstraction
        self.cluster_sizes, self.noise_size = get_cluster_sizes(self.clusters)
        self.cluster_sizes_abstracted, self.noise_size_abstracted = get_cluster_sizes(self.clusters_abstracted)
        self.fancy_cluster_list, self.noise = fancy_cluster_representation(self.data, self.clusters)
        self.fancy_cluster_list_abstracted, self.noise_abstracted = fancy_cluster_representation(self.values_abstracted, self.clusters_abstracted)
        self.no_clusters = len(self.fancy_cluster_list)
        self.no_noise = len(self.noise)

    "Get functions"

    def get_abstraction_function(self):
        return get_abstraction_method(self.abstraction_answers)

    def get_distance_function(self):
        return get_weighted_levenshtein_distance(self.cost_map)

    def get_clustering_function(self):
        algorithms = np.array(algorithm_array, dtype=object)
        clustering_function_parameterized = algorithms[np.where(algorithms[:, 2] == self.clustering_algorithm)][:, 4][0]
        return clustering_function_parameterized(**self.clustering_parameters)

    "Export"

    def save(self, path):
        self.translate_cost_map_to_json()
        output_text = self.hub_configuration_to_json()
        f = open(path, "w")
        f.write(output_text)
        self.translate_cost_map_to_dict()
        f.close()

    def translate_cost_map_to_json(self):
        cost_map_case, cost_map_regex, cost_map_weights = split_cost_map(self.cost_map)
        self.cost_map = {"weight_case_switch": cost_map_case, "rgx": cost_map_regex.tolist(), "w": cost_map_weights.tolist()}

    def translate_cost_map_to_dict(self):
        self.cost_map = get_cost_map(**self.cost_map)

    def hub_configuration_to_json(self):
        json_text = json.dumps(self, default=self.default_object_to_json)
        my_options = jsbeautifier.default_options()
        my_options.indent_size = 2
        json_text = jsbeautifier.beautify(json_text, my_options)
        return json_text

    def default_object_to_json(self, o):
        if isinstance(o, numpy.ndarray):
            return o.tolist()
        elif isinstance(o, dt.timedelta):
            return str(o)
        else:
            return o.__dict__

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
        return self.cost_map, self.blob_configuration

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
            self.reset_abstraction()
            self.reset_distances()
            self.reset_clustering()

    def set_distance_configuration(self, cost_map, blob_configuration=None):
        if not self.cost_map == cost_map:
            self.cost_map = cost_map
            self.blob_configuration = blob_configuration
            self.reset_distances()
            self.reset_clustering()

    def set_clustering_selection(self, clustering_algorithm, clustering_answers=None):
        if not self.clustering_algorithm == clustering_algorithm or not self.clustering_answers == clustering_answers:
            self.clustering_algorithm = clustering_algorithm
            self.clustering_answers = clustering_answers
            self.reset_clustering()

    def set_clustering_configuration(self, clustering_parameters):
        if not self.clustering_parameters == clustering_parameters:
            self.clustering_parameters = clustering_parameters
            self.reset_clustering()

    def reset_abstraction(self):
        self.blob_configuration = None
        self.values_abstracted = None
        self.abstraction_dict = None
        self.num_abstracted_data = None
        self.abstraction_rate = None
        self.timedelta_abstraction = None
        self.timedelta_total = None

    def reset_distances(self):
        self.distance_matrix_map = None
        self.timedelta_distance = None
        self.timedelta_total = None

    def reset_clustering(self):
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
        self.timedelta_total = None
        self.clusters = None
        self.clusters_abstracted = None

    def create_blob_configuration(self):
        self.blob_configuration = get_blob_configuration(self.abstraction_answers)
        return self.blob_configuration