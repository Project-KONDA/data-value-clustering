from distance.weighted_levenshtein_distance import get_cost_map
from gui_center.hub_configuration import HubConfiguration


if __name__ == "__main__":
    hub_config = HubConfiguration()

    abstraction_answers = [False, False, False, False, False, False, False, False, False,
                           True, True, True,
                           False, False, False, False, False, False,
                           True]

    weight_case = 1
    regex = ["", "0123456789", "abcdefghijklmnopqrstuvwxyzäöüßáàéèíìóòúùABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜÁÀÉÈÍÌÓÒÚÙ", "<rest>"]
    weights = [
        [0, 2, 1, 2],  #
        [2, 0, 3, 4],  # 1
        [1, 3, 1, 3],  # aA
        [2, 4, 3, 2],  # <rest>
    ]

    costmap = get_cost_map(weight_case, regex, weights)

    algorithm = "Hierarchical"
    algorithm_params = {'method': 'complete', 'n_clusters': None, 'distance_threshold': 3.5,
                        'criterion': 'distance'}

    hub_config.set_data_configuration("../data/xlido_measurement_unit.txt", 0, 1000)
    hub_config.set_abstraction_configuration(abstraction_answers)
    hub_config.set_distance_configuration(costmap)
    hub_config.set_clustering_selection(algorithm)
    hub_config.set_clustering_configuration(algorithm_params)

    hub_config.execute_data()
    hub_config.execute_abstraction()
    hub_config.execute_distance()
    hub_config.execute_clustering()

    print(hub_config.fancy_cluster_list)