from tkinter import IntVar, Radiobutton

import numpy as np

from gui_cluster_configuration.parameter_frames.ClusteringParameter import ClusteringParameter
from gui_general.ToolTip import CreateToolTip


def create_enum_frame(name, explanation, dropdown_options, suggestions, deactivatable=False, default_active=False):
    return lambda parent: EnumClusteringParameter(
        parent, name, explanation, dropdown_options, suggestions, deactivatable, default_active)


class EnumClusteringParameter(ClusteringParameter):

    def __init__(self, parent, name, explanation, options, suggestions, deactivatable=False, default_active=False):
        super().__init__(parent, name, explanation, deactivatable, default_active)

        assert len(suggestions) > 0
        self.suggestions = suggestions

        self.options = options
        self.n = len(self.options)
        self.option_labels = self.options[:, 0]
        self.option_explanation = self.options[:, 1]
        self.option_labels_activated = self.option_labels

        self.default = np.where(self.option_labels == self.suggestions[0])[0][0]
        self.radiobuttons = np.empty(self.n, Radiobutton)
        self.choice = IntVar()
        self.choice.set(self.default)

        for i, option in enumerate(self.options):
            is_suggested = option[0] in self.suggestions
            text = option[0]  # if not is_suggested else "♣ " + option[0]
            self.radiobuttons[i] = Radiobutton(self.frame, text=text,
                                               padx=20, variable=self.choice, command=self.update_enum, value=i, justify='left', anchor='w')

            CreateToolTip(self.radiobuttons[i], option[1])
            self.radiobuttons[i].grid(row=i + 10, column=1, sticky='nswe')

        # self.update_active()

        # self.value_var = StringVar()
        # self.value_var.set(self.default)
        # self.dropdown_menu = OptionMenu(self.frame, self.value_var, *self.options)
        # self.dropdown_menu.grid(row=2, column=1, sticky='nw')
        # CreateToolTip(self.dropdown_menu, textfunction=self.message)

    # def message(self):
    #     return self.option_explanation[self.get_current_index()]
    # def get_current_index(self):
    #     return list(self.options).index(self.value_var.get())

    def update_options(self, new_options):
        self.option_labels_activated = new_options
        assert len(new_options) > 0
        for i, o in enumerate(self.option_labels):
            if o in new_options:
                self.radiobuttons[i].config(state='normal')
            else:
                self.radiobuttons[i].config(state='disabled')
        if not self.option_labels[self.choice.get()] in new_options:
            self.choice.set(np.where(self.option_labels == new_options[0])[0][0])

    def update_enum(self):
        self.update_dependency('enum_value_activation')

    def update_dependency(self, type):
        super().update_dependency(type)
        if type == 'enum_value_activation':
            for i, dep in enumerate(self.dependencies[type]):
                [other_param, dependency_param] = dep
                activated = dependency_param[self.option_labels[self.choice.get()]]
                other_param.is_activated.set(activated)
                other_param.update_active()

    def activate(self):
        super().activate()
        for i, button in enumerate(self.radiobuttons):
            self.update_options(self.option_labels_activated)
            is_suggested = self.option_labels[i] in self.suggestions
            if is_suggested:
                self.radiobuttons[i].config(bg='#f0fff0')  # fg
            else:
                self.radiobuttons[i].config(bg='#fff0f0')  # fg

    def deactivate(self):
        super().deactivate()
        for i, button in enumerate(self.radiobuttons):
            self.radiobuttons[i].config(state='disabled')
            self.radiobuttons[i].config(bg='grey90')  # fg

    def get_result(self):
        return self.option_labels[self.choice.get()] if self.is_activated.get() else None


if __name__ == "__main__":
    import gui_cluster_configuration
    options1 = np.array([["a", "AA"], ["b", "BB"], ["c", "CC"]])
    suggestions1 = ["a", "b"]
    options2 = np.array([["0", "00"], ["1", "11"], ["2", "22"]])
    suggestions2 = ["0"]

    enum1 = create_enum_frame(
        "My Param", "This is a test parameter.", options1, suggestions1, False)
    enum2 = create_enum_frame(
        "My Param", "This is a test parameter.", options2, suggestions2, True)
    enum3 = create_enum_frame(
        "My Param", "This is a test parameter.", options1, suggestions1, True)
    enum4 = create_enum_frame(
        "My Param", "This is a test parameter.", options2, suggestions2, False)
    enum_input = gui_cluster_configuration.get_configuration_parameters("Test", [enum1, enum2, enum3, enum4])
    print(enum_input.get_result())
