from tkinter import Entry, StringVar
import numpy as np
import re

from gui_result.validation_frames.EnumValidationQuestion import EnumValidationQuestion


def create_enum_int_validation_question(parent, question_and_explanation, answers, result_view):
    return EnumIntValidationQuestion(parent, question_and_explanation, answers, result_view)


class EnumIntValidationQuestion(EnumValidationQuestion):
    def __init__(self, parent, question_and_explanation, answers, result_view):
        assert (len(answers[0]) == 4)
        super().__init__(parent, question_and_explanation, answers, result_view)

        self.entries = np.full(self.n, Entry)
        self.vars = np.empty(self.n, StringVar)

        for i, answer in enumerate(answers):
            self.radio_buttons[i].configure(command = lambda j=i: self.activate_entry(j))
            if answer[3]:
                self.vars[i] = StringVar(self.root)
                self.vars[i].trace("w", lambda name, index, mode, sv=self.vars[i]: self.validate_entry(sv))
                self.entries[i] = Entry(self.frame, textvariable=self.vars[i], state='disabled')
                self.entries[i].grid(row=i + 10, column=2, sticky='nsw')

    def activate_entry(self, j):
        self.update_advice()
        for i, answer in enumerate(self.answers):
            if answer[3]:
                self.vars[i].set("")
                self.entries[i].configure(state="disabled")
        if self.answers[j,3]:
            self.entries[j].configure(state="normal")

    def validate_entry(self, var):
        value = var.get()
        split = value.split(",")
        for val in split:
            if val != "":
                try:
                    x = int(val)
                except ValueError:
                    self.shorten(var)

    def shorten(self, var):
        var.set(var.get()[0:len(var.get()) - 1])
        self.validate_entry(var)

    def get_result(self):
        return self.answers[self.choice.get(), 0], self.get_cluster_list(self.vars[self.choice.get()])

    def get_cluster_list(self, var):
        if var is None:
            return None
        value = var.get()
        split = value.split(",")
        int_list = list()
        for val in split:
            try:
                int_val = int(val)
                int_list.append(int_val)
            except ValueError:
                pass
        return int_list
