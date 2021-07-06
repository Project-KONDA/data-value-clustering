from tkinter import Radiobutton, IntVar, NORMAL, DISABLED

import numpy as np

import gui_cluster_selection
from gui_cluster_selection.algorithm_selection import algorithm_array
from gui_cluster_selection.clustering_questions import clustering_question_array
from util.question_result_array_util import get_array_part
from gui_general.QuestionnaireResultInput import QuestionnaireResultInput


def cluster_suggest():
    predefined_answers = None  # TODO
    answers, cluster_f = input_questionnaire_clustering(clustering_question_array, predefined_answers)
    return answers, cluster_f


def input_questionnaire_clustering(config, predefined_answers=None):
    questionnaire = ClusteringQuestionnaireResultInput(config, predefined_answers)
    questionnaire.run()
    answers, cluster_f = questionnaire.get()
    return answers, cluster_f


class ClusteringQuestionnaireResultInput(QuestionnaireResultInput):
    """Binary questionnaire view to support the selection of the clustering algorithm"""

    def __init__(self, config, predefined_answers=None):
        self.help_text = "Please choose one of the suggested algorithms:\n"
        super().__init__("Clustering Configuration", config, predefined_answers)
        self.algorithms = np.array(algorithm_array, dtype=object)
        self.choice = IntVar()
        self.choice.set(0)
        self.radio_buttons = np.empty(len(self.algorithms), dtype=Radiobutton)
        self.build_result_frame()
        self.update_visibility_and_result()

    def build_result_frame(self):
        for i, algorithm in enumerate(self.algorithms):
            self.radio_buttons[i] = Radiobutton(self.scrollable_result_frame, text=algorithm[2], padx=20, variable=self.choice,
                                       value=i, justify='left')
            self.radio_buttons[i].grid(row=i + 10, column=0, sticky='w')

    def close(self, event=None):
        answers, algorithm = self.get()
        if algorithm is None:
            self.result_caption_label.config(fg="red")
        else:
            super().close()

    def get(self):
        answers = super().get()
        if self.choice.get() >= 0:
            selected_algorithm_f = self.algorithms[self.choice.get(), 3]
        else:
            selected_algorithm_f = None
        return answers, selected_algorithm_f

    def apply(self):
        answers = self.get()[0]
        suggested_algorithms = get_array_part(self.algorithms, clustering_question_array, answers)
        suggested_algorithms_names = self.get_suggested_algorithm_names(suggested_algorithms)
        for i, button in enumerate(self.radio_buttons):
            if self.algorithms[i, 2] in suggested_algorithms_names:
                button.config(state=NORMAL)
            else:
                button.config(state=DISABLED)
                if self.choice.get() == i:
                    self.choice.set(-1)

    def get_suggested_algorithm_names(self, suggested_algorithms):
        if len(suggested_algorithms.shape) == 2:
            return suggested_algorithms[:, 0]
        else:
            return []


if __name__ == '__main__':
    title = "myQuestions"
    q_config = np.array(
        # 0              1                 2     3        4         5             6
        # [dependencies, not-dependencies, name, default, question, explanation?, example?]
        [[[], [], "name0", False, "question0?"],
         [[], [], "name1", True, "question1?"],
         [[0], [], "name2", False, "question2?"],
         [[1], [], "name3", True, "question3?"],
         [[], [3], "name4", False, "question4?"],
         [[3], [], "name5", True, "question5?"],
         [[0], [1], "name6", False, "question6?"]],
        dtype=object)

    q_config3 = gui_cluster_selection.clustering_questions.clustering_question_array

    qc = ClusteringQuestionnaireResultInput(q_config3, [True, True, False, True, True, True])
    qc.run()
    result = qc.get()

    print(result)


