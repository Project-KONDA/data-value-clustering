import numpy as np

from distance.dice_coefficient import dice_coefficient_distance
from distance.levenshtein_distance import levenshtein_distance
from distance.longest_common_subsequence_distance import longest_common_subsequence_distance
from distance.weighted_levenshtein_distance import weighted_levenshtein_distance, suggest_cost_map

# pass method of this module as distance_function to clustering.clustering.cluster
from gui.DropdownInput import DropdownInput, input_dropdown
from gui_distances.BlobInput import BlobInput, input_blobs
from gui_distances.CostMatrixInput import CostMatrixInput, input_costmatrix


def distance_dice():
    return dice_coefficient_distance


def distance_levenshtein():
    return levenshtein_distance


def distance_longest_common_subsequence():
    return longest_common_subsequence_distance


def distance_weighted_levenshtein():
    # TODO: let user choose one of cost_maps and execute function

    titlex = "Choose a Cost Map"
    labelsx = ["Cost Map"]

    # TODO4
    num = 5
    config = None

    optionsx = np.array([
        ["Costmatrix",
         lambda: input_costmatrix(num)],
        ["Costmatrix Empty",
         lambda: input_costmatrix(num, empty=True)],
        ["BlobInput",
         lambda: input_blobs(config)],
    ])

    myDropdown = DropdownInput(titlex, list(labelsx), list([optionsx[:, 0]]))
    answer, index = myDropdown.get()

    cost_map = optionsx[index[0], 1]()

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
    ["Weighted Levenshtein",
     distance_weighted_levenshtein],
    ["Levenshtein",
     distance_levenshtein],
    ["Longest Common Subsequence",
     distance_longest_common_subsequence],
    ["Dice",
     distance_dice],
])

if __name__ == "__main__":
    print(distance_weighted_levenshtein())
