'''text popup for context menu, used as help'''
from tkinter import *


def menu_help_distance_choice(master):
    """help popup for Distance Choice view"""
    text = [
        "The Distance Choice view allows you to select a method for configuring the distance calculation.",
        "Currently only the weighted Levenshtein distance is supported and can be configured via 3 different methods.",
        "Note that the easier methods allow less flexibility.",
        "Further note that once you use the Slider or Matrix View, you cannot open your configuration via the Blob View."
    ]
    menu_information_display(master, "Abstraction Configuration - Help", text)


def menu_help_abstraction(master):
    """help popup for Abstraction Configuration view"""
    text = [
        "The Abstraction Configuration view allows you to configure the abstraction from irrelevant features of the data values.",
        "For this, you should answer the questions on the left-hand side.",
        "You can start with one of the predefined configurations if you like.",
        "When answering the questions, please use your domain knowledge about the selected data and data field to decide which feature of the data values are irrelevant for clustering.",
        "Make sure that you do not abstract from features that you do not expect or that may alter the data values’ meaning significantly.",
        "Note that each question is explained in detail in the corresponding tool tip shown when hovering over the question.",
        "On the right hand side, the result of applying the abstraction to the first 100 data values is shown and updated dynamically.",
    ]
    menu_information_display(master, "Abstraction Configuration - Help", text)


def menu_help_data_add(master):
    """help popup for Add Data view"""
    text = [
        "The Add Data view allows you to add a data set to the list of supported data sets selectable in the Select Data view.",
        "Currently only XML data is supported.",
        "For this, you must specify a name for the data set, which will be displayed in the Select Data view.",
        "Further, you must specify the XML file containing the data and specify the data field (i.e. XML element) of interest.",
        "Per default the content of the corresponding XML elements will be extracted."
        "Alternatively you can specify an attribute whose value will be extracted.",
    ]
    menu_information_display(master, "Add Data - Help", text)


def menu_help_data_selection(master):
    """help popup for Select Data view"""
    text = [
        "The Select Data view allows you to select the data set to be clustered.",
        "Each data set consists of a set of data values extracted from a database.",
        "When first starting the program, a few predefined data sets are available.",
        "To add a data set, press the '+' button below.",
        "To remove a data set, press the '-' button below, but be careful as once removed data sets cannot be recovered."
    ]
    menu_information_display(master, "Select Data - Help", text)


def menu_help_hub(master):
    """help popup for hub view"""
    text = [
        "The Hub view is the central view of this program for data value clustering.",
        "The data value clustering requires you to perform 4 configuration steps: data, abstraction, distance and clustering configuration.",
        "The hub view allows you to navigate through the 4 configuration steps and access the calculated clustering subsequently.",
        "",
        "The configuration steps are performed in separate views which are opened upon clicking the corresponding button in the hub view.",
        "The configuration step required to be performed next is highlighted in blue.",
        "We advice you to perform the configuration steps in the given order.",
        "",
        "Once configured, the data extraction and abstraction are performed automatically.",
        "This typically takes only a few seconds.",
        "But since distance calculation and clustering may take up to multiple hours, they are startet manually by pressing the corresponding play button.",
        "",
        "Note that below each configuration button there is a small label indicating the status, "
        "i.e. whether no configuration is present, the configuration is in progress, ",
        "the calculation is in progress or the calculation is done.",
        "On the right hand side you see previews of the 4 configurations.",
        "You can save, load and reset your configuration via the menu.",
        "",
        "Once the clustering is ready, you can open the result view to see further information and perform the validation or save the clustering in an Excel file.",
    ]
    menu_information_display(master, "Hub - Help", text)

def menu_help_cost_map(master):
    """help popup for matrix view"""
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
    menu_information_display(master, "Costmatrix - Help", text)


def menu_help_blob_input(master):
    """help popup for Blob view"""
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
        "When the blobs just barely touch each other the distance between them is interpreted",
        "as the value 1.",
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
    menu_information_display(master, "Distance Specification - Help", text)


def menu_information_display(master, title, content):
    """
    Show window with text
    as help feature for context menu

    :param title: str
        window title
    :param content: list[str]
        help text for window content
        one string per line
    :return:
    """

    root = Toplevel(master)
    # root.geometry("500x200")
    root.title("Help")
    root.configure(bg='white')
    root.resizable(False, False)
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
        root.quit()
        root.destroy()

    Button(root, text='OK', command=button_quit,
           justify=RIGHT, width=15, background='snow'
           ).grid(row=len(content) + 3, column=1)

    root.update()
    # root.geometry("500x" + str(root.winfo_height() + 10))
    root.protocol("WM_DELETE_WINDOW", button_quit)
    root.mainloop()


if __name__ == "__main__":
    # menu_help_cost_matrix()
    menu_help_blob_input()
