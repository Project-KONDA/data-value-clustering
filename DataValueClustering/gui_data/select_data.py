import os
from tkinter import Tk, Listbox, Button, Label, END, Scrollbar, Toplevel, messagebox
from tkinter.messagebox import WARNING

import numpy as np

from data_extraction import get_sources_in_experiment_data_directory


def get_list(path=""):
    return get_sources_in_experiment_data_directory()[:, 0]


def select_data(master, previous=None):
    return SelectData("", master, previous).get()


class SelectData:
    def __init__(self, path, master, previous=None):
        self.path = path
        self.previous = previous

        self.root = Toplevel(master)
        # self.root.title("Select Data")

        self.result = None
        self.datalist = list()
        self.canceled = False

        self.label_title = Label(self.root, text="Select Data Set", bg="white",
                                 font=('Helvatical bold', 19))

        self.listbox = Listbox(self.root, selectmode="single", width=40, height=20)
        self.scrollbar = Scrollbar(self.root, command=self.listbox.yview)
        self.listbox.config(yscrollcommand=self.scrollbar.set)

        self.button_add = Button(self.root, text="+", command=self.add, width=3, state="disabled")
        self.button_remove = Button(self.root, text="-", command=self.remove, width=3)
        self.button_ok = Button(self.root, text="OK", command=self.close, width=27)

        self.label_title.grid(sticky='nswe', row=1, column=1, columnspan=4)
        self.listbox.grid(sticky='nswe', row=3, column=1, columnspan=3)
        self.scrollbar.grid(sticky='nse', row=3, column=4)
        self.button_add.grid(sticky='nswe', row=5, column=1, columnspan=1)
        self.button_remove.grid(sticky='nswe', row=5, column=2, columnspan=1)
        self.button_ok.grid(sticky='nswe', row=5, column=3, columnspan=2)

        self.load()
        self.root.protocol("WM_DELETE_WINDOW", self.cancel)
        self.root.mainloop()

    def load(self):
        self.listbox.delete(0, END)
        self.datalist = get_list(self.path)
        for i in self.datalist:
            self.listbox.insert(END, i)
        if self.previous is not None:
            index = np.where(self.datalist == self.previous)[0][0]
            self.listbox.select_set(index)

    def add(self):
        # TODO load
        self.load()

    def remove(self):
        index = self.listbox.curselection()
        if index == ():
            return
        text = "Do you really want to delete the following "
        if len(index) == 1:
            text += "file?\n" + self.datalist[index]
        else:
            print(index)
            text += "files?"
            for i in index:
                text += "\n" + self.datalist[i]
        if messagebox.askokcancel("Deletion", text, icon=WARNING):
            for i in index:
                path = self.datalist[index] + ".txt"
                if self.path != "":
                    path += self.path + "\\"
                if os.path.exists(path):
                    os.remove(path)
                else:
                    print("File", path, "can not be found in order to delete it.")
        self.load()

    def cancel(self):
        self.canceled = True
        self.root.quit()
        self.root.destroy()

    def close(self):
        index = self.listbox.curselection()
        try:
            index = index[0]
            self.result = self.datalist[index]
        except:
            self.result = None
        # print(self.datalist[index])

        self.root.quit()
        self.root.destroy()

    def get(self):
        if self.canceled:
            return None
        return self.result


if __name__ == "__main__":
    # path = ""
    # SelectData(path)
    print(select_data(Tk()))
