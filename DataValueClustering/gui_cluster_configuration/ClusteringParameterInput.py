from tkinter import Label, Button, Tk, StringVar, Frame, font, Canvas, Scrollbar
import numpy as np

from gui_cluster_configuration.parameter_frames.ClusteringParameter import ClusteringParameter


def get_configuration_parameters(title, parameter_frame_inits, dependencies):
    input = ClusterConfigurationInput(title, parameter_frame_inits, dependencies)
    return input.get()


class ClusterConfigurationInput:
    '''
    A view that contains widgets for specifying the parameters of the clustering algorithm.
    '''

    def __init__(self, title, parameter_frame_inits, dependencies):
        self.root = Tk()
        self.root.title(title)
        self.root.resizable(False, True)
        self.root.minsize(200, 200)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.config(bg='white')

        self.root.bind_all("<Return>", self.close)

        self.parameter_frame_inits = parameter_frame_inits
        self.n = len(self.parameter_frame_inits)
        self.dependencies = dependencies
        self.parameters = np.empty(self.n, dtype=ClusteringParameter)

        # scrollable canvas:
        self.canvas_border = Frame(self.root, bg='SystemButtonFace', bd=2, relief='groove')
        self.canvas_border.grid_rowconfigure(0, weight=1)
        self.canvas = Canvas(self.canvas_border, bg='SystemButtonFace', highlightthickness=0,
                             width=self.root.winfo_screenwidth() / 25 + self.root.winfo_screenwidth() / 3 + 12)
        self.scrollbar = Scrollbar(self.canvas_border, orient='vertical', command=self.canvas.yview)
        self.canvas.bind_all('<MouseWheel>', self.on_mousewheel)
        self.scrollable_frame = Frame(self.canvas)
        self.scrollable_frame.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox('all')))
        self.canvas_frame = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor='nw',
                                                      width=self.canvas.winfo_screenwidth())
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # caption:
        self.label_text = StringVar()
        self.label_text.set("Please specify the following parameters")
        self.label = Label(self.root, anchor='w', textvariable=self.label_text, bg='white',
                           font=font.Font(size=14))

        # button:
        self.button = Button(self.root, text='OK', command=self.close, bg='white')

        for i, frame_init in enumerate(self.parameter_frame_inits):
            self.parameters[i] = frame_init(self.scrollable_frame)

        for i, dep in enumerate(self.dependencies):
            print(str(dep))
            param1 = self.get_frame_with_name(dep[0])
            param2 = self.get_frame_with_name(dep[1])
            param1.add_dependency(param2, dep[2], dep[3])

        for i, p in enumerate(self.parameters):
            p.update_active()

        self.record_parameters()

    def get_frame_with_name(self, name):
        for i, param in enumerate(self.parameters):
            if param.name == name:
                return param

    def on_mousewheel(self, event):
        if self.scrollable_frame.winfo_height() > self.canvas.winfo_height():
            self.canvas.yview_scroll(-1 * (event.delta // 120), 'units')

    def close(self, event=None):
        self.root.destroy()

    def record_parameters(self):

        self.label.grid(row=0, column=0, sticky='w', pady=5, padx=5)
        self.canvas_border.grid(row=1, column=0, sticky='nsew')
        self.canvas.grid(row=0, column=0, sticky='nsew')
        self.scrollbar.grid(row=0, column=1, sticky='nsew')

        for i, param in enumerate(self.parameters):
            param.frame.grid(row=i + 1, column=0, sticky='nsew', pady=5, padx=5)

        self.button.grid(row=2, column=0, sticky='nsew')

        # Center Window on Screen
        self.root.update_idletasks()
        midx = max(0, self.root.winfo_screenwidth() // 2 - self.root.winfo_reqwidth() // 2)
        midy = max(0, self.root.winfo_screenheight() // 3 - self.root.winfo_reqheight() // 2)
        self.root.geometry(f"+%s+%s" % (midx, midy))

        self.root.after(1, lambda: self.root.focus_force())
        self.root.mainloop()

    def get(self):
        parameter_values = ()
        for i, param in enumerate(self.parameters):
            parameter_values += (param.get_result(),)
        return parameter_values


if __name__ == "__main__":
    import gui_cluster_configuration

    explanation = "This is a test parameter."
    bool_param1 = gui_cluster_configuration.parameter_frames.BooleanClusteringParameter.create_boolean_frame(
        "First Boolean Parameter", explanation, True, True)
    bool_param2 = gui_cluster_configuration.parameter_frames.BooleanClusteringParameter.create_boolean_frame(
        "Second Boolean Parameter", explanation, True, False)

    enum1_options = np.array([["a", "AA"], ["b", "BB"], ["c", "CC"]])
    enum1_suggestions = ["a", "b"]
    enum2_options = np.array([["0", "00"], ["1", "11"], ["2", "22"]])
    enum2_suggestions = ["0"]
    enum_param1 = gui_cluster_configuration.parameter_frames.EnumClusteringParameter.create_enum_frame(
        "First Enumeration Parameter", explanation, enum1_options, enum1_suggestions, True)
    enum_param2 = gui_cluster_configuration.parameter_frames.EnumClusteringParameter.create_enum_frame(
        "Second Enumeration Parameter", explanation, enum2_options, enum2_suggestions, False)

    slider_param1 = gui_cluster_configuration.parameter_frames.SliderClusteringParameter.create_slider_frame(
        "First Slider Parameter", explanation, 1, 30, 4, 2, True)
    slider_param2 = gui_cluster_configuration.parameter_frames.SliderClusteringParameter.create_slider_frame(
        "Second Slider Parameter", explanation, 1.0, 10.0, 2.0, 0.01, False)

    param_list = [bool_param1, bool_param2, enum_param1, enum_param2, slider_param1, slider_param2]
    params = get_configuration_parameters("Test", param_list)
    print(params)