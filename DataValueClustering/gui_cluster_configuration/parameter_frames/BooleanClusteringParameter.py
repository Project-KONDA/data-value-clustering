from tkinter import IntVar, Checkbutton, Label

from gui_cluster_configuration.parameter_frames.ClusteringParameter import ClusteringParameter


def create_boolean_frame(name, explanation, default, deactivatable=False, default_active=False,
                         plot_function=None, previous_value=None, suggestion=None):
    return lambda parent: BooleanClusteringParameter(parent, name, explanation, default, previous_value=previous_value, deactivatable=deactivatable,
                                                     default_active=default_active, plot_function=plot_function, suggestion=suggestion)


class BooleanClusteringParameter(ClusteringParameter):
    '''
    A widget for specifying a boolean parameter of a clusering algorithm via a check button.
    '''

    def __init__(self, parent, name, explanation, default, previous_value=None, deactivatable=False,
                 default_active=False, plot_function=None, suggestion=None):
        super().__init__(parent, name, explanation, deactivatable, default_active, plot_function)
        self.default = default
        self.previous = previous_value

        self.value_var = IntVar()
        if self.previous is None:
            self.value_var.set(int(self.default))
        else:
            self.value_var.set(int(self.previous))

        self.check_boolean = Checkbutton(self.frame, variable=self.value_var, bg='white', anchor='nw', padx=20)
        # self.check_boolean.grid(row=0, column=1, sticky='se')
        self.check_boolean.grid(row=2, column=1, sticky='nw')

        self.validation_suggestion = None
        self.label_suggested = None
        if suggestion is not None and self.name in suggestion:
            self.validation_suggestion = suggestion[self.name]
            self.label_suggested = Label(self.frame,
                                         text="Advice: " + self.validation_suggestion,
                                         anchor='nw', pady=10, fg='blue', bg='white')
            self.label_suggested.grid(row=2, column=2, sticky='w')


        self.update_active()

    def activate(self):
        super().activate()
        self.check_boolean.config(state='normal', bg='white')
        if self.label_suggested is not None:
            self.label_suggested.config(state='normal', fg="blue", bg='white')

    def deactivate(self):
        super().deactivate()
        self.check_boolean.config(state='disabled', bg='grey90')
        if self.label_suggested is not None:
            self.label_suggested.config(state='disabled', bg='grey90')

    def reset(self):
        self.value_var.set(int(self.default))
        super().reset()

    def get_result(self):
        return bool(self.value_var.get()) if self.is_activated.get() else None


if __name__ == "__main__":
    import gui_cluster_configuration
    bool1 = create_boolean_frame("My Param 1", "This is a test parameter.", True, deactivatable=False)
    bool2 = create_boolean_frame("My Param 2", "This is a test parameter.", True, deactivatable=True)
    bool3 = create_boolean_frame("My Param 3", "This is a test parameter.", False, deactivatable=False)
    bool4 = create_boolean_frame("My Param 4", "This is a test parameter.", False, deactivatable=True)
    bool_input = gui_cluster_configuration.get_configuration_parameters("Test", [bool1, bool2, bool3, bool4])
    print(bool_input.get_result())
