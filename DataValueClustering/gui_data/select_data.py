import os
from tkinter import Tk, Listbox, Button, Label, END, Scrollbar, Toplevel, messagebox, Menu
from tkinter.messagebox import WARNING
from BaseXClient import BaseXClient

import numpy as np

from data_extraction import get_sources_in_experiment_data_directory
from data_extraction.write_cluster_excel import data_to_excel
from export.path import getExcelSavePath
from gui_data.add_data import add_data
from gui_general import CreateToolTip
from gui_general.help_popup_gui import menu_help_data_selection
from gui_general.window_size import set_window_size_simple


def get_list(path=""):
    return get_sources_in_experiment_data_directory()[:, 0]


def select_data(master, previous=None, single_cluster_data=None, restricted=False):
    return SelectData(master, "", previous, single_cluster_data, restricted).get()


class SelectData:
    def __init__(self, master, path, previous=None, single_cluster_data=None, restricted=False):
        self.path = path
        self.previous = previous
        self.single_cluster_data = single_cluster_data

        self.root = Toplevel(master)
        self.root.attributes('-alpha', 0.0)
        self.root.title("Data Selection")
        self.root.resizable(False, True)
        if hasattr(master, "icon"):
            self.root.icon = master.icon
            self.root.iconphoto(False, master.icon)

        self.menu = Menu(self.root)
        if not restricted:
            self.menu.add_command(label="Files", command=self.openFolder)
            self.menu.add_command(label="Reload", command=self.load)
            self.menu.add_command(label="Export", command=self.export_data_as_excel)
        self.menu.add_command(label="Help", command=lambda: menu_help_data_selection(self.root, restricted))
        self.root.config(menu=self.menu)

        self.result = None
        self.datalist = list()
        self.canceled = False

        self.label_title = Label(self.root, text="Select the data value set to be clustered", bg="white",
                                 font=('TkDefaultFont', 12, 'bold'), anchor='c', justify="center", pady=10)

        if self.single_cluster_data is not None:
            self.label_hint = Label(self.root, text="Data value sets generated from a previously calculated\ncluster are highlighted in green", bg="white", fg='blue')

        self.root.grid_rowconfigure(3, weight=1)

        self.listbox = Listbox(self.root, selectmode="single", width=50, height=20)
        self.scrollbar = Scrollbar(self.root, command=self.listbox.yview)
        self.listbox.config(yscrollcommand=self.scrollbar.set)

        self.button_add = Button(self.root, text="+", command=self.add, width=3)
        self.button_remove = Button(self.root, text="-", command=self.remove, width=3)
        self.button_ok = Button(self.root, text="OK", command=self.close, width=27)

        self.label_title.grid(sticky='nswe', row=1, column=1, columnspan=4)
        if self.single_cluster_data is not None:
            self.label_hint.grid(sticky='nswe', row=2, column=1, columnspan=4, padx=10)
        self.listbox.grid(sticky='nswe', row=3, column=1, columnspan=3)
        self.scrollbar.grid(sticky='nse', row=3, column=4)
        if restricted:
            self.button_ok.grid(sticky='nswe', row=5, column=1, columnspan=4)
        else:
            self.button_add.grid(sticky='nswe', row=5, column=1, columnspan=1)
            self.button_remove.grid(sticky='nswe', row=5, column=2, columnspan=1)
            self.button_ok.grid(sticky='nswe', row=5, column=3, columnspan=2)

        CreateToolTip(self.button_add, "Add a data value set.")
        CreateToolTip(self.button_remove, "Remove selected data value set.")

        self.load()

        self.root.protocol("WM_DELETE_WINDOW", self.cancel)
        set_window_size_simple(self.root)
        self.root.attributes('-alpha', 1.0)
        self.root.grab_set()
        self.root.focus_force()
        self.root.mainloop()

    def load(self):
        self.listbox.delete(0, END)
        self.datalist = get_list(self.path)
        for i, data_name in enumerate(self.datalist):
            self.listbox.insert(END, data_name)
            if self.single_cluster_data is not None and data_name in self.single_cluster_data:
                self.listbox.itemconfig(i, bg='SeaGreen1')
        if self.previous is not None:
            try:
                index = np.where(self.datalist == self.previous)[0][0]
                self.listbox.select_set(index)
            except IndexError:
                pass

    def openFolder(self):
        os.startfile(os.getcwd())

    def export_data_as_excel(self):

        def read_data_values_from_file(path):
            with open(path, encoding='UTF-8') as f:
                values = f.read().splitlines()
            assert len(values) > 0
            return values

        index = self.listbox.curselection()
        if index == ():
            return
        path = getExcelSavePath()
        data_path = "..\\data\\" + self.datalist[index] + ".txt"
        data = read_data_values_from_file(data_path)

        if not (data and path):
            return
        data_to_excel(path, data)

    def add(self):
        try:
            BaseXClient.Session('localhost', 1984, 'admin', 'admin')
            add_data(self.root, self.path)
            self.load()
        except ConnectionRefusedError:
            messagebox.showwarning("BaseX Client not started",
                                   "The connection to the local BaseX server could not be established. \n"
                                   "Please start the local BaseX server! \n"
                                   "For this, please install BaseX and execute 'bin/basexserver.bat'.")

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
