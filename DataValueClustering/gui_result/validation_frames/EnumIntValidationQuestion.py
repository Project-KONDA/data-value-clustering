from tkinter import Entry, StringVar, Frame, Canvas, Scrollbar, Checkbutton, IntVar
import numpy as np
import re

from gui_center.hub_configuration import cluster_label_from_txt_name
from gui_result.validation_frames.EnumValidationQuestion import EnumValidationQuestion


def create_enum_int_validation_question(parent, question_and_explanation, answers, result_view, previous=None, previous_cluster=None, check_labels=None):
    return EnumIntValidationQuestion(parent, question_and_explanation, answers, result_view, previous, previous_cluster, check_labels)


class EnumIntValidationQuestion(EnumValidationQuestion):
    def __init__(self, parent, question_and_explanation, answers, result_view, previous=None, previous_cluster=None, check_labels=None):
        assert (len(answers[0]) == 4)
        super().__init__(parent, question_and_explanation, answers, result_view, previous)

        assert (previous_cluster is None or len(previous_cluster) == len(answers))

        self.check_labels_per_answer = check_labels

        self.check_buttons_per_answer = np.empty(len(self.check_labels_per_answer), dtype=object)
        self.check_vars_per_answer = np.empty(len(self.check_labels_per_answer), dtype=object)
        for i in range(len(self.check_labels_per_answer)):
            self.check_buttons_per_answer[i] = []
            self.check_vars_per_answer[i] = []

        for i, answer in enumerate(answers):
            self.radio_buttons[i].configure(command = lambda j=i: self.activate_check_buttons(j))
            if answer[3]:
                assert self.check_labels_per_answer[i] is not None
                assert self.check_labels_per_answer[i]

                self.around_canvas_frame = Frame(self.frame, width=75, height=75, bg="white", highlightbackground="grey", highlightthickness=1)
                self.canvas = Canvas(self.around_canvas_frame, bg="white", width=75, height=75, highlightthickness=0)
                self.scrollbar = Scrollbar(self.around_canvas_frame, orient="vertical", command=self.canvas.yview)
                self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)
                self.scrollable_check_frame = Frame(self.canvas)
                self.scrollable_check_frame.bind(
                    "<Configure>",
                    lambda e: self.canvas.configure(
                        scrollregion=self.canvas.bbox("all")
                    )
                )
                self.canvas_frame = self.canvas.create_window((1, 1), window=self.scrollable_check_frame, anchor="nw")
                self.canvas.configure(yscrollcommand=self.scrollbar.set)
                self.around_canvas_frame.grid(row=i + 10, column=2, sticky='nsw', padx=5, pady=5)
                self.canvas.grid(row=0, column=0, sticky='nsw', padx=5, pady=5)
                self.scrollbar.grid(row=0, column=1, sticky='nsw')

                for j,v in enumerate(self.check_labels_per_answer[i]):
                    var = IntVar()
                    self.check_vars_per_answer[i].append(var)
                    check_button = Checkbutton(self.scrollable_check_frame, variable=var, bg='white', anchor='w', text=(str(v)))
                    check_button.grid(row=j + 10, column=0, sticky='w')
                    self.check_buttons_per_answer[i].append(check_button)

                if previous_cluster is not None:
                    self.set_previously_selected_checks(previous_cluster)

    def on_mousewheel(self, event):
        if self.scrollable_check_frame.winfo_height() > self.canvas.winfo_height():
            self.canvas.yview_scroll(-1 * (event.delta // 120), "units")

    def activate_check_buttons(self, j):
        self.update_advice()
        for i, answer in enumerate(self.answers):
            if answer[3]:
                for k,btn in enumerate(self.check_buttons_per_answer[i]):
                    btn.configure(state="disabled")
        if self.answers[j,3]:
            for k, btn in enumerate(self.check_buttons_per_answer[j]):
                btn.configure(state="normal")

    def get_result(self):
        if self.choice.get() == -1:
            return None, None
        return self.answers[self.choice.get(), 0], self.get_selected_checks()

    def get_selected_checks(self):
        selected_checks_per_answer = []
        for i, check_vars in enumerate(self.check_vars_per_answer):  # iterate through answers
            selected_checks = list()
            if check_vars:
                for j,a in enumerate(check_vars):  # iterate through check vars of answer
                    if a.get():
                        selected_checks.append(self.check_labels_per_answer[i][j])
            selected_checks_per_answer.append(selected_checks)
        return selected_checks_per_answer

    def set_previously_selected_checks(self, prev_selected_labels):
        for i, prev_clusters in enumerate(prev_selected_labels):
            if prev_clusters:
                for j, label in enumerate(prev_clusters):
                    no = self.check_labels_per_answer[i].index(label)
                    self.check_vars_per_answer[i][no].set(1)