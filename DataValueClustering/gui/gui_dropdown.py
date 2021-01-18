from tkinter import Tk, StringVar, Label, OptionMenu, Button

import numpy as np


class DropdownInput:

    def __init__(self, title, labels, option_array):
        self.title = title
        self.label_text = labels
        self.options = option_array
        self.num = len(option_array)
        print(self.num)

        self.root = Tk()
        self.root.title(self.title)

        self.label = np.empty(self.num, dtype=Label)
        self.option_menu = np.empty(self.num, dtype=OptionMenu)
        # self.optionmenu = np.full(self.num, OptionMenu(self.root))

        self.answers = np.empty(self.num, dtype=StringVar)

        # self.root.geometry("570x110")

        for i in range(self.num):
            self.answers[i] = StringVar(value=self.options[i][0])
            self.label[i] = Label(self.root, text=self.label_text[i], justify='left', width=15)
            self.label[i].grid(row=3, column=i, sticky='we')
            self.option_menu[i] = OptionMenu(self.root, self.answers[i], *self.options[i])
            self.option_menu[i].grid(row=4, column=i, sticky='we')

        self.button = Button(self.root, text='OK', command=self.close)
        self.button.grid(sticky='nswe', row=6, column=0, columnspan=self.num)

        self.root.mainloop()

    def close(self):
        self.root.destroy()

    def get(self):
        answers = list()
        for i in range(self.num):
            answers.append(self.answers[i].get())
        return answers


if __name__ == '__main__':
    title = "My wonderful example title!"
    labels = ["Label0", "Label1", "Label2", "Label3", "Label4", "Label5"]
    matrix = [
        ["Option00", "Option01", "Option02", "Option03", "Option04", "Option05"],
        ["Option10", "Option11"],
        ["Option20", "Option21", "Option22", "Option23"],
        ["Option30", "Option31", "Option32"],
        ["Option40"],
        ["Option50", "Option51", "Option52", "Option53", "Option54"]
    ]
    print(DropdownInput(title, labels, matrix).get())
