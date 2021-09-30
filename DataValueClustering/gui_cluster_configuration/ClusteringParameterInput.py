from tkinter import Label, Button, Tk, StringVar, Frame, font, Canvas, Scrollbar, Toplevel, Menu
import numpy as np

from gui_cluster_configuration.parameter_frames.ClusteringParameter import ClusteringParameter
from gui_general.help_popup_gui import menu_help_clustering_configuration
from gui_general.scrollable_frame import create_scrollable_frame
from gui_general.window_size import set_window_size_simple


def get_configuration_parameters(master, title, parameter_frame_inits, dependencies, suggestion=None):
    input = ClusterConfigurationInput(master, title, parameter_frame_inits, dependencies, suggestion)
    return input.get()


class ClusterConfigurationInput:
    '''
    A view that contains widgets for specifying the parameters of the clustering algorithm.
    '''

    def __init__(self, master, title, parameter_frame_inits, dependencies, suggestion=None):
        self.root = Toplevel(master)
        self.root.title(title)
        self.root.resizable(False, True)
        self.root.minsize(200, 200)
        self.root.grid_rowconfigure(3, weight=1)
        self.root.config(bg='white')
        self.canceled = False
        self.root.focus_force()
        self.root.grab_set()

        self.menu = Menu(self.root)
        self.menu.add_command(label="Help", command=lambda: menu_help_clustering_configuration(self.root))
        self.root.config(menu=self.menu)

        self.root.bind_all("<Return>", self.close)

        self.parameter_frame_inits = parameter_frame_inits
        self.n = len(self.parameter_frame_inits)
        self.dependencies = dependencies
        self.parameters = np.empty(self.n, dtype=ClusteringParameter)

        # scrollable canvas:
        self.around_canvas_frame, self.canvas, self.scrollable_frame = create_scrollable_frame(self.root)
        self.root.rowconfigure(3, weight=1)
        self.around_canvas_frame.grid(row=3, column=0, sticky='nsew')
        self.around_canvas_frame.configure(bd=2, relief='groove')
        self.scrollable_frame.configure(bg='SystemButtonFace')
        self.canvas.configure(bg='SystemButtonFace')

        # caption:
        self.label_text = StringVar()
        self.label_text.set("Specify the following parameters of the selected clustering algorithm")
        self.label = Label(self.root, anchor='c', justify="center", textvariable=self.label_text, bg='white',
                           font=('TkDefaultFont', 12, 'bold'))

        self.hint_label_text = StringVar()
        self.hint_label_text.set("Typically the default values are a good starting point.")
        self.hint_label = Label(self.root, anchor='c', justify="center", textvariable=self.hint_label_text, bg='white')

        self.label_suggested = None
        if suggestion is not None:
            self.label_suggested = Label(self.root, text="Advice based on the evaluation is given in blue next to sliders and highlighted in green for enumerations.", bg="white", anchor='w', pady=10, fg='blue', justify='left')

        # button:
        self.button = Button(self.root, text='OK', command=self.close, bg='white')

        for i, frame_init in enumerate(self.parameter_frame_inits):
            self.parameters[i] = frame_init(self.scrollable_frame)

        for i, dep in enumerate(self.dependencies):
            param1 = self.get_frame_with_name(dep[0])
            param2 = self.get_frame_with_name(dep[1])
            param1.add_dependency(param2, dep[2], dep[3])

        for i, p in enumerate(self.parameters):
            if isinstance(p, ClusteringParameter):
                p.adopt_previous_activation()
                p.update_active()


        self.record_parameters()

    def get_frame_with_name(self, name):
        for i, param in enumerate(self.parameters):
            if param.name == name:
                return param

    def close(self, event=None):
        self.unbind_all()
        self.root.quit()
        self.root.destroy()

    def record_parameters(self):

        self.label.grid(row=0, column=0, sticky='nsew', pady=(10,0), padx=5)
        self.hint_label.grid(row=1, column=0, sticky='nsew', pady=(0,10), padx=5)
        if self.label_suggested is not None:
            self.label_suggested.grid(row=2, column=0, sticky='senw', padx=10)

        for i, param in enumerate(self.parameters):
            param.frame.grid(row=i + 1, column=0, sticky='nsew', pady=5, padx=5)

        self.button.grid(row=4, column=0, sticky='nsew')

        set_window_size_simple(self.root)

        self.root.after(1, lambda: self.root.focus_force())

        self.root.protocol("WM_DELETE_WINDOW", self.cancel)
        self.root.mainloop()

    def unbind_all(self):
        self.root.unbind_all("<Return>")
        self.root.unbind_all("<MouseWheel>")

    def cancel(self):
        self.canceled = True
        self.close()

    def get(self):
        parameter_values = ()
        for i, param in enumerate(self.parameters):
            if isinstance(param, ClusteringParameter):
                if self.canceled:
                    parameter_values += (None, )
                else:
                    parameter_values += (param.get_result(),)
        return parameter_values


if __name__ == "__main__":
    import gui_cluster_configuration

    explanation = "This is a test parameter."
    bool_param1 = gui_cluster_configuration.parameter_frames.BooleanClusteringParameter.create_boolean_frame(
        "First Boolean Parameter", explanation, True, deactivatable=True)
    bool_param2 = gui_cluster_configuration.parameter_frames.BooleanClusteringParameter.create_boolean_frame(
        "Second Boolean Parameter", explanation, True, deactivatable=False)

    enum1_options = np.array([["a", "AA"], ["b", "BB"], ["c", "CC"]])
    enum1_suggestions = ["a", "b"]
    enum1_previous = ["c"]
    enum2_options = np.array([["0", "00"], ["1", "11"], ["2", "22"]])
    enum2_suggestions = ["0"]
    enum_param1 = gui_cluster_configuration.parameter_frames.EnumClusteringParameter.create_enum_frame(
        "First Enumeration Parameter", explanation, enum1_options, enum1_suggestions, previous_value=enum1_previous, deactivatable=True)
    enum_param2 = gui_cluster_configuration.parameter_frames.EnumClusteringParameter.create_enum_frame(
        "Second Enumeration Parameter", explanation, enum2_options, enum2_suggestions, deactivatable=False)

    slider_param1 = gui_cluster_configuration.parameter_frames.SliderClusteringParameter.create_slider_frame(
        "First Slider Parameter", explanation, 1, 30, 4, resolution=2, deactivatable=True)
    slider_param2 = gui_cluster_configuration.parameter_frames.SliderClusteringParameter.create_slider_frame(
        "Second Slider Parameter", explanation, 1.0, 10.0, 2.0, resolution=0.01, deactivatable=False)

    param_list = [bool_param1, bool_param2, enum_param1, enum_param2, slider_param1, slider_param2]
    params = get_configuration_parameters(Tk(), "Test", param_list, list())
    print(params)