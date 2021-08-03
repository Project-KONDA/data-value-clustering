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


question_1 = np.array(["How do you feel about the meaningfulness of the clustering concerning the grouping of similar values in the same cluster?",
                      "Reflect upon the aspects on which the partitioning is oriented, the aspects that do not influence the partitioning and whether the partitioning is useful and provides an overview of the different values. "
                      "The colors in the MDS Scatter plot being very mixed may indicate a lack of meaningful grouping."])
question_1_answers = np.array([[ValidationAnswer.HAPPY, "I'm happy", "Choose this of the clustering seems meaningful, similar values are in the same clusters and dissimilar values in different clusters."],
                               [ValidationAnswer.UNHAPPY,
                                "I’m not happy, a lot of values that seem pretty similar are in "
                                "different clusters and a lot of values that seem pretty "
                                "dissimilar are in the same cluster", "Choose this if you are unhappy with the aspects on which the grouping is oriented."]], dtype=object)
question_2 = np.array(["How do you feel about the number of noisy values?",
                      "Inspect the noisy values. Typically they should make up a relatively small part of all values. They should be outliers that are very different from all other values."])
question_2_answers = np.array([[ValidationAnswer.HAPPY, "I'm happy", "Choose this if the number of noisy values seems appropriate."],
                               [ValidationAnswer.MORE, "More noise please", "Choose this if a lot of values within clusters seem extremely different from all other values."],
                               [ValidationAnswer.LESS, "Less noise please", "Choose this if a lot of noisy values do not seem extremely different from the other values."]], dtype=object)
question_3 = np.array(["How do you feel about the overall level of detail of the clustering?",
                      "Reflect upon whether the clustering helps you in getting an overview of the different kinds of data values and whether a more or less finge-grained partitioning would be more helpful."])
question_3_answers = np.array([[ValidationAnswer.HAPPY, "I'm happy", "Choose this if you are happy with the level of detail, i.e. number of clusters, in general."],
                               [ValidationAnswer.MORE, "More clusters please", "Choose this if in general the level of detail of the clustering is too low and you want a more fine grained partitioning."],
                               [ValidationAnswer.LESS, "Less clusters please", "Choose this if in general the level of detail of the clustering is too high and you want a less fine grained partitioning."]], dtype=object)
question_4 = np.array(["Do you consider individual clusters too heterogeneous (i.e., level of detail too low) while the others are fine?",
                      "Inspect whether individual clusters contain a lot of extremely heterogeneous values, that you would like to get an overview of. "
                      "In the third sheet of the Excel file, check clusters with extremely high variance containing a lot of values."])
question_4_answers = np.array([[ValidationAnswer.HAPPY, "I'm happy", "Choose this if all clusters seem to be at a similar level of abstraction.", False],
                               [ValidationAnswer.UNHAPPY, "I'm unhappy, the following clusters are too heterogeneous:",
                                "Choose this if most clusters seem at an appropriate level of abstraction but one or few clusters seem to contain extremely heterogeneous values that you would like to partition further.", True]], dtype=object)


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
        if configuration.get_clustering_selection()[0] == HIERARCHICAL or configuration.get_clustering_selection()[0] == K_MEDOIDS and configuration.cluster_no == configuration.no_values_abstracted:
            abstraction_advice = "\nUse a lower-level abstraction, i.e. uncheck some checked answers."
        else:
            abstraction_advice += "\nYou might want to consider using a lower-level abstraction, i.e. unchecking some checked answers."
    if validation_answers[2] is not None and validation_answers[2] == ValidationAnswer.LESS:
        abstraction_advice += "\nYou might want to consider using a higher abstraction level, i.e. checking some unchecked answers."
    return abstraction_advice if abstraction_advice != "" else None


