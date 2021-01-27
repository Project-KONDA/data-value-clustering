from tkinter import Label, Checkbutton, Button, Tk, IntVar, StringVar

import numpy as np

import gui_clustering.clustering_questions
import gui_compression.compression_questionnaire
import gui_compression.questions
from gui_clustering import algorithm_selection
from compression import compression
from gui_general.ToolTip import CreateToolTip


def input_questionnaire(title, config):
    questionnaire = QuestionnaireInput(title, config)
    result = questionnaire.get()
    return result

class QuestionnaireInput:

    # config: [dependencies, not-dependencies, name, default, question, notes?]

    def __init__(self, title, config):
        # Parameters
        self.config = np.array(config, dtype=object)
        self.n = len(config)
        self.m = len(self.config[0])
        self.check_config()

        # Variables
        self.config_dep = self.config[:, 0]
        self.config_notdep = self.config[:, 1]
        self.config_name = self.config[:, 2]
        self.config_default = self.config[:, 3]
        self.config_question = self.config[:, 4]
        self.config_notes = self.config[:, 5] if self.m > 5 else None

        # GUI
        self.root = Tk()
        self.root.title(title)
        self.root.config(bg='white')
        self.labels = np.empty(self.n, dtype=Label)
        self.checks = np.empty(self.n, dtype=Checkbutton)
        self.answers = np.empty(self.n, dtype=IntVar)
        self.questions = np.empty(self.n, dtype=StringVar)

        # Initialize Widgets
        for i, question in enumerate(self.questions):
            self.questions[i] = StringVar()
            self.questions[i].set(self.config_question[i])
            self.labels[i] = Label(self.root, width=100, anchor='w', textvariable=self.questions[i], text=question, bg='white')
            if self.m > 5:
                message = str(self.config_notes[i])
                CreateToolTip(self.labels[i], text=message)
                # self.labels[i].bind("<Enter>", (lambda event, i2=i: self.on_label_enter(event, i2)))
                # self.labels[i].bind("<Leave>", (lambda event, i2=i: self.on_label_leave(event, i2)))

            self.answers[i] = IntVar()
            self.answers[i].set(int(self.config_default[i]))
            self.checks[i] = Checkbutton(self.root, variable=self.answers[i], command=self.update_visibility, bg='white')

        self.visible = np.full(self.n, False)
        self.update_visibility()

        self.button = Button(self.root, text='OK', command=self.close, bg='white')
        self.button.grid(sticky='nsew', row=self.n + 10, column=0, columnspan=2)

        self.root.mainloop()

    def update_visibility(self):
        for i in range(self.n):
            is_visible = self.visible[i]
            should_visible = self.should_be_visible(i)
            if not is_visible and should_visible:
                self.labels[i].grid(row=i + 5, column=0, sticky='w')
                self.checks[i].grid(row=i + 5, column=1)
            if is_visible and not should_visible:
                self.labels[i].grid_forget()
                self.checks[i].grid_forget()
                self.answers[i].set(False)
            self.visible[i] = should_visible

    def should_be_visible(self, i):
        """ test if question i should be visible"""
        bool = True
        for d in self.config_dep[i]:
            bool &= self.answers[d].get() and self.visible[d]
        for nd in self.config_notdep[i]:
            bool &= not self.answers[nd].get()  # or not self.visible[nd]
        return bool

    def check_questions(self):
        pass

    def get(self):
        answers = []
        for i, v in enumerate(self.answers):
            answers.append(v.get() == 1)
        return answers

    def close(self):
        self.root.destroy()

    def check_config(self):
        assert self.n > 0
        assert 5 <= self.m <= 6
        for i in range(self.n):
            assert self.m == len(self.config[i])
            assert isinstance(self.config[i, 0], list)
            assert isinstance(self.config[i, 1], list)
            assert isinstance(self.config[i, 2], str)
            assert isinstance(self.config[i, 3], bool)
            assert isinstance(self.config[i, 4], str)
            if self.m > 5:
                assert isinstance(self.config[i, 5], str)

            assert not self.config[i, 0] or max(self.config[i, 0]) < i
            assert not self.config[i, 1] or max(self.config[i, 1]) < i

    # def on_label_enter(self, event, i):
    #     message = str(self.config_notes[i])
    #
    #
    #     print("on index " + str(i) + " show message: " + message)
    #
    # def on_label_leave(self, event, i):
    #     print("hide")


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

    q_config2 = gui_compression.questions.compression_question_array
    q_config3 = gui_clustering.clustering_questions.clustering_question_array

    print(QuestionnaireInput(title, q_config3).get())
