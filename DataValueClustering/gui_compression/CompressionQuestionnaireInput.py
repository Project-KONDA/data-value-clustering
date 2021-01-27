from tkinter import StringVar, Label, LEFT

import numpy as np
import gui_compression.questions
from compression.compression import get_compression_method
from gui_general.QuestionnaireResultInput import QuestionnaireInputWithResult


def input_questionnaire_compression(config, data, predefined_answers=None):
    questionnaire = QuestionnaireInputCompression(config, data, predefined_answers)
    questionnaire.run()
    answers = questionnaire.get()
    return answers


class QuestionnaireInputCompression(QuestionnaireInputWithResult):

    def __init__(self, config, data, predefined_answers=None):
        self.help_text = "Compression of the first 100 data values:\n"
        super().__init__("Compression Configuration", config, predefined_answers)
        self.data = data
        self.update_visibility_and_result()

    def apply(self):
        answers = self.get()
        compression_f = get_compression_method(answers)
        values_compressed, compression_dict = compression_f(self.data[0:100])
        for i in range(len(self.result_widgets)):
            self.result_widgets[i].destroy()

        for i, key in enumerate(compression_dict):
            s1 = StringVar()
            s1.set(key)
            compression_target_label = Label(self.result_frame, anchor='nw', textvariable=s1, bg='lemonchiffon')
            compression_target_label.grid(row=i + 10, column=0, sticky='nwse')
            self.result_widgets.append(compression_target_label)

            s2 = StringVar()
            s2.set(str(compression_dict[key])[1:len(str(compression_dict[key]))-1])
            compression_source_label = Label(self.result_frame, anchor='nw', textvariable=s2, bg='ivory', wraplength=400, justify=LEFT)
            compression_source_label.grid(row=i + 10, column=1, sticky='nwse')
            self.result_widgets.append(compression_source_label)


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

    q_config2 = gui_compression.questions.question_array

    qc = QuestionnaireInputCompression(q_config2,
                                        ["abcLBSDH", "bbbGDGD", "c", "a", "b", "c", "a", "b", "c", "a", "b", "c", "a",
                                         "b", "c", "a", "b", "c", "a", "b", "c", "a", "b", "c", "a", "b", "c", "a", "b",
                                         "c", "a", "b", "c", "a", "b", "c", "a", "b", "c", "a", "b", "c", "a", "b", "c",
                                         "a", "b", "c", "a", "b", "c", "a", "b", "c", "a", "b", "c", "a", "b", "c", "a",
                                         "b", "c", "?", "3", "1234"], None)
    qc.run()

    result = qc.get()
    print(result)
