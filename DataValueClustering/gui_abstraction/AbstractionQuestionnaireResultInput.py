from tkinter import StringVar, Label, LEFT

import numpy as np
import gui_abstraction.abstraction_questions
from abstraction.abstraction import get_abstraction_method
from gui_abstraction.abstraction_questions import abstraction_question_array
from gui_general.QuestionnaireResultInput import QuestionnaireResultInput


def abstraction_configuration(data, predefined_answers=None):
    answers = input_questionnaire_abstraction(abstraction_question_array, data, predefined_answers)
    return get_abstraction_method(answers), answers


def input_questionnaire_abstraction(config, data, predefined_answers=None):
    questionnaire = AbstractionQuestionnaireResultInput(config, data, predefined_answers)
    questionnaire.run()
    answers = questionnaire.get()
    return answers


class AbstractionQuestionnaireResultInput(QuestionnaireResultInput):
    """ binary questionaire GUI for configuring the abstraction function """

    def __init__(self, config, data, predefined_answers=None):
        self.help_text = "Abstraction of the first 100 data values:\n"
        super().__init__("Abstraction Configuration", config, predefined_answers)
        self.data = data
        self.labels = []
        self.update_visibility_and_result()

    def apply(self):
        answers = self.get()
        abstraction_f = get_abstraction_method(answers)
        values_abstracted, abstraction_dict = abstraction_f(self.data[0:100])
        for i in range(len(self.labels)):
            self.labels[i].destroy()

        for i, key in enumerate(abstraction_dict):
            s1 = StringVar()
            s1.set(key)
            abstraction_target_label = Label(self.scrollable_result_frame, anchor='nw', textvariable=s1, bg='lemonchiffon')
            abstraction_target_label.grid(row=i + 10, column=0, sticky='nwse')
            self.labels.append(abstraction_target_label)
            s2 = StringVar()
            s2.set(str(abstraction_dict[key])[1:len(str(abstraction_dict[key]))-1])
            abstraction_source_label = Label(self.scrollable_result_frame, anchor='nw', textvariable=s2, bg='ivory', wraplength=540, justify=LEFT)  # TODO: calculate wraplength
            abstraction_source_label.grid(row=i + 10, column=1, sticky='nwse')
            self.labels.append(abstraction_source_label)


if __name__ == '__main__':
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

    q_config2 = gui_abstraction.abstraction_questions.abstraction_question_array

    qc = AbstractionQuestionnaireResultInput(q_config2,
                                             ["abcLBSDH", "bbbGDGD", "c", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j",
                                         "k", "l", "m", "n", "o", "p", "q", "r", "a", "b", "c", "a", "b", "c", "a", "b",
                                         "c", "a", "b", "c", "a", "b", "c", "a", "b", "c", "a", "b", "c", "a", "b", "c",
                                         "a", "b", "c", "a", "b", "c", "a", "b", "c", "a", "b", "c", "a", "b", "c", "a",
                                         "b", "c", "?", "3", "1234"], None)
    qc.run()

    result = qc.get()
    print(result)