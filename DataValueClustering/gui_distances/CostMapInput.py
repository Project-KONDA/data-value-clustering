from tkinter import *
import numpy as np

from gui_general.help_popup_gui import menu_help_cost_map
from gui_distances.costmapinput_helper import validate_input_float, print_cost_map, character_escape, get_n_from_map, \
    preprocess_regexes, example_costmap, get_regexes_from_map, groups_to_enumerations


def input_costmap(root, size=None, empty=False, regexes=None, costmap=None, abstraction=None, suggestion=None, configuration=None):
    if size is not None:
        size += 2
    assert (size is None or size in range(2, 21))
    myMap = CostMapInput(root, n=size, regexes=regexes, costmap=costmap, empty=empty, abstraction=abstraction, suggestion=suggestion, configuration=configuration)
    return myMap.get()


class CostMapInput:
    """ GUI for direct input of the weight matrix for configuring the weighted levenstein distance function """

    def __init__(self, master, n=None, regexes=None, costmap=None, empty=False, abstraction=None, suggestion=None, configuration=None):
        if costmap is not None:
            regexes = None
        self.master = master
        self.regexes = regexes
        self.costmap = costmap
        self.map_n = get_n_from_map(costmap) if costmap is not None else -1
        self.empty = empty
        self.abstraction = abstraction
        self.suggestion = suggestion
        self.configuration = configuration

        self.next_matrix_view = None

        self.canceled = False
        self.n = n if n is not None \
            else len(regexes) if regexes is not None \
            else self.map_n if costmap is not None \
            else 7

        self.root = Toplevel(master)
        self.root.focus_force()
        self.root.grab_set()

        self.root.bind_all("<Return>", self.button_click_output_map)

        self.regex = np.full(self.n, Entry(self.root))
        self.regex_label = np.full(self.n, Label(self.root))
        self.label = np.full(self.n, Label(self.root))
        self.value_entries = np.full((self.n, self.n), Entry(self.root))

        self.predefined_labels = \
            preprocess_regexes(regexes) if regexes is not None \
                else preprocess_regexes(get_regexes_from_map(costmap)) if costmap is not None \
                else ['delete', 'a-z', 'A-Z', '0-9', '.,:;?!', '+-*/%=<>&|', '()[]{}', '"\'`´', '_\\#~§^°µ@²³']

        self.case_entry = Entry(self.root)

        self.root.title('Dissimilarity Configuration - Matrix')
        self.root.configure(background='white')
        # self.root.resizable(False, False)

        menu = Menu(self.root)
        menu.add_command(label='Help', command=lambda: menu_help_cost_map(self.root))
        self.root.config(menu=menu)

        self.title = Label(self.root,
                           text="Weight the influence of characters on the dissimilarity between data values",
                           bg="white",
                           font=('TkDefaultFont', 12, 'bold'), anchor='c', justify="center", pady=10)
        self.title.grid(sticky='nswe', row=0, column=1, columnspan=self.n+4)

        if suggestion is not None:
            self.label_suggested = Label(self.root, text="Advice based on your answers to the clustering evaluation questionnaire:" + suggestion, wraplengt=800, bg="white", anchor='w', pady=10, fg='blue', justify='left')
            self.label_suggested.grid(row=1, column=1, sticky='senw', columnspan=self.n+4)

        Label(self.root, text='Case Change:', background='white').grid(sticky=W, row=9, column=1, columnspan=2)
        self.case_entry = Entry(self.root, width=10, validate='key', justify=RIGHT,
                                validatecommand=(self.case_entry.register(validate_input_float), '%P'))
        if not self.empty and self.costmap is None:
            self.case_entry.insert(END, '.5')
        elif not self.empty and self.costmap is not None:
            self.case_entry.insert(END, str(self.costmap[()]))

        self.case_entry.grid(sticky=W, row=9, column=4)

        for i in range(self.n):
            self.label[i] = Label(self.root, width=7, bg='lightgrey', anchor=W)
            self.label[i].grid(sticky=W, row=9, column=i + 5)
            self.regex[i] = Entry(self.root, width=20, bg='ivory2', validate=ALL, validatecommand=(
                self.regex[i].register(lambda s, i2=i: self.copy_to_column(i2, s)), '%P'))
            self.regex_label[i] = Label(self.root, anchor=W)
            self.regex[i].grid(row=i + 10, column=1, columnspan=3)
            self.regex_label[i].grid(sticky="nswe", row=i + 10, column=4, columnspan=1)

            if i == 0:
                self.regex[i].insert(END, '<insert>')
                self.label[i].configure(text='<delete>', state='disabled')
                self.regex[i].config(state='disabled')
            elif i == self.n - 1:
                self.regex[i].insert(END, '<rest>')
                self.label[i].configure(text='<rest>', state='disabled')
                self.regex[i].config(state='disabled')
            else:
                if not self.empty and i < len(self.predefined_labels):
                    self.regex[i].insert(END, self.predefined_labels[i])
                    self.label[i].configure(text=self.predefined_labels[i])

            for j in range(self.n):
                if j == 0 and i == 0:
                    continue

                self.value_entries[i, j] = Entry(self.root, validate='key', width=7, justify=RIGHT, bg='alice blue')
                self.value_entries[i, j]['validatecommand'] = (
                    self.value_entries[i, j].register(
                        lambda s, i2=i, j2=j: self.validate_input_float_copy(text=s, i2=i2, j2=j2)), '%P')  # , '%d')
                self.value_entries[i, j].grid(column=i + 5, row=j + 10)

                if not self.empty:
                    if self.costmap is None or i >= self.map_n or j >= self.map_n:
                        self.value_entries[i, j].insert(END, int(i != j))
                    else:
                        self.value_entries[i, j].insert(END, self.costmap[(i, j)])
                if i == j:
                    self.value_entries[i, i].config(bg='floral white')
                if i > j:
                    self.value_entries[i, j].config(state='readonly')

        self.button_ok = Button(self.root, text='OK', command=self.button_click_output_map,
                                justify=RIGHT, background='snow')
        self.button_ok.grid(sticky="nswe", row=self.n + 12, column=4, columnspan=self.n + 3, pady=2, padx=2)

        self.button_reset = Button(self.root, text='Reset', command=self.reset_groups,
                                   justify=LEFT, width=3, background='snow')
        self.button_reset.grid(sticky=E, row=self.n + 12, column=1, pady=2, padx=2)
        self.button_minus = Button(self.root, text='-', command=self.minus,
                                   justify=LEFT, width=3, background='snow')
        self.button_minus.grid(sticky=E, row=self.n + 12, column=2, pady=2, padx=2)

        self.button_plus = Button(self.root, text='+', command=self.plus, justify=RIGHT, width=3, background='snow')
        self.button_plus.grid(sticky=W, row=self.n + 12, column=3, pady=2, padx=2)

        # Center Window on Screen
        self.root.update_idletasks()
        midx = max(0, self.root.winfo_screenwidth() // 2 - self.root.winfo_reqwidth() // 2)
        midy = max(0, self.root.winfo_screenheight() // 3 - self.root.winfo_reqheight() // 2)
        self.root.geometry(f"+%s+%s" % (midx, midy))

        self.root.after(1, lambda: self.root.focus_force())
        self.root.protocol("WM_DELETE_WINDOW", self.cancel)
        self.root.mainloop()

    def reset_groups(self):
        blob_configuration = self.configuration.create_blob_configuration()
        self.root.withdraw()
        self.next_matrix_view = input_costmap(self.root, regexes=list(blob_configuration[1:, 1]), costmap=self.costmap,
                                         abstraction=blob_configuration[1:, 0:2], suggestion=self.suggestion, configuration=self.configuration)
        self.quit()

    def copy_to_column(self, i, text):
        if type(self.regex[i]) is Entry and \
                type(self.label[i]) is Label and \
                type(self.regex_label[i] is Label):
            self.label[i].configure(text=text)
            self.regex_label[i].configure(text=self.text_map(text))
        return True

    def text_map(self, text):
        if self.abstraction is None:
            return ""
        label_text = ""
        separator = " & "
        other_chars = text
        for i, chars in enumerate(self.abstraction[:, 1]):
            if chars in text:
                label_text += self.abstraction[i, 0] + separator
                other_chars = other_chars.replace(chars, "")
        if other_chars != "":
            print(other_chars)
            label_text += "individual" + separator
        k = len(label_text) - len(separator)
        label_text = label_text[0:k]
        return label_text

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

    def build_output_map(self):
        self.costmap = {}
        # set case-sensitive weight
        text = self.case_entry.get()
        if text != '':
            self.costmap[()] = float(text)
        else:
            self.costmap[()] = 1.

        # single character regex
        self.costmap[0] = ''
        for i in range(1, self.n):
            self.costmap[i] = groups_to_enumerations(self.label[i].cget("text"))

        # weights
        for i in range(self.n):
            for j in range(self.n):
                v = self.value_entries[i, j].get()
                if v != '':
                    self.costmap[(i, j)] = float(v)
                else:
                    self.costmap[(i, j)] = 1. + (i != j)

    def button_click_output_map(self, event=None):
        self.build_output_map()
        self.root.quit()
        self.root.destroy()

    def plus(self):
        regex = np.full(self.n + 1, None)
        label = np.full(self.n + 1, None)
        regex_label = np.full(self.n + 1, None)
        label_text = np.full(self.n + 1, "", dtype=object)
        value_entries = np.full((self.n + 1, self.n + 1), Entry(self.root))

        for i in range(self.n):
            regex[i] = self.regex[i]
            label[i] = self.label[i]
            regex_label[i] = self.regex_label[i]
            for j in range(self.n):
                value_entries[i, j] = self.value_entries[i, j]

        self.regex = regex
        self.label = label
        self.value_entries = value_entries
        self.regex_label = regex_label

        self.regex[self.n-1].config(state='normal')
        self.regex[self.n - 1].delete(0, END)

        self.label[self.n] = Label(self.root, width=7, bg='lightgrey', anchor=W)
        self.label[self.n].grid(sticky=W, row=9, column=self.n + 5)

        self.regex[self.n] = Entry(self.root, width=20, bg='ivory2', validate=ALL)
        self.regex[self.n].insert(0, '<rest>')
        self.regex[self.n].config(state='disabled')

        self.regex[self.n]['validatecommand'] = (
            self.regex[self.n].register(lambda s, i2=self.n: self.copy_to_column(i2, s)), '%P')  # , '%d')
        self.regex[self.n].grid(row=self.n + 10, column=1, columnspan=3)
        self.regex_label[self.n] = Label(self.root, anchor=W)
        self.regex_label[self.n].grid(sticky="nswe", row=self.n + 10, column=4, columnspan=1)

        # TODO:
        # self.regex_label[self.n]

        for j in range(self.n):
            self.value_entries[self.n, j] = Entry(self.root, validate='key', width=7, justify=RIGHT, bg='alice blue')
            self.value_entries[self.n, j]['validatecommand'] = (
                self.value_entries[self.n, j].register(
                    lambda s, i2=self.n, j2=j: self.validate_input_float_copy(text=s, i2=i2, j2=j2)), '%P')  # , '%d')
            self.value_entries[self.n, j].grid(column=self.n + 5, row=j + 10)
            self.value_entries[self.n, j].config(state='readonly')

            self.value_entries[j, self.n] = Entry(self.root, validate='key', width=7, justify=RIGHT, bg='alice blue')
            self.value_entries[j, self.n]['validatecommand'] = (
                self.value_entries[j, self.n].register(
                    lambda s, i2=j, j2=self.n: self.validate_input_float_copy(text=s, i2=i2, j2=j2)), '%P')  # , '%d')
            self.value_entries[j, self.n].grid(column=j + 5, row=self.n + 10)

            if not self.empty:
                self.value_entries[self.n, j].insert(END, int(self.n != j))
                self.value_entries[j, self.n].insert(END, int(self.n != j))
        self.value_entries[self.n, self.n] = Entry(self.root, validate='key', width=7, justify=RIGHT, bg='alice blue')
        self.value_entries[self.n, self.n].config(bg='floral white')
        self.value_entries[self.n, self.n]['validatecommand'] = (
            self.value_entries[self.n, self.n].register(
                lambda s, i2=self.n, j2=self.n: self.validate_input_float_copy(text=s, i2=i2, j2=j2)), '%P')  # , '%d')
        self.value_entries[self.n, self.n].grid(column=self.n + 5, row=self.n + 10)
        if not self.empty:
            self.value_entries[self.n, self.n].insert(END, int(i != j))

        self.n = self.n + 1
        self.button_ok.grid(sticky="nswe", row=self.n + 12, column=4, columnspan=self.n + 3, pady=2, padx=2)
        self.button_reset.grid(sticky=E, row=self.n + 12, column=1, pady=2, padx=2)
        self.button_minus.grid(sticky=E, row=self.n + 12, column=2, pady=2, padx=2)
        self.button_plus.grid(sticky=W, row=self.n + 12, column=3, pady=2, padx=2)

    def minus(self):
        if self.n > 2:
            self.n = self.n - 1
            self.button_ok.grid(sticky="nswe", row=self.n + 12, column=4, columnspan=self.n + 3, pady=2, padx=2)
            self.button_reset.grid(sticky=E, row=self.n + 12, column=1, pady=2, padx=2)
            self.button_minus.grid(sticky=E, row=self.n + 12, column=2, pady=2, padx=2)
            self.button_plus.grid(sticky=W, row=self.n + 12, column=3, pady=2, padx=2)

            regex = np.full(self.n, Entry(self.root))
            regex_label = np.full(self.n, Label(self.root))
            label = np.full(self.n, Label(self.root))
            value_entries = np.full((self.n, self.n), Entry(self.root))

            self.regex[self.n].destroy()
            self.label[self.n].destroy()
            for i in range(self.n):
                self.value_entries[i, self.n].destroy()
                self.value_entries[self.n, i].destroy()
            self.value_entries[self.n, self.n].destroy()
            self.regex_label[self.n].destroy()

            for i in range(self.n):
                regex[i] = self.regex[i]
                label[i] = self.label[i]
                regex_label[i] = self.regex_label[i]
                for j in range(self.n):
                    value_entries[i, j] = self.value_entries[i, j]
            self.regex = regex
            self.label = label
            self.value_entries = value_entries
            self.regex_label = regex_label

            self.regex[self.n - 1].delete(0, END)
            self.regex[self.n - 1].insert(0, "<rest>")
            self.regex[self.n - 1].config(state='disabled')

    def update_regex_label(self):
        pass

    def unbind_all(self):
        self.root.unbind_all("<Return>")

    def cancel(self):
        self.canceled = True
        self.quit()

    def quit(self):
        self.root.update()
        self.unbind_all()
        self.root.quit()
        self.root.destroy()

    def get(self):
        if self.canceled:
            return None
        if self.next_matrix_view is not None:
            return self.next_matrix_view
        return self.costmap


if __name__ == '__main__':
    test_regexes = ["^$", "^a$", "^b$", "^c$", "^d$"]
    test_regexes = ["", "0-9", "a-z", "A-Z", "$"]
    test_costmap = example_costmap()

    # print_cost_map(input_costmap(costmap=test_costmap))

    print_cost_map(input_costmap(Tk(), regexes=test_regexes))

    # print_cost_map(input_costmap(9))
    # print_cost_map(input_costmap(9, True))
