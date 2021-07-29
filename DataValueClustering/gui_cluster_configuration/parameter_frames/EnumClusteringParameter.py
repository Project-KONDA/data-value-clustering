from tkinter import IntVar, Radiobutton

import numpy as np

from gui_cluster_configuration.parameter_frames.ClusteringParameter import ClusteringParameter, \
    DEPENDENCY_ENUM_ACTIVATION
from gui_general.ToolTip import CreateToolTip


def create_enum_frame(name, explanation, dropdown_options, suggestions, deactivatable=False,
                      default_active=False, plot_function=None, previous_value=None, suggestion=None):
    return lambda parent: EnumClusteringParameter(parent, name, explanation, dropdown_options, suggestions, previous_value=previous_value,
                                                  deactivatable=deactivatable, default_active=default_active,
                                                  plot_function=plot_function, suggestion=suggestion)


class EnumClusteringParameter(ClusteringParameter):
    '''
    A widget for specifying an enumeration parameter of a clusering algorithm via radio buttons.
    '''

    def __init__(self, parent, name, explanation, options, suggestions, previous_value=None, deactivatable=False,
                 default_active=False, plot_function=None, suggestion=None):
        super().__init__(parent, name, explanation, deactivatable, default_active, plot_function)

        assert len(suggestions) > 0, name
        self.suggestions = suggestions

        self.validation_suggestions = None
        if suggestion is not None and self.name in suggestion:
            self.validation_suggestions = suggestion[self.name]

        self.options = options
        self.n = len(self.options)
        self.option_labels = self.options[:, 0]
        self.option_explanation = self.options[:, 1]
        self.option_labels_activated = self.option_labels

        try:
            self.default = np.where(self.option_labels == self.suggestions[0])[0][0]
            if previous_value is None:
                self.previous = None
            else:
                self.previous = np.where(self.option_labels == previous_value)[0][0]
        except IndexError:
            raise ValueError("Suggestions of parameter " + name + " are not correct: " + str(suggestions))

        self.radiobuttons = np.empty(self.n, Radiobutton)
        self.choice = IntVar()
        if self.previous is None:
            self.choice.set(self.default)
        else:
            self.choice.set(self.previous)


        for i, option in enumerate(self.options):
            is_suggested = option[0] in self.suggestions
            text = option[0]  # if not is_suggested else "♣ " + option[0]
            self.radiobuttons[i] = Radiobutton(self.frame, text=text,
                                               padx=20, variable=self.choice, command=self.update_enum, value=i,
                                               justify='left', anchor='w')

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
        self.update_active()
        if not self.option_labels[self.choice.get()] in new_options:
            self.choice.set(np.where(self.option_labels == new_options[0])[0][0])
            self.update_dependency(DEPENDENCY_ENUM_ACTIVATION)

    def update_enum(self):
        self.update_dependency(DEPENDENCY_ENUM_ACTIVATION)

    def update_dependency(self, type):
        super().update_dependency(type)
        if type == DEPENDENCY_ENUM_ACTIVATION:
            for i, dep in enumerate(self.dependencies[type]):
                [other_param, dependency_param] = dep
                activated = dependency_param[self.option_labels[self.choice.get()]]
                other_param.is_activated.set(activated)
                if other_param.deactivatable:
                    if activated:
                        other_param.check_active.config(state='normal')
                    else:
                        other_param.check_active.config(state='disabled')

                other_param.update_active()

    def update_active(self):
        super().update_active()
        self.update_dependency(DEPENDENCY_ENUM_ACTIVATION)

    def activate(self):
        super().activate()
        for i, button in enumerate(self.radiobuttons):
            # self.update_options(self.option_labels_activated)
            is_suggested = self.option_labels[i] in self.suggestions
            is_suggested_by_validation = False if self.validation_suggestions is None else self.option_labels[i] in self.validation_suggestions
            is_active_label = (self.option_labels[i] in self.option_labels_activated)
            if is_active_label:
                button.config(state='normal')
                if is_suggested_by_validation:
                    button.config(bg='SeaGreen1')
                elif is_suggested:
                    button.config(bg='#f0fff0')  # fg
                else:
                    button.config(bg='#fff0f0')  # fg
            else:
                button.config(bg='#ffffff')  # fg
                button.config(state='disabled')

    def deactivate(self):
        super().deactivate()
        for i, button in enumerate(self.radiobuttons):
            self.radiobuttons[i].config(state='disabled')
            self.radiobuttons[i].config(bg='grey90')  # fg

    def reset(self):
        self.choice.set(self.default)
        super().reset()

    def get_result(self):
        return self.option_labels[self.choice.get()] if self.is_activated.get() else None


if __name__ == "__main__":
    import gui_cluster_configuration
    options1 = np.array([["a", "AA"], ["b", "BB"], ["c", "CC"]])
    suggestions1 = ["a", "b"]
    options2 = np.array([["0", "00"], ["1", "11"], ["2", "22"]])
    suggestions2 = ["0"]

    enum1 = create_enum_frame("My Param", "This is a test parameter.", options1, suggestions1, deactivatable=False)
    enum2 = create_enum_frame("My Param", "This is a test parameter.", options2, suggestions2, deactivatable=True)
    enum3 = create_enum_frame("My Param", "This is a test parameter.", options1, suggestions1, deactivatable=True)
    enum4 = create_enum_frame("My Param", "This is a test parameter.", options2, suggestions2, deactivatable=False)
    enum_input = gui_cluster_configuration.get_configuration_parameters("Test", [enum1, enum2, enum3, enum4])
    print(enum_input.get_result())
