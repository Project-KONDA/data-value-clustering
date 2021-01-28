import tkinter as Tk
import numpy as np


def get_configuration_parameters():
    input = ClusterConfigurationInput()
    return input.get()


class ClusterConfigurationInput:

    def __init__(self, parameter_frame_inits):
        self.root = Tk()
        self.parameters = parameter_frame_inits

        # TODO

        self.record_parameters()
        pass

    def record_parameters(self):

        # TODO

        self.root.mainloop()
        pass

    def get(self):
        parameter_values = list()
        # TODO
        return parameter_values
