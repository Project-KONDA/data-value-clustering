from abc import ABC, abstractmethod
from tkinter import Frame, GROOVE, IntVar, Checkbutton, StringVar, Label, font, NORMAL, DISABLED


class ClusteringParameter(ABC):

    def __init__(self, parent, name, explanation, deactivatable):
        self.frame = Frame(parent, highlightthickness=1, highlightbackground="grey", bg='white')
        self.frame.grid_columnconfigure(0, minsize=self.frame.winfo_screenwidth() / 25)
        self.frame.grid_columnconfigure(1, minsize=self.frame.winfo_screenwidth() / 3)

        self.name = name
        self.explanation = explanation
        self.deactivatable = deactivatable

        # define frame content:

        # check box:
        if deactivatable:
            self.is_activated = IntVar()
            self.is_activated.set(1)
            self.check = Checkbutton(self.frame, variable=self.is_activated, command=self.change_checked, bg='white',
                                     anchor='nw', padx=20)
            self.check.grid(row=0, column=0, sticky='w')

        # name label:
        self.label_text = StringVar()
        self.label_text.set(self.name)
        self.label = Label(self.frame, anchor='w', textvariable=self.label_text, bg='white', padx=5,
                           font=font.Font(size=14))
        self.label.grid(row=0, column=1, sticky='w')

        # explanation label:
        self.explanation_text = StringVar()
        self.explanation_text.set(self.explanation)
        self.label_explanation = Label(self.frame, anchor='w', textvariable=self.explanation_text, bg='white', padx=5,
                                       wraplength=500)
        self.label_explanation.grid(row=1, column=1, sticky='w')


    def change_checked(self):
        if self.is_activated.get() == 1:
            self.label.config(state=NORMAL, bg='white')
            self.label_explanation.config(state=NORMAL, bg='white')
            self.frame.config(bg='white')
            self.check.config(bg='white')
        else:
            self.label.config(state=DISABLED, bg='grey90')
            self.label_explanation.config(state=DISABLED, bg='grey90')
            self.frame.config(bg='grey90')
            self.check.config(bg='grey90')

    @abstractmethod
    def get(self):
        pass




