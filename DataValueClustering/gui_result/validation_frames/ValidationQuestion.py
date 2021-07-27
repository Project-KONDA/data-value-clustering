from tkinter import Frame, StringVar, Label, font


class ValidationQuestion:

    def __init__(self, parent, question, explanation):

        self.root = parent
        self.question = question
        self.explanation = explanation

        # frame:
        self.frame = Frame(self.root, highlightthickness=1, highlightbackground='grey', bg='white')

        # question label:
        self.label_text = StringVar()
        self.label_text.set(self.question)
        self.label = Label(self.frame, anchor='w', textvariable=self.label_text, bg='white', padx=5,
                           font=font.Font(size=14))
        self.label.grid(row=0, column=1, sticky='w', columnspan=2)

        # explanation label:
        self.explanation_text = StringVar()
        self.explanation_text.set(self.explanation)
        self.label_explanation = Label(self.frame, anchor='nw', textvariable=self.explanation_text, bg='white', padx=5,
                                       wraplength=500, justify='left')
        self.label_explanation.grid(row=1, column=1, sticky='w', columnspan=2)

    def get_result(self):
        pass

    def update_advice(self):
        pass