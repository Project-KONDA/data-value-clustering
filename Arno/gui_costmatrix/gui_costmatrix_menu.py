from tkinter import *

text = [
    ["Characters"],
    "The right input fields represent groups of characters. Please enter all characters, that",
    "should be in the group. Note, that the interface supports sequences like 'a-z' for",
    "letters and digits.",
    ["Weights"],
    "Enter numbers as weights when transforming the characters of the row to the column.",
    "Only the relative size of these fictive values matters."
]


def menu_help_cost_matrix():
    menu_information_display("Costmatrix Helper", text)


def menu_information_display(title, content):
    root = Tk()
    # root.geometry("500x200")
    root.title(title)
    root.configure(bg='white')

    for i, t in enumerate(content):
        if isinstance(t, str):
            Label(root, text=t, font=('Arial', 10),
                  anchor=W, justify=LEFT, background='white'
                  ).grid(row=i + 2, column=1, sticky=W + E)
        else:
            Label(root, text=t[0], font=('Arial', 12, 'bold'),
                  anchor=W, justify=LEFT, background='white'
                  ).grid(row=i + 2, column=1, sticky=W)

    def button_quit():
        root.destroy()

    Button(root, text='OK', command=button_quit,
           justify=RIGHT, width=15, background='snow'
           ).grid(row=len(text) + 3, column=1)

    root.update()
    root.geometry("500x" + str(root.winfo_height() + 10))

    root.mainloop()


if __name__ == "__main__":
    print(re.escape(".,:;?!"))
    print(re.escape("+-*/=\#€$%&|<>"))
    menu_help_cost_matrix()
