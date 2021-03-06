from tkinter import Radiobutton, IntVar, NORMAL, DISABLED, Tk, Label, Menu

import numpy as np

import gui_cluster_selection
from gui_cluster_selection.algorithm_selection import algorithm_array
from gui_cluster_selection.clustering_questions import clustering_question_array
from gui_general import CreateToolTip
from gui_general.help_popup_gui import menu_help_clustering_selection
from util.question_result_array_util import get_array_part
from gui_general.QuestionnaireResultInput import QuestionnaireResultInput


def cluster_suggest(master, answers=None, clustering_algorithm=None, suggested_algorithms=None):
    answers, cluster_f, cluster_algo = input_questionnaire_clustering(master, clustering_question_array, answers, clustering_algorithm, suggested_algorithms)
    return answers, cluster_f, cluster_algo


def input_questionnaire_clustering(master, config, predefined_answers=None, predefined_algorithm=None, suggested_algorithms=None):
    questionnaire = ClusteringQuestionnaireResultInput(master, config, predefined_answers, predefined_algorithm, suggested_algorithms)
    questionnaire.run()
    answers, cluster_f, cluster_algo = questionnaire.get()
    return answers, cluster_f, cluster_algo


class ClusteringQuestionnaireResultInput(QuestionnaireResultInput):
    """Binary questionnaire view to support the selection of the clustering algorithm"""

    def __init__(self, master, config, predefined_answers=None, predefined_algorithm=None, suggested_algorithms=None):
        self.caption_text = "Answer the questions to narrow the set of\nfitting clustering algorithms and choose one"
        self.hint_text = "Typically the highlighted algorithm achieves good results."
        suggestion = None
        if suggested_algorithms is not None:
            suggestion = "Algorithms suggested based on the evaluation are highlighted in green."
        super().__init__(master, "Clustering Algorithm Selection", config, predefined_answers, suggestion=suggestion)

        self.menu = Menu(self.root)
        self.menu.add_command(label="Help", command=lambda: menu_help_clustering_selection(self.root))
        self.root.config(menu=self.menu)

        self.suggested_algorithms = suggested_algorithms
        self.algorithms = np.array(algorithm_array, dtype=object)
        self.choice = IntVar()
        if predefined_algorithm is None:
            self.choice.set(0)
        else:
            self.choice.set(np.where(self.algorithms[:, 2] == predefined_algorithm)[0][0])
        self.radio_buttons = np.empty(len(self.algorithms), dtype=Radiobutton)
        self.orig_color = None
        self.build_result_frame()
        self.selection_changed()

    def build_result_frame(self):
        for i, algorithm in enumerate(self.algorithms):
            self.radio_buttons[i] = Radiobutton(self.scrollable_result_frame, text=algorithm[2], padx=20, variable=self.choice, bg="white",
                                       value=i, justify='left')
            self.radio_buttons[i].grid(row=i + 10, column=0, sticky='w')
            CreateToolTip(self.radio_buttons[i], algorithm[5])
            if self.orig_color is None:
                self.orig_color = self.radio_buttons[i].cget("bg")
            if self.suggested_algorithms is not None and algorithm[2] in self.suggested_algorithms:
                self.radio_buttons[i].configure(bg='pale green')
            # elif i == 0 or i == 3:
            #     self.radio_buttons[i].configure(bg='pale green')


    def get(self):
        if self.canceled:
            return None, None, None
        answers = super().get()
        if self.choice.get() >= 0:
            selected_algorithm_f = self.algorithms[self.choice.get(), 3]
            cluster_algo = self.algorithms[self.choice.get(), 2]
        else:
            selected_algorithm_f = None
            cluster_algo = None
        return answers, selected_algorithm_f, cluster_algo

    def apply(self):
        answers = self.get()[0]
        suggested_algorithms = get_array_part(self.algorithms, clustering_question_array, answers)
        suggested_algorithms_names = self.get_suggested_algorithm_names(suggested_algorithms)
        previous_choice = self.choice.get()
        preferred_choice = -1
        first_enabled = -1
        for i, button in enumerate(self.radio_buttons):
            if self.suggested_algorithms is None:
                button.configure(bg=self.orig_color)
            if self.algorithms[i, 2] in suggested_algorithms_names:
                button.config(state=NORMAL)
                if i == 0:
                    preferred_choice = 0  # hierarchical
                    if self.suggested_algorithms is None:
                        button.configure(bg='pale green')
                elif preferred_choice == -1 and i == 3:
                    preferred_choice = 3  # optics
                    if self.suggested_algorithms is None:
                        button.configure(bg='pale green')
                if first_enabled == -1:
                    first_enabled = i
            else:
                button.config(state=DISABLED)
                # button.configure(bg=self.orig_color)
                if previous_choice == i:
                    previous_choice = -1
        if previous_choice != -1:
            self.choice.set(previous_choice)
        elif preferred_choice != -1:
            self.choice.set(preferred_choice)
        else:
            self.choice.set(first_enabled)

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

    # qc = ClusteringQuestionnaireResultInput(q_config3, [True, True, False, True, True, True])
    qc = ClusteringQuestionnaireResultInput(Tk(), q_config3, [True, False, False, False, False, False], "KMedoids")

    qc.run()
    result = qc.get()

    print(result)


