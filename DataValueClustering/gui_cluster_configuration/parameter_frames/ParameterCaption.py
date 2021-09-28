from tkinter import Label, Frame


def create_parameter_caption(caption, sub, color="black"):
    return lambda parent: ParameterCaption(parent, caption, sub, color)


class ParameterCaption:

    def __init__(self, root, caption, sub, color="black"):
        self.frame = Frame(root)
        caption_label = Label(self.frame, anchor='center', text=caption, fg=color, font=('TkDefaultFont', 14, 'bold'))
        caption_label.grid(row=0, column=0, sticky='nswe', columnspan=2)
        sub_label = Label(self.frame, anchor='nw', justify="left", text=sub)
        sub_label.grid(row=1, column=0, sticky='nswe')
        self.name = "Caption " + caption
