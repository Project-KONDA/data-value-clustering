from tkinter import *


def menu_help_cost_matrix():
    text = [
        "This view is designed to give full control over the configuration of distances between",
        "text values.",
        "",
        ["Characters"],
        "The right input fields represent groups of characters. Please enter all characters, that",
        "should be in the group. Note, that the interface supports sequences like 'a-z' for",
        "letters and digits.",
        "The first row and column is reserved for the empty string. Here the cost of adding",
        "and deleting a character is entered.",
        "The last row and column does catch all not included characters.",
        "",
        ["Weights"],
        "Enter numbers as weights when transforming the characters of the row to the column.",
        "Only the relative size of these fictive values matters.",
        "Because the distance between two text values shall be symmetrical, the matrix is",
        "mirrored on the diagonal. The entry fields above the diagonal are read only."
    ]
    menu_information_display("Costmatrix Helper", text)


def menu_help_blob_input():
    text = [
        "This view is used to simplify the configuration of distances between text values.",
        "",
        ["Blobs"],
        "Each of the spheres (we call them 'blobs') in this diagram represent a group of similar",
        "characters. That group of characters is described in the label. There is one empty",
        "blue blob. This represents an empty text.",
        "",
        ["Distance"],
        "An important input is the distance between these blobs. We interpret these as the ",
        "cost to replace one character of one blob to a character of the second blob. The cost ",
        "of deleting or adding a character is represented by the distance to the special empty ",
        "blue blob.",
        # interpretation
        " When the blobs just barely touch each other the distance between them is interpreted as the value 1.",
        # controls
        "The distances can be modified via drag&drop.",
        "",
        ["Size"],
        "The size of each blob represents the distance between characters of said group.",
        "Some blobs can not be scaled. These are on default fixed on the minimal size and",
        "are slightly less saturated. The fixed blobs depend on your previous selection.",
        # interpretation
        "Hereby the minimum size represents the value 0. The default size is 1.",
        # controls
        "The size of not fixed blobs can be changed via the scroll wheel while the mouse is ",
        "over it. The default size can be restored by pressing N on mouse over."
    ]
    menu_information_display("Distance Specification Helper", text)


def menu_information_display(title, content):
    root = Tk()
    # root.geometry("500x200")
    root.title("Help")
    root.configure(bg='white')
    Label(root, text=title, font='Arial 14 bold underline',
          anchor=W, justify=LEFT, fg="green", background='white'
          ).grid(row=1, column=1, sticky=W)

    for i, t in enumerate(content):
        if isinstance(t, str):
            Label(root, text=t, font='Arial 10',
                  anchor=W, justify=LEFT, fg="green", background='white'
                  ).grid(row=i + 2, column=1, sticky=W + E)
        else:
            Label(root, text=t[0], font='Arial 12 bold',
                  anchor=W, justify=LEFT, fg="green", background='white'
                  ).grid(row=i + 2, column=1, sticky=W)

    def button_quit():
        root.destroy()

    Button(root, text='OK', command=button_quit,
           justify=RIGHT, width=15, background='snow'
           ).grid(row=len(content) + 3, column=1)

    root.update()
    root.geometry("500x" + str(root.winfo_height() + 10))

    root.mainloop()


if __name__ == "__main__":
    # menu_help_cost_matrix()
    menu_help_blob_input()
