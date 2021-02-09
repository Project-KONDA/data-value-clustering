import json
import re
from datetime import datetime

import jsbeautifier

from clustering.clustering import clustering_args_functions
from compression.compression import get_compression_method
from data_extraction import read_data_values_from_file
from distance.distance import distance_functions
from distance.weighted_levenshtein_distance import get_cost_map, split_cost_map
from gui_center.main import Main


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


def ExecutionConfigurationFromParams(data_path, compression_answers, distance_func, algorithm, algorithm_params, costmap=None):

    if costmap is None:
        costmap_case, costmap_regex, costmap_weights = None, None, None
    else:
        costmap_case, costmap_regex, costmap_weights = split_cost_map(costmap)

    dict = {
        "data_path": data_path,
        "data_name": re.sub("\..*", "", re.sub(".*/", "", data_path)),
        "compression_answers": compression_answers,
        "distance_func": distance_func,
        "algorithm": algorithm,
        "algorithm_params": algorithm_params,
        "costmap_case": costmap_case,
        "costmap_regex": costmap_regex,
        "costmap_weights": costmap_weights,
    }

    return ExecutionConfiguration(dict)


class ExecutionConfiguration(object):

    def __init__(self, dict):
        for key, value in dict.items():
            setattr(self, key, value)
        self.validate_params()

        if not hasattr(self, "target_file_name"):
            self.target_file_name = self.generate_filename()
            self.json_file_name = self.target_file_name + ".json"
            self.picture_file_name = self.target_file_name + ".png"

    def validate_params(self):
        for p in self.algorithm_params:
            assert len(p) == 2
            assert type(p[0]) is str, p[0]

    def __eq__(self, other):
        json_self = self.toJSON().replace(self.target_file_name, "")
        json_other = other.toJSON().replace(other.target_file_name, "")
        return json_self == json_other

    def get_compression(self):
        import compression.compression
        # return compression.get_compression_method(self.compression_answers), self.compression_answers
        return get_compression_method(self.compression_answers)

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
        return self.data_name + "_" + self.algorithm + "_" + datetime.now().strftime("%Y%m%d-%H%M%S")

    def execute(self):
        # extract data
        data = read_data_values_from_file(self.data_path)[0:1000]

        # get_compression
        compression_f = self.get_compression()

        # specify distance function
        distance_f = distance_functions[self.distance_func](self.get_costmap())

        # specify cluster function with parameters
        cluster_f = clustering_args_functions[self.algorithm](**self.params_to_dict())

        main = Main(data=data, compression_f=compression_f, distance_f=distance_f, cluster_f=cluster_f)

        # TODO: save result

        self.cluster_list = main.fancy_cluster_list
        self.noise = main.noise
        self.time_total = str(main.timedelta_total)
        self.time_distance = str(main.timedelta_distance)
        self.time_cluster = str(main.timedelta_cluster)

    def params_to_dict(self):
        dict = {}
        for p in self.algorithm_params:
            dict[p[0]] = p[1]
        return dict

if __name__ == '__main__':

    """SPECIFY PARAMETERS"""
    # data
    target_file_name = "target_file_name"
    # compression
    compression_answers = [True, True, True, True, True, True, True, True, True, True, True, True, True, False, False, False, False, False, True]
    #distance
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
    object = ExecutionConfigurationFromParams("../data/midas_dates.txt", compression_answers, "distance_weighted_levenshtein", algorithm, algorithm_params, costmap)

    """EXECUTE"""
    object.execute()

    """SAVE"""
    object.save()

    """LOAD"""
    # load = load_ExecutionConfiguration(target_file_name)
    # print(object is load, object == load)
    # print(type(load), load)
