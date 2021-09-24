from tkinter import Label


def create_parameter_caption(caption, color="black"):
    return lambda parent: ParameterCaption(parent, caption, color)


class ParameterCaption:

    def __init__(self, root, caption, color="black"):
        self.frame = Label(root, anchor='center', text=caption, fg=color, font=('TkDefaultFont', 14, 'bold'), )
        self.name = "Caption " + caption
