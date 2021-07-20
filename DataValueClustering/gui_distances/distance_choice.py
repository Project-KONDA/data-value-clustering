from enum import Enum
from tkinter import Tk, Button, Label, LEFT, W, Toplevel


class DistanceView(Enum):
    SLIDER = 1
    BLOB = 2
    MATRIX = 3


def get_distance_choice(root):
    dc = DistanceChoice(root)
    return dc.get()


class DistanceChoice:

    def __init__(self, root):
        self.result = None

        self.root = Toplevel(root)
        self.root.title("Distance Choice")
        self.root.config(bg="white")
        self.title = Label(self.root, text="Distance Choice", bg="white",
                           font=('Helvatical bold', 19))

        self.label_wld = Label(self.root, text="Weighted Levenstein Distance", width=40, bg="white", justify=LEFT, anchor=W)
        self.button_wld_slider = Button(self.root, text="Slider View (Easy)", width=30,
                                        command=lambda: quit(DistanceView.SLIDER))
        self.button_wld_blob = Button(self.root, text="Blob View (Medium)", width=30,
                                        command=lambda: quit(DistanceView.BLOB))
        self.button_wld_matrix = Button(self.root, text="Matrix View (Hard)", width=30,
                                        command=lambda: quit(DistanceView.MATRIX))

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

        self.root.mainloop()

    def quit(self, result):
        self.result = result
        self.root.quit()
        self.root.destroy()

    def get(self):
        return self.result


if __name__ == "__main__":
    print(get_distance_choice(Tk()))
