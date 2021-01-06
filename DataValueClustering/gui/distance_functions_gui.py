import numpy as np

from distance.dice_coefficient import dice_coefficient_distance
from distance.levenshtein_distance import levenshtein_distance
from distance.longest_common_subsequence_distance import longest_common_subsequence_distance
from distance.weighted_levenshtein_distance import weighted_levenshtein_distance, suggest_cost_map


# pass method of this module as distance_function to clustering.clustering.cluster


def distance_dice():
    return dice_coefficient_distance


def distance_levenshtein():
    return levenshtein_distance


def distance_longest_common_subsequence():
    return longest_common_subsequence_distance


def distance_weighted_levenshtein():
    # TODO: let user choose one of cost_maps and execute function
    cost_map = None

    return lambda s1, s2: weighted_levenshtein_distance(cost_map, s1, s2)


def automatic():
    # TODO: ask user questions about the data

    return suggest_cost_map  # TODO: add arguments


def custom_full():
    # TODO: let user specify compression
    pass


cost_maps = np.array([
    ["Automatic",
     automatic],
    # TODO: add predefined cost maps
    ["Custom Full",
     custom_full]
])


distance_functions = np.array([
    ["Dice",
     distance_dice],
    ["Levenshtein",
     distance_levenshtein],
    ["Longest Common Subsequence",
     distance_longest_common_subsequence],
    ["Weighted Levenshtein",
     distance_weighted_levenshtein]
])
