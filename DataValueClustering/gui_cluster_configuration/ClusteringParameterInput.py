from tkinter import Label, Checkbutton, Button, Tk, IntVar, StringVar, Frame, LEFT, RIGHT, BOTH, GROOVE, font, Canvas, \
    Scrollbar, FLAT
import numpy as np

from gui_cluster_configuration.parameter_frames.ClusteringParameter import ClusteringParameter


def get_configuration_parameters(title, parameter_frame_inits):
    input = ClusterConfigurationInput(title, parameter_frame_inits)
    return input.get()


class ClusterConfigurationInput:

    def __init__(self, title, parameter_frame_inits):
        self.root = Tk()
        self.root.title(title)
        self.root.resizable(False, True)
        self.root.minsize(200, 200)
        self.root.grid_rowconfigure(1, weight=1)

        self.parameter_frame_inits = parameter_frame_inits
        self.n = len(self.parameter_frame_inits)
        self.parameters = np.empty(self.n, dtype=ClusteringParameter)

        # scrollable canvas:
        self.canvas_border = Frame(self.root, bd=2, relief='groove')
        self.canvas_border.grid_rowconfigure(0, weight=1)
        self.canvas = Canvas(self.canvas_border, bg='white', highlightthickness=0, width=self.root.winfo_screenwidth() / 25 + self.root.winfo_screenwidth() / 3 + 12)
        self.scrollbar = Scrollbar(self.canvas_border, orient="vertical", command=self.canvas.yview)
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)
        self.scrollable_frame = Frame(self.canvas)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        self.canvas_frame = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", width=self.canvas.winfo_screenwidth())
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # caption:
        self.label_text = StringVar()
        self.label_text.set("Please specify the following parameters")
        self.label = Label(self.root, anchor='w', textvariable=self.label_text, bg='SystemButtonFace',
                           font=font.Font(size=14))


        # button:
        self.button = Button(self.root, text='OK', command=self.close, bg='white')

        for i, frame_init in enumerate(self.parameter_frame_inits):
            self.parameters[i] = frame_init(self.scrollable_frame)

        self.record_parameters()
        pass

    def on_mousewheel(self, event):
        if self.scrollable_frame.winfo_height() > self.canvas.winfo_height():
            self.canvas.yview_scroll(-1 * (event.delta // 120), "units")

    def close(self):
        self.root.destroy()

    def record_parameters(self):

        self.label.grid(row=0, column=0, sticky='w', pady=5, padx=5)
        self.canvas_border.grid(row=1, column=0, sticky='nswe')
        self.canvas.grid(row=0, column=0, sticky='nswe')
        self.scrollbar.grid(row=0, column=1, sticky='nswe')

        for i, param in enumerate(self.parameters):
            param.frame.grid(row=i+1, column=0, sticky='nswe', pady=5, padx=5)

        self.button.grid(row=2, column=0, sticky='nswe')

        self.root.mainloop()
        pass

    def get(self):
        parameter_values = list()
        for i, param in enumerate(self.parameters):
            parameter_values.append(param.get())
        return parameter_values


if __name__ == "__main__":
    ClusterConfigurationInput("Test", list())