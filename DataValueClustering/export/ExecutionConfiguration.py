'''Manage configurations for data value clustering.'''
import json
import re
from datetime import datetime

import jsbeautifier

from sklearn.metrics import adjusted_rand_score, adjusted_mutual_info_score, completeness_score, fowlkes_mallows_score, \
    homogeneity_score, mutual_info_score, normalized_mutual_info_score, v_measure_score
from sklearn.metrics.cluster import contingency_matrix

from clustering.clusterings import clustering_args_functions
from abstraction.abstractions import get_abstraction_method
from data_extraction import read_data_values_from_file
from data_extraction.write_cluster_excel import cluster_to_excel
from distance.distances import distance_functions
from distance.costmap import get_cost_map, split_cost_map
from gui_center.main import Main
from gui_abstraction.abstraction_choices import abstraction_functions
from validation.external_validation import compare_true_and_pred_clusters, get_pred_clustering_of_true_values, \
    get_true_and_pred_clusters_parts, check_completeness_of_true_values, filter_clusters_true_fancy


def load_ExecutionConfiguration(filepath):
    text = open(filepath + ".json", "r")

    # translationfunction = \
    #     lambda dict: \
    #         ExecutionConfiguration(
    #             dict["data_path"],
    #             dict["compression_answers"],
    #             dict["distance_func"],
    #             dict["algorithm"],
    #             dict["algorithm_params"],
    #             get_cost_map(dict["costmap_case"], dict["costmap_regex"], dict["costmap_weights"])
    #         )

    data = json.load(text, object_hook=ExecutionConfiguration)
    return data
    # return json.loads(filepath + ".json")


def get_abstraction_answers(abstraction):
    for i, e in enumerate(abstraction_functions):
        if e[0] == abstraction:
            return e[1](None)[1]


def ExecutionConfigurationFromParams(data_path, lower_limit, upper_limit, abstraction, distance_func, algorithm,
                                     algorithm_params, costmap=None, clusters_true_fancy=None):
    if isinstance(abstraction, list):
        abstraction_answers = abstraction
        abstraction_function = ""
    elif isinstance(abstraction, str):
        abstraction_answers = get_abstraction_answers(abstraction)
        abstraction_function = abstraction
    else:
        pass

    if costmap is None:
        costmap_case, costmap_regex, costmap_weights = None, None, None
    else:
        costmap_case, costmap_regex, costmap_weights = split_cost_map(costmap)
        costmap_regex, costmap_weights = costmap_regex.tolist(), costmap_weights.tolist()

    dict = {
        "data_path": data_path,
        "data_name": re.sub("\..*", "", re.sub(".*/", "", data_path)),
        "lower_limit": lower_limit,
        "upper_limit": upper_limit,
        "abstraction_function": abstraction_function,
        "abstraction_answers": abstraction_answers,
        "distance_func": distance_func,
        "algorithm": algorithm,
        "algorithm_params": algorithm_params,
        "costmap_case": costmap_case,
        "costmap_regex": costmap_regex,
        "costmap_weights": costmap_weights,
        "clusters_true_fancy": clusters_true_fancy,
    }

    return ExecutionConfiguration(dict)


