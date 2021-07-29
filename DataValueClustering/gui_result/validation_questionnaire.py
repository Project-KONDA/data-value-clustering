from enum import Enum

import numpy as np

from clustering.affinity_propagation_clustering import DAMPING, PREFERENCE
from clustering.dbscan_clustering import EPS, MIN_SAMPLES
from clustering.hierarchical_clustering import THRESHOLD, N_CLUSTERS, METHOD
from clustering.optics_clustering import MAX_EPS, MIN_CLUSTER_SIZE
from gui_cluster_selection.algorithm_selection import HIERARCHICAL, OPTICS, DBSCAN, K_MEDOIDS, SPECTRAL_CLUSTERING, \
    AFFINITY_PROPAGATION


class ValidationAnswer(str, Enum):
    HAPPY = 'HAPPY'
    UNHAPPY = 'UNHAPPY'
    MORE = 'MORE'
    LESS = 'LESS'

# TODO: complete answers
question_1_answers = np.array([[ValidationAnswer.HAPPY, "I'm happy", "happy tip"],
                               [ValidationAnswer.UNHAPPY,
                                "I’m not happy, a lot of values that seem pretty similar are in "
                                "different clusters and a lot of values that seem pretty "
                                "dissimilar are in the same cluster", "unhappy tip"]], dtype=object)
question_2_answers = np.array([[ValidationAnswer.HAPPY, "I'm happy", "happy tip"],
                               [ValidationAnswer.MORE, "More noise please", "more tip"],
                               [ValidationAnswer.LESS, "Less noise please", "less tip"]], dtype=object)
question_3_answers = np.array([[ValidationAnswer.HAPPY, "I'm happy", "happy tip"],
                               [ValidationAnswer.MORE, "More clusters please", "more tip"],
                               [ValidationAnswer.LESS, "Less clusters please", "less tip"]], dtype=object)
question_4_answers = np.array([[ValidationAnswer.HAPPY, "I'm happy", "happy tip", False],
                               [ValidationAnswer.UNHAPPY, "I'm unhappy, the following clusters are too heterogeneous:",
                                "unhappy tip", True]], dtype=object)


def get_suggested_data(validation_answers):
    suggested_data_names = None
    if validation_answers[3] is not None and validation_answers[3][1] is not None:
        print(validation_answers)
        suggested_data_names = validation_answers[3][1]
    return suggested_data_names if suggested_data_names is None or len(suggested_data_names) > 0 else None


def get_suggested_abstraction_modifications(validation_answers, configuration):
    abstraction_advice = ""
    if validation_answers[0] is not None and validation_answers[0] == ValidationAnswer.UNHAPPY:
        abstraction_advice += "\nFirst, check your configuration concerning an erroneous abstraction of aspects that actually cause significant dissimilarity of data values. " \
                              "For this, please reconsider the checked questions." \
                              "\nFurther, check that all details that do not cause significant dissimilarity of data values are abstracted from. " \
                              "For this, please reconsider the unchecked questions."
    if validation_answers[2] is not None and validation_answers[2] == ValidationAnswer.MORE:
        if configuration.get_clustering_selection[0] == HIERARCHICAL or configuration.get_clustering_selection[0] == K_MEDOIDS and configuration.cluster_no == configuration.no_values_abstracted:
            abstraction_advice += "\nUse a lower-level abstraction, i.e. uncheck some checked answers."
        else:
            abstraction_advice += "\nYou might want to consider using a lower-level abstraction, i.e. unchecking some checked answers."
    if validation_answers[2] is not None and validation_answers[2] == ValidationAnswer.LESS:
        abstraction_advice += "\nYou might want to consider using a higher abstraction level, i.e. checking some unchecked answers."
    return abstraction_advice if abstraction_advice != "" else None


def get_suggested_distance_modifications(validation_answers, configuration):
    distance_advice = ""
    if validation_answers[0] is not None and validation_answers[0] == ValidationAnswer.UNHAPPY:
        distance_advice += "\nEnsure that you specify higher weights for aspects that cause more dissimilarity."
    if validation_answers[2] is not None and validation_answers[2] == ValidationAnswer.MORE:
        # TODO: check calculated distances concerning lack of diversity!?
        distance_advice += "\nYou might want to consider choosing more diverse weights, i.e. emphasise character groups that you do not expect or that alter the values’ meaning significantly."
    return distance_advice if distance_advice != "" else None


