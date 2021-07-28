from enum import Enum

import numpy as np

from gui_cluster_selection.algorithm_selection import HIERARCHICAL, OPTICS, DBSCAN


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
    print(validation_answers[3])
    if validation_answers[3] is not None and validation_answers[3][1] is not None:
        print(validation_answers)
        suggested_data_names = validation_answers[3][1]
    return suggested_data_names if len(suggested_data_names) > 0 else None

def get_suggested_algorithms(validation_answers):
    suggested_algorithms = list()
    if validation_answers[1] is not None and validation_answers[1] == ValidationAnswer.MORE:
        suggested_algorithms.append(DBSCAN)
        suggested_algorithms.append(OPTICS)
    elif validation_answers[0] is not None and validation_answers[0] == ValidationAnswer.UNHAPPY:
        suggested_algorithms.append(HIERARCHICAL)
        suggested_algorithms.append(OPTICS)
    return suggested_algorithms


