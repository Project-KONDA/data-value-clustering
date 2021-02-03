from abc import ABC, abstractmethod
from tkinter import Frame, IntVar, Checkbutton, StringVar, Label, font


class ClusteringParameter(ABC):

    def __init__(self, parent, name, explanation, deactivatable=False):
        self.frame = Frame(parent, highlightthickness=1, highlightbackground='grey', bg='white')
        self.frame.grid_columnconfigure(0, minsize=self.frame.winfo_screenwidth() // 25)
        self.frame.grid_columnconfigure(1, minsize=self.frame.winfo_screenwidth() // 3)

        self.root = parent
        self.name = name
        self.explanation = explanation
        self.deactivatable = deactivatable

        self.is_activated = IntVar()
        self.is_activated.set(int(not deactivatable))

        # define frame content:

        # check box:
        if self.deactivatable:
            self.check_active = Checkbutton(self.frame, variable=self.is_activated, command=self.update_active,
                                            bg='white', anchor='nw', padx=20)
            self.check_active.grid(row=0, column=0, sticky='w')

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

    def update_active(self):
        if self.is_activated.get() == 1:
            self.activate()
        else:
            self.deactivate()

    def deactivate(self):
        self.label.config(state='disabled', bg='grey90')
        self.label_explanation.config(state='disabled', bg='grey90')
        self.frame.config(bg='grey90')
        self.check_active.config(bg='grey90')

    def activate(self):
        self.label.config(state='normal', bg='white')
        self.label_explanation.config(state='normal', bg='white')
        self.frame.config(bg='white')
        if self.deactivatable:
            self.check_active.config(bg='white')

    @abstractmethod
    def get(self):
        pass
