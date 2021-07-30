from tkinter import Radiobutton, IntVar
import numpy as np

from gui_general import CreateToolTip
from gui_result.validation_frames.ValidationQuestion import ValidationQuestion
from gui_result.validation_questionnaire import ValidationAnswer


def create_enum_validation_question(parent, question_and_explanation, answers, advice_var):
    return EnumValidationQuestion(parent, question_and_explanation, answers, advice_var)


class EnumValidationQuestion(ValidationQuestion):

    def __init__(self, parent, question_and_explanation, answers, result_view):
        # answers: value, text, tip, (int?)
        assert (len(answers[0, :]) >= 3)
        super().__init__(parent, question_and_explanation, result_view)

        self.answers = answers

        self.n = len(answers)
        self.radio_buttons = np.empty(self.n, Radiobutton)
        self.choice = IntVar()
        self.choice.set(0)

        for i, answer in enumerate(answers):
            self.radio_buttons[i] = Radiobutton(self.frame, text=answer[1], variable=self.choice, value=i,
                                                command=self.update_advice, justify='left', anchor='w',
                                                bg='white', padx=20)
            CreateToolTip(self.radio_buttons[i], answer[2])
            self.radio_buttons[i].grid(row=i + 10, column=1, sticky='nsw')

    def get_result(self):
        return self.answers[self.choice.get(), 0]


