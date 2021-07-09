from tkinter import Tk, Button, Label, Entry, Scale, IntVar

import numpy as np


def slider_view(n, matrix=None, texts=None, values=None, fixed=False):
    assert (not (matrix and (texts or values)))
    if matrix:
        texts = list()
        values = list()
        for i in range(n):
            if i in matrix and (i, 0) in matrix:
                texts.append(matrix(i))
                values.append(matrix((i, 0)))
            else:
                texts.append("")
                values.append(1)

    view = SliderInput(n, texts, values, fixed)
    return view.get()


class SliderInput:

    def __init__(self, n, text=None, values=None, fixed=False):
        self.n = n
        self.texts = text
        self.values = values
        self.fixed = fixed

        self.root = Tk()
        self.root.title("Slider Input")
        self.root.config(bg="white")
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
            text = ""
            value = 1
            if self.texts and len(self.texts) > i:
                text = self.texts[i]
            if self.values and len(self.values) > i:
                value = self.values[i]

            self.valuelist[i] = IntVar(self.root, value)
            self.entrylist[i] = Entry(self.root, font="12", text=text)
            self.entrylist[i].insert(0, text)
            if self.fixed:
                self.entrylist[i].configure(state="disabled")

            self.sliderlist[i] = Scale(self.root, from_=0, to_=10, orient='horizontal', variable=self.valuelist[i],
                                       length=400, bg='white', highlightthickness=0, resolution=1)

            self.entrylist[i].grid(row=i + 2, column=1, sticky='sew', columnspan=2)
            self.sliderlist[i].grid(row=i + 2, column=3, sticky='sew', columnspan=2)

        self.root.mainloop()

    def get(self):
        pass

    def plus(self):
        self.quit()
        self.__init__(self.n + 1, self.texts, self.values, self.fixed)

    def minus(self):
        self.quit()
        self.__init__(self.n - 1, self.texts, self.values, self.fixed)

    def update(self):
        self.texts = list()
        self.values = list()
        for i in range(self.n):
            self.texts.append(self.entrylist[i].get())
            self.values.append(self.sliderlist[i].get())

    def quit(self):
        self.update()
        self.root.destroy()


if __name__ == "__main__":
    slider_view(3, texts=("a-zA-Z", "0-9", "<rest>"), values=(1, 0, 4))
