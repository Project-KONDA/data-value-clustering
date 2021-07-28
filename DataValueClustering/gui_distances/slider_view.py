from tkinter import Tk, Button, Label, Entry, Scale, IntVar, Toplevel, StringVar, W, LEFT

import numpy as np

from gui_distances.costmapinput_helper import costmap_is_valid, character_escape, print_cost_map, get_n_from_map, \
    example_costmap, groups_to_enumerations
from gui_general import CreateToolTip


def slider_view(master, n=None, costmap=None, abstraction=None, texts=list(), values=None, fixed=False):
    view = SliderInput(master, n, costmap, abstraction, texts, values, fixed)
    return view.get()


class SliderInput:

    def __init__(self, master, n=None, costmap=None, abstraction=None, texts=list(), value=None, fixed=False):
        assert (not (costmap and value))  # (not (costmap and (abstraction_chars_and_names is not None or value)))
        assert (n or costmap or abstraction is not None)

        self.master = master
        self.n = n if n or costmap else len(texts)+1
        self.abstraction = np.array((2, 0)) if abstraction is None else abstraction
        self.texts = texts
        self.abstraction_keys = self.texts
        self.abstraction_values = list() if abstraction is None else abstraction[:, 0].tolist()
        self.values = value
        self.fixed = fixed
        self.updating_labels = False

        self.canceled = False

        if costmap:
            assert (not self.values)
            self.texts = list()
            self.values = list()
            if not n:
                self.n = get_n_from_map(costmap) - 1  # n_rows = amount slider + row for deletion/addition
            for i in range(self.n):
                if i in costmap and (i, 0) in costmap:
                    self.texts.append(costmap[(i + 1)])
                    self.values.append(costmap[(i + 1, 0)])

        self.root = Toplevel(self.master)
        self.root.title("Slider Input")
        self.root.config(bg="white")
        self.root.resizable(False, True)
        self.root.focus_force()
        self.root.grab_set()

        self.title = Label(self.root, text="Slider View", bg="white",
                           font=('bold 12', 19))
        self.label_heading1 = Label(self.root, text="Characters", bg="white", font=('Sans', '10', 'bold'))
        CreateToolTip(self.label_heading1, "Enumerate all characters of this group. Only the first occurrence of a "
                                           "character in one of the groups is relevant. Note that some characters may "
                                           "represent abstracted details. This mapping is provided in the column "
                                           "'Abstraction Mapping'.")
        self.label_heading2 = Label(self.root, text="Abstraction Mapping", bg="white", font=('Sans', '10', 'bold'))
        CreateToolTip(self.label_heading2, "Mapping between characters of the column 'Characters' and the abstracted "
                                           "aspects they represent.")
        self.label_heading3 = Label(self.root, text="Weights", bg="white", font=('Sans', '10', 'bold'))
        CreateToolTip(self.label_heading3, "Weights for the given character groups.")
        self.button_plus = Button(self.root, text='+', command=self.plus, width=3)
        self.button_minus = Button(self.root, text='-', command=self.minus, width=3)
        self.button_ok = Button(self.root, text='OK', command=self.quit)
        if self.fixed:
            self.button_minus.configure(state="disabled")
            self.button_plus.configure(state="disabled")

        self.title.grid(sticky='nswe', row=0, column=1, columnspan=4)
        self.label_heading1.grid(sticky='nsw', row=1, column=1)
        self.label_heading2.grid(sticky='nsw', row=1, column=3)
        self.label_heading3.grid(sticky='nsw', row=1, column=5)
        self.button_minus.grid(sticky='ns', row=self.n + 5, column=1, pady=(10,0))
        self.button_plus.grid(sticky='ns', row=self.n + 5, column=2, pady=(10,0))
        self.button_ok.grid(sticky='nswe', row=self.n + 5, column=5, columnspan=2, pady=(10,0))

        self.entrylist = np.full(self.n, Entry(self.root))
        self.entry_var_list = np.full(self.n, StringVar())
        self.label_list = np.full(self.n, Label(self.root))
        self.sliderlist = np.full(self.n, Scale(self.root))
        self.valuelist = np.full(self.n, IntVar())

        for i in range(0, self.n):
            t = ""
            v = 1
            if self.texts and len(self.texts) > i:
                t = self.texts[i]
            if self.values and len(self.values) > i:
                v = self.values[i]

            self.label_list[i] = Label(self.root, bg="white", anchor=W, justify=LEFT)
            self.valuelist[i] = IntVar(self.root, v)
            self.entry_var_list[i] = StringVar(self.root, t)
            self.entry_var_list[i].trace("w", lambda name, index, mode, sv=self.entry_var_list[i], j=i: self.update_labels())
            self.entry_var_list[i].set("<rest>" if i == self.n-1 else t)
            self.entrylist[i] = Entry(self.root, font="12", textvariable=self.entry_var_list[i])
            if i == self.n-1 or self.fixed:
                self.entrylist[i].configure(state="disabled")

            self.sliderlist[i] = Scale(self.root, from_=0, to_=10, orient='horizontal', variable=self.valuelist[i],
                                       length=400, bg='white', highlightthickness=0, resolution=1)

            self.entrylist[i].grid(sticky='new', row=i + 2, column=1, columnspan=2, pady=(15,0), padx=1)
            self.label_list[i].grid(sticky='new', row=i + 2, column=3, columnspan=2, pady=(15,0), padx=1)
            self.sliderlist[i].grid(sticky='new', row=i + 2, column=5, columnspan=2, pady=(0, 0))

        self.root.protocol("WM_DELETE_WINDOW", self.cancel)
        self.root.mainloop()

    def update_labels(self):
        if self.updating_labels:
            return
        self.updating_labels = True
        abstraction = self.abstraction.tolist()
        entry_from = self.entrylist
        string_to = self.label_list
        for st in string_to:
            st.config(text="")
        for mapping in abstraction:
            for i, entry in enumerate(entry_from):
                value = entry.get()
                if len(mapping[1]) == 1 and mapping[1] in value:
                    string = string_to[i].cget("text")
                    if string != "":
                        string += "\n"
                    string += "'" + mapping[1] + "' - " + mapping[0]
                    string_to[i].config(text=string)
                    break
        self.updating_labels = False

    def get(self):
        if self.canceled:
            return None
        map = {(()): 100., 0: "", (0, 0): 0}
        for i in range(self.n):
            map[i + 1] = groups_to_enumerations(self.entry_var_list[i].get())
            map[(0, i + 1)] = self.valuelist[i].get()
            map[(i + 1, 0)] = self.valuelist[i].get()
            for j in range(self.n):
                map[(i + 1, j + 1)] = max(self.valuelist[i].get(), self.valuelist[j].get())
        return map

    def plus(self):
        # 1. create arrays
        entrylist = np.full(self.n+1, Entry(self.root))
        entry_var_list = np.full(self.n+1, StringVar())
        label_list = np.full(self.n+1, Label(self.root))
        sliderlist = np.full(self.n+1, Scale(self.root))
        valuelist = np.full(self.n+1, IntVar())

        # 2. copy elements
        for i in range(self.n-1):
            entrylist[i] = self.entrylist[i]
            entry_var_list[i] = self.entry_var_list[i]
            label_list[i] = self.label_list[i]
            sliderlist[i] = self.sliderlist[i]
            valuelist[i] = self.valuelist[i]

        # 3. add element n-1 TODO TODO TODO

        entry_var_list[self.n-1].set("")
        valuelist[self.n-1].set(1)

        entrylist[self.n-1] = Entry(self.root, font="12", textvariable=entry_var_list[self.n-1],
                                    state=("disabled" if self.fixed else "normal"))
        label_list[self.n-1] = Label(self.root, bg="white", anchor=W, justify=LEFT)
        sliderlist[self.n-1] = Scale(self.root, from_=0, to_=10, orient='horizontal', variable=valuelist[self.n-1],
                                        length=400, bg='white', highlightthickness=0, resolution=1)

        label_list[self.n-1].grid(sticky='new', row=self.n+1, column=3, columnspan=2, pady=(15,0), padx=1)
        entrylist[self.n-1].grid(sticky='new', row=self.n+1, column=1, columnspan=2, pady=(15,0), padx=1)
        sliderlist[self.n-1].grid(sticky='new', row=self.n+1, column=5, columnspan=2, pady=(0, 0))

        entry_var_list[self.n-1].trace("w", lambda name, index, mode, sv=self.entry_var_list[self.n-1], j=self.n: self.update_labels())

        # 4. move element n
        entrylist[self.n] = self.entrylist[self.n-1]
        entry_var_list[self.n] = self.entry_var_list[self.n-1]
        label_list[self.n] = self.label_list[self.n-1]
        sliderlist[self.n] = self.sliderlist[self.n-1]
        valuelist[self.n] = self.valuelist[self.n-1]

        entrylist[self.n].grid(sticky='new', row=self.n+2, column=1, columnspan=2, pady=(15,0), padx=1)
        label_list[self.n].grid(sticky='new', row=self.n+2, column=3, columnspan=2, pady=(15,0), padx=1)
        sliderlist[self.n].grid(sticky='new', row=self.n+2, column=5, columnspan=2, pady=(0, 0))

        # 5. complete
        self.n = self.n+1
        self.entrylist = entrylist
        self.entry_var_list = entry_var_list
        self.label_list = label_list
        self.sliderlist = sliderlist
        self.valuelist = valuelist

        # 6. finish
        self.button_minus.grid(sticky='ns', row=self.n + 5, column=1, pady=(10,0))
        self.button_plus.grid(sticky='ns', row=self.n + 5, column=2, pady=(10,0))
        self.button_ok.grid(sticky='nswe', row=self.n + 5, column=5, columnspan=2, pady=(10,0))
        self.update_labels()
        self.root.update()

    def minus(self):
        if self.n < 3:
            return

        # 1. create arrays
        self.n = self.n - 1
        entrylist = np.full(self.n, Entry(self.root))
        entry_value_list = np.full(self.n, StringVar())
        label_list = np.full(self.n, Label(self.root))
        sliderlist = np.full(self.n, Scale(self.root))
        valuelist = np.full(self.n, IntVar())

        # 2. copy elements
        for i in range(self.n-1):
            entrylist[i] = self.entrylist[i]
            entry_value_list[i] = self.entry_var_list[i]
            label_list[i] = self.label_list[i]
            sliderlist[i] = self.sliderlist[i]
            valuelist[i] = self.valuelist[i]

        # 3. delete element n-1
        self.entrylist[self.n - 1].destroy()
        self.label_list[self.n - 1].destroy()
        self.sliderlist[self.n - 1].destroy()

        # 4. move element n
        entrylist[self.n-1] = self.entrylist[self.n]
        entry_value_list[self.n-1] = self.entry_var_list[self.n]
        label_list[self.n-1] = self.label_list[self.n]
        sliderlist[self.n-1] = self.sliderlist[self.n]
        valuelist[self.n-1] = self.valuelist[self.n]

        entrylist[self.n-1].grid(sticky='new', row=self.n+1, column=1, columnspan=2, pady=(15,0), padx=1)
        label_list[self.n-1].grid(sticky='new', row=self.n+1, column=3, columnspan=2, pady=(15,0), padx=1)
        sliderlist[self.n-1].grid(sticky='new', row=self.n+1, column=5, columnspan=2, pady=(0, 0))

        # 5. complete
        self.entrylist = entrylist
        self.entry_var_list = entry_value_list
        self.label_list = label_list
        self.sliderlist = sliderlist
        self.valuelist = valuelist

        # 6. finish
        self.button_minus.grid(sticky='ns', row=self.n + 5, column=1, pady=(10,0))
        self.button_plus.grid(sticky='ns', row=self.n + 5, column=2, ppady=(10,0))
        self.button_ok.grid(sticky='nswe', row=self.n + 5, column=5, columnspan=2, pady=(10,0))
        self.root.update()

    def cancel(self):
        self.canceled = True
        self.quit()

    def quit(self):
        self.root.quit()
        self.root.destroy()


if __name__ == "__main__":
    # result = slider_view(3, texts=("a-zA-Z", "0-9", "<rest>"), values=(1, 0, 4))
    result = slider_view(None, costmap=example_costmap())
    valid = costmap_is_valid(result)
    print("Costmap result is valid: ", valid)
    if valid:
        print_cost_map(result)
