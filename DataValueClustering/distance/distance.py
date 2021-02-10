from distance import levenshtein_distance, longest_common_subsequence_distance, dice_coefficient_distance, \
    weighted_levenshtein_distance

distance_functions = {
    "distance_weighted_levenshtein":
        get_weighted_levenshtein_distance,
        # lambda cost_map: lambda s1, s2: weighted_levenshtein_distance(cost_map, s1, s2),
    "distance_levenshtein": lambda cost_map: lambda s1, s2: levenshtein_distance(s1, s2),
    "longest_common_subsequence_distance": lambda cost_map: lambda s1, s2: longest_common_subsequence_distance(s1, s2),
    "dice_coefficient_distance": lambda cost_map: lambda s1, s2: dice_coefficient_distance(s1, s2),
}