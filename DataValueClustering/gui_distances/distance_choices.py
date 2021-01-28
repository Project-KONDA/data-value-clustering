import numpy as np

from gui_distances.distance_functions_gui import distance_weighted_levenshtein, distance_levenshtein, \
    distance_longest_common_subsequence, distance_dice

distance_functions = np.array([
    ["Weighted Levenshtein",
     distance_weighted_levenshtein],
    ["Levenshtein",
     lambda blob_configuration: (distance_levenshtein(), blob_configuration)],
    ["Longest Common Subsequence",
     lambda blob_configuration: (distance_longest_common_subsequence(), blob_configuration)],
    ["Dice",
     lambda blob_configuration: (distance_dice(), blob_configuration)],
])