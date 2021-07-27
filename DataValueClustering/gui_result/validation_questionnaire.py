from enum import Enum

import numpy as np


class ValidationAnswer(Enum):
    HAPPY = 1
    UNHAPPY = 2
    MORE = 3
    LESS = 4

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