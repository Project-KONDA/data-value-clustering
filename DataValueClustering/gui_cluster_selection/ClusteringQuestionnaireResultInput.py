from tkinter import Radiobutton, IntVar

import numpy as np

import gui_cluster_selection.clustering_questions
from util.question_result_array_util import get_array_part
from gui_general.QuestionnaireResultInput import QuestionnaireResultInput
from gui_cluster_selection.algorithm_selection import algorithm_array
from gui_cluster_selection.clustering_questions import clustering_question_array


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

    def __init__(self, config, predefined_answers=None):
        self.help_text = "Please choose one of the suggested algorithms:\n"
        super().__init__("Clustering Configuration", config, predefined_answers)
        self.choice = IntVar()
        self.choice.set(-1)
        self.suggested_algorithms = algorithm_array[2:]
        self.update_visibility_and_result()

    def get(self):
        answers = super().get()
        if self.choice.get() >= 0:
            selected_algorithm_f = self.suggested_algorithms[self.choice.get()][1]
        else:
            selected_algorithm_f = None
        return answers, selected_algorithm_f

    def show_choice(self):
        print(self.choice.get())

    def apply(self):
        answers = self.get()[0]
        self.suggested_algorithms = get_array_part(algorithm_array, clustering_question_array, answers)

        for i in range(len(self.result_widgets)):
            self.result_widgets[i].destroy()

        for i, algorithm in enumerate(self.suggested_algorithms):
            radio_button = Radiobutton(self.scrollable_result_frame, text=algorithm[0], padx=20, variable=self.choice,
                                       command=self.show_choice, value=i, justify='left')
            radio_button.grid(row=i + 10, column=0, sticky='w')
            self.result_widgets.append(radio_button)


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


