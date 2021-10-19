from tkinter import Tk, Label, Canvas, mainloop

import numpy as np
from PIL import Image, ImageTk

from distance import calculate_distance_matrix_map
from distance.weighted_levenshtein_distance import get_weighted_levenshtein_distance
from gui_general.window_size import set_window_size_simple
import os
from pathlib import Path

def load_and_compile():
    color = '#eeeeee'
    w, h, offset = 200, 225, 10
    root = Tk()
    root.wm_attributes('-transparentcolor', color)
    root.config(borderwidth=0, relief="flat", bg=color, highlightthickness=0)
    root.geometry('{}x{}'.format(w, h))
    root.pack_propagate(False)

    dir_path = str(Path(__file__).parent.parent) + "\\gui_general"
    os.chdir(dir_path)

    img = Image.open(dir_path + "\\logo_loading.png")
    img = img.resize((w-2*offset, w-2*offset), Image.NEAREST)
    img = ImageTk.PhotoImage(img)
    canvas = Canvas(root, bg=color, highlightthickness=0)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(offset, offset, image=img, anchor="nw")
    root.overrideredirect(True)
    label = Label(root, text="Loading ...", bg="white")
    label.pack()

    set_window_size_simple(root)

    def compile_numba():
        cost_map = {(()): 100., 0: "", (0, 0): 1}
        distance_f = get_weighted_levenshtein_distance(cost_map)
        values_abstracted = np.array(["a", "b"])
        duplicates_removed = True
        calculate_distance_matrix_map(distance_f, values_abstracted, duplicates_removed)
        root.destroy()

    root.after(20, compile_numba)
    mainloop()
