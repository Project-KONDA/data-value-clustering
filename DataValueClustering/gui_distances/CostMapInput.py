from tkinter import *
from tkinter.font import Font

import numpy as np

from gui_distances.distance_warnings import create_array_of_empty_lists, redundant_char_warning, update_label_text, \
    undefined_char_warning, update_warning_for_entry, update_global_warning, set_tool_tips, undo_highlight_entries, \
    update_warnings, update_warnings_no_vars
from gui_general import CreateToolTip
from gui_general.help_popup_gui import menu_help_cost_map
from gui_distances.costmapinput_helper import validate_input_float, print_cost_map, get_n_from_map, \
    preprocess_regexes, example_costmap, get_regexes_from_map, groups_to_enumerations
from gui_general.window_size import set_window_size_simple

warning_color = "#ffbb00"


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

        self.canceled = False
        self.n = n if n is not None \
            else len(regexes) if regexes is not None \
            else self.map_n if costmap is not None \
            else 7

        self.root = Toplevel(master)
        self.root.resizable(True, True)
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

        heading = "Weight the influence of characters on the dissimilarity between data values"
        font = Font(family="TkDefaultFont", size=12, weight="bold")
        self.title = Label(self.root,
                           text=heading,
                           bg="white",
                           font=font, anchor='c', justify="center")

        caption_width = font.measure(heading)

        self.hint = Label(self.root,
                          text="Choose heigher weights for characters that you do not expect to find frequently in the data values and that may cause great dissimilarity.",
                          bg="white", anchor='c', justify="center",  wraplength=caption_width)

        if suggestion is not None:
            self.label_suggested = Label(self.root, text="Advice based on the evaluation: " + suggestion, wraplength=caption_width,
                                         bg="white", anchor='w', fg='blue', justify='left')
            self.title.grid(sticky='nswe', row=0, column=1, columnspan=4, pady=(10, 0))
            self.hint.grid(sticky='nswe', row=1, column=1, columnspan=4, pady=(0, 0))
            self.label_suggested.grid(row=2, column=1, sticky='senw', columnspan=4, pady=(0, 10), padx=10)
        else:
            self.title.grid(sticky='nswe', row=0, column=1, columnspan=4, pady=(10, 0))
            self.hint.grid(sticky='nswe', row=1, column=1, columnspan=4, pady=(0, 10))

        self.label_warning = Label(self.root, text="", wraplength=caption_width, bg=warning_color, anchor='nw',
                                   justify='left', borderwidth=1, relief="solid")
        self.label_warning.grid(sticky='ns', row=3, column=1, columnspan=4, pady=(0, 10), padx=10)

        # Frames and Canvas

        self.frame = Frame(self.root, relief="groove", borderwidth=2, bg="white")

        self.frame.grid(sticky='nswe', row=4, column=1, columnspan=4)

        self.root.rowconfigure(4, weight=1)
        self.root.columnconfigure(4, weight=1)
        self.frame.rowconfigure(1, weight=1)
        self.frame.columnconfigure(2, weight=1)

        self.scrollbarE = Scrollbar(self.frame, orient='vertical')
        self.scrollbarS = Scrollbar(self.frame, orient='horizontal')

        def scrollbarSet(scrollbar, low, high):
            if float(low) <= 0.0 and float(high) >= 1.0:
                scrollbar.grid_remove()
            else:
                if scrollbar.grid_info() == {}:
                    scrollbar.grid()
            scrollbar.set(low, high)

        self.canvasNE = Canvas(self.frame, height=5, highlightthickness=0,
                               yscrollcommand=self.scrollbarE.set)
        self.canvasSW = Canvas(self.frame, width=100, highlightthickness=0,
                               xscrollcommand=self.scrollbarS.set)
        self.canvasSE = Canvas(self.frame, highlightthickness=0,
                               yscrollcommand=lambda l, h: scrollbarSet(self.scrollbarE, l, h),
                               xscrollcommand=lambda l, h: scrollbarSet(self.scrollbarS, l, h))

        self.canvasNE.xview_moveto(0)
        self.canvasNE.yview_moveto(0)
        self.canvasSW.xview_moveto(0)
        self.canvasSW.yview_moveto(0)
        self.canvasSE.xview_moveto(0)
        self.canvasSE.yview_moveto(0)

        self.canvasNE.grid(sticky='nswe', row=0, column=2, padx=3)
        self.canvasSW.grid(sticky='nswe', row=1, column=0, columnspan=2, pady=3)
        self.canvasSE.grid(sticky='nswe', row=1, column=2, padx=3, pady=3)
        self.scrollbarE.grid(sticky='nes', row=1, column=3)
        self.scrollbarS.grid(sticky='sew', row=2, column=2)

        self.scrollableframeNE = Frame(self.canvasNE)
        self.canvasNE.create_window((0, 0), window=self.scrollableframeNE, anchor='nw')
        self.scrollableframeSW = Frame(self.canvasSW)
        self.canvasSW.create_window((0, 0), window=self.scrollableframeSW, anchor='nw')
        self.scrollableframeSE = Frame(self.canvasSE)
        self.canvasSE.create_window((0, 0), window=self.scrollableframeSE, anchor='nw')

        def configE(command, amount, units=None):
            self.canvasSW.yview(command, amount, units)
            self.canvasSE.yview(command, amount, units)

        def configS(command, amount, units=None):
            self.canvasNE.xview(command, amount, units)
            self.canvasSE.xview(command, amount, units)

        self.scrollbarE.config(command=configE)
        self.scrollbarS.config(command=configS)

        def _configure_scrollable_frame(event, scrollable_frame, canvas, outer_frame, w=False, h=False):
            canvas.config(scrollregion=scrollable_frame.bbox("all"))

            if w and scrollable_frame.winfo_reqwidth() != canvas.winfo_width():
                canvas.config(width=scrollable_frame.winfo_reqwidth())
                outer_frame.config(width=scrollable_frame.winfo_reqwidth())

            if h and scrollable_frame.winfo_reqheight() != canvas.winfo_height():
                canvas.config(height=scrollable_frame.winfo_reqheight())
                outer_frame.config(height=scrollable_frame.winfo_reqheight())

        self.scrollableframeNE.bind('<Configure>',
                                    lambda event: _configure_scrollable_frame(event, self.scrollableframeNE,
                                                                              self.canvasNE, self.frame, w=True))

        self.scrollableframeSW.bind('<Configure>',
                                    lambda event: _configure_scrollable_frame(event, self.scrollableframeSW,
                                                                              self.canvasSW, self.frame, h=True, w=True))

        self.scrollableframeSE.bind('<Configure>',
                                    lambda event: _configure_scrollable_frame(event, self.scrollableframeSE,
                                                                              self.canvasSE, self.frame, h=True,
                                                                              w=True))

        # Labels and Entry Fields

        case_change_label = Label(self.frame, width=17, text='Capitalization change:')
        case_change_label.grid(sticky=NW, row=0, column=0)
        CreateToolTip(case_change_label,
                      "Weight for the substitution of any lower case letter by its upper case variant or vice versa.")
        self.case_entry = Entry(self.frame, width=10, validate='key', justify=RIGHT, borderwidth=2,
                                validatecommand=(self.case_entry.register(validate_input_float), '%P'))
        if not self.empty and self.costmap is None:
            self.case_entry.insert(END, '.5')
        elif not self.empty and self.costmap is not None:
            self.case_entry.insert(END, str(self.costmap[()]))

        self.case_entry.grid(sticky=NW, row=0, column=1)

        self.tooltips = list()

        for i in range(self.n):
            self.label[i] = Label(self.scrollableframeNE, width=7, bg='ivory2', anchor=W, relief="groove", borderwidth=2)
            self.label[i].grid(sticky=NW, row=9, column=i, padx=(0, 1))
            self.regex[i] = Entry(self.scrollableframeSW, width=20, bg='white', validate=ALL, validatecommand=(
                self.regex[i].register(lambda s, i2=i: self.copy_to_column(i2, s)), '%P'))
            self.regex_label[i] = Label(self.scrollableframeSW, anchor=W, justify="left")
            self.regex[i].grid(sticky=NW, row=i, column=1)
            self.regex_label[i].grid(sticky=NW, row=i, column=4, columnspan=1)

            if i == 0:
                self.regex[i].insert(END, '<insert>')
                CreateToolTip(self.regex[i], "This row contains the weights for the insertion of characters.")
                self.label[i].configure(text='<delete>', state='disabled')
                CreateToolTip(self.label[i], "This column contains the weights for the deletion of characters.")
                self.regex[i].config(state='disabled')
            elif i == self.n - 1:
                self.regex[i].insert(END, '<rest>')
                CreateToolTip(self.regex[i], "<rest> represents all characters not covered above.")
                self.label[i].configure(text='<rest>', state='disabled')
                CreateToolTip(self.label[i],
                              "<rest> represents all characters not covered above by the columns to the left.")
                self.regex[i].config(state='disabled')
            else:
                if not self.empty and i < len(self.predefined_labels):
                    self.regex[i].insert(END, self.predefined_labels[i])
                    self.label[i].configure(text=self.predefined_labels[i])

            for j in range(self.n):
                self.value_entries[i, j] = self.generate_entry(i, j)

        self.costmap = None

        # BUTTONS

        self.button_ok = Button(self.root, text='OK', command=self.button_click_output_map,
                                justify=RIGHT, background='snow')
        self.button_ok.grid(sticky="nswe", row=5, column=4, pady=2, padx=2)

        self.button_reset = Button(self.root, text='Reset', command=self.reset_groups,
                                   background='snow', width=16)
        self.button_reset.grid(sticky="nswe", row=5, column=1, pady=2, padx=2)
        self.button_minus = Button(self.root, text='-', command=self.minus,
                                   justify=LEFT, width=3, background='snow')
        self.button_minus.grid(sticky="nswe", row=5, column=2, pady=2, padx=2)

        self.button_plus = Button(self.root, text='+', command=self.plus, justify=RIGHT, width=3, background='snow')
        self.button_plus.grid(sticky="nswe", row=5, column=3, pady=2, padx=2)

        set_window_size_simple(self.root)

        self.root.after(1, lambda: self.root.focus_force())
        self.root.protocol("WM_DELETE_WINDOW", self.cancel)
        self.root.mainloop()

    def generate_entry(self, i, j):
        entry = Entry(self.scrollableframeSE, validate='key', width=7, justify=RIGHT, bg='alice blue')
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
        if i + j > 0:
            entry.grid(sticky=NW, column=i, row=j, padx=5, pady=1)
        return entry

    def reset_groups(self):
        blob_configuration = self.configuration.create_blob_configuration()
        newtexts = list(blob_configuration[1:, 1])
        new_n = len(newtexts)+1

        while self.n < new_n:
            self.plus()
        while self.n > new_n:
            self.minus()
        for i in range(new_n):
            if i > 0 and i < new_n-1:
                t = newtexts[i-1]
                self.regex[i].delete(0, END)
                self.regex[i].insert(0, t)
            for j in range(self.n):
                self.value_entries[i, j].delete(0, END)
                self.value_entries[i, j].insert(0, int(i != j))
        self.costmap = None

    def copy_to_column(self, regex_index, text):
        if self.updating_labels:
            return
        self.updating_labels = True
        self.label[regex_index].configure(text=text)

        if self.abstraction is None:
            return

        undo_highlight_entries(self.regex, self.label_warning)

        update_warnings_no_vars(self.regex, self.label_warning, self.n, self.regex_label, self.abstraction, self.tooltips, 1,
                        regex_index, text, None, None, True)

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
        self.regex[self.n - 1] = Entry(self.scrollableframeSW, width=20, bg='white', validate=ALL)
        self.regex[self.n - 1]['validatecommand'] = (
            self.regex[self.n - 1].register(lambda s, i2=self.n - 1: self.copy_to_column(i2, s)), '%P')

        self.regex_label[self.n - 1] = Label(self.scrollableframeSW, anchor=W)
        self.label[self.n - 1] = Label(self.scrollableframeNE, width=7, bg='ivory2', anchor=W, relief="groove", borderwidth=2)

        for i in range(self.n + 1):
            for j in range(self.n + 1):
                if i + j == 0:
                    continue
                if not self.value_entries[i, j]:
                    self.value_entries[i, j] = self.generate_entry(i, j)
                self.value_entries[i, j]['validatecommand'] = (self.value_entries[i, j].register(
                    lambda s, i2=i, j2=j: self.validate_input_float_copy(text=s, i2=i2, j2=j2)), '%P')

        # 4. place elements
        self.regex[self.n - 1].grid(sticky=NW, row=self.n - 1, column=1, columnspan=3)
        self.regex[self.n].grid(sticky=NW, row=self.n, column=1)
        self.label[self.n - 1].grid(sticky=NW, row=9, column=self.n - 1, padx=(0, 1))
        self.label[self.n].grid(sticky=NW, row=9, column=self.n, padx=(0, 1))
        self.regex_label[self.n - 1].grid(sticky=NW, row=self.n - 1, column=4, columnspan=1)
        self.regex_label[self.n].grid(sticky=NW, row=self.n, column=4, columnspan=1)

        for j in range(self.n + 1):
            for i in range(self.n + 1):
                if i > self.n - 2 or j > self.n - 2:
                    if self.value_entries[i, j]:
                        self.value_entries[i, j].grid(sticky=NW, column=i, row=j)
                    else:
                        print("not", i, j)

        # 5. complete
        self.n = self.n + 1
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
            self.regex[self.n - 1].grid(sticky=NW, row=self.n - 1, column=1)
            self.label[self.n - 1].grid(sticky=NW, row=9, column=self.n - 1, padx=(0, 1))
            self.regex_label[self.n - 1].grid(sticky=NW, row=self.n - 1, column=4, columnspan=1)

            for j in range(self.n):
                for i in range(self.n):
                    if i > self.n - 2 or j > self.n - 2:
                        self.value_entries[i, j].grid(sticky=NW, column=i, row=j)
                        self.value_entries[i, j]['validatecommand'] = (self.value_entries[i, j].register(
                            lambda s, i2=i, j2=j: self.validate_input_float_copy(text=s, i2=i2, j2=j2)), '%P')

            # 6. complete
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
        return self.costmap


def input_costmap(root, size=None, empty=False, regexes=None, costmap=None, abstraction=None, suggestion=None,
                  configuration=None):
    if size is not None:
        size += 2
    assert (size is None or size in range(2, 21))
    myMap = CostMapInput(root, n=size, regexes=regexes, costmap=costmap, empty=empty, abstraction=abstraction,
                         suggestion=suggestion, configuration=configuration)
    return myMap.get()


if __name__ == '__main__':
    test_regexes = ["^$", "^a$", "^b$", "^c$", "^d$"]
    test_regexes = ["", "0-9", "a-z", "A-Z", "$"]
    test_costmap = example_costmap()

    # print_cost_map(input_costmap(costmap=test_costmap))

    print_cost_map(input_costmap(Tk(), regexes=test_regexes))

    # print_cost_map(input_costmap(9))
    # print_cost_map(input_costmap(9, True))
