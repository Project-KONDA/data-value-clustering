from gui.cluster_algorithms_gui import cluster_algorithms
from gui.compression_functions_gui import compression_functions
from gui.distance_functions_gui import distance_functions
from data_extraction.read_file import get_sources_in_experiment_data_directory


class Main:

    def __init__(self):

        self.l_data = get_sources_in_experiment_data_directory()
        self.l_compressions = compression_functions
        self.l_distances = distance_functions
        self.l_clusters = cluster_algorithms



