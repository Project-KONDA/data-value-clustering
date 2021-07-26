import os
from tkinter import Button, Label, Toplevel, Tk, Entry, END, Checkbutton, IntVar, messagebox

import tk

from data_extraction.extract_xml_field import write_fielddata_from_xml, get_attributenames, get_fieldnames, \
    execute_xquery
from export.path import getOpenFilePath


def add_data(master, path=""):
    AddData(master, path)


class AddData:

    def __init__(self, master, path=""):
        self.path = path

        self.root = Toplevel(master)
        self.root.title("Add Data")
        self.root.configure(bg="white")
        self.root.grab_set()
        self.root.focus_force()
        self.canceled = False

        self.label_title = Label(self.root, text="Extrude New Data Set", font=('Helvatical bold', 19))
        self.label_title.grid(sticky='nswe', row=1, column=1, columnspan=4)

        self.label_name = Label(self.root, anchor="w", text="Name:")
        self.entry_name = Entry(self.root, width=50)
        self.label_name.grid(sticky='nswe', row=2, column=1, columnspan=1)
        self.entry_name.grid(sticky='nswe', row=2, column=2, columnspan=3)

        self.label_path = Label(self.root, anchor="w", text="File:")
        self.entry_path = Entry(self.root, width=50, state="readonly")
        self.button_path = Button(self.root, text="...", width=3, command=self.selectpath)
        self.label_path.grid(sticky='nswe', row=3, column=1, columnspan=1)
        self.entry_path.grid(sticky='nswe', row=3, column=2, columnspan=2)
        self.button_path.grid(sticky='nse', row=3, column=4, pady=1, padx=1)

        self.label_field = Label(self.root, anchor="w", text="Field:")
        self.entry_field = Entry(self.root, state="disabled")
        self.label_field.grid(sticky='nswe', row=4, column=1, columnspan=1)
        self.entry_field.grid(sticky='nswe', row=4, column=2, columnspan=3)

        self.label_attribute = Label(self.root, anchor="w", text="Attribute:")
        self.entry_attribute = Entry(self.root, width=50, state="disabled")
        self.state_attribute = IntVar(0)
        self.check_attribute = Checkbutton(self.root, variable=self.state_attribute, command=self.activate_attribute,
                                           state="disabled")
        self.label_attribute.grid(sticky='nswe', row=5, column=1, columnspan=1)
        self.check_attribute.grid(sticky='nswe', row=5, column=2, columnspan=1)
        self.entry_attribute.grid(sticky='nswe', row=5, column=3, columnspan=2)

        self.button_ok = Button(self.root, text="OK", command=self.execute, width=55)
        self.button_ok.grid(sticky='nswe', row=6, column=1, columnspan=4)

        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.root.mainloop()

    def selectpath(self):
        newpath = getOpenFilePath("Select XML database")
        try:
            size = os.stat(newpath).st_size
            if size > 62914560:
                messagebox.showerror("Too large", "Selected File is larger than 60 MB\nPlease select a smaller file")
                return
        except:
            return
        self.entry_path.configure(state="normal")
        self.entry_path.delete(0, END)
        self.entry_path.insert(0, newpath)
        self.entry_path.configure(state="readonly")

        self.fieldnames = get_fieldnames(newpath)
        self.attributenames = get_attributenames(newpath)

        self.entry_field.configure(state="normal")
        self.check_attribute.configure(state="normal")

    def activate_attribute(self):
        self.entry_attribute.configure(state="normal" if self.state_attribute.get() == 1 else "disabled")

    def execute(self):
        xmlfile = self.entry_path.get()
        field = self.entry_field.get()
        path = self.entry_name.get() + ".txt"
        if xmlfile != "" and field != "" and path != "":
            if self.path != "":
                if self.path.endswith("/"):
                    path = self.path + path
                else:
                    path = self.path + "/" + path
            attribute = None
            if self.state_attribute.get() == 1:
                attribute = self.entry_attribute.get()
            write_fielddata_from_xml(xmlfile, field, path, attribute)
            self.close()

    def close(self):
        self.root.quit()
        self.root.destroy()


if __name__ == "__main__":
    print(add_data(Tk()))
