import datetime as dt
import os
from datetime import datetime
import json
from pathlib import Path
import copy
import jsbeautifier
import numpy
import numpy as np

from abstraction.abstraction import get_abstraction_method
from clustering.clustering import get_clusters_original_values, get_cluster_sizes
from data_extraction import read_data_values_from_file
from data_extraction.write_cluster_excel import cluster_to_excel
from data_extraction.write_file import write_data_values_to_file
from distance import calculate_distance_matrix_map
from distance.weighted_levenshtein_distance import get_weighted_levenshtein_distance, split_cost_map, get_cost_map
from gui_center.cluster_representation import fancy_cluster_representation
from gui_cluster_selection.algorithm_selection import algorithm_array
from gui_distances.blobinput_helper import get_blob_configuration
from gui_result.validation_questionnaire import question_1_answers, question_2_answers, question_3_answers, \
    question_4_answers, ValidationAnswer
from validation.intra_inter_cluster_distance import max_intra_cluster_distances, \
    average_intra_cluster_distances_per_cluster_per_value


def load_hub_configuration(path):
    text = open(path, "r")
    json_data = json.load(text)
    hub_config = create_hub_configuration_from_dict(json_data)
    blob_config_to_nparray(hub_config)
    return hub_config


def blob_config_to_nparray(hub_config):
    bc = hub_config.blob_configuration
    if bc is not None:
        x_len = len(bc)
        y_len = len(bc[0])
        array = np.empty((x_len, y_len), dtype=object)
        for x in range(x_len):
            for y in range(y_len):
                array[x,y] = bc[x][y]
        hub_config.blob_configuration = array


def create_hub_configuration_from_dict(dict):
    hub = HubConfiguration()
    hub.fill_hub_configuration_from_dict(dict)
    if hub.data_path is not None and hub.data is None:
        hub.execute_data()
    if hub.data is not None and hub.abstraction_configuration_valid() and not hub.abstraction_result_valid():
        hub.execute_abstraction()
    return hub


def cluster_label_from_txt_name(txt_name):
    split = txt_name.split("_")
    return int(split[1])


