from abc import ABC
from tkinter import Frame


class ClusteringParameter(ABC):

    def __init__(self, parent):
        self.frame = Frame(parent)
        self.final_value = None
        pass

    def get(self):
        return self.final_value
