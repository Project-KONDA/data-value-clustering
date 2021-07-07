from tkinter import Tk, Listbox, Button, Label, END

from data_extraction import get_sources_in_experiment_data_directory


def select_data(path):
    pass


def get_list(path = ""):
    return get_sources_in_experiment_data_directory()[:,0]


class SelectData():
    def __init__(self, path):
        self.path = path

        self.root = Tk()
        self.root.title("Select Data")

        self.label_title = Label(self.root, text="Select Data Set", bg="white",
                                 font=('Helvatical bold', 19))

        self.listbox = Listbox(self.root, selectmode="single", width=40)

        self.button_ok = Button(self.root, text="OK", command=self.close)

        self.label_title.pack()
        self.listbox.pack()
        self.button_ok.pack()

        self.load()
        self.root.mainloop()

    def load(self):
        self.datalist = get_list(self.path)
        for i in self.datalist:
            self.listbox.insert(END, i)

    def add(self):
        self.load()

    def close(self):
        print(self.datalist(self.listbox.curselection().__getitem__(0)))


if __name__ == "__main__":
    path = ""
    SelectData(path)
