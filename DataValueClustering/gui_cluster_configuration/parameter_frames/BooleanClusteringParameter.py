from tkinter import IntVar, Checkbutton

from gui_cluster_configuration.parameter_frames.ClusteringParameter import ClusteringParameter


def create_boolean_frame(name, explanation, default, deactivatable=False):
    return lambda parent: BooleanClusteringParameter(
        parent, name, explanation, default, deactivatable)


class BooleanClusteringParameter(ClusteringParameter):

    def __init__(self, parent, name, explanation, default, deactivatable=False):
        super().__init__(parent, name, explanation, deactivatable)
        self.default = default

        self.value_var = IntVar()
        self.value_var.set(int(self.default))

        self.check_boolean = Checkbutton(self.frame, variable=self.value_var, bg='white', anchor='nw', padx=20)
        self.check_boolean.grid(row=0, column=1, sticky='se')
        # self.check_boolean.grid(row=2, column=1, sticky='nw')


        self.update_active()

    def activate(self):
        super().activate()
        self.check_boolean.config(state='normal', bg='white')

    def deactivate(self):
        super().deactivate()
        self.check_boolean.config(state='disabled', bg='grey90')

    def get_result(self):
        return bool(self.value_var.get()) if self.is_activated.get() else None


if __name__ == "__main__":
    import gui_cluster_configuration
    bool1 = create_boolean_frame(
        "My Param 1", "This is a test parameter.", True, False)
    bool2 = create_boolean_frame(
        "My Param 2", "This is a test parameter.", True, True)
    bool3 = create_boolean_frame(
        "My Param 3", "This is a test parameter.", False, False)
    bool4 = create_boolean_frame(
        "My Param 4", "This is a test parameter.", False, True)
    bool_input = gui_cluster_configuration.get_configuration_parameters("Test", [bool1, bool2, bool3, bool4])
    print(bool_input.get_result())
