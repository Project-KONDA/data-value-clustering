from tkinter import Button, Label, Entry, Scale, IntVar, Toplevel, StringVar, W, LEFT, Menu, Checkbutton

import numpy as np

from gui_distances.costmapinput_helper import costmap_is_valid, print_cost_map, get_n_from_map, \
    groups_to_enumerations
from gui_distances.distance_choice import DistanceView
from gui_distances.distance_warnings import warning_color, \
    undo_highlight_entries, update_warnings, update_warnings_vars
from gui_distances.CostMapInput import input_costmap
from gui_general import CreateToolTip
from gui_general.help_popup_gui import menu_help_distance_slider
from gui_general.scrollable_frame import create_scrollable_frame
from gui_general.window_size import set_window_size_simple

disable_scale_color_trough = "grey90"
disable_scale_color_fg = "grey40"

def slider_view(master, n=None, costmap=None, abstraction=None, texts=list(), values=None, fixed=False, suggestion=None, configuration=None, restricted=False):
    view = SliderInput(master, n, costmap, abstraction, texts, values, fixed, suggestion, configuration, restricted)
    return view.get()


class SliderInput:

    def __init__(self, master, n=None, costmap=None, abstraction=None, texts=list(), value=None, fixed=False, suggestion=None, configuration=None, restricted=False):
        assert (not (costmap and value))  # (not (costmap and (abstraction_chars_and_names is not None or value)))
        assert (n or costmap or abstraction is not None)

        self.costmap = costmap
        self.matrix_costmap = None
        self.abstraction = abstraction
        self.texts = texts
        self.value = value
        self.fixed = fixed
        self.suggestion = suggestion
        self.configuration = configuration

        self.master = master
        self.n = n if n or costmap else len(texts)
        self.abstraction = abstraction
        self.texts = texts
        self.abstraction_keys = self.texts
        self.abstraction_values = list() if abstraction is None else abstraction[:, 0].tolist()
        self.values = value
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

        self.root = Toplevel(self.master, bg="white")
        self.root.attributes('-alpha', 0.0)
        self.root.title("Distance Configuration - Sliders")
        if hasattr(master, "icon"):
            self.root.icon = master.icon
            self.root.iconphoto(False, master.icon)

        self.root.resizable(False, True)
        self.root.focus_force()
        self.root.grab_set()

        self.menu = Menu(self.root)
        self.menu.add_command(label="Help", command=lambda: menu_help_distance_slider(self.root, restricted))
        self.root.config(menu=self.menu)

        self.title = Label(self.root, text="Weight the influence of character groups on the dissimilarity between data values", bg="white",
                           font=('TkDefaultFont', 12, 'bold'), anchor='c', justify="center")
        self.hint = Label(self.root, text="Choose heigher weights for characters or character sequences that you do not expect to find frequently in the data values\nand that may cause great dissimilarity. Rows with empty entries will be ignored. You can custimize the character groups.", bg="white", anchor='c', justify="center")
        self.button_expert = Button(self.root, text='Expert Mode', command=self.matrix_view, state="disabled" if restricted else "normal")
        CreateToolTip(self.button_expert, "Open Matrix view, which allows setting the weights entirely flexible.")
        self.extended = IntVar(self.root, 0)
        self.checkbutton_extend = Checkbutton(self.root, text="Custom Character Groups", bg="white", variable=self.extended, command=self.trigger_extend)
        CreateToolTip(self.checkbutton_extend, "Enable/disable modification of character groups.")
        self.button_reset = Button(self.root, text='Reset', command=self.reset_groups)
        self.button_plus = Button(self.root, text='+', command=self.plus, width=3)
        self.button_minus = Button(self.root, text='-', command=self.minus, width=3)
        self.button_ok = Button(self.root, text='OK', command=self.quit)

        self.button_minus.grid(sticky='nse', row=8, column=0, pady=2, padx=10)
        self.button_plus.grid(sticky='nsw', row=8, column=1, pady=2, padx=10)
        self.button_reset.grid(sticky='nsw', row=8, column=2, columnspan=1, pady=2, padx=2)
        self.button_ok.grid(sticky='nswe', row=8, column=3, columnspan=6, pady=2, padx=2)

        if self.fixed:
            self.button_minus.grid_remove()
            self.button_plus.grid_remove()
            self.button_reset.grid_remove()

        self.button_expert.grid(sticky='ne', row=4, column=7, padx=10)
        if suggestion is not None:
            self.label_suggested = Label(self.root, text="Advice based on the evaluation: " + suggestion, wraplengt=800, bg="white", anchor='w', fg='blue', justify='left')
            self.title.grid(sticky='nswe', row=0, column=0, columnspan=8, pady=(10, 0))
            self.hint.grid(sticky='nswe', row=1, column=0, columnspan=8, pady=(0, 0))
            self.label_suggested.grid(row=2, column=0, sticky='senw', columnspan=8, pady=(0,10), padx=10)
        else:
            self.title.grid(sticky='nswe', row=0, column=0, columnspan=8, pady=(10, 0))
            self.hint.grid(sticky='nswe', row=1, column=0, columnspan=8, pady=(0, 10))

        self.label_warning = Label(self.root, text="", wraplengt=800, bg=warning_color, anchor='nw', justify='left', borderwidth=1, relief="solid")
        self.label_warning.grid(sticky='ns', row=3, column=0, columnspan=8, pady=(0, 10), padx=10)

        CreateToolTip(self.button_reset, "Reset character groups to original groups derived from abstraction and reset values.")
        CreateToolTip(self.button_minus, "Remove the second to last line.")
        CreateToolTip(self.button_plus, "Add line.")

        self.checkbutton_extend.grid(sticky="nw", row=4, column=0, padx=10, columnspan=2)

        # scrollable frame:
        self.around_canvas_frame, self.canvas, self.scrollable_frame = create_scrollable_frame(self.root)
        self.root.rowconfigure(7, weight=1)
        self.around_canvas_frame.grid(sticky='nswe', row=7, column=0, columnspan=8, pady=1, padx=1)
        self.canvas.configure(bg='SystemButtonFace')
        self.scrollable_frame.configure(highlightbackground='grey', highlightthickness=1)

        # headings:
        self.label_head_characters = Label(self.root, text="Character Groups", bg="white", font=('Sans', '10', 'bold'))
        influence_text = "  low                                                   medium                                                   high  "

        self.label_head_weights_sub = Label(self.root, text=influence_text, bg="white")
        self.label_head_weights = Label(self.root, text="Weights of Influence", bg="white", font=('Sans', '10', 'bold'))
        CreateToolTip(self.label_head_characters, "Enumerate all characters of this group. Only the first occurrence of a "
                                           "character in one of the groups is relevant.\nNote that some characters may "
                                           "represent abstracted details. This mapping is provided in the column "
                                           "to the right.")
        CreateToolTip(self.label_head_weights, "Weights indicating the influence of the given character groups on the dissimilarity between data values.")
        self.label_head_characters.grid(sticky='nswe', row=5, column=0, columnspan=3, pady=(20,0))
        self.label_head_weights.grid(sticky='nswe', row=5, column=4, columnspan=4, pady=(20,0))
        self.label_head_weights_sub.grid(sticky='nse', row=6, column=4, columnspan=4, padx=(15,15))

        self.row_offset = 6

        self.entrylist = np.full(self.n, Entry(self.scrollable_frame))
        self.entry_var_list = np.full(self.n, StringVar())
        self.label_list = np.full(self.n, Label(self.scrollable_frame))
        self.sliderlist = np.full(self.n, Scale(self.scrollable_frame))
        self.valuelist = np.full(self.n, IntVar())

        self.tooltips = list()

        for i in range(0, self.n):
            t = ""
            v = 4
            if self.texts and len(self.texts) > i:
                t = self.texts[i]
            if self.values and len(self.values) > i:
                v = self.values[i]-1

            self.label_list[i] = Label(self.scrollable_frame, width=27, bg="white", anchor=W, justify=LEFT)
            self.label_list[i].config(text = "<rest>" if i == self.n-1 else "")
            self.valuelist[i] = IntVar(self.scrollable_frame, v)
            self.entry_var_list[i] = StringVar(self.scrollable_frame, t)
            self.entry_var_list[i].trace("w", lambda name, index, mode: self.update_labels())
            self.entry_var_list[i].set("<rest>" if i == self.n-1 else t)
            self.entrylist[i] = Entry(self.scrollable_frame, font="12", textvariable=self.entry_var_list[i], width=25, highlightthickness=2)
            if i == self.n-1 or self.fixed:
                self.entrylist[i].configure(state="disabled")


            self.sliderlist[i] = Scale(self.scrollable_frame, from_=0, to_=8, orient='horizontal', variable=self.valuelist[i],
                                       length=400, bg='white', highlightthickness=0, resolution=4, showvalue=0)
            self.entrylist[i].grid(sticky='new', row=i + self.row_offset, column=1, columnspan=1, pady=(15, 0), padx=2)
            self.label_list[i].grid(sticky='new', row=i + self.row_offset, column=3, columnspan=1, pady=(15, 0), padx=2)
            self.sliderlist[i].grid(sticky='new', row=i + self.row_offset, column=5, columnspan=1, pady=(15, 0))

        self.fg_color = self.sliderlist[0].cget("fg")
        self.troughcolor_color = self.sliderlist[0].cget("troughcolor")

        self.trigger_extend()

        set_window_size_simple(self.root)

        self.root.attributes('-alpha', 1.0)

        self.root.protocol("WM_DELETE_WINDOW", self.cancel)
        self.root.mainloop()

    def unbind_all(self):
        self.root.unbind_all("<MouseWheel>")

    def disable_slider(self, i):
        self.valuelist[i].set(0)
        self.sliderlist[i].configure(state="disabled", fg=disable_scale_color_fg, troughcolor=disable_scale_color_trough)

    def enable_slider(self, i):
        if self.sliderlist[i]['state'] == 'disabled':
            self.valuelist[i].set(4)
        self.sliderlist[i].configure(state="normal", fg=self.fg_color, troughcolor=self.troughcolor_color)

    def remove_duplicate_chars(self):
        for i, entry in enumerate(self.entrylist):
            if i < len(self.entrylist) - 1:
                shortened = list()
                for k, entry_char in enumerate(entry.get()):
                    print(entry_char)
                    if entry_char not in shortened:
                        shortened.append(entry_char)
                print(shortened)
                self.entry_var_list[i].set(''.join(shortened))

    def update_labels(self):
        if self.updating_labels:
            return
        if self.abstraction is None:
            if not self.extended.get():
                for i, e in enumerate(self.entrylist):
                    self.label_list[i].config(text=e.get())
            else:
                for i, e in enumerate(self.entrylist):
                    self.label_list[i].config(text="")
            return


        undo_highlight_entries(self.entrylist, self.label_warning)

        if self.extended.get():
            update_warnings_vars(self.entrylist, self.label_warning, self.n, self.label_list, self.abstraction, self.tooltips, 0, self.entry_var_list, self.disable_slider, self.enable_slider)
            self.updating_labels = False

        else:
            tool_tips_labels = np.full(self.n, "").tolist()
            text = np.full(self.n, "", dtype=object)
            label_text = np.full(self.n, "", dtype=object)
            for i, e in enumerate(self.entrylist):
                self.label_list[i].config(text="")
                text[i] = e.get()
                if self.entry_var_list[i].get() == "":
                    self.disable_slider(i)
                    tool_tips_labels[i] = "This row will be ignored."
            for i, t in enumerate(text):
                for abstraction_char in t:
                    for j in range(i+1, self.n):
                        text[j] = text[j].replace(abstraction_char, "")
            for mapping in self.abstraction:
                for i, t in enumerate(text):
                    if len(mapping[1]) == 1 and mapping[1] in t:
                        text[i] = t.replace(mapping[1], "")
                        label_text[i] += "\n" + " <" + mapping[0] + ">"
                        tip = "<" + mapping[0] + ">" + mapping[3][3:]
                        if tool_tips_labels[i] != "":
                            tool_tips_labels[i] = tool_tips_labels[i] + "\n" + tip
                        else:
                            tool_tips_labels[i] = tip
                        break
            for i, l in enumerate(self.label_list):

                if text[i] == "":
                    label_text[i] = label_text[i][2:]
                newtext = text[i] + label_text[i]
                if i == self.n-1:
                    newtext = "<rest>"
                l.config(text=newtext)
            for i, tip in enumerate(tool_tips_labels):
                if i == self.n-1:
                    CreateToolTip(self.label_list[i], "<rest> represents all characters not covered above.")
                else:
                    CreateToolTip(self.label_list[i], tip)

    def get(self):
        if self.canceled:
            return None, None
        if self.matrix_costmap:
            return DistanceView.MATRIX, self.matrix_costmap
        map = {(()): 1., 0: "", (0, 0): 0}
        for i in range(self.n):
            map[i + 1] = groups_to_enumerations(self.entry_var_list[i].get())
            map[(0, i + 1)] = self.valuelist[i].get()+1
            map[(i + 1, 0)] = self.valuelist[i].get()+1
            for j in range(self.n):
                map[(i + 1, j + 1)] = max(self.valuelist[i].get()+1, self.valuelist[j].get()+1)
        return DistanceView.SLIDER, map

    def reset_groups(self):
        if not self.configuration:
            return
        blob_configuration = self.configuration.create_blob_configuration()
        newtexts = list(blob_configuration[1:, 1])
        new_n = len(newtexts)
        newtexts[new_n-1] = "<rest>"

        while self.n < new_n:
            self.plus()
        while self.n > new_n:
            self.minus()
        self.updating_labels = True
        for i, t in enumerate(newtexts):
            self.entry_var_list[i].set(t)
            self.sliderlist[i].set(1)
        self.updating_labels = False
        self.trigger_extend()

    def plus(self):
        # 1. create arrays
        entrylist = np.full(self.n+1, Entry(self.scrollable_frame))
        entry_var_list = np.full(self.n+1, StringVar())
        label_list = np.full(self.n+1, Label(self.scrollable_frame))
        sliderlist = np.full(self.n+1, Scale(self.scrollable_frame))
        valuelist = np.full(self.n+1, IntVar())

        # 2. copy elements
        for i in range(self.n-1):
            entrylist[i] = self.entrylist[i]
            entry_var_list[i] = self.entry_var_list[i]
            label_list[i] = self.label_list[i]
            sliderlist[i] = self.sliderlist[i]
            valuelist[i] = self.valuelist[i]

        # 3. add element n-1

        entry_var_list[self.n-1].set("")
        valuelist[self.n-1].set(1)

        entrylist[self.n-1] = Entry(self.scrollable_frame, font="12", textvariable=entry_var_list[self.n-1], width=25,
                                    highlightthickness=2)
        label_list[self.n-1] = Label(self.scrollable_frame, bg="white", anchor=W, justify=LEFT, width=24)


        sliderlist[self.n-1] = Scale(self.scrollable_frame, from_=0, to_=8, orient='horizontal',
                                       variable=valuelist[self.n-1],
                                       length=400, bg='white', highlightthickness=0, resolution=4, showvalue=0)


        label_list[self.n-1].grid(sticky='new', row=self.n-1+self.row_offset, column=3, columnspan=2, pady=(15,0), padx=1)
        entrylist[self.n-1].grid(sticky='new', row=self.n-1+self.row_offset, column=1, columnspan=2, pady=(15,0), padx=1)
        sliderlist[self.n-1].grid(sticky='new', row=self.n-1+self.row_offset, column=5, columnspan=2, pady=(15, 0))

        entry_var_list[self.n-1].trace("w", lambda name, index, mode: self.update_labels())

        # 4. move element n
        entrylist[self.n] = self.entrylist[self.n-1]
        entry_var_list[self.n] = self.entry_var_list[self.n-1]
        label_list[self.n] = self.label_list[self.n-1]
        sliderlist[self.n] = self.sliderlist[self.n-1]
        valuelist[self.n] = self.valuelist[self.n-1]

        entrylist[self.n].grid(sticky='new', row=self.n + self.row_offset, column=1, columnspan=2, pady=(15, 0), padx=1)
        label_list[self.n].grid(sticky='new', row=self.n + self.row_offset, column=3, columnspan=2, pady=(15, 0), padx=1)
        sliderlist[self.n].grid(sticky='new', row=self.n + self.row_offset, column=5, columnspan=2, pady=(15, 0))

        # 5. complete
        self.n = self.n+1
        self.entrylist = entrylist
        self.entry_var_list = entry_var_list
        self.label_list = label_list
        self.sliderlist = sliderlist
        self.valuelist = valuelist

        # 6. finish
        self.update_labels()
        self.root.update()

    def minus(self):
        if self.n < 3:
            return

        # 1. create arrays
        self.n = self.n - 1
        entrylist = np.full(self.n, Entry(self.scrollable_frame))
        entry_value_list = np.full(self.n, StringVar())
        label_list = np.full(self.n, Label(self.scrollable_frame))
        sliderlist = np.full(self.n, Scale(self.scrollable_frame))
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

        entrylist[self.n-1].grid(sticky='new', row=self.n-1+self.row_offset, column=1, columnspan=2, pady=(15,0), padx=1)
        label_list[self.n-1].grid(sticky='new', row=self.n-1+self.row_offset, column=3, columnspan=2, pady=(15,0), padx=1)
        sliderlist[self.n-1].grid(sticky='new', row=self.n-1+self.row_offset, column=5, columnspan=2, pady=(15, 0))

        # 5. complete
        self.entrylist = entrylist
        self.entry_var_list = entry_value_list
        self.label_list = label_list
        self.sliderlist = sliderlist
        self.valuelist = valuelist

        # 6. finish
        self.root.update()

    def matrix_view(self):
        self.matrix_costmap = input_costmap(self.root, regexes=self.texts, costmap=self.get()[1],
                                            abstraction=self.abstraction, suggestion=self.suggestion,
                                            configuration=self.configuration)
        if self.matrix_costmap is not None:
            self.quit()

    def trigger_extend(self):
        if self.extended.get() == 1:
            self.label_head_characters.configure(text="Custom Character Groups")
            if not self.fixed:
                self.button_plus.grid()
                self.button_minus.grid()
                self.button_reset.grid()
            for i, e in enumerate(self.entrylist):
                e.grid()
                self.label_list[i].grid(column=3, columnspan=1, padx=2)
                self.label_list[i].configure(width=27)
        else:
            self.label_head_characters.configure(text="Character Groups")
            self.button_plus.grid_remove()
            self.button_minus.grid_remove()
            self.button_reset.grid_remove()
            for i, e in enumerate(self.entrylist):
                e.grid_remove()
                self.label_list[i].grid(column=2, columnspan=2, padx=2)
                self.label_list[i].configure(width=61)
        self.root.update()
        self.update_labels()

    def cancel(self):
        self.canceled = True
        self.quit()

    def quit(self):
        self.unbind_all()
        self.root.quit()
        self.root.destroy()


if __name__ == "__main__":
    # result = slider_view(3, texts=("a-zA-Z", "0-9", "<rest>"), values=(1, 0, 4))
    # result = slider_view(None, costmap=example_costmap())
    result = slider_view(None, n=4)
    try:
        costmap_is_valid(result)
        print("Costmap result is valid:", True)
        print_cost_map(result)
    except:
        print("Costmap result is valid:", False)
