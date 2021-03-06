'''collection of measure functions between string values and small interface for choice'''
import numpy as np

from distance.dice_coefficient import dice_coefficient_distance
from distance.levenshtein_distance import levenshtein_distance
from distance.longest_common_subsequence_distance import longest_common_subsequence_distance
from distance.weighted_levenshtein_distance import weighted_levenshtein_distance, get_weighted_levenshtein_distance
from distance.costmap import suggest_cost_map

# pass method of this module as distance_function to clustering.clustering.cluster
from gui_general.DropdownInput import DropdownInput
from gui_distances import input_blobs, input_costmap


def distance_dice():
    return dice_coefficient_distance


def distance_levenshtein():
    return levenshtein_distance


def distance_longest_common_subsequence():
    return longest_common_subsequence_distance


def distance_weighted_levenshtein(blob_configuration, costmap=None):
    assert blob_configuration is not None
    # TODO: let user choose one of cost_maps and execute function

    titlex = "Choose a Cost Map"
    labelsx = ["Cost Map"]

    # TODO4
    num = 5

    optionsx = np.array([
        ["BlobInput",
         lambda: input_blobs(blob_configuration)],
        ["Costmap Prefilled",
         lambda: (
             input_costmap(regexes=blob_configuration[:, 1], costmap=costmap),
             blob_configuration)],
        ["Costmap",
         lambda: (input_costmap(size=len(blob_configuration[:, 1]), regexes=blob_configuration[:, 1]),
                  blob_configuration)],
        ["Costmap Empty",
         lambda: (
             input_costmap(size=len(blob_configuration), empty=True),
             blob_configuration)],
    ])

    myDropdown = DropdownInput(titlex, list(labelsx), list([optionsx[:, 0]]))
    answer, index = myDropdown.get()

    cost_map, new_blob_configuration = optionsx[index[0], 1]()

    if cost_map is None:
        quit()

    return get_weighted_levenshtein_distance(cost_map), new_blob_configuration


def automatic():
    # TODO: ask user questions about the data

    return suggest_cost_map  # TODO: add arguments


def custom_full():
    # TODO: let user specify abstraction
    pass


cost_maps = np.array([
    ["Automatic",
     automatic],
    # TODO: add predefined cost maps
    ["Custom Full",
     custom_full]
])

if __name__ == "__main__":
    print(distance_weighted_levenshtein())