class ExecutionConfiguration(object):
    '''
    A class for executing data value clustering with a given configuration and saving both the configuration and results in JSON format.
    '''

    def __init__(self, dict):
        for key, value in dict.items():
            setattr(self, key, value)
        self.validate_params()

        if not hasattr(self, "target_file_name"):
            self.target_file_name = self.generate_filename()
        self.json_file_name = self.target_file_name + ".json"
        self.picture_file_name = self.target_file_name + ".png"
        self.excel_file_name = self.target_file_name + ".xlsx"

    def validate_params(self):
        for p in self.algorithm_params:
            assert len(p) == 2
            assert type(p[0]) is str, p[0]

    def __eq__(self, other):
        json_self = self.toJSON().replace(self.target_file_name, "")
        json_other = other.toJSON().replace(other.target_file_name, "")
        return json_self == json_other

    def get_abstraction(self):
        import abstraction.abstractions
        # return abstraction.get_compression_method(self.compression_answers), self.compression_answers
        return get_abstraction_method(self.abstraction_answers)

    def get_costmap(self):
        if self.costmap_case is None or self.costmap_regex is None or self.costmap_weights is None:
            return None
        return get_cost_map(self.costmap_case, self.costmap_regex, self.costmap_weights)

    def save(self, path):
        output_text = self.toJSON()

        f = open(path + self.json_file_name, "w")
        f.write(output_text)
        f.close()

    def toJSON(self):
        json_text = json.dumps(self, default=lambda o: o.__dict__)
        my_options = jsbeautifier.default_options()
        my_options.indent_size = 2
        json_text = jsbeautifier.beautify(json_text, my_options)
        return json_text

    def generate_filename(self):
        return self.data_name + "_" + str(self.lower_limit) + "_" + str(
            self.upper_limit) + "_" + self.algorithm + "_" + datetime.now().strftime("%Y%m%d-%H%M%S")

    def execute(self):
        # extract data
        data = read_data_values_from_file(self.data_path)[self.lower_limit:self.upper_limit]

        # get_abstraction
        abstraction_f = self.get_abstraction()

        # specify distance function
        distance_f = distance_functions[self.distance_func](self.get_costmap())

        # specify cluster function with parameters
        cluster_f = clustering_args_functions[self.algorithm](**self.params_to_dict())

        main = Main(data=data, abstraction_f=abstraction_f, distance_f=distance_f, cluster_f=cluster_f)

        # self.compressed_values = main.values_compressed.tolist()
        self.cluster_list = main.fancy_cluster_list
        self.noise = main.noise
        self.cluster_list_abstracted = main.fancy_cluster_list_abstracted
        self.noise_abstracted = main.noise_abstracted
        self.comp_to_normal_map = [list(elem) for elem in main.abstraction_dict.items()]
        self.cluster_sizes = main.cluster_sizes
        self.noise_size = main.noise_size
        self.cluster_sizes_abstracted = main.cluster_sizes_abstracted
        self.noise_size_abstracted = main.noise_size_abstracted
        self.amount_data = main.num_data
        self.amount_abstracted_data = main.num_abstracted_data
        self.abstraction_rate = main.abstraction_rate
        self.no_clusters = main.no_clusters
        self.no_noise = main.no_noise
        self.time_total = str(main.timedelta_total)
        self.time_abstraction = str(main.timedelta_abstraction)
        self.time_distance = str(main.timedelta_distance)
        self.time_cluster = str(main.timedelta_cluster)
        self.wb_index = main.wb_index
        self.calinski_harabasz_index = main.calinski_harabasz_index
        self.dunn_index = main.dunn_index
        self.intra_cluster_distances = main.intra_cluster_distances.tolist()
        self.average_intra_cluster_distances_per_cluster_per_value = main.average_intra_cluster_distances_per_cluster_per_value

        if not (self.clusters_true_fancy is None):
            self.external_validation(main.values_abstracted, main.clusters_abstracted, abstraction_f)

    def external_validation(self, values_abstracted, clusters_abstracted, abstraction_f):
        self.completeness, self.missing_values, self.superflous_values = check_completeness_of_true_values(
            abstraction_f, self.clusters_true_fancy, values_abstracted)

        clusters_true_fancy_filtered = filter_clusters_true_fancy(self.clusters_true_fancy, values_abstracted,
                                                                  abstraction_f)

        self.pred_clustering_of_true_values = get_pred_clustering_of_true_values(abstraction_f,
                                                                                 clusters_true_fancy_filtered,
                                                                                 values_abstracted, clusters_abstracted)

        clusters_true_part, clusters_pred_part = get_true_and_pred_clusters_parts(
            abstraction_f, values_abstracted, clusters_true_fancy_filtered, clusters_abstracted)
        self.clusters_true_part = clusters_true_part.tolist()
        self.clusters_pred_part = clusters_pred_part.tolist()

        self.adjusted_mutual_info_score = adjusted_mutual_info_score(self.clusters_true_part, self.clusters_pred_part)
        self.adjusted_rand_score = adjusted_rand_score(self.clusters_true_part, self.clusters_pred_part)
        self.completeness_score = completeness_score(self.clusters_true_part, self.clusters_pred_part)
        self.fowlkes_mallows_score = fowlkes_mallows_score(self.clusters_true_part, self.clusters_pred_part)
        self.homogeneity_score = homogeneity_score(self.clusters_true_part, self.clusters_pred_part)
        self.mutual_info_score = mutual_info_score(self.clusters_true_part, self.clusters_pred_part)
        self.normalized_mutual_info_score = normalized_mutual_info_score(self.clusters_true_part,
                                                                         self.clusters_pred_part)
        # self.rand_score = compare_true_and_pred_clusters(rand_score(clusters_true_part, self.clusters_pred_part)
        self.v_measure_score = v_measure_score(self.clusters_true_part, self.clusters_pred_part)

        self.contingency_matrix = contingency_matrix(self.clusters_true_part, self.clusters_pred_part).tolist()
        # # self.pair_confusion_matrix = compare_true_and_pred_clusters(pair_confusion_matrix, self.compressed_values,
        # #                                                          self.clusters_true_fancy,
        # #                                                          clusters_compressed)

        print("Clusters Filtered:", self.clusters_true_part)
        print("Clusters Expected:", self.clusters_pred_part)
        print("Completeness:", self.completeness)
        print("Missing Values:", self.missing_values)
        print("Superflous Values:", self.superflous_values)
        print("Scores:",
              self.adjusted_mutual_info_score, self.adjusted_rand_score,
              self.completeness_score, self.fowlkes_mallows_score,
              self.fowlkes_mallows_score, self.homogeneity_score,
              self.mutual_info_score, self.normalized_mutual_info_score
              )
        print("Contigency Matrix:")
        print(self.contingency_matrix)

    def params_to_dict(self):
        dict = {}
        for p in self.algorithm_params:
            dict[p[0]] = p[1]
        return dict

    def export_to_excel(self, path):
        assert (
                hasattr(self, 'excel_file_name')
            and hasattr(self, 'cluster_list')
            and hasattr(self, 'noise')
            and hasattr(self, 'cluster_list_abstracted')
            and hasattr(self, 'noise_abstracted')
            # and hasattr(self, 'comp_to_normal_map')
        )

        if not hasattr(self, 'comp_to_normal_map'):
            map = None
        else:
            map = dict([tuple(l) for l in self.comp_to_normal_map])

        cluster_to_excel(path + self.excel_file_name,
                         self.cluster_list,
                         self.noise,
                         self.cluster_list_abstracted,
                         self.noise_abstracted,
                         map,
                         self.average_intra_cluster_distances_per_cluster_per_value,
                         self.intra_cluster_distances)


