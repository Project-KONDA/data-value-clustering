from tkinter import Toplevel, Menu, StringVar, Label, IntVar, Radiobutton, Button
from tkinter.font import Font

import numpy as np
from gui_cluster_selection.algorithm_selection import algorithm_array
from gui_general import CreateToolTip
from gui_general.help_popup_gui import menu_help_clustering_selection
from gui_general.scrollable_frame import create_scrollable_frame
from gui_general.window_size import set_window_size_simple


def select_algorithm(master, predefined_algorithm=None, suggested_algorithms=None):
    return SelectAlgorithm(master, predefined_algorithm, suggested_algorithms).get()

class SelectAlgorithm:
    def __init__(self, master, predefined_algorithm=None, suggested_algorithms=None):
        self.root = Toplevel(master)
        self.root.title("Algorithm Selection")
        self.root.resizable(False, True)
        if hasattr(master, "icon"):
            self.root.icon = master.icon
            self.root.iconphoto(False, master.icon)

        self.canceled = False

        self.menu = Menu(self.root)
        self.menu.add_command(label="Help", command=lambda: menu_help_clustering_selection(self.root))
        self.root.config(menu=self.menu)

        # caption:
        heading = "Select a Clustering Algorithm"
        font = Font(family="TkDefaultFont", size=12, weight="bold")
        self.question_caption_label = Label(self.root, anchor='c', justify="center", text=heading, bg='white',
                                            font=font)
        self.caption_width = font.measure(heading)

        self.hint_label = Label(self.root, anchor='c', justify="center", text="Typically the highlighted algorithm achieves good results.", bg='white', padx=10)

        self.label_suggested = None
        if suggested_algorithms is not None:
            self.label_suggested = Label(self.root, text="Algorithms suggested based on the evaluation are highlighted in green.", bg="white", anchor='w', padx=10, fg='blue', justify='left')
            self.question_caption_label.grid(row=0, column=0, sticky='nsew', columnspan=6)
            self.hint_label.grid(row=1, column=0, sticky='nsew', columnspan=6, pady=(0, 0))
            self.label_suggested.grid(row=2, column=0, sticky='senw', columnspan=6)
        else:
            self.question_caption_label.grid(row=0, column=0, sticky='nsew', columnspan=6)
            self.hint_label.grid(row=1, column=0, sticky='nsew', columnspan=6)

        # scrollable result frame:
        self.around_canvas_frame_result, self.canvas_result, self.scrollable_result_frame = create_scrollable_frame(self.root)
        self.root.rowconfigure(4, weight=1)
        self.around_canvas_frame_result.grid(row=4, column=0, sticky='ns', columnspan=6, pady=1, padx=1)

        # OK button:
        self.button = Button(self.root, text='OK', command=self.close, bg='white')
        self.button.grid(row=5, column=0, sticky='nswe', columnspan=6)

        self.suggested_algorithms = suggested_algorithms
        self.algorithms = np.array(algorithm_array, dtype=object)
        self.choice = IntVar()
        if predefined_algorithm is None:
            self.choice.set(0)
        else:
            self.choice.set(np.where(self.algorithms[:, 2] == predefined_algorithm)[0][0])
        self.radio_buttons = np.empty(len(self.algorithms), dtype=Radiobutton)
        self.orig_color = None
        self.build_result_frame()

        self.root.protocol("WM_DELETE_WINDOW", self.cancel)
        set_window_size_simple(self.root)
        self.root.grab_set()
        self.root.focus_force()
        self.root.mainloop()

    def build_result_frame(self):
        for i, algorithm in enumerate(self.algorithms):
            self.radio_buttons[i] = Radiobutton(self.scrollable_result_frame, text=algorithm[2], padx=20,
                                                variable=self.choice, bg="white",
                                                value=i, justify='left')
            self.radio_buttons[i].grid(row=i + 10, column=0, sticky='w')
            CreateToolTip(self.radio_buttons[i], algorithm[5])
            if self.orig_color is None:
                self.orig_color = self.radio_buttons[i].cget("bg")
            if self.suggested_algorithms is not None and algorithm[2] in self.suggested_algorithms:
                self.radio_buttons[i].configure(bg='pale green')
            # elif i == 0 or i == 3:
            #     self.radio_buttons[i].configure(bg='pale green')

    def get(self):
        if self.canceled:
            return None, None
        if self.choice.get() >= 0:
            selected_algorithm_f = self.algorithms[self.choice.get(), 3]
            cluster_algo = self.algorithms[self.choice.get(), 2]
        else:
            selected_algorithm_f = None
            cluster_algo = None
        return selected_algorithm_f, cluster_algo

    def get_suggested_algorithm_names(self, suggested_algorithms):
        if len(suggested_algorithms.shape) == 2:
            return suggested_algorithms[:, 0]
        else:
            return []

    def unbind_all(self):
        self.root.unbind_all("<MouseWheel>")

    def cancel(self):
        self.canceled = True
        self.close()

    def close(self, event=None):
        self.unbind_all()
        self.root.quit()
        self.root.destroy()