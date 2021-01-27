from tkinter import StringVar, Label, LEFT, Radiobutton, IntVar

import numpy as np
import gui_compression.questions
from compression.compression import get_compression_method, get_array_part
from gui.QuestionnaireInputWithResult import QuestionnaireInputWithResult
from gui_clustering import algorithm_selection
from gui_clustering.algorithm_selection import algorithm_array, question_array


class QuestionnaireInputClustering(QuestionnaireInputWithResult):

    def __init__(self, title, config, predefined_answers=None):
        self.help_text = "Please choose one of the suggested algorithms:\n"
        super().__init__(title, config, predefined_answers)
        self.choice = IntVar()
        self.choice.set(-1)
        self.suggested_algorithms = question_array[2:]
        self.update_visibility_and_result()

    def get(self):
        answers = super().get()
        if self.choice.get() >= 0:
            selected_algorithm_f = self.suggested_algorithms[self.choice.get()]
        else:
            selected_algorithm_f = None
        return answers, selected_algorithm_f

    def show_choice(self):
        print(self.choice.get())

    def apply(self):
        answers = self.get()[0]
        self.suggested_algorithms = get_array_part(algorithm_array, question_array, answers)

        for i in range(len(self.result_widgets)):
            self.result_widgets[i].destroy()

        for i, algorithm in enumerate(self.suggested_algorithms):
            radio_button = Radiobutton(self.result_frame, text=algorithm[0], padx=20, variable=self.choice,
                                       command=self.show_choice, value=i, justify=LEFT)
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

    q_config2 = gui_compression.questions.question_array
    q_config3 = algorithm_selection.question_array

    qc = QuestionnaireInputClustering(title, q_config3, [True, True, False, True, True, True])
    qc.run()
    result = qc.get()

    print(result)
