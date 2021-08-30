from tkinter import Scale, IntVar, DoubleVar, Label

from gui_cluster_configuration.parameter_frames.ClusteringParameter import ClusteringParameter, \
    DEPENDENCY_VALUE_SLIDER_MAX


def create_slider_frame(name, explanation, mini, maxi, default, resolution=1, deactivatable=False,
                        default_active=False, plot_function=None, previous_value=None, suggestion=None):
    return lambda parent: SliderClusteringParameter(parent, name, explanation, mini, maxi, default, previous_value=previous_value,
                                                    resolution=resolution, deactivatable=deactivatable,
                                                    default_active=default_active, plot_function=plot_function, suggestion=suggestion)


class SliderClusteringParameter(ClusteringParameter):
    '''
    A widget for specifying a number parameter of a clusering algorithm via a slider.
    '''

    def __init__(self, parent, name, explanation, mini, maxi, default, previous_value=None, resolution=1,
                 deactivatable=False, default_active=False, plot_function=None, suggestion=None):
        super().__init__(parent, name, explanation, deactivatable, default_active, plot_function)

        assert type(mini) == type(maxi) == type(default) == type(resolution), str(name) + str(type(mini)) + str(type(maxi)) + str(type(default)) + str(type(resolution))
        assert type(resolution) is int or type(resolution) is float

        self.mini = mini
        self.maxi = maxi
        self.maxi_default = maxi
        self.default = default
        self.previous = previous_value
        self.resolution = resolution

        # slider:
        if type(self.resolution) is int:
            self.value_var = IntVar()
            # self.mini = round(self.mini)
        else:
            self.value_var = DoubleVar()
        if self.previous is None:
            self.start_value = self.default
        else:
            self.start_value = self.previous
        self.value_var.set(self.start_value)

        self.slider = Scale(self.frame, from_=mini, to=maxi, orient='horizontal', variable=self.value_var, command=self.update_slider, length=400,
                            bg='white', highlightthickness=0, resolution=self.resolution, tickinterval=maxi-mini)
        self.slider.grid(row=2, column=1, sticky='w')

        self.validation_suggestion = None
        self.label_suggested = None
        if suggestion is not None and self.name in suggestion:
            self.validation_suggestion = suggestion[self.name]
            if self.check_suggestion_in_bounds():
                self.label_suggested = Label(self.frame,
                                             text="Advice: " + self.validation_suggestion,
                                            anchor='nw', pady=10, fg='blue', bg='white')
                self.label_suggested.grid(row=2, column=2, sticky='w')

        # self.update_active()

    def check_suggestion_in_bounds(self):
        too_high = self.validation_suggestion == '⬇' and self.start_value == self.mini
        too_low = self.validation_suggestion == '⬆' and self.start_value == self.maxi
        return not(too_high or too_low)

    def update_active(self):
        super().update_active()
        self.update_dependency(DEPENDENCY_VALUE_SLIDER_MAX)

    def update_slider(self, event):
        self.update_dependency(DEPENDENCY_VALUE_SLIDER_MAX)

    def update_dependency(self, type):
        super().update_dependency(type)
        if type == DEPENDENCY_VALUE_SLIDER_MAX:
            for i, dep in enumerate(self.dependencies[type]):
                [other_param, dependency_param] = dep
                if not self.deactivatable or self.is_activated.get() == 1:
                    other_param.maxi = dependency_param(self.value_var.get())
                else:
                    other_param.maxi = other_param.maxi_default
                other_param.slider.config(to=other_param.maxi, tickinterval=other_param.maxi-other_param.mini)

    def activate(self):
        super().activate()
        self.update_dependency(DEPENDENCY_VALUE_SLIDER_MAX)
        self.slider.config(state='normal', fg='black', troughcolor='SystemScrollbar', bg='white')
        if self.label_suggested is not None:
            self.label_suggested.config(state='normal', fg="blue", bg='white')

    def deactivate(self):
        super().deactivate()
        self.slider.config(state='disabled', fg='grey', troughcolor='grey70', bg='grey90')
        if self.label_suggested is not None:
            self.label_suggested.config(state='disabled', bg='grey90')

    def reset(self):
        self.value_var.set(self.default)
        super().reset()

    def get_result(self):
        return self.value_var.get() if self.is_activated.get() else None


if __name__ == '__main__':
    import gui_cluster_configuration
    slide1 = create_slider_frame("My Param", "This is a test parameter.", 1, 10, 4, resolution=1, deactivatable=False)
    slide2 = create_slider_frame("My Param", "This is a test parameter.", 1, 30, 4, resolution=2, deactivatable=True)
    slide3 = create_slider_frame("My Param", "This is a test parameter.", 1.0, 10.0, 2.0, resolution=0.01,
                                 deactivatable=False)
    slide4 = create_slider_frame("My Param", "This is a test parameter.", 10.0, 14.0, 5.0, resolution=0.1,
                                 deactivatable=True)
    slide_input = gui_cluster_configuration.get_configuration_parameters("Test", [slide1, slide2, slide3, slide4])
    print(slide_input)
