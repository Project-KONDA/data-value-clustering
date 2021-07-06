'''Read individual information from JSON file containing configuration and results.'''
from export.ExecutionConfiguration import load_ExecutionConfiguration
from gui_center.cluster_representation import fancy_cluster_representation_reverse


def read_clusters_compressed(path, values):
    exe = load_ExecutionConfiguration(path)
    fancy = exe.cluster_list_compressed
    return fancy_cluster_representation_reverse(values, fancy)