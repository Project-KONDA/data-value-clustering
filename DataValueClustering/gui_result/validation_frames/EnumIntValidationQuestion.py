from tkinter import Entry, StringVar
import numpy as np
import re

from gui_result.validation_frames.EnumValidationQuestion import EnumValidationQuestion


def create_enum_int_validation_question(parent, question, explanation, answers):
    return EnumIntValidationQuestion(parent, question, explanation, answers)


class EnumIntValidationQuestion(EnumValidationQuestion):
    def __init__(self, parent, question, explanation, answers):
        assert (len(answers[0]) == 4)
        super().__init__(parent, question, explanation, answers)

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
        return self.answers[self.choice.get(), 0], self.get_cluster_list(self.entries[self.choice.get()])

    def get_cluster_list(self, entry):
        if entry is None:
            return None
        else:
            split = entry.split(",")
            for val in split:
                if not type(val) == int:
                    return None
        return split
