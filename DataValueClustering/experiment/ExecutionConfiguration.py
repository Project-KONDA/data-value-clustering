import json
import re
from datetime import datetime

import jsbeautifier

from compression.compression import get_compression_method
from distance.weighted_levenshtein_distance import get_cost_map, split_cost_map


def load_ExecutionConfiguration(filepath):
    text = open(filepath + ".json", "r")

    translationfunction = \
        lambda dict: \
            ExecutionConfiguration(
                dict["data_path"],
                dict["compression_answers"],
                get_cost_map(dict["costmap_case"], dict["costmap_regex"], dict["costmap_weights"]),
                dict["algorithm"],
                dict["algorithm_params"]
            )

    data = json.load(text, object_hook=translationfunction)
    return data
    # return json.loads(filepath + ".json")


class ExecutionConfiguration(object):

    def __init__(self, data_path, compression_answers, costmap, algorithm, algorithm_params):
        self.data_path = data_path
        self.data_name = re.sub(".*/", "", data_path)

        self.compression_answers = compression_answers
        self.costmap_case, self.costmap_regex, self.costmap_weights = split_cost_map(costmap)

        self.algorithm = algorithm

        self.algorithm_params = algorithm_params

        self.target_file_name = self.generate_filename()
        self.json_file_name = target_file_name + ".json"
        self.picture_file_name = target_file_name + ".png"

    def __eq__(self, other):
        json_self = self.toJSON().replace(self.target_file_name, "")
        json_other = other.toJSON().replace(other.target_file_name, "")
        return json_self == json_other

    def get_compression(self):
        import compression.compression
        # return compression.get_compression_method(self.compression_answers), self.compression_answers
        return get_compression_method(self.compression_answers), self.compression_answers

    def get_costmap(self):
        get_cost_map(self.costmap_weights, self.costmap_case, self.costmap_regex)

    def save(self):
        output_text = self.toJSON()

        f = open(self.json_file_name, "w")
        f.write(output_text)
        f.close()

    def toJSON(self):
        json_text = json.dumps(self, default=lambda o: o.__dict__)
        my_options = jsbeautifier.default_options()
        my_options.indent_size = 2
        json_text = jsbeautifier.beautify(json_text, my_options)
        return json_text

    def generate_filename(self):
        return self.algorithm + str(datetime.now())


    def execute(self):
        pass


if __name__ == '__main__':

    """SPECIFY PARAMETERS"""
    # data
    target_file_name = "target_file_name"
    # compression
    compression_answers = [True, True, True, True, True, True, True, True, True, True, True, True, True, False, False, False, False, False, True]
    #distance
    costmap = get_cost_map()
    # clustering
    algorithm = "algorithm"
    algorithm_params = "algorithm_params"

    """INITIALIZE"""
    object = ExecutionConfiguration("data_file", compression_answers, costmap, algorithm, algorithm_params)

    """EXECUTE"""
    object.execute()

    """SAVE"""
    object.save()

    """LOAD"""
    load = load_ExecutionConfiguration(target_file_name)
    print(object is load, object == load)
    print(type(load), load)
