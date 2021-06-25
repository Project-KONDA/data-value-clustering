from tkinter import Tk, StringVar, Label, OptionMenu, Button

import numpy as np


def input_dropdown(title, labels, matrix, initial_indices=None):
    dropdown = DropdownInput(title, labels, matrix, initial_indices)
    result = dropdown.get()
    return result


class DropdownInput:
    """ GUI for multiple dropdown menus """

    def __init__(self, title, labels, option_array, initial_indices=None):
        self.title = title
        self.label_text = labels
        self.num = len(labels)
        self.options = option_array

        if initial_indices is None:
            self.initial_indices = list(np.full(self.num, 0))
        else:
            self.initial_indices = initial_indices

        assert self.num == len(option_array) > 0
        assert self.initial_indices is None or len(self.initial_indices) == self.num

        self.root = Tk()
        self.root.title(self.title)

        self.label = np.empty(self.num, dtype=Label)
        self.option_menu = np.empty(self.num, dtype=OptionMenu)
        # self.optionmenu = np.full(self.num, OptionMenu(self.root))

        self.root.bind_all("<Return>", self.close)

        self.answers = np.empty(self.num, dtype=StringVar)

        # self.root.geometry("570x110")

        for i in range(self.num):
            if self.initial_indices[i] not in range(len(self.options[i])):
                self.initial_indices[i] = 0
            self.answers[i] = StringVar(value=self.options[i][self.initial_indices[i]])

            self.label[i] = Label(self.root, text=self.label_text[i], justify='left', width=15)
            self.label[i].grid(row=i, column=3, sticky='we')
            self.option_menu[i] = OptionMenu(self.root, self.answers[i], *self.options[i])
            self.option_menu[i].grid(row=i, column=4, sticky='we')

        self.button = Button(self.root, text='OK', command=self.close)
        self.button.grid(sticky='nswe', row=self.num + 6, column=3, columnspan=2)

        # Center Window on Screen
        self.root.update_idletasks()
        midx = max(0, self.root.winfo_screenwidth() // 2 - self.root.winfo_reqwidth() // 2)
        midy = max(0, self.root.winfo_screenheight() // 3 - self.root.winfo_reqheight() // 2)
        self.root.geometry(f"+%s+%s" % (midx, midy))

        self.root.after(1, lambda: self.root.focus_force())
        self.root.mainloop()

    def close(self, event=None):
        self.root.destroy()

    def get(self):
        answer_choice = list()
        answer_index = list()
        for i in range(self.num):
            answer_test = self.answers[i].get()
            answer_choice.append(answer_test)
            answer_index.append(list(self.options[i]).index(answer_test))
        return answer_choice, answer_index


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
    answer, index = input_dropdown(title, labels, matrix)
    print("Result:", answer, index)