if __name__ == '__main__':
    """SPECIFY PARAMETERS"""
    # data
    # target_file_name = "target_file_name"
    # abstraction
    abstraction_answers = [True, True, True, True, True, True, True, True, True, True, True, True, True, False, False,
                           False, False, False, True]
    # distance
    weight_case = 1
    regex = ["", "[a-zäöüßáàéèíìóòúù]", "[A-ZÄÖÜÁÀÉÈÍÌÓÒÚÙ]", "[0-9]", " ", "[^a-zäöüßáàéèíìóòúùA-ZÄÖÜÁÀÉÈÍÌÓÒÚÙ0-9 ]"]
    weights_dates = [
        [0, 2, 2, 1, 3, 3],
        [2, 0, 1, 3, 3, 3],
        [2, 1, 0, 3, 3, 3],
        [1, 3, 3, 0, 3, 3],
        [3, 3, 3, 3, 0, 3],
        [3, 3, 3, 3, 3, 3]
    ]
    costmap = get_cost_map(weight_case, regex, weights_dates)
    # clustering
    algorithm = "dbscan"
    # algorithm_params = {"eps": 3, "min_samples": 3, "n_jobs": None}
    algorithm_params = [["eps", 3], ["min_samples", 3], ["n_jobs", None]]

    """INITIALIZE"""
    object = ExecutionConfigurationFromParams("../data/midas_dates.txt", 0, 1000, abstraction_answers,
                                              "distance_weighted_levenshtein", algorithm, algorithm_params, costmap)

    """EXECUTE"""
    object.execute()

    """SAVE"""
    object.save("../data/")
    object.export_to_excel("../data/")

    """LOAD"""
    load = load_ExecutionConfiguration("../data/dbscan20210209-103005")
    load.execute()
    # print(object is load, object == load)
    # print(type(load), load)