def get_suggested_distance_modifications(validation_answers, configuration):
    distance_advice = ""
    if validation_answers[0] is not None and validation_answers[0] == ValidationAnswer.UNHAPPY:
        distance_advice += "Ensure that you specify higher weights for aspects that cause more dissimilarity."
    if validation_answers[2] is not None and validation_answers[2] == ValidationAnswer.MORE:
        # TODO: check calculated distances concerning lack of diversity!?
        if distance_advice != "":
            distance_advice += " "
        distance_advice += "You might want to consider choosing more diverse weights, i.e. emphasise character groups that you do not expect or that alter the values’ meaning significantly."
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
        if configuration.get_clustering_selection()[0] == HIERARCHICAL:
            parameter_modifications[METHOD] = ('single', 'average', 'centroid')
    if validation_answers[1] is not None and validation_answers[1] == ValidationAnswer.MORE:
        if configuration.get_clustering_selection()[0] == DBSCAN:
            parameter_modifications[EPS] = '⬇'
            parameter_modifications[MIN_SAMPLES] = '⬆'
        if configuration.get_clustering_selection()[0] == OPTICS:
            parameter_modifications[MIN_SAMPLES] = '⬆'
            parameter_modifications[MAX_EPS] = '⬇'
            parameter_modifications[EPS] = '⬇'
            parameter_modifications[MIN_CLUSTER_SIZE] = '⬆'
    if validation_answers[1] is not None and validation_answers[1] == ValidationAnswer.LESS:
        if configuration.get_clustering_selection()[0] == DBSCAN:
            parameter_modifications[EPS] = '⬆'
            parameter_modifications[MIN_SAMPLES] = '⬇'
        if configuration.get_clustering_selection()[0] == OPTICS:
            parameter_modifications[MIN_SAMPLES] = '⬇'
            parameter_modifications[MAX_EPS] = '⬆'
            parameter_modifications[EPS] = '⬆'
            parameter_modifications[MIN_CLUSTER_SIZE] = '⬇'
    if validation_answers[2] is not None and validation_answers[2] == ValidationAnswer.MORE:
        if configuration.get_clustering_selection()[0] == HIERARCHICAL:
            parameter_modifications[N_CLUSTERS] = '⬆'
            parameter_modifications[THRESHOLD] = '⬇'
        if configuration.get_clustering_selection()[0] == K_MEDOIDS:
            parameter_modifications[N_CLUSTERS] = '⬆'
        if configuration.get_clustering_selection()[0] == DBSCAN:
            parameter_modifications[EPS] = '⬇'
            parameter_modifications[MIN_SAMPLES] = '⬇'
        if configuration.get_clustering_selection()[0] == OPTICS:
            parameter_modifications[MIN_SAMPLES] = '⬇'
            parameter_modifications[MAX_EPS] = '⬇'
            parameter_modifications[EPS] = '⬇'
            parameter_modifications[MIN_CLUSTER_SIZE] = '⬇'
        if configuration.get_clustering_selection()[0] == SPECTRAL_CLUSTERING:
            parameter_modifications[N_CLUSTERS] = '⬆'
        if configuration.get_clustering_selection()[0] == AFFINITY_PROPAGATION:
            parameter_modifications[DAMPING] = '⬇'
            parameter_modifications[PREFERENCE] = '⬆'
    if validation_answers[2] is not None and validation_answers[2] == ValidationAnswer.LESS:
        if configuration.get_clustering_selection()[0] == HIERARCHICAL:
            parameter_modifications[N_CLUSTERS] = '⬇'
            parameter_modifications[THRESHOLD] = '⬆'
        if configuration.get_clustering_selection()[0] == K_MEDOIDS:
            parameter_modifications[N_CLUSTERS] = '⬇'
        if configuration.get_clustering_selection()[0] == DBSCAN:
            parameter_modifications[EPS] = '⬆'
            parameter_modifications[MIN_SAMPLES] = '⬆'
        if configuration.get_clustering_selection()[0] == OPTICS:
            parameter_modifications[MIN_SAMPLES] = '⬆'
            parameter_modifications[MAX_EPS] = '⬆'
            parameter_modifications[EPS] = '⬆'
            parameter_modifications[MIN_CLUSTER_SIZE] = '⬆'
        if configuration.get_clustering_selection()[0] == SPECTRAL_CLUSTERING:
            parameter_modifications[N_CLUSTERS] = '⬇'
        if configuration.get_clustering_selection()[0] == AFFINITY_PROPAGATION:
            parameter_modifications[DAMPING] = '⬆'
            parameter_modifications[PREFERENCE] = '⬇'
    return parameter_modifications if parameter_modifications != {} else None