class HubConfiguration():

    def fill_hub_configuration_from_dict(self, dic):
        for key, value in dic.items():
            if value is None:
                setattr(self, key, None)
            elif key == "timedelta_abstraction" or key == "timedelta_distance" or key == "timedelta_cluster":
                value_split = value.split(":")
                value_adapted = dt.timedelta(hours=float(value_split[0]), minutes=float(value_split[1]),
                                             seconds=float(value_split[2]))
                setattr(self, key, value_adapted)
            elif key == "values_abstracted" or key == "clusters_abstracted" or key == "clusters":
                value_adapted = np.array(value)
                setattr(self, key, value_adapted)
            elif key == "distance_matrix_map":
                value_adapted = {"distance_matrix": np.array(value["distance_matrix"]),
                                 "condensed_distance_matrix": np.array(value["condensed_distance_matrix"]),
                                 "affinity_matrix": np.array(value["affinity_matrix"]),
                                 "min_distance": value["min_distance"], "max_distance": value["max_distance"]}
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
        self.no_values_abstracted = None
        self.abstraction_dict = None
        self.num_abstracted_data = None
        self.abstraction_rate = None
        self.timedelta_abstraction = None

        # self.distance_f = None
        # self.distance_algorithm = None # string
        self.distance_config_method = None
        self.blob_configuration = None
        self.cost_map = None  # dict
        self.distance_matrix_map = None
        self.timedelta_distance = None

        self.clustering_expert_mode = False
        self.clustering_algorithm = None  # string
        # self.clustering_algorithm = "Hierarchical"  # string
        self.clustering_parameters = None  # dict
        # self.clustering_parameters = {'method': 'single',
        #               'n_clusters': 7,
        #               'distance_threshold': None,
        #               'criterion': 'maxclust',
        #               'depth': None}  # dict
        # self.cluster_config_f = None
        # self.cluster_f = None
        self.clusters_abstracted = None
        self.clusters = None
        self.cluster_sizes = None
        self.noise_size = None
        self.cluster_sizes_abstracted = None
        self.noise_size_abstracted = None
        self.fancy_cluster_list = None
        self.fancy_simple_cluster_list = None
        self.noise = None
        self.fancy_cluster_list_abstracted = None
        self.noise_abstracted = None
        self.no_clusters = None
        self.no_noise = None
        self.timedelta_cluster = None

        self.json_save_path = None
        self.json_saved = False
        self.excel_save_path = None
        self.excel_saved = False
        self.excel_simple_save_path = None
        self.excel_simple_saved = False


        self.timedelta_total = None

        self.validation_answer_1 = None  # binary: ValidationAnswer.HAPPY or UNHAPPY
        self.validation_answer_2 = None  # ternary: ValidationAnswer.HAPPY or MORE or LESS
        self.validation_answer_3 = None  # ternary: ValidationAnswer.HAPPY or MORE or LESS
        self.validation_answer_4 = (None, None)  # binary & list(int): ValidationAnswer.HAPPY or UNHAPPY & and if UNHAPPY list(int)

    def execute_data(self):
        self.data = read_data_values_from_file(self.data_path)[self.data_lower_limit:self.data_upper_limit]
        self.num_data = len(self.data)

    def execute_abstraction(self):
        time_abstraction_start = datetime.now()
        abstraction_f = self.get_abstraction_function()
        self.values_abstracted, self.abstraction_dict = abstraction_f(self.data)
        self.no_values_abstracted = len(self.values_abstracted)
        time_abstraction_end = datetime.now()
        self.timedelta_abstraction = time_abstraction_end - time_abstraction_start
        self.num_abstracted_data = len(self.values_abstracted)
        self.abstraction_rate = self.num_data / self.num_abstracted_data
        self.fancy_simple_cluster_list = list()
        for i,v in enumerate(self.abstraction_dict.values()):
            self.fancy_simple_cluster_list.append(v)


    def execute_distance(self):
        time_distance_start = datetime.now()
        distance_f = self.get_distance_function()
        duplicates_removed = self.get_abstraction_configuration()[len(self.get_abstraction_configuration())-1]
        self.distance_matrix_map = calculate_distance_matrix_map(distance_f, self.values_abstracted, duplicates_removed)
        time_distance_end = datetime.now()
        self.timedelta_distance = time_distance_end - time_distance_start

    def execute_clustering(self):
        time_cluster_start = datetime.now()
        cluster_f = self.get_clustering_function()
        self.clusters_abstracted = cluster_f(self.distance_matrix_map, self.values_abstracted)
        time_cluster_end = datetime.now()
        self.clusters = get_clusters_original_values(self.clusters_abstracted, self.values_abstracted,
                                                     self.get_abstraction_function(), self.data)
        self.timedelta_cluster = time_cluster_end - time_cluster_start
        self.timedelta_total = self.timedelta_cluster + self.timedelta_distance + self.timedelta_abstraction
        self.cluster_sizes, self.noise_size = get_cluster_sizes(self.clusters)
        self.cluster_sizes_abstracted, self.noise_size_abstracted = get_cluster_sizes(self.clusters_abstracted)
        self.fancy_cluster_list, self.noise = fancy_cluster_representation(self.data, self.clusters)
        self.fancy_cluster_list_abstracted, self.noise_abstracted = fancy_cluster_representation(self.values_abstracted,
                                                                                                 self.clusters_abstracted)
        self.no_clusters = len(self.fancy_cluster_list)
        self.no_noise = len(self.noise)

    def save_simple_as_excel(self):
        if self.excel_simple_save_path is not None:
            cluster_to_excel(self.excel_simple_save_path, self.fancy_simple_cluster_list, [], None,
                             self.noise_abstracted, None, None, None)

    def save_as_excel(self, restricted):
        if self.excel_save_path is not None:
            # TODO: add the following to json exports?
            comp_to_normal_map = [list(elem) for elem in self.abstraction_dict.items()]
            map = dict([tuple(l) for l in comp_to_normal_map])
            lines = np.where(self.clusters_abstracted != -1)[0]
            distance_matrix_lines = self.distance_matrix_map['distance_matrix'][lines, :]
            filtered_distance_matrix = distance_matrix_lines[:, lines]
            index_parameters = self.clusters_abstracted[self.clusters_abstracted != -1], filtered_distance_matrix
            intra_cluster_distances = max_intra_cluster_distances(*index_parameters).tolist()
            intra_cluster_distances_per_cluster_per_value = average_intra_cluster_distances_per_cluster_per_value(
                *index_parameters)
            cluster_to_excel(self.excel_save_path, self.fancy_cluster_list, self.noise, self.fancy_cluster_list_abstracted,
                             self.noise_abstracted, map,
                             intra_cluster_distances_per_cluster_per_value,
                             intra_cluster_distances, restricted, self.fancy_simple_cluster_list)

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

    def get_as_json_tiny(self):
        c = copy.deepcopy(self)
        c.translate_cost_map_to_json()
        c.reset_data()
        c.reset_abstraction()
        c.reset_distances()
        c.reset_clustering()

        char = "\\"
        if "/" in c.data_path:
            char = "/"
        data_path_split = c.data_path.split(char)
        c.data_path = data_path_split[len(data_path_split)-1]

        c.json_save_path = None

        if c.excel_save_path is not None:
            char_excel = "\\"
            if "/" in c.excel_save_path:
                char_excel = "/"
            excel_save_path_split = c.excel_save_path.split(char_excel)
            c.excel_save_path = excel_save_path_split[len(excel_save_path_split) - 1]

        if c.excel_simple_save_path is not None:
            char_simple = "\\"
            if "/" in c.excel_simple_save_path:
                char_simple = "/"
            excel_simple_save_path_split = c.excel_simple_save_path.split(char_simple)
            c.excel_simple_save_path = excel_simple_save_path_split[len(excel_simple_save_path_split) - 1]

        return c.hub_configuration_to_json()

    def save_as_json(self):
        self.translate_cost_map_to_json()
        output_text = self.hub_configuration_to_json()
        f = open(self.json_save_path, "w")
        f.write(output_text)
        self.translate_cost_map_to_dict()
        f.close()

    def translate_cost_map_to_json(self):
        if not self.cost_map is None:
            cost_map_case, cost_map_regex, cost_map_weights = split_cost_map(self.cost_map)
            rgx_list = list()
            for sublist in cost_map_regex.tolist():
                s = ""
                for item in sublist:
                    s += item
                rgx_list.append(s)
            self.cost_map = {"weight_case_switch": cost_map_case, "rgx": rgx_list,
                             "w": cost_map_weights.tolist()}

    def translate_cost_map_to_dict(self):
        self.cost_map = None if self.cost_map is None else get_cost_map(**self.cost_map)

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

    def json_path_configuration_valid(self):
        return not self.json_save_path is None \
               and not self.json_save_path == ""

    def excel_path_configuration_valid(self):
        return not self.excel_save_path is None \
               and not self.excel_save_path == ""

    def data_configuration_valid(self):
        return self.data is not None

    def abstraction_configuration_valid(self):
        return self.abstraction_answers is not None

    def abstraction_result_valid(self):
        return self.values_abstracted is not None

    def distance_configuration_valid(self):
        return self.cost_map is not None

    def distance_result_valid(self):
        return self.distance_matrix_map is not None

    def clustering_configuration_valid(self):
        return self.clustering_algorithm is not None \
               and self.clustering_parameters is not None

    def clustering_result_valid(self):
        return self.clusters is not None

    "Test if ready for configuration"

    def distance_configuration_possible(self):
        return self.data_configuration_valid() \
               and self.abstraction_configuration_valid() \
               and self.abstraction_result_valid()

    def distance_execution_possible(self):
        return self.distance_configuration_possible() \
               and self.distance_configuration_valid()

    def clustering_configuration_possible(self):
        return self.distance_execution_possible() \
               and self.distance_result_valid()

    def clustering_execution_possible(self):
        return self.clustering_configuration_possible() \
            and self.clustering_configuration_valid()

    def result_is_ready(self):
        return self.clustering_execution_possible() \
               and self.clustering_result_valid()

    "Get configuration"

    def get_data_configuration(self):
        return self.data_path, self.data_lower_limit, self.data_upper_limit

    def get_abstraction_configuration(self):
        return self.abstraction_answers

    def get_distance_configuration(self):
        blobconfig = self.create_blob_configuration() if self.blob_configuration is None else self.blob_configuration
        return self.cost_map, blobconfig

    def get_clustering_selection(self):
        return self.clustering_algorithm

    def get_clustering_configuration(self):
        return self.clustering_parameters

    "Set & Get configuration methods"

    def get_distance_config_method(self):
        return self.distance_config_method

    def set_distance_config_method(self, method):
        self.distance_config_method = method

    "Set configuration"

    def set_data_configuration(self, data_path, data_lower_limit=None, data_upper_limit=None):
        if not self.data_path == data_path or not self.data_lower_limit == data_lower_limit or not self.data_upper_limit == data_upper_limit:
            self.data_path = data_path
            self.data_lower_limit = data_lower_limit
            self.data_upper_limit = data_upper_limit
            self.reset_data()
            self.reset_abstraction()
            self.reset_distances()
            self.reset_clustering()

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

    def set_clustering_selection(self, clustering_algorithm):
        if not self.clustering_algorithm == clustering_algorithm:
            self.clustering_algorithm = clustering_algorithm
            self.reset_clustering()

    def set_clustering_configuration(self, clustering_parameters):
        if not self.clustering_parameters == clustering_parameters:
            self.clustering_parameters = clustering_parameters
            self.reset_clustering()

    def set_validation_answer_1(self, answer):
        assert (answer is None or answer in question_1_answers[:, 0].tolist())
        self.validation_answer_1 = answer

    def set_validation_answer_2(self, answer):
        assert (answer is None or answer in question_2_answers[:, 0].tolist())
        self.validation_answer_2 = answer

    def set_validation_answer_3(self, answer):
        assert (answer is None or answer in question_3_answers[:, 0].tolist())
        self.validation_answer_3 = answer

    def set_validation_answer_4(self, answer, clusters):
        assert (answer is None or answer in question_4_answers[:, 0].tolist())
        if clusters is not None:
            for i, v in enumerate(clusters):
                assert (type(v) == int)
                assert (v <= self.no_clusters)
        data_names = None
        if clusters is not None:
            data_names = list()
            for i, v in enumerate(clusters):
                data_name = self.export_cluster_as_txt(v)
                data_names.append(data_name)
        self.validation_answer_4 = answer, data_names

    def export_cluster_as_txt(self, cluster_label):
        now = str(datetime.now())
        now = now.replace(":", "-").replace(" ", "_").replace(".", "-")
        data_name = "cluster_" + str(cluster_label) + "_" + str(now)
        data_file = data_name + ".txt"
        path = str(Path(__file__).parent.parent) + "/data/" + data_file
        if cluster_label == "noise":
            data = self.noise
        else:
            cluster_number = int(cluster_label) - 1
            data = self.fancy_cluster_list[cluster_number]
        write_data_values_to_file(path, data)
        return data_name

    def get_validation_answer_1(self):
        return self.validation_answer_1

    def get_validation_answer_2(self):
        return self.validation_answer_2

    def get_validation_answer_3(self):
        return self.validation_answer_3

    def get_validation_answer_4(self):
        return self.validation_answer_4

    def reset_validation_answers(self):
        self.validation_answer_1 = None
        self.validation_answer_2 = None
        self.validation_answer_3 = None
        self.validation_answer_4 = (None, None)

    def reset_data(self):
        self.data = None
        self.num_data = None

    def reset_abstraction(self):
        self.blob_configuration = None
        self.values_abstracted = None
        self.no_values_abstracted = None
        self.fancy_simple_cluster_list = None
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