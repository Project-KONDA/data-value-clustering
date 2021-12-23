import datetime
import json
import os
import time
from pathlib import Path

from gui_center.hub_configuration import object_to_json


def append_log(configuration, is_refined_clustering, restricted):
    dir_path = str(Path(__file__).parent.parent) + "/log"
    Path(dir_path).mkdir(exist_ok=True)
    os.chdir(dir_path)
    file_path = dir_path + "\\log.log"
    tiny_json = configuration.get_as_json_tiny()

    json_dict = json.loads(tiny_json)

    del json_dict["data"]
    del json_dict["data_lower_limit"]
    del json_dict["data_upper_limit"]
    del json_dict["num_data"]

    del json_dict["values_abstracted"]
    del json_dict["no_values_abstracted"]
    del json_dict["abstraction_dict"]
    del json_dict["num_abstracted_data"]
    del json_dict["abstraction_rate"]
    del json_dict["timedelta_abstraction"]
    del json_dict["blob_configuration"]

    del json_dict["distance_matrix_map"]
    del json_dict["timedelta_distance"]

    del json_dict["clusters_abstracted"]
    del json_dict["clusters"]
    del json_dict["cluster_sizes"]
    del json_dict["noise_size"]
    del json_dict["cluster_sizes_abstracted"]
    del json_dict["noise_size_abstracted"]
    del json_dict["fancy_cluster_list"]
    del json_dict["fancy_simple_cluster_list"]
    del json_dict["noise"]
    del json_dict["noise_abstracted"]
    del json_dict["no_clusters"]
    del json_dict["no_noise"]
    del json_dict["timedelta_cluster"]
    del json_dict["json_save_path"]
    del json_dict["json_saved"]
    del json_dict["excel_saved"]
    del json_dict["excel_simple_saved"]
    del json_dict["timedelta_total"]
    del json_dict["validation_answer_1"]
    del json_dict["validation_answer_2"]
    del json_dict["validation_answer_3"]
    del json_dict["validation_answer_4"]

    if is_refined_clustering:
        del json_dict["excel_simple_save_path"]
    else:
        del json_dict["cost_map"]
        del json_dict["excel_save_path"]
        del json_dict["fancy_cluster_list_abstracted"]
        del json_dict["distance_config_method"]
        del json_dict["clustering_expert_mode"]
        del json_dict["clustering_algorithm"]
        del json_dict["clustering_parameters"]

    if restricted:
        del json_dict["abstraction_answers"]

        if is_refined_clustering:
            del json_dict["distance_config_method"]
            del json_dict["clustering_expert_mode"]
            del json_dict["clustering_algorithm"]
            json_dict["rgx"] = json_dict["cost_map"]["rgx"]
            json_dict["w"] = json_dict["cost_map"]["w"][0]
            del json_dict["cost_map"]
            json_dict["n_clusters"] = json_dict["clustering_parameters"]["n_clusters"]
            del json_dict["clustering_parameters"]

    json_string = object_to_json(json_dict)

    f = open(file_path, mode="a", encoding='UTF-8')
    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    type = "Refined Clustering" if is_refined_clustering else "Simple Clustering"
    text = "{\n" + "\"timestamp\": \"" + timestamp + "\",\n" + "\"type\": \"" + type + "\",\n" + "\"configuration\":\n" + json_string + "\n},\n"
    f.write(text)
    f.close()
