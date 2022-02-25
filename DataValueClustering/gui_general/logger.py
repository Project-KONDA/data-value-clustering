import datetime
import json
import os
import time
from pathlib import Path

from gui_center.hub_configuration import object_to_json


def append_log_clustering(configuration, is_refined_clustering, restricted):
    dir_path = str(Path(__file__).parent.parent) + "/log"
    Path(dir_path).mkdir(exist_ok=True)
    os.chdir(dir_path)
    file_path = dir_path + "\\log.log"
    tiny_json = configuration.get_as_json_tiny()

    json_dict = json.loads(tiny_json)

    new_json_dict = dict()

    new_json_dict["data_path"] = json_dict["data_path"]

    if is_refined_clustering:
        new_json_dict["excel_save_path"] = json_dict["excel_save_path"]
        new_json_dict["fancy_cluster_list_abstracted"] = json_dict["fancy_cluster_list_abstracted"]
    else:
        new_json_dict["excel_simple_save_path"] = json_dict["excel_simple_save_path"]

    if restricted:
        if is_refined_clustering:
            new_json_dict["rgx"] = json_dict["cost_map"]["rgx"]
            new_json_dict["w"] = json_dict["cost_map"]["w"][0]
            new_json_dict["n_clusters"] = json_dict["clustering_parameters"]["n_clusters"]
    else:
        new_json_dict["abstraction_answers"] = json_dict["abstraction_answers"]
        if is_refined_clustering:
            new_json_dict["distance_config_method"] = json_dict["distance_config_method"]
            new_json_dict["cost_map"] = json_dict["cost_map"]
            new_json_dict["clustering_default_mode"] = json_dict["clustering_default_mode"]
            new_json_dict["clustering_algorithm"] = json_dict["clustering_algorithm"]
            new_json_dict["clustering_parameters"] = json_dict["clustering_parameters"]

    json_string = object_to_json(new_json_dict)

    f = open(file_path, mode="a", encoding='UTF-8')
    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    type = "Refined Clustering" if is_refined_clustering else "Simple Clustering"
    text = "{\n" + "\"timestamp\": \"" + timestamp + "\",\n" + "\"type\": \"" + type + "\",\n" + "\"configuration\":\n" + json_string + "\n},\n"
    f.write(text)
    f.close()


def append_log_evaluation(configuration):
    dir_path = str(Path(__file__).parent.parent) + "/log"
    Path(dir_path).mkdir(exist_ok=True)
    os.chdir(dir_path)
    file_path = dir_path + "\\log.log"
    tiny_json = configuration.get_as_json_tiny()

    json_dict = json.loads(tiny_json)

    evaluation_json_dict = dict()
    evaluation_json_dict["validation_answer_1"] = json_dict["validation_answer_1"]
    evaluation_json_dict["validation_answer_2"] = json_dict["validation_answer_2"]
    evaluation_json_dict["validation_answer_3"] = json_dict["validation_answer_3"]
    evaluation_json_dict["validation_answer_4"] = json_dict["validation_answer_4"]

    json_string = object_to_json(evaluation_json_dict)

    f = open(file_path, mode="a", encoding='UTF-8')
    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    type = "Evaluation"
    text = "{\n" + "\"timestamp\": \"" + timestamp + "\",\n" + "\"type\": \"" + type + "\",\n" + "\"configuration\":\n" + json_string + "\n},\n"
    f.write(text)
    f.close()

