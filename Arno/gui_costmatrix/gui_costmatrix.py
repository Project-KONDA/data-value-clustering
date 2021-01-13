from tkinter import *
import numpy as np

from gui_costmatrix_helper import validate_input_float, character_escape, matrix_is_valid, print_cost_matrix
from gui_costmatrix_menu import menu_help_cost_matrix


def input_costmatrix(size, empty=False):
    size += 2
    assert (size in range(2, 21))
    myMatrix = CostMatrix(size)
    myMatrix.record_matrix(empty)
    return myMatrix.matrix


class CostMatrix:

    def __init__(self, n):
        self.n = n
        self.root = Tk()
        self.value_entries = np.full((self.n, self.n), Entry(self.root))

        self.regex = np.full(self.n, None)

        self.label = np.full(self.n, None)
        self.label_text = np.full(self.n, "", dtype=object)
        self.example_labels = ['delete', 'a-z', 'A-Z', '0-9', '.,:;?!', '+-*/%=<>&|', '()[]{}', '"\'`´', '_\\#~§^°µ@²³']

        self.case_entry = Entry(self.root)
        self.matrix = {}

    def copy_to_column(self, i, text):
        if type(self.regex[i]) is Entry and type(self.label[i]) is Label:
            # text = self.regex[i].get()
            self.label_text[i] = text
            self.label[i].configure(text=text)
        return True

    def validate_input_float_copy(self, text, i2, j2):
        if not validate_input_float(text):
            return False
        if i2 < j2:
            # print(str(self) + " " + text + " " + str(i2) + " " + str(j2))
            self.value_entries[j2, i2].config(state='normal')
            self.value_entries[j2, i2].delete(0, END)
            self.value_entries[j2, i2].insert(0, text)
            self.value_entries[j2, i2].config(state='readonly')
        return True

    # main matrix record GUI
    def record_matrix(self, empty=False):
        # self.root.title('Cost Matrix')
        self.root.title('Please enter Cost Matrix')
        self.root.configure(background='white')
        width = 220 + 48 * self.n  # 300 #270 # 240
        # width = max(470, 220 + 48 * self.n)  # 300 #270 # 240
        height = 55 + 19 * self.n  # 130 # 110 # 90
        width_text = str(width) + "x" + str(height)
        self.root.geometry(width_text)

        menu = Menu(self.root)
        menu.add_command(label='Help', command=menu_help_cost_matrix)
        self.root.config(menu=menu)

        Label(self.root, text='Case Change:',
              anchor=W, justify=LEFT, background='white'
              ).grid(row=9, column=2, sticky=W)
        self.case_entry = Entry(self.root, width=10, validate='key', justify=RIGHT)
        if not empty:
            self.case_entry.insert(END, '.5')
        self.case_entry['validatecommand'] = (self.case_entry.register(validate_input_float), '%P')  # , '%d')

        self.case_entry.grid(row=9, column=3, columnspan=2, sticky=W)

        for i in range(self.n):

            self.label[i] = Label(self.root, textvariable=self.label_text[i],
                                  width=6, bg='lightgrey', anchor=W)
            self.label[i].grid(row=9, column=i + 4)

            self.regex[i] = Entry(self.root,
                                  width=35, bg='ivory2',
                                  validate=ALL)
            self.regex[i]['validatecommand'] = (
                self.regex[i].register(lambda s, i2=i: self.copy_to_column(i2, s)), '%P')  # , '%d')

            if i == 0:
                self.regex[i].insert(END, 'add')
                self.label[i].configure(text='delete', state='disabled')

            if i == self.n - 1:
                self.regex[i].insert(END, '<rest>')
                self.label[i].configure(text='<rest>', state='disabled')

            if i == 0 or i == self.n - 1:
                self.regex[i].config(state='disabled')
            else:
                if not empty and i < len(self.example_labels):
                    self.regex[i].insert(END, self.example_labels[i])
                    self.label_text[i] = self.example_labels[i]
                    self.label[i].configure(text=self.example_labels[i])

            self.regex[i].grid(row=i + 10, column=2, columnspan=2)

            for j in range(self.n):
                if j == 0 and i == 0:
                    continue

                self.value_entries[i, j] = Entry(self.root, validate='key', width=7, justify=RIGHT, bg='alice blue')
                self.value_entries[i, j]['validatecommand'] = (
                    self.value_entries[i, j].register(
                        lambda s, i2=i, j2=j: self.validate_input_float_copy(text=s, i2=i2, j2=j2)), '%P')  # , '%d')
                self.value_entries[i, j].grid(column=i + 4, row=j + 10)

                if not empty:
                    self.value_entries[i, j].insert(END, int(i != j))
                if i == j:
                    self.value_entries[i, i].config(bg='floral white')
                if i > j:
                    self.value_entries[i, j].config(state='readonly')

        Button(self.root, text='OK', command=self.button_click_output_matrix,
               justify=RIGHT, width=5 * self.n + 15, background='snow'
               ).grid(row=self.n + 12, column=2, columnspan=self.n + 2)

        self.root.mainloop()

    def build_output_matrix(self):
        # set case-sensitive weight
        text = self.case_entry.get()
        if text != '':
            self.matrix[()] = float(text)
        else:
            self.matrix[()] = 1.

        # single character regex
        self.matrix[0] = '^$'
        for i in range(1, self.n - 1):
            if self.label_text[i] != '':
                self.matrix[i] = character_escape(self.label_text[i])
            else:
                self.matrix[i] = '.^'
        self.matrix[self.n - 1] = '^.$'

        # weights
        for i in range(self.n):
            for j in range(self.n):
                v = self.value_entries[i, j].get()
                if v != '':
                    self.matrix[(i, j)] = float(v)
                else:
                    self.matrix[(i, j)] = 1. + (i != j)

    def button_click_output_matrix(self):
        self.build_output_matrix()
        self.root.destroy()


if __name__ == '__main__':
    print_cost_matrix(input_costmatrix(5, False))
    # print_cost_matrix(input_costmatrix(9))
    # print_cost_matrix(input_costmatrix(9, True))
