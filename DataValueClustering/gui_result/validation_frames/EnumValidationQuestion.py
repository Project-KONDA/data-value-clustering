from tkinter import Radiobutton, IntVar
import numpy as np

from gui_general import CreateToolTip
from gui_result.validation_frames.ValidationQuestion import ValidationQuestion


def create_enum_validation_question(parent, question, explanation, answers):
    return EnumValidationQuestion(parent, question, explanation, answers)


class EnumValidationQuestion(ValidationQuestion):

    def __init__(self, parent, question, explanation, answers):
        # answers: value, text, tip, (int?)
        assert (len(answers[0, :]) >= 3)
        super().__init__(parent, question, explanation)

        self.answers = answers

        self.n = len(answers)
        self.radio_buttons = np.empty(self.n, Radiobutton)
        self.choice = IntVar()
        self.choice.set(0)

        for i, answer in enumerate(answers):
            self.radio_buttons[i] = Radiobutton(self.frame, text=answer[1], variable=self.choice, value=i,
                                                command=self.update_advice, justify='left', anchor='w',
                                                bg='white')
            CreateToolTip(self.radio_buttons[i], answer[2])
            self.radio_buttons[i].grid(row=i + 10, column=1, sticky='nsw')

    def get_result(self):
        return self.answers[self.choice.get(), 0]
