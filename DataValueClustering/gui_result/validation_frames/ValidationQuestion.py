from tkinter import Frame, StringVar, Label, font, PhotoImage


class ValidationQuestion:

    def __init__(self, parent, question_and_explanation, update_advice_function, question_break):

        self.root = parent
        self.question = question_and_explanation[0]
        self.explanation = question_and_explanation[1]
        self.update_suggestion_function = update_advice_function

        # frame:
        self.frame = Frame(self.root, highlightbackground='grey', bg='white', pady=10) # , width=question_break

        pixelVirtual = PhotoImage(width=1, height=1)

        # question label:
        self.label_text = StringVar()
        self.label_text.set(self.question)

        self.label = Label(self.frame, anchor='w', textvariable=self.label_text, bg='white',
                           font=('TkDefaultFont', 12, 'bold'), justify='left', wraplength=question_break, compound="c", width=question_break, image=pixelVirtual)
        self.label.grid(row=0, column=1, sticky='w', columnspan=3)

        self.explanation_text = StringVar()
        self.explanation_text.set(self.explanation)
        self.label_explanation = Label(self.frame, anchor='nw', textvariable=self.explanation_text, bg='white',
                                       wraplength=question_break, justify='left', compound="c", width=question_break, image=pixelVirtual)
        self.label_explanation.grid(row=1, column=1, sticky='w', columnspan=3)

    def get_result(self):
        pass

    def update_advice(self):
        self.update_suggestion_function()