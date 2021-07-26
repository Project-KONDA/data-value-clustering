from tkinter import Button, Label, Toplevel, Tk, Entry, END

from data_extraction.extract_xml_field import write_fielddata_from_xml
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

        self.datalist = list()
        self.canceled = False

        self.label_title = Label(self.root, text="Extrude New Data Set", font=('Helvatical bold', 19))
        self.label_title.grid(sticky='nswe', row=1, column=1, columnspan=4)

        self.label_name = Label(self.root, text="Name:")
        self.entry_name = Entry(self.root, width=50)
        self.label_name.grid(sticky='nswe', row=2, column=1, columnspan=1)
        self.entry_name.grid(sticky='nswe', row=2, column=2, columnspan=3)

        self.label_path = Label(self.root, text="File:")
        self.entry_path = Entry(self.root, width=50)
        self.button_path = Button(self.root, text="...", width=3, command=self.selectpath)
        self.label_path.grid(sticky='nswe', row=3, column=1, columnspan=1)
        self.entry_path.grid(sticky='nswe', row=3, column=2, columnspan=3)
        self.button_path.grid(sticky='nse', row=3, column=4, pady=1, padx=1)

        self.label_field = Label(self.root, text="Field:")
        self.entry_field = Entry(self.root)
        self.label_field.grid(sticky='nswe', row=4, column=1, columnspan=1)
        self.entry_field.grid(sticky='nswe', row=4, column=2, columnspan=3)

        # self.label_attribute = Label(self.root, text="Attribute:")
        # self.entry_attribute = Entry(self.root, width=50, state="disabled")
        # self.label_attribute.grid(sticky='nswe', row=5, column=1, columnspan=1)
        # self.entry_attribute.grid(sticky='nswe', row=5, column=2, columnspan=3)

        self.button_ok = Button(self.root, text="OK", command=self.execute, width=55)
        self.button_ok.grid(sticky='nswe', row=6, column=1, columnspan=4)

        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.root.mainloop()

    def selectpath(self):
        newpath = getOpenFilePath("Select XML database")
        self.entry_path.insert(0, newpath)

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
            write_fielddata_from_xml(xmlfile, field, path)
        self.close()

    def close(self):
        self.root.quit()
        self.root.destroy()


if __name__ == "__main__":
    print(add_data(Tk()))
