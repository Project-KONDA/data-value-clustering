from tkinter import Tk, Listbox, Button, Label, END, Scrollbar, Toplevel

from data_extraction import get_sources_in_experiment_data_directory


def get_list(path=""):
    return get_sources_in_experiment_data_directory()[:, 0]


def select_data(root):
    return SelectData("", root).get()


class SelectData:
    def __init__(self, path, root):
        self.path = path

        self.root = Toplevel(root)
        # self.root.title("Select Data")

        self.result = None

        self.label_title = Label(self.root, text="Select Data Set", bg="white",
                                 font=('Helvatical bold', 19))

        self.listbox = Listbox(self.root, selectmode="single", width=40, height=10)

        self.button_add = Button(self.root, text="+", command=self.add, width=3, state="disabled", bg="grey80")
        self.button_ok = Button(self.root, text="OK", command=self.close, width=27)

        self.button_add.grid(sticky='nswe', row=5, column=1, columnspan=1)
        self.label_title.grid(sticky='nswe', row=1, column=1, columnspan=2)
        self.listbox.grid(sticky='nswe', row=3, column=1, columnspan=2)
        self.button_ok.grid(sticky='nswe', row=5, column=2, columnspan=1)

        self.load()
        self.root.mainloop()

    def load(self):
        self.datalist = get_list(self.path)
        for i in self.datalist:
            self.listbox.insert(END, i)

    def add(self):
        # TODO load
        self.load()

    def close(self):
        index = self.listbox.curselection()
        try:
            index = index[0]
        except:
            return
        # print(self.datalist[index])
        self.result = self.datalist[index]
        self.root.quit()
        self.root.destroy()


    def get(self):
        return self.result


if __name__ == "__main__":
    # path = ""
    # SelectData(path)
    print(select_data(Tk()))
