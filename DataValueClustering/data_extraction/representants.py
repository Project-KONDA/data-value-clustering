'''Get original values as representatives for abstracted data values.'''
import numpy as np


def get_repr_cluster(clusters_compressed, comp_to_normal_map):
    print(clusters_compressed)
    print(type(clusters_compressed))
    clusters2 = clusters_compressed
    for i, cluster in enumerate(clusters2):
        clusters2[i] = get_repr_list(cluster, comp_to_normal_map)
    return clusters2


def get_repr_list(values_compressed, comp_to_normal_map):
    result = []
    for i in values_compressed:
        result.append(get_repr(i, comp_to_normal_map))
    return result


def get_repr(value_compressed, comp_to_normal_map):
    try:
        all_values = comp_to_normal_map[value_compressed]
        distinct_values = list(set(all_values))
        distinct_values = sorted(distinct_values, key=lambda k: all_values.count(k), reverse=True)
        return distinct_values[0]
    except:
        return ""


if __name__ == '__main__':
    clusters = np.array([["1", "2", "3"], ["3", "4", "5"]])
    map = {"1": ["a", "b"], "2": ["c", "d"], "3": ["e", "f"], "4": ["g", "h"], "5": ["i", "j"]}
    print(get_repr_cluster(clusters, map))
