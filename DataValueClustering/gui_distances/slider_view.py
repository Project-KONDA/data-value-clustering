from tkinter import Tk, Button, Label, Entry, Scale, IntVar

import numpy as np


def sliderview(n, texts=None, values=None):
    view = SliderInput(n, texts, values)
    return view.get()


class SliderInput:

    def __init__(self, n, text=None, values=None):
        self.n = n
        self.texts = text
        self.values = values

        self.root = Tk()
        self.root.config(bg="white")
        self.title = Label(self.root, text="Slider View", bg="white",
                           font=('Helvatical bold', 19))
        self.button_plus = Button(self.root, text='+', command=self.plus, width=3)
        self.button_minus = Button(self.root, text='-', command=self.minus, width=3)
        self.button_ok = Button(self.root, text='OK', command=self.quit)

        self.title.grid(sticky='nswe', row=0, column=1, columnspan=4)
        self.button_minus.grid(sticky='ns', row=self.n + 5, column=1)
        self.button_plus.grid(sticky='ns', row=self.n + 5, column=2)
        self.button_ok.grid(sticky='nswe', row=self.n + 5, column=3, columnspan=2)

        self.entrylist = np.full(self.n, Entry(self.root))
        self.sliderlist = np.full(self.n, Scale(self.root))
        self.valuelist = np.full(self.n, IntVar())

        for i in range(0, self.n):
            text = ""
            if self.texts and len(self.texts) > i:
                text = self.texts[i]
            self.valuelist[i] = IntVar(self.root, 1)
            self.entrylist[i] = Entry(self.root, font="Calibri 12", text=text)
            self.entrylist[i].insert(0, text)

            self.sliderlist[i] = Scale(self.root, from_=0, to_=10, orient='horizontal', variable=self.valuelist[i],
                                        length=400, bg='white', highlightthickness=0, resolution=1)
            self.entrylist[i].grid(row=i + 2, column=1, sticky='sew', columnspan=2)
            self.sliderlist[i].grid(row=i + 2, column=3, sticky='sew', columnspan=2)

        self.root.mainloop()

    def get(self):
        pass

    def plus(self):
        self.root.destroy()
        self.__init__(self.n + 1, self.texts, self.values)

    def minus(self):
        self.root.destroy()
        self.__init__(self.n - 1, self.texts, self.values)

    def quit(self):
        for v in self.valuelist:
            print(v.get())
        print(self.entrylist)
        print(self.sliderlist)
        self.root.quit()


if __name__ == "__main__":
    sliderview(3, ("Letters", "Digits", "Specials"))
