from tkinter import IntVar, Checkbutton

from gui_cluster_configuration.ClusteringParameterInput import ClusterConfigurationInput
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

    def change_checked(self):
        super().change_checked()
        if self.is_activated.get() == 1:
            self.check_boolean.config(state='normal', bg='white')
        else:
            self.check_boolean.config(state='disabled', bg='grey90')

    def get(self):
        return bool(self.value_var.get())


if __name__ == "__main__":
    bool1 = create_boolean_frame(
        "My Param 1", "This is a test parameter.", True, False)
    bool2 = create_boolean_frame(
        "My Param 2", "This is a test parameter.", True, True)
    bool3 = create_boolean_frame(
        "My Param 3", "This is a test parameter.", False, False)
    bool4 = create_boolean_frame(
        "My Param 4", "This is a test parameter.", False, True)
    bool_input = ClusterConfigurationInput("Test", [bool1, bool2, bool3, bool4])
    print(bool_input.get())
