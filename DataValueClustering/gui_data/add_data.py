import os
from tkinter import Button, Label, Toplevel, Tk, Entry, END, Checkbutton, IntVar, messagebox, OptionMenu, StringVar, \
    ttk, Menu

import tk

from data_extraction.extract_xml_field import write_fielddata_from_xml, get_attributenames, get_fieldnames, \
    execute_xquery
from export.path import getOpenFilePath
from gui_general import CreateToolTip
from gui_general.help_popup_gui import menu_help_data_add


def add_data(master, path=""):
    AddData(master, path)


class AddData:

    def __init__(self, master, path=""):
        self.path = path

        self.root = Toplevel(master)
        self.root.title("Data Addition")
        self.root.configure(bg="white")
        self.root.grab_set()
        self.root.focus_force()
        self.canceled = False

        self.menu = Menu(self.root)
        self.menu.add_command(label="Help", command=lambda: menu_help_data_add(self.root))
        self.root.config(menu=self.menu)

        self.label_title = Label(self.root, text="Specify data from which to create the data value set", font=('TkDefaultFont', 12, 'bold'), anchor='c', justify="center", pady=10)
        self.label_title.grid(sticky='nswe', row=1, column=1, columnspan=4)

        self.label_name = Label(self.root, anchor="w", text="Name:")
        CreateToolTip(self.label_name, "The name of the data value set to be created.")
        self.entry_name = Entry(self.root, width=50)
        self.label_name.grid(sticky='nswe', row=2, column=1, columnspan=1)
        self.entry_name.grid(sticky='nswe', row=2, column=2, columnspan=3, pady=1, padx=1)

        self.label_path = Label(self.root, anchor="w", text="File:")
        CreateToolTip(self.label_path, "The XML file containing the data from which to generate the data value set.")
        self.entry_path = Entry(self.root, width=50, state="readonly")
        self.button_path = Button(self.root, text="...", command=self.selectpath)
        self.label_path.grid(sticky='nswe', row=3, column=1, columnspan=1)
        self.entry_path.grid(sticky='nswe', row=3, column=2, columnspan=2, pady=1, padx=1)
        self.button_path.grid(sticky='nsew', row=3, column=4, pady=1, padx=1)

        self.label_field = Label(self.root, anchor="w", text="Field:")
        CreateToolTip(self.label_field, "The name of the XML element from which to extract the data values.")
        self.fieldnames = list()
        self.field_selection = StringVar()
        self.combobox_field = ttk.Combobox(self.root, values=list(), state="disabled",
                                           textvariable=self.field_selection)
        self.field_selection.trace('w', (
            lambda a1, a2, a3: self.combobox_validation(self.fieldnames, self.field_selection, self.combobox_field)))
        self.label_field.grid(sticky='nswe', row=4, column=1, columnspan=1)
        self.combobox_field.grid(sticky='nswe', row=4, column=2, columnspan=3, pady=1, padx=1)

        self.label_attribute = Label(self.root, anchor="w", text="Attribute:")
        CreateToolTip(self.label_attribute, "Instead of extracting the XML content of the chosen element, the value of a specified attribute can be extracted.")
        self.attributenames = list()
        self.attribute_selection = StringVar()
        self.combobox_attribute = ttk.Combobox(self.root, width=50, state="disabled",
                                               textvariable=self.attribute_selection)
        self.attribute_selection.trace('w', (
            lambda a1, a2, a3: self.combobox_validation(self.attributenames, self.attribute_selection,
                                                        self.combobox_attribute)))
        self.state_attribute = IntVar(0)
        self.check_attribute = Checkbutton(self.root, variable=self.state_attribute,
                                           command=self.checkbox_attribute_change, state="disabled")
        self.label_attribute.grid(sticky='nswe', row=5, column=1, columnspan=1)
        self.check_attribute.grid(sticky='nswe', row=5, column=2, columnspan=1)
        self.combobox_attribute.grid(sticky='nswe', row=5, column=3, columnspan=2, pady=1, padx=1)

        self.button_ok = Button(self.root, text="OK", command=self.execute, width=55)
        self.button_ok.grid(sticky='nswe', row=6, column=1, columnspan=4)

        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.root.mainloop()

    def selectpath(self):
        newpath = getOpenFilePath("Select XML database")
        self.fieldnames = list()
        self.attributenames = list()
        try:
            size = os.stat(newpath).st_size
            if newpath.endswith(".gz") and size > 62914560:
                messagebox.showerror("Too large", "Selected File is larger than 60 MB\nPlease select a smaller file")
                return
            if newpath.endswith(".xml") and size > 716800000:
                messagebox.showerror("Too large", "Selected File is larger than 700 MB\nPlease select a smaller file")
                return
        except:
            return

        self.entry_path.configure(state="normal")
        self.entry_path.delete(0, END)
        self.entry_path.insert(0, newpath)
        self.entry_path.configure(state="readonly")

        self.fieldnames = get_fieldnames(newpath)
        if self.fieldnames:
            self.combobox_field.configure(state="normal")
            self.combobox_field.configure(values=self.fieldnames)
            self.check_attribute.configure(state="normal")
        else:
            self.combobox_field.configure(state="disabled")
            self.check_attribute.configure(state="disabled")

    def combobox_validation(self, values, selection, combobox):
        newlist = list()
        for i in values:
            if i.startswith(selection.get()):
                newlist.append(i)
        newcolor = "green" if selection.get() in newlist else "red" if newlist == list() else "black"
        combobox.configure(values=newlist, foreground=newcolor)
        return True

    def checkbox_attribute_change(self):
        if self.state_attribute.get() == 1:
            if self.attributenames == list():
                self.attributenames = get_attributenames(self.entry_path.get())
            self.combobox_attribute.configure(values=self.attributenames)
            self.combobox_attribute.configure(state="normal")
        else:
            self.combobox_attribute.configure(state="disabled")

    def execute(self):
        filename = self.entry_name.get() + ".txt"
        xmlfile = self.entry_path.get()
        field = self.combobox_field.get()

        if filename == ".txt":
            messagebox.showwarning("Wrong Configuration", "Please enter an identifiable name for your data.")
            return
        if xmlfile == "" or not self.fieldnames:
            messagebox.showwarning("Wrong Configuration", "The XML file is not valid.")
            return
        if field not in self.fieldnames:
            messagebox.showwarning("Wrong Configuration", "The input for field name is not valid.")
            return
        if self.state_attribute.get() == 1 and self.combobox_attribute.get() not in self.attributenames:
            messagebox.showwarning("Wrong Configuration", "The input for attribute name is not valid.")
            return

        if self.path != "":
            filename = self.path + "/" + filename

        attribute = None if self.state_attribute.get() == 0 else self.combobox_attribute.get()
        values = write_fielddata_from_xml(xmlfile, field, filename, attribute)
        if not values:
            messagebox.showwarning("No data", "Your configuration did result in no results.")
        else:
            self.close()

    def close(self):
        self.root.quit()
        self.root.destroy()


if __name__ == "__main__":
    print(add_data(Tk()))
