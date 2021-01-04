import numpy as np
from tkinter import *

matrix = {}

class Costmatrix():

    def __init__(self, i):
        self.n = i
        self.root = Tk()
        self.values = np.full([self.n, self.n], None)

        self.regex = np.full([self.n], None)

        self.label = np.full([self.n], None)
        self.label_text = np.full([self.n], "", dtype=object)
        self.entry = Entry(self.root, width=3)


    def output_Matrix(self):
        matrix[()] = 0
        if self.entry.get() != "":
            matrix[()] = int(self.entry.get())

        for i in range(self.n):
            matrix[(i)] = self.label_text[i]
        for i in range(self.n):
            for j in range(self.n):
                v = self.values[i, j].get()
                if v == "":
                    matrix[(i, j)] = 0
                if v != "":
                    matrix[(i, j)] = int(v)
        self.root.quit()
        # print(d)

    def copyToColumn(self, i):
        if type(self.regex[i]) is Entry and type(self.label[i]) is Label:
            text = self.regex[i].get()
            self.label_text[i] = text
            self.label[i].configure(text=text)
        return True

    def testVal(self, inStr, acttyp):
        if acttyp == '1':  # insert
            if not inStr.isdigit():
                return False
        return True

    def recordmatrix(self):
        # root = Tk()
        self.root.title("Cost Matrix")
        width = 210 + 32 * self.n  # 300 #270 # 240
        hight = 70 + 19 * self.n  # 130 # 110 # 90
        widthtext = str(width) + "x" + str(hight)
        self.root.geometry(widthtext)
        # root.geometry("450x200")

        Label(self.root, text="Enter The New Cost Matrix", anchor="w").grid(row=1, column=2, columnspan=self.n + 3)

        Label(self.root, text="Case Change:", anchor="w").grid(row=4, column=2)

        self.entry['validatecommand'] = (self.entry.register(self.testVal), '%P', '%d')
        self.entry.grid(row=4, column=3)

        for i in range(self.n):
            self.label[i] = Label(self.root, textvariable=self.label_text[i], width=3, bg="lightgrey", anchor="w")
            self.label[i].grid(row=4, column=i + 5)
            self.regex[i] = Entry(self.root, width=35, bg="lightgrey", validate="focusout",
                             validatecommand=lambda i2=i: self.copyToColumn(i2))
            self.regex[i].grid(row=i + 5, column=2, columnspan=3)
            for j in range(self.n):
                self.values[i, j] = Entry(self.root, validate="key", width=3)
                self.values[i, j]['validatecommand'] = (self.values[i, j].register(self.testVal), '%P', '%d')
                self.values[i, j].grid(column=i + 5, row=j + 5)

        # for i in range(n):

        d2 = np.full([self.n, self.n], "")

        Button(self.root, text='OK', justify=RIGHT, width=5 * self.n + 15, command=self.output_Matrix) \
            .grid(row=self.n + 7, column=2, columnspan=self.n + 3)

        self.root.mainloop()
        return "aa"

    def getcostmatrix(size):
        mymatrix = Costmatrix(size)
        mymatrix.recordmatrix()
        return matrix


if __name__ == "__main__":
    print(Costmatrix.getcostmatrix(5))
