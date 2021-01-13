import numpy as np
from tkinter import *

n = 30

root = Tk()
values = np.full([n, n], None)

regex = np.full([n], None)

label = np.full([n], None)
label_text = np.full([n], "", dtype=object)
entry = Entry(root, width=3)

matrix = {}


def output_Matrix():
    matrix[()] = 0
    if entry.get() != "":
        matrix[()] = int(entry.get())

    for i in range(n):
        matrix[(i)] = label_text[i]
    for i in range(n):
        for j in range(n):
            v = values[i, j].get()
            if v == "":
                matrix[(i, j)] = 0
            if v != "":
                matrix[(i, j)] = int(v)
    root.quit()
    # print(d)


def copy_to_column(i):
    if type(regex[i]) is Entry and type(label[i]) is Label:
        text = regex[i].get()
        label_text[i] = text
        label[i].configure(text=text)
    return True


def test_val(text, acttyp):
    if acttyp == '1':  # insert
        if not text.isdigit():
            return False
    return True


def record_matrix():
    # root = Tk()
    root.title("Cost Matrix")
    width = 210 + 32 * n  # 300 #270 # 240
    hight = 70 + 19 * n  # 130 # 110 # 90
    widthtext = str(width) + "x" + str(hight)
    root.geometry(widthtext)
    # root.geometry("450x200")

    Label(root, text="Enter The New Cost Matrix", anchor="w").grid(row=1, column=2, columnspan=n + 3)

    Label(root, text="Case Change:", anchor="w").grid(row=4, column=2)

    entry['validatecommand'] = (entry.register(test_val), '%P', '%d')
    entry.grid(row=4, column=3)

    for i in range(n):
        label[i] = Label(root, textvariable=label_text[i], width=3, bg="lightgrey", anchor="w")
        label[i].grid(row=4, column=i + 5)
        regex[i] = Entry(root, width=35, bg="lightgrey", validate="focusout",
                         validatecommand=lambda i2=i: copy_to_column(i2))
        regex[i].grid(row=i + 5, column=2, columnspan=3)
        for j in range(n):
            values[i, j] = Entry(root, validate="key", width=3)
            values[i, j]['validatecommand'] = (values[i, j].register(test_val), '%P', '%d')
            values[i, j].grid(column=i + 5, row=j + 5)

    # for i in range(n):

    d2 = np.full([n, n], "")

    Button(root, text='OK', justify=RIGHT, width=5 * n + 15, command=output_Matrix) \
        .grid(row=n + 7, column=2, columnspan=n + 3)

    root.mainloop()
    return "aa"


def getcostmatrix(size):
    n = size
    record_matrix()
    return matrix


if __name__ == "__main__":
    print(getcostmatrix(4))
