from enum import Enum
from tkinter import Tk, Button, Label, LEFT, W, Toplevel, Menu

from gui_general import CreateToolTip
from gui_general.help_popup_gui import menu_help_distance_choice


class DistanceView(str, Enum):
    SLIDER = 'SLIDER'
    BLOB = 'BLOB'
    MATRIX = 'MATRIX'


def get_distance_choice(root):
    dc = DistanceChoice(root)
    return dc.get()


class DistanceChoice:

    def __init__(self, master):
        self.result = None
        self.canceled = False

        self.root = Toplevel(master)
        self.root.title("Dissimilarity Configuration Method Selection")
        self.root.config(bg="white")
        self.root.resizable(False, False)
        self.root.focus_force()
        self.root.grab_set()

        self.menu = Menu(self.root)
        self.menu.add_command(label="Help", command=lambda: menu_help_distance_choice(self.root))
        self.root.config(menu=self.menu)

        self.title = Label(self.root, text="Select the method for configuring dissimilarities", bg="white",
                           font=('TkDefaultFont', 12, 'bold'), anchor='c', justify="center", pady=10)

        self.label_wld = Label(self.root, text="Weighted Levenstein Distance", width=40, bg="white", justify=LEFT, anchor=W)
        self.button_wld_slider = Button(self.root, text="Sliders View (Easy)", width=30,
                                        command=lambda: self.close(DistanceView.SLIDER))
        self.button_wld_blob = Button(self.root, text="Blobs View (Medium)", width=30,
                                        command=lambda: self.close(DistanceView.BLOB))
        self.button_wld_matrix = Button(self.root, text="Matrix View (Difficult)", width=30,
                                        command=lambda: self.close(DistanceView.MATRIX))

        CreateToolTip(self.button_wld_slider,"Specify the dissimilarity between character groups via a few sliders. Easy method with very limited flexibility.")
        CreateToolTip(self.button_wld_blob, "Specify the dissimilarity between character groups by moving and scaling graphical objects on a 2D canvas. Method with medium difficulty and flexibility.")
        CreateToolTip(self.button_wld_matrix, "Specify the dissimilarity between all character groups by filling a matrix. Difficult but completely flexibel method.")

        # self.label_other = Label(self.root, text="Other", width=40, bg="white", justify=LEFT, anchor=W)
        # self.button_lcss = Button(self.root, text="Longest Common Subsequence", width=30,
        #                                 command=lambda: quit("lcss"))

        self.title.pack()
        self.label_wld.pack()
        self.button_wld_slider.pack()
        self.button_wld_blob.pack()
        self.button_wld_matrix.pack()
        # self.label_other.pack()
        # self.button_lcss.pack()

        self.root.protocol("WM_DELETE_WINDOW", self.cancel)
        self.root.mainloop()

    def cancel(self):
        self.canceled = True
        self.root.quit()
        self.root.destroy()

    def close(self, result):
        self.result = result
        self.root.quit()
        self.root.destroy()

    def get(self):
        if self.canceled:
            return None
        return self.result


if __name__ == "__main__":
    print(get_distance_choice(Tk()))