def get_suggested_algorithms(validation_answers):
    suggested_algorithms = list()
    if validation_answers[1] is not None and validation_answers[1] == ValidationAnswer.MORE:
        suggested_algorithms.append(DBSCAN)
        suggested_algorithms.append(OPTICS)
    elif validation_answers[1] is not None and validation_answers[1] == ValidationAnswer.LESS:
        suggested_algorithms.append(HIERARCHICAL)
        suggested_algorithms.append(K_MEDOIDS)
        suggested_algorithms.append(SPECTRAL_CLUSTERING)
        suggested_algorithms.append(AFFINITY_PROPAGATION)
    elif validation_answers[0] is not None and validation_answers[0] == ValidationAnswer.UNHAPPY:
        suggested_algorithms.append(HIERARCHICAL)
        suggested_algorithms.append(OPTICS)
    return suggested_algorithms


def get_suggested_parameter_modifications(validation_answers, configuration):
    parameter_modifications = {}
    if validation_answers[0] is not None and validation_answers[0] == ValidationAnswer.UNHAPPY:
        if configuration.get_clustering_selection[0] == HIERARCHICAL:
            parameter_modifications[METHOD] = ('single', 'average', 'centroid')
    if validation_answers[1] is not None and validation_answers[1] == ValidationAnswer.MORE:
        if configuration.get_clustering_selection[0] == DBSCAN:
            parameter_modifications[EPS] = '-'
            parameter_modifications[MIN_SAMPLES] = '+'
        if configuration.get_clustering_selection[0] == OPTICS:
            parameter_modifications[MIN_SAMPLES] = '+'
            parameter_modifications[MAX_EPS] = '-'
            parameter_modifications[EPS] = '-'
            parameter_modifications[MIN_CLUSTER_SIZE] = '+'
    if validation_answers[1] is not None and validation_answers[1] == ValidationAnswer.LESS:
        if configuration.get_clustering_selection[0] == DBSCAN:
            parameter_modifications[EPS] = '+'
            parameter_modifications[MIN_SAMPLES] = '-'
        if configuration.get_clustering_selection[0] == OPTICS:
            parameter_modifications[MIN_SAMPLES] = '-'
            parameter_modifications[MAX_EPS] = '+'
            parameter_modifications[EPS] = '+'
            parameter_modifications[MIN_CLUSTER_SIZE] = '-'
    if validation_answers[2] is not None and validation_answers[2] == ValidationAnswer.MORE:
        if configuration.get_clustering_selection[0] == HIERARCHICAL:
            parameter_modifications[N_CLUSTERS] = '+'
            parameter_modifications[THRESHOLD] = '-'
        if configuration.get_clustering_selection[0] == K_MEDOIDS:
            parameter_modifications[N_CLUSTERS] = '+'
        if configuration.get_clustering_selection[0] == DBSCAN:
            parameter_modifications[EPS] = '-'
            parameter_modifications[MIN_SAMPLES] = '-'
        if configuration.get_clustering_selection[0] == OPTICS:
            parameter_modifications[MIN_SAMPLES] = '-'
            parameter_modifications[MAX_EPS] = '-'
            parameter_modifications[EPS] = '-'
            parameter_modifications[MIN_CLUSTER_SIZE] = '-'
        if configuration.get_clustering_selection[0] == SPECTRAL_CLUSTERING:
            parameter_modifications[N_CLUSTERS] = '+'
        if configuration.get_clustering_selection[0] == AFFINITY_PROPAGATION:
            parameter_modifications[DAMPING] = '-'
            parameter_modifications[PREFERENCE] = '+'
    if validation_answers[2] is not None and validation_answers[2] == ValidationAnswer.LESS:
        if configuration.get_clustering_selection[0] == HIERARCHICAL:
            parameter_modifications[N_CLUSTERS] = '-'
            parameter_modifications[THRESHOLD] = '+'
        if configuration.get_clustering_selection[0] == K_MEDOIDS:
            parameter_modifications[N_CLUSTERS] = '-'
        if configuration.get_clustering_selection[0] == DBSCAN:
            parameter_modifications[EPS] = '+'
            parameter_modifications[MIN_SAMPLES] = '+'
        if configuration.get_clustering_selection[0] == OPTICS:
            parameter_modifications[MIN_SAMPLES] = '+'
            parameter_modifications[MAX_EPS] = '+'
            parameter_modifications[EPS] = '+'
            parameter_modifications[MIN_CLUSTER_SIZE] = '+'
        if configuration.get_clustering_selection[0] == SPECTRAL_CLUSTERING:
            parameter_modifications[N_CLUSTERS] = '-'
        if configuration.get_clustering_selection[0] == AFFINITY_PROPAGATION:
            parameter_modifications[DAMPING] = '+'
            parameter_modifications[PREFERENCE] = '-'
    return parameter_modifications if parameter_modifications != {} else None




