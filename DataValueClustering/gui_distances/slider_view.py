from tkinter import Tk, Button, Label, Entry, Scale, IntVar, Toplevel

import numpy as np

from gui_distances.costmapinput_helper import costmap_is_valid, character_escape, print_cost_map, get_n_from_map, \
    example_costmap, groups_to_enumerations


def slider_view(master, n=None, costmap=None, texts=None, values=None, fixed=False):
    view = SliderInput(master, n, costmap, texts, values, fixed)
    return view.get()


class SliderInput:

    def __init__(self, master, n=None, costmap=None, text=None, value=None, fixed=False):
        assert (not (costmap and (text or value)))
        assert (n or costmap or text)

        self.n = n if n or costmap else len(text)
        self.texts = text
        self.values = value
        self.fixed = fixed
        self.master = master

        self.canceled = False

        if costmap:
            assert (not self.texts and not self.values)
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
        self.root.focus_force()
        self.root.grab_set()

        self.title = Label(self.root, text="Slider View", bg="white",
                           font=('bold 12', 19))
        self.button_plus = Button(self.root, text='+', command=self.plus, width=3)
        self.button_minus = Button(self.root, text='-', command=self.minus, width=3)
        self.button_ok = Button(self.root, text='OK', command=self.quit)
        if self.fixed:
            self.button_minus.configure(state="disabled")
            self.button_plus.configure(state="disabled")

        self.title.grid(sticky='nswe', row=0, column=1, columnspan=4)
        self.button_minus.grid(sticky='ns', row=self.n + 5, column=1)
        self.button_plus.grid(sticky='ns', row=self.n + 5, column=2)
        self.button_ok.grid(sticky='nswe', row=self.n + 5, column=3, columnspan=2)

        self.entrylist = np.full(self.n, Entry(self.root))
        self.sliderlist = np.full(self.n, Scale(self.root))
        self.valuelist = np.full(self.n, IntVar())

        for i in range(0, self.n):
            t = ""
            v = 1
            if self.texts and len(self.texts) > i:
                t = self.texts[i]
            if self.values and len(self.values) > i:
                v = self.values[i]

            self.valuelist[i] = IntVar(self.root, v)
            self.entrylist[i] = Entry(self.root, font="12")
            self.entrylist[i].insert(0, t)
            if self.fixed:
                self.entrylist[i].configure(state="disabled")

            self.sliderlist[i] = Scale(self.root, from_=0, to_=10, orient='horizontal', variable=self.valuelist[i],
                                       length=400, bg='white', highlightthickness=0, resolution=1)

            self.entrylist[i].grid(row=i + 2, column=1, sticky='sew', columnspan=2)
            self.sliderlist[i].grid(row=i + 2, column=3, sticky='sew', columnspan=2)

        self.root.protocol("WM_DELETE_WINDOW", self.cancel)
        self.root.mainloop()

    def get(self):
        if self.canceled:
            return None
        map = {(()): 100., 0: "", (0, 0): 0}
        for i in range(self.n):
            map[i + 1] = groups_to_enumerations(self.texts[i])
            map[(0, i + 1)] = self.values[i]
            map[(i + 1, 0)] = self.values[i]
            for j in range(self.n):
                map[(i + 1, j + 1)] = max(self.values[i], self.values[j])
        return map

    def plus(self):
        entrylist = np.full(self.n + 1, Entry(self.root))
        sliderlist = np.full(self.n + 1, Scale(self.root))
        valuelist = np.full(self.n + 1, IntVar())

        for i in range(self.n):
            entrylist[i] = self.entrylist[i]
            sliderlist[i] = self.sliderlist[i]
            valuelist[i] = self.valuelist[i]

        self.entrylist = entrylist
        self.sliderlist = sliderlist
        self.valuelist = valuelist

        self.valuelist[self.n].set(1)
        self.entrylist[self.n].grid(row=self.n + 2, column=1, sticky='sew', columnspan=2)
        self.sliderlist[self.n] = Scale(self.root, from_=0, to_=10, orient='horizontal',
                                        variable=self.valuelist[self.n],
                                        length=400, bg='white', highlightthickness=0, resolution=1)
        self.sliderlist[self.n].grid(row=self.n + 2, column=3, sticky='sew', columnspan=2)

        self.n = self.n + 1

        self.button_minus.grid(sticky='ns', row=self.n + 5, column=1)
        self.button_plus.grid(sticky='ns', row=self.n + 5, column=2)
        self.button_ok.grid(sticky='nswe', row=self.n + 5, column=3, columnspan=2)

    def minus(self):
        if self.n > 1:

            self.n = self.n - 1
            entrylist = np.full(self.n + 1, Entry(self.root))
            sliderlist = np.full(self.n + 1, Scale(self.root))
            valuelist = np.full(self.n + 1, IntVar())

            for i in range(self.n):
                entrylist[i] = self.entrylist[i]
                sliderlist[i] = self.sliderlist[i]
                valuelist[i] = self.valuelist[i]

            self.entrylist[self.n].destroy()
            self.sliderlist[self.n].destroy()

            self.entrylist = entrylist
            self.sliderlist = sliderlist
            self.valuelist = valuelist

            self.button_minus.grid(sticky='ns', row=self.n + 5, column=1)
            self.button_plus.grid(sticky='ns', row=self.n + 5, column=2)
            self.button_ok.grid(sticky='nswe', row=self.n + 5, column=3, columnspan=2)
            self.root.update()

    def update(self):
        self.texts = list()
        self.values = list()
        for i in range(self.n):
            t = self.entrylist[i].get()
            self.texts.append(t)
            v = self.sliderlist[i].get()
            self.values.append(v)

    def cancel(self):
        self.canceled = True
        self.quit()

    def quit(self):
        self.update()
        self.root.quit()
        self.root.destroy()


if __name__ == "__main__":
    # result = slider_view(3, texts=("a-zA-Z", "0-9", "<rest>"), values=(1, 0, 4))
    result = slider_view(None, costmap=example_costmap())
    print("Costmap result is valid: ", costmap_is_valid(result))
    print_cost_map(result)
