from tkinter import Radiobutton, IntVar, PhotoImage
import numpy as np

from gui_general import CreateToolTip
from gui_result.validation_frames.ValidationQuestion import ValidationQuestion
from gui_result.validation_questionnaire import ValidationAnswer, question_1_answers


def create_enum_validation_question(parent, question_and_explanation, answers, advice_var, question_break, previous=None):
    return EnumValidationQuestion(parent, question_and_explanation, answers, advice_var, question_break, previous)


class EnumValidationQuestion(ValidationQuestion):

    def __init__(self, parent, question_and_explanation, answers, result_view, question_break, previous=None):
        # answers: value, text, tip, (int?)
        assert (len(answers[0, :]) >= 3)
        super().__init__(parent, question_and_explanation, result_view, question_break)

        self.answers = answers

        self.n = len(answers)
        self.radio_buttons = np.empty(self.n, Radiobutton)
        self.choice = IntVar()

        if previous is not None:
            answer_types = np.array(answers[:, 0], dtype=ValidationAnswer).tolist()
            index = answer_types.index(previous)
            self.choice.set(index)
        else:
            self.choice.set(-1)

        circle_size = 22
        width_pixels = question_break - circle_size

        for i, answer in enumerate(answers):
            self.radio_buttons[i] = Radiobutton(self.frame, text=answer[1], variable=self.choice, value=i,
                                                command=self.update_advice, justify='left', anchor='w',
                                                bg='white', wraplength=width_pixels)
            CreateToolTip(self.radio_buttons[i], answer[2])
            self.radio_buttons[i].grid(row=i + 10, column=1, sticky='nswe')

    def get_result(self):
        if self.choice.get() == -1:
            return None
        return self.answers[self.choice.get(), 0]


