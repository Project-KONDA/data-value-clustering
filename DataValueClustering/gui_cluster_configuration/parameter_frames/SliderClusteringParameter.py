from tkinter import Scale, IntVar, DoubleVar

from gui_cluster_configuration.ClusteringParameterInput import ClusterConfigurationInput
from gui_cluster_configuration.parameter_frames.ClusteringParameter import ClusteringParameter


def create_slider_frame(name, explanation, mini, maxi, default, resolution=1, deactivatable=False):
    return lambda parent: SliderClusteringParameter(
        parent, name, explanation, mini, maxi, default, resolution, deactivatable)


class SliderClusteringParameter(ClusteringParameter):

    def __init__(self, parent, name, explanation, mini, maxi, default, resolution=1, deactivatable=False):
        super().__init__(parent, name, explanation, deactivatable)

        assert type(mini) == type(maxi) == type(default) == type(resolution)
        assert type(mini) is int or type(maxi) is float

        self.mini = mini
        self.maxi = maxi
        self.default = default
        self.resolution = resolution

        # slider:
        if type(self.resolution) is int:
            self.value_var = IntVar()
            self.value_var.set(default)
        else:
            self.value_var = DoubleVar()
            self.value_var.set(default)
        self.slider = Scale(self.frame, from_=mini, to=maxi, orient='horizontal', variable=self.value_var, length=400,
                            bg='white', highlightthickness=0, resolution=self.resolution)
        self.slider.grid(row=2, column=1, sticky='w')

    def change_checked(self):
        super().change_checked()
        if self.is_activated.get() == 1:
            self.slider.config(state='normal', fg='black', troughcolor='SystemScrollbar', bg='white')
        else:
            self.slider.config(state='disabled', fg='grey', troughcolor='grey70', bg='grey90')

    def get(self):
        return self.value_var.get()


if __name__ == '__main__':
    slide1 = create_slider_frame(
        "My Param", "This is a test parameter.", 1, 10, 4, 1, False)
    slide2 = create_slider_frame(
        "My Param", "This is a test parameter.", 1, 30, 4, 2, True)
    slide3 = create_slider_frame(
        "My Param", "This is a test parameter.", 1.0, 10.0, 2.0, 0.01, False)
    slide4 = create_slider_frame(
        "My Param", "This is a test parameter.", 10.0, 14.0, 5.0, 0.1, True)
    slide_input = ClusterConfigurationInput("Test", [slide1, slide2, slide3, slide4])
    print(slide_input.get())
