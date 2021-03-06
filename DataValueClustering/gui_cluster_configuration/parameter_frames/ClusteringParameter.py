from abc import ABC, abstractmethod
from tkinter import Frame, IntVar, Checkbutton, StringVar, Label, font, Button

# from gui_cluster_configuration.parameter_frames import EnumClusteringParameter, SliderClusteringParameter

DEPENDENCY_VALUE_SLIDER_MAX = 'slider_value_slider_max'
DEPENDENCY_ENUM_ACTIVATION = 'enum_value_activation'
DEPENDENCY_ACTIVATION_ENUM = 'activation_enum'
DEPENDENCY_ACTIVATION_ACTIVATION = 'activation_activation'


class ClusteringParameter(ABC):
    '''
    A widget for specifying a parameter of a clusering algorithm.
    '''

    def __init__(self, parent, name, explanation, deactivatable=False, reverse_default_active=False, plot_function=None):
        self.frame = Frame(parent, highlightthickness=1, highlightbackground='grey', bg='white')
        self.frame.grid_columnconfigure(0, minsize=self.frame.winfo_screenwidth() // 25)
        self.frame.grid_columnconfigure(1, minsize=self.frame.winfo_screenwidth() // 3.5)

        self.root = parent
        self.name = name
        self.explanation = explanation
        self.deactivatable = deactivatable
        self.plot_function = plot_function

        self.dependencies = {'activation_activation': [], 'activation_enum': [], 'enum_value_activation': [], 'slider_value_slider_max': []}

        self.is_activated = IntVar()
        self.is_activated.set(int(deactivatable == reverse_default_active))

        # define frame content:

        # check box:
        if self.deactivatable:
            self.check_active = Checkbutton(self.frame, variable=self.is_activated, command=self.update_active,
                                            bg='white', anchor='w', padx=20)
            self.check_active.grid(row=0, column=0, sticky='w')

        # name label:
        self.label_text = StringVar()
        self.label_text.set(self.name)
        self.label = Label(self.frame, anchor='w', textvariable=self.label_text, bg='white', padx=5,
                           font=('TkDefaultFont', 14, 'bold'))
        self.label.grid(row=0, column=1, sticky='w')

        # explanation label:
        self.explanation_text = StringVar()
        self.explanation_text.set(self.explanation)
        self.label_explanation = Label(self.frame, anchor='nw', textvariable=self.explanation_text, bg='white', padx=5,
                                       wraplength=400, justify='left')
        self.label_explanation.grid(row=1, column=1, sticky='w')

        # reset button:
        self.reset_button = Button(self.frame, anchor='nw', text="Reset", command=self.reset)
        self.reset_button.grid(row=1, column=2, sticky='ne', padx=5, pady=5)

        # plot
        self.plot_button = None
        if plot_function:
            self.plot_button = Button(self.frame, anchor='nw', text="Show plot", command=self.plot_button_pressed)
            self.plot_button.grid(row=0, column=2, sticky='ne', padx=5, pady=5)
            self.reset_button.grid(row=1, column=2, sticky='nw', padx=5, pady=5)

    def reset(self):
        self.update_dependency(DEPENDENCY_ACTIVATION_ACTIVATION)
        self.update_dependency(DEPENDENCY_ACTIVATION_ENUM)
        self.update_dependency(DEPENDENCY_ENUM_ACTIVATION)
        self.update_dependency(DEPENDENCY_VALUE_SLIDER_MAX)


    def plot_button_pressed(self):
        self.plot_function(self.get_result())

    def add_dependency(self, other_param, type, dependency_param):
        assert type in [DEPENDENCY_ACTIVATION_ACTIVATION, DEPENDENCY_ACTIVATION_ENUM, DEPENDENCY_ENUM_ACTIVATION, DEPENDENCY_VALUE_SLIDER_MAX]
        # assert not(type=='activation_enum') or other_param is EnumClusteringParameter
        # assert not(type=='enum_value_activation') or self is EnumClusteringParameter
        # assert not (type == 'slider_value_slider_max') or (self is SliderClusteringParameter and other_param is SliderClusteringParameter)
        self.dependencies[type].append([other_param, dependency_param])

    def update_active(self):
        if self.is_activated.get() == 1:
            self.activate()
        else:
            self.deactivate()
        self.update_dependency(DEPENDENCY_ACTIVATION_ACTIVATION)
        self.update_dependency(DEPENDENCY_ACTIVATION_ENUM)

    def update_dependency(self, type):
        if type == DEPENDENCY_ACTIVATION_ACTIVATION:
            for i, dep in enumerate(self.dependencies[type]):
                [other_param, dependency_param] = dep
                activate = self.is_activated.get() == dependency_param
                if activate:
                    other_param.activate()
                else:
                    other_param.deactivate()
        elif type == DEPENDENCY_ACTIVATION_ENUM:
            for i, dep in enumerate(self.dependencies[type]):
                [other_param, dependency_param] = dep
                other_param.update_options(dependency_param[self.is_activated.get()])
        # elif type == 'enum_value_activation':
        #     pass
        # elif type == 'slider_value_slider_max':
        #     pass

    def deactivate(self):
        self.is_activated.set(int(False))
        self.label.config(state='disabled', bg='grey90')
        self.label_explanation.config(state='disabled', bg='grey90')
        if self.plot_button is not None:
            self.plot_button.config(state='disabled', bg='grey90')
        self.reset_button.config(state='disabled', bg='grey90')
        self.frame.config(bg='grey90')
        if self.deactivatable:
            self.check_active.config(bg='grey90')

    def activate(self):
        self.is_activated.set(int(True))
        self.label.config(state='normal', bg='white')
        self.label_explanation.config(state='normal', bg='white')
        if self.plot_button is not None:
            self.plot_button.config(state='normal', bg='white')
        self.reset_button.config(state='normal', bg='white')
        self.frame.config(bg='white')
        if self.deactivatable:
            self.check_active.config(bg='white')

    @abstractmethod
    def adopt_previous_activation(self):
        pass

    @abstractmethod
    def get_result(self):
        pass
