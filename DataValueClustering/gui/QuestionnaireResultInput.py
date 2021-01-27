from abc import ABC, abstractmethod
from tkinter import Label, Checkbutton, Button, Tk, IntVar, StringVar, Frame, LEFT, RIGHT, BOTH, GROOVE, font

import numpy as np

from gui.ToolTip import CreateToolTip


class QuestionnaireInputWithResult(ABC):

    # config: [dependencies, not-dependencies, name, default, question, notes?]

    def __init__(self, title, config, predefined_answers=None):
        # Parameters
        self.config = np.array(config, dtype=object)
        self.n = len(config)
        self.m = len(self.config[0])
        self.check_config()

        # Variables
        self.config_dep = self.config[:, 0]
        self.config_notdep = self.config[:, 1]
        self.config_name = self.config[:, 2]
        if predefined_answers is None or len(predefined_answers) != self.n:
            self.config_default = self.config[:, 3]
        else:
            self.config_default = predefined_answers
        self.config_question = self.config[:, 4]
        self.config_notes = self.config[:, 5] if self.m > 5 else None

        # GUI
        self.root = Tk()
        self.root.title(title)
        self.root.config(bg='white')
        self.question_frame = Frame(self.root, bg="white")
        self.result_frame = Frame(self.root, bg="white")
        # self.button_frame = Frame(self.root, bg="blue")
        self.question_frame.grid(row=0, column=0, sticky='n')
        self.result_frame.grid(row=0, column=1, sticky='n')
        # self.button_frame.grid(row=1, column=0, sticky='nswe', columnspan=2)
        self.result_widgets = []

        self.labels = np.empty(self.n, dtype=Label)
        self.checks = np.empty(self.n, dtype=Checkbutton)
        self.answers = np.empty(self.n, dtype=IntVar)
        self.questions = np.empty(self.n, dtype=StringVar)

        self.question_caption = StringVar()
        self.question_caption.set("Please answer the following questions:")
        self.question_caption_label = Label(self.question_frame, anchor='w', textvariable=self.question_caption, text="test", bg='white',
                                            fg="midnightblue", font=font.Font(size=14))
        self.question_caption_label.grid(row=0, column=0, sticky='w', columnspan=2)

        # Initialize Widgets
        for i, question in enumerate(self.questions):
            self.questions[i] = StringVar()
            self.questions[i].set(self.config_question[i])
            self.labels[i] = Label(self.question_frame, width=100, anchor='nw', textvariable=self.questions[i], text=question, bg='white')
            if self.m > 5:
                message = str(self.config_notes[i])
                CreateToolTip(self.labels[i], text=message)
                # self.labels[i].bind("<Enter>", (lambda event, i2=i: self.on_label_enter(event, i2)))
                # self.labels[i].bind("<Leave>", (lambda event, i2=i: self.on_label_leave(event, i2)))

            self.answers[i] = IntVar()
            self.answers[i].set(int(self.config_default[i]))
            self.checks[i] = Checkbutton(self.question_frame, variable=self.answers[i], command=self.update_visibility_and_result, bg='white')

        self.visible = np.full(self.n, False)
        self.update_visibility()

        self.result_caption = StringVar()
        self.result_caption.set(self.help_text)
        self.result_caption_label = Label(self.result_frame, anchor='w', textvariable=self.result_caption, text="test", bg='white',
                                          fg="midnightblue", font=font.Font(size=14))
        self.result_caption_label.grid(row=0, column=0, sticky='w', columnspan=2)

        self.button = Button(self.root, text='OK', command=self.close, bg='white')
        self.button.grid(row=1, column=0, sticky='nswe', columnspan=2)

    def run(self):
        self.root.mainloop()

    def update_visibility(self):
        for i in range(self.n):
            is_visible = self.visible[i]
            should_visible = self.should_be_visible(i)
            if not is_visible and should_visible:
                self.labels[i].grid(row=i + 5, column=0, sticky='nw')
                self.checks[i].grid(row=i + 5, column=1)
            if is_visible and not should_visible:
                self.labels[i].grid_forget()
                self.checks[i].grid_forget()
                self.answers[i].set(False)
            self.visible[i] = should_visible

    def update_visibility_and_result(self):
        self.update_visibility()
        self.apply()

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

    @abstractmethod
    def apply(self):
        pass

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