from tkinter import *
import numpy as np

from gui_general import CreateToolTip
from gui_general.help_popup_gui import menu_help_cost_map
from gui_distances.costmapinput_helper import validate_input_float, print_cost_map, character_escape, get_n_from_map, \
    preprocess_regexes, example_costmap, get_regexes_from_map, groups_to_enumerations


def input_costmap(root, size=None, empty=False, regexes=None, costmap=None, abstraction=None, suggestion=None,
                  configuration=None):
    if size is not None:
        size += 2
    assert (size is None or size in range(2, 21))
    myMap = CostMapInput(root, n=size, regexes=regexes, costmap=costmap, empty=empty, abstraction=abstraction,
                         suggestion=suggestion, configuration=configuration)
    return myMap.get()


class CostMapInput:
    """ GUI for direct input of the weight matrix for configuring the weighted levenstein distance function """

    def __init__(self, master, n=None, regexes=None, costmap=None, empty=False, abstraction=None, suggestion=None,
                 configuration=None):
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
        self.root.resizable(False, False)
        self.root.focus_force()
        self.root.grab_set()

        self.root.bind_all("<Return>", self.button_click_output_map)

        self.regex = np.full(self.n, Entry(self.root))
        self.regex_label = np.full(self.n, Label(self.root))
        self.label = np.full(self.n, Label(self.root))
        self.value_entries = np.full((self.n, self.n), Entry(self.root))

        self.updating_labels = False

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
                           font=('TkDefaultFont', 12, 'bold'), anchor='c', justify="center")

        self.hint = Label(self.root,
                          text="Choose heigher weights for characters that you do not expect to find frequently in the data values\nand that may cause great dissimilarity.",
                          bg="white", anchor='c', justify="center")

        if suggestion is not None:
            self.label_suggested = Label(self.root, text="Advice based on the evaluation: " + suggestion, wraplengt=800,
                                         bg="white", anchor='w', fg='blue', justify='left')
            self.title.grid(sticky='nswe', row=0, column=1, columnspan=self.n + 4, pady=(10, 0))
            self.hint.grid(sticky='nswe', row=1, column=1, columnspan=self.n + 4, pady=(0, 0))
            self.label_suggested.grid(row=2, column=1, sticky='senw', columnspan=self.n + 4, pady=(0, 10), padx=10)
        else:
            self.title.grid(sticky='nswe', row=0, column=1, columnspan=self.n + 4, pady=(10, 0))
            self.hint.grid(sticky='nswe', row=1, column=1, columnspan=self.n + 4, pady=(0, 10))

        case_change_label = Label(self.root, text='Capitalization change:', background='white')
        case_change_label.grid(sticky=NW, row=9, column=1, columnspan=3)
        CreateToolTip(case_change_label, "Weight for the substitution of any lower case letter by its upper case variant or vice versa.")
        self.case_entry = Entry(self.root, width=10, validate='key', justify=RIGHT,
                                validatecommand=(self.case_entry.register(validate_input_float), '%P'))
        if not self.empty and self.costmap is None:
            self.case_entry.insert(END, '.5')
        elif not self.empty and self.costmap is not None:
            self.case_entry.insert(END, str(self.costmap[()]))

        self.case_entry.grid(sticky=NW, row=9, column=4)

        for i in range(self.n):
            self.label[i] = Label(self.root, width=7, bg='lightgrey', anchor=W)
            self.label[i].grid(sticky=NW, row=9, column=i + 5)
            self.regex[i] = Entry(self.root, width=20, bg='ivory2', validate=ALL, validatecommand=(
                self.regex[i].register(lambda s, i2=i: self.copy_to_column(i2, s)), '%P'))
            self.regex_label[i] = Label(self.root, anchor=W, bg="white")
            self.regex[i].grid(sticky=NW, row=i + 10, column=1, columnspan=3)
            self.regex_label[i].grid(sticky=NW, row=i + 10, column=4, columnspan=1)

            if i == 0:
                self.regex[i].insert(END, '<insert>')
                CreateToolTip(self.regex[i], "This row contains the weights for the insertion of characters.")
                self.label[i].configure(text='<delete>', state='disabled')
                CreateToolTip(self.label[i], "This column contains the weights for the deletion of characters.")
                self.regex[i].config(state='disabled')
            elif i == self.n - 1:
                self.regex[i].insert(END, '<rest>')
                CreateToolTip(self.regex[i], "This row represents any characters not covered above.")
                self.label[i].configure(text='<rest>', state='disabled')
                CreateToolTip(self.label[i], "This column represents any characters not covered by the columns to the left.")
                self.regex[i].config(state='disabled')
            else:
                if not self.empty and i < len(self.predefined_labels):
                    self.regex[i].insert(END, self.predefined_labels[i])
                    self.label[i].configure(text=self.predefined_labels[i])

            for j in range(self.n):
                self.value_entries[i, j] = self.generate_entry(i, j)

        self.button_ok = Button(self.root, text='OK', command=self.button_click_output_map,
                                justify=RIGHT, background='snow')
        self.button_ok.grid(sticky="nswe", row=self.n + 12, column=4, columnspan=self.n + 3, pady=2, padx=2)

        self.button_reset = Button(self.root, text='Reset', command=self.reset_groups,
                                   justify=LEFT, background='snow')
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

    def generate_entry(self, i, j):
        if i == 0 and j == 0:
            return None
        entry = Entry(self.root, validate='key', width=7, justify=RIGHT, bg='alice blue')
        entry['validatecommand'] = (
            entry.register(
                lambda s, i2=i, j2=j: self.validate_input_float_copy(text=s, i2=i2, j2=j2)), '%P')  # , '%d')
        if not self.empty:
            if self.costmap is None or i >= self.map_n or j >= self.map_n:
                entry.insert(END, int(i != j))
            else:
                entry.insert(END, self.costmap[(i, j)])
        if i == j:
            entry.config(bg='floral white')
        if i > j:
            entry.config(state='readonly')
        entry.grid(sticky=NW, column=i + 5, row=j + 10)
        return entry

    def reset_groups(self):
        blob_configuration = self.configuration.create_blob_configuration()
        self.root.withdraw()
        self.next_matrix_view = input_costmap(self.root, regexes=list(blob_configuration[1:, 1]), costmap=self.costmap,
                                              abstraction=blob_configuration[1:, 0:2], suggestion=self.suggestion,
                                              configuration=self.configuration)
        self.quit()

    def copy_to_column(self, i, text):
        if self.updating_labels:
            return
        self.updating_labels = True
        self.label[i].configure(text=text)

        if self.abstraction is None:
            return
        for st in self.regex_label:
            st.config(text="")
        for mapping in self.abstraction.tolist():
            for x, entry in enumerate(self.regex):
                value = text if x == i else entry.get()
                if len(mapping[1]) == 1 and mapping[1] in value:
                    string = self.regex_label[x].cget("text")
                    if string != "":
                        string += "\n"
                    string += "'" + mapping[1] + "' - " + mapping[0]
                    self.regex_label[x].config(text=string)
                    break

        self.updating_labels = False
        return True

    def validate_input_float_copy(self, text, i2, j2):
        if not validate_input_float(text):
            return False
        if i2 < j2 and self.value_entries[j2, i2]:
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
        # 1. create arrays
        regex = np.full(self.n + 1, None)
        label = np.full(self.n + 1, None)
        regex_label = np.full(self.n + 1, None)
        value_entries = np.full((self.n + 1, self.n + 1), None)

        # 2. copy elements
        for i in range(self.n):
            i2 = self.n if i == self.n - 1 else i
            regex[i2] = self.regex[i]
            label[i2] = self.label[i]
            regex_label[i2] = self.regex_label[i]
            for j in range(self.n):
                j2 = self.n if j == self.n - 1 else j
                value_entries[i2, j2] = self.value_entries[i, j]

        self.regex = regex
        self.label = label
        self.value_entries = value_entries
        self.regex_label = regex_label

        # 3. add element n-1
        self.regex[self.n - 1] = Entry(self.root, width=20, bg='ivory2', validate=ALL)
        self.regex[self.n - 1]['validatecommand'] = (
            self.regex[self.n - 1].register(lambda s, i2=self.n: self.copy_to_column(i2, s)), '%P')

        self.regex_label[self.n - 1] = Label(self.root, anchor=W, bg="white")
        self.label[self.n - 1] = Label(self.root, width=7, bg='lightgrey', anchor=W)

        for i in range(self.n + 1):
            for j in range(self.n + 1):
                if i+j == 0:
                    continue
                if not self.value_entries[i, j]:
                    self.value_entries[i, j] = self.generate_entry(i, j)
                self.value_entries[i, j]['validatecommand'] = (self.value_entries[i, j].register(
                    lambda s, i2=i, j2=j: self.validate_input_float_copy(text=s, i2=i2, j2=j2)), '%P')

        # 4. place elements
        self.regex[self.n - 1].grid(sticky=NW, row=self.n + 9, column=1, columnspan=3)
        self.regex[self.n].grid(sticky=NW, row=self.n + 10, column=1, columnspan=3)
        self.label[self.n - 1].grid(sticky=NW, row=9, column=self.n + 4)
        self.label[self.n].grid(sticky=NW, row=9, column=self.n + 5)
        self.regex_label[self.n - 1].grid(sticky=NW, row=self.n + 9, column=4, columnspan=1)
        self.regex_label[self.n].grid(sticky=NW, row=self.n + 10, column=4, columnspan=1)

        for j in range(self.n + 1):
            for i in range(self.n + 1):
                if i > self.n - 2 or j > self.n - 2:
                    if self.value_entries[i, j]:
                        self.value_entries[i, j].grid(sticky=NW, column=i + 5, row=j + 10)
                    else:
                        print("not", i, j)

        # 5. complete
        self.n = self.n + 1
        self.button_ok.grid(sticky="nswe", row=self.n + 12, column=4, columnspan=self.n + 3, pady=2, padx=2)
        self.button_reset.grid(sticky=E, row=self.n + 12, column=1, pady=2, padx=2)
        self.button_minus.grid(sticky=E, row=self.n + 12, column=2, pady=2, padx=2)
        self.button_plus.grid(sticky=W, row=self.n + 12, column=3, pady=2, padx=2)
        self.root.update()

    def minus(self):
        if self.n > 2:
            self.n = self.n - 1

            # 1. create arrays
            regex = np.full(self.n, None)
            label = np.full(self.n, None)
            regex_label = np.full(self.n, None)
            value_entries = np.full((self.n, self.n), None)

            # 2. destroy n-2
            self.regex[self.n - 1].destroy()
            self.label[self.n - 1].destroy()
            self.regex_label[self.n - 1].destroy()

            for i in range(self.n + 1):
                self.value_entries[self.n - 1, i].destroy()
                if i != self.n - 1:
                    self.value_entries[i, self.n - 1].destroy()

            # 3. copy elements
            for i in range(self.n):
                i2 = self.n if i == self.n - 1 else i
                regex[i] = self.regex[i2]
                label[i] = self.label[i2]
                regex_label[i] = self.regex_label[i2]
                for j in range(self.n):
                    j2 = self.n if j == self.n - 1 else j
                    value_entries[i, j] = self.value_entries[i2, j2]

            # 4. complete copy
            self.regex = regex
            self.label = label
            self.value_entries = value_entries
            self.regex_label = regex_label

            # 5. move elements
            self.regex[self.n - 1].grid(sticky=NW, row=self.n + 9, column=1, columnspan=3)
            self.label[self.n - 1].grid(sticky=NW, row=9, column=self.n + 4)
            self.regex_label[self.n - 1].grid(sticky=NW, row=self.n + 9, column=4, columnspan=1)

            for j in range(self.n):
                for i in range(self.n):
                    if i > self.n - 2 or j > self.n - 2:
                        self.value_entries[i, j].grid(sticky=NW, column=i + 5, row=j + 10)
                        self.value_entries[i, j]['validatecommand'] = (self.value_entries[i, j].register(
                            lambda s, i2=i, j2=j: self.validate_input_float_copy(text=s, i2=i2, j2=j2)), '%P')

            # 6. complete
            self.button_ok.grid(sticky="nswe", row=self.n + 12, column=4, columnspan=self.n + 3, pady=2, padx=2)
            self.button_reset.grid(sticky=E, row=self.n + 12, column=1, pady=2, padx=2)
            self.button_minus.grid(sticky=E, row=self.n + 12, column=2, pady=2, padx=2)
            self.button_plus.grid(sticky=W, row=self.n + 12, column=3, pady=2, padx=2)
            self.root.update()

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
