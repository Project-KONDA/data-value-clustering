from tkinter import Scale, IntVar, DoubleVar

from gui_cluster_configuration.parameter_frames.ClusteringParameter import ClusteringParameter, \
    DEPENDENCY_VALUE_SLIDER_MAX


def create_slider_frame(name, explanation, mini, maxi, default, resolution=1, deactivatable=False, default_active=False):
    return lambda parent: SliderClusteringParameter(
        parent, name, explanation, mini, maxi, default, resolution, deactivatable, default_active)


class SliderClusteringParameter(ClusteringParameter):

    def __init__(self, parent, name, explanation, mini, maxi, default, resolution=1, deactivatable=False, default_active =False):
        super().__init__(parent, name, explanation, deactivatable, default_active)

        assert type(mini) == type(maxi) == type(default) == type(resolution), str(name) + str(type(mini)) + str(type(maxi)) + str(type(default)) + str(type(resolution))
        assert type(resolution) is int or type(resolution) is float

        self.mini = mini
        self.maxi = maxi
        self.default = default
        self.resolution = resolution

        # slider:
        if type(self.resolution) is int:
            self.value_var = IntVar()
            self.value_var.set(default)
            # self.mini = round(self.mini)
        else:
            self.value_var = DoubleVar()
            self.value_var.set(default)
        self.slider = Scale(self.frame, from_=mini, to=maxi, orient='horizontal', variable=self.value_var, command=self.update_slider, length=400,
                            bg='white', highlightthickness=0, resolution=self.resolution, tickinterval=maxi-mini)
        self.slider.grid(row=2, column=1, sticky='w')

        # self.update_active()

    def update_slider(self, event):
        self.update_dependency(DEPENDENCY_VALUE_SLIDER_MAX)

    def update_dependency(self, type):
        super().update_dependency(type)
        if type == DEPENDENCY_VALUE_SLIDER_MAX:
            for i, dep in enumerate(self.dependencies[type]):
                [other_param, dependency_param] = dep
                other_param.maxi = dependency_param(self.value_var.get())
                other_param.slider.config(to=other_param.maxi, tickinterval=other_param.maxi-other_param.mini)

    def activate(self):
        super().activate()
        self.slider.config(state='normal', fg='black', troughcolor='SystemScrollbar', bg='white')

    def deactivate(self):
        super().deactivate()
        self.slider.config(state='disabled', fg='grey', troughcolor='grey70', bg='grey90')

    def get_result(self):
        return self.value_var.get() if self.is_activated.get() else None


if __name__ == '__main__':
    import gui_cluster_configuration
    slide1 = create_slider_frame(
        "My Param", "This is a test parameter.", 1, 10, 4, 1, False)
    slide2 = create_slider_frame(
        "My Param", "This is a test parameter.", 1, 30, 4, 2, True)
    slide3 = create_slider_frame(
        "My Param", "This is a test parameter.", 1.0, 10.0, 2.0, 0.01, False)
    slide4 = create_slider_frame(
        "My Param", "This is a test parameter.", 10.0, 14.0, 5.0, 0.1, True)
    slide_input = gui_cluster_configuration.get_configuration_parameters("Test", [slide1, slide2, slide3, slide4])
    print(slide_input)
