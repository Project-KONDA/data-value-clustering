import os
import subprocess
from tkinter import Tk, Button, Label, messagebox, Menu, Checkbutton, IntVar, LabelFrame, \
    OptionMenu, StringVar
from pathlib import Path
from tkinter.messagebox import WARNING, ERROR
import numpy as np
import sys

import xlsxwriter
from PIL import ImageTk, Image

from abstraction.abstractions import sequence_abstraction_function
from clustering.hierarchical_clustering import METHOD
from data_extraction.path_handling import data_name_from_path
from export.path import getJsonSavePath, getJsonLoadPath, getExcelSavePath
from gui_abstraction.AbstractionQuestionnaireResultInput import abstraction_configuration
from gui_abstraction.preconfigured_abstractions import ABSTRACTION_OPTION_CUSTOM, \
    ABSTRACTION_OPTION_CASE_LETTERS_DIGITS, ABSTRACTION_OPTION_LETTERS_DIGITS, ABSTRACTION_OPTION_CASE_LETTER_DIGIT_SEQ, \
    ABSTRACTION_OPTION_DEFAULT, ABSTRACTION_OPTION_WORDS_DIGIT_SEQ, ABSTRACTION_OPTION_WORDS_DECIMALS, \
    ABSTRACTION_OPTION_SENTENCES_DIGIT_SEQ, ABSTRACTION_OPTION_MAX, preconfigured_abstraction_answers, \
    get_predefined_option_from_answers
from gui_abstraction.abstraction_questions import abstraction_question_array
from gui_center.hub_configuration import HubConfiguration, load_hub_configuration
from gui_cluster_configuration.cluster_algorithms_gui import simple_cluster_hierarchical
from gui_cluster_selection.algorithm_selection import HIERARCHICAL, OPTICS
from gui_cluster_selection.select_algorithm import select_algorithm
from gui_data.select_data import select_data
from gui_distances.BlobInput import input_blobs
from gui_distances.CostMapInput import input_costmap
from gui_distances.costmapinput_helper import string_simplified_cost_map_split
from gui_distances.distance_choice import DistanceView
from gui_distances.slider_view import slider_view
from gui_general import CreateToolTip
from gui_general.LoadingWindow import load_and_compile
from gui_general.help_popup_gui import menu_help_hub
from gui_general.logger import append_log_clustering
from gui_general.scrollable_frame import create_scrollable_frame
from gui_general.window_size import set_window_size_simple
from gui_result.ResultView import result_view
from gui_result.validation_questionnaire import get_suggested_algorithms, get_suggested_data, \
    get_suggested_abstraction_modifications, get_suggested_distance_modifications, \
    get_suggested_parameter_modifications, ValidationAnswer

TITLE = "Data Value Clustering Hub"

SIMPLE_CLUSTERING_HINT_1 = "The simple clustering yielded "
SIMPLE_CLUSTERING_HINT_2 = " clusters. You can stop here \nor continue below to achieve a coarser clustering."
# SIMPLE_CLUSTERING_HINT_2 = " clusters.\nTo achieve a coarser clustering, go to 'Refined Clustering'."

CONFIG_DISSIMILARITIES = 'Configure Separation...'
CONFIG_DISSIMILARITIES_SLIDERS = 'Configure Separation... (Sliders)'
CONFIG_DISSIMILARITIES_BLOBS = 'Configure Separation... (Blobs)'
CONFIG_DISSIMILARITIES_MATRIX = 'Configure Separation... (Matrix)'

DISTANCE_OPTION_MATRIX = "Matrix (expert)"
DISTANCE_OPTION_BLOBS = "Blobs (advanced)"
DISTANCE_OPTION_SLIDERS = "Sliders (easy)"

CONFIG_CLUSTERING = 'Configure Grouping...'

STATUS = "Status: "
CLUSTERING_NOT_CALC = STATUS + 'Grouping configured but not executed'
CLUSTERING_DONE = STATUS + 'Grouping execution done'
DISTANCE_NOT_CALC = STATUS + 'Separation configured but not calculated'
DISTANCE_DONE = STATUS + 'Separation calculation done'
ABSTRACTION_CONFIGURED = STATUS + 'Aggregation configured'
ABSTRACTION_DONE = STATUS + 'Aggregation done'
DATA_DONE = STATUS + 'Data extraction done'
CLUSTERING_IN_PROGRESS = STATUS + "Grouping in progress ..."
CLUSTERING_CONFIG_IN_PROGRESS = STATUS + "Grouping configuration in progress ..."
DISTANCE_CALC_IN_PROGRESS = STATUS + "Separation in progress ..."
DISTANCE_CONFIGURATION_IN_PROGRESS = STATUS + "Separation configuration in progress ..."
ABSTRACTION_CONFIG_IN_PROGRESS = STATUS + "Aggregation configuration in progress ..."
ABSTRACTION_IN_PROGRESS = STATUS + "Aggregation in progress ..."
DATA_EXTRACTION_IN_PROGRESS = STATUS + "Data extraction in progress ..."
DATA_CONFIG_IN_PROGRESS = STATUS + "Data configuration in progress ..."
CLUSTERING_NOT_CONFIGURED = STATUS + "Grouping not configured"
DISTANCE_NOT_CONFIGURED = STATUS + "Separation not configured"
ABSTRACTION_NOT_CONFIGURED = STATUS + "Aggregation not configured"
DATA_NOT_CONFIGURED = STATUS + "Data not configured"

NONE = "None"

CLUSTERING_ADVICE = "Advice: reconfigure grouping"
CLUSTERING_ADVICE_SIMPLE = "Advice: consider simple mode"
CLUSTERING_ADVICE_EXPERT = "Advice: consider expert mode"

DISTANCE_ADVICE = "Advice: reconfigure separation"
ABSTRACTION_ADVICE = "Advice: reconfigure aggregation"
DATA_ADVICE = "Advice: reconfigure data"


class Hub:

    def __init__(self, loadpath=None, restricted=False, logging=False):
        os.chdir(str(Path(__file__).parent))

        load_and_compile()

        "initialisation"
        self.root = Tk()
        self.root.attributes('-alpha', 0.0)
        self.root.title(TITLE)
        icon = Image.open('..\\gui_general\\logo.ico')
        self.root.icon = ImageTk.PhotoImage(icon)
        self.root.iconphoto(False, self.root.icon)

        self.root.configure(background='white')

        self.restricted = restricted
        self.logging = logging

        self.configuration = HubConfiguration()
        self.configuration.set_abstraction_configuration(sequence_abstraction_function()[1])

        "labels"
        self.label_title = Label(self.root, text=TITLE, bg="white",
                                 font=('TkDefaultFont', 14, 'bold'), anchor="c", justify="center")
        self.label_title.grid(sticky='nswe', row=0, column=0, columnspan=4, pady=(10, 0))

        self.label_explanation = Label(self.root, text="Perform the following steps to obtain a clustering of your data.\nThe steps required next are highlighted in blue.", bg="white")
        self.label_explanation.grid(sticky='nswe', row=1, column=0, columnspan=4, pady=(0, 10))

        "menu"
        self.menu = Menu(self.root)
        self.menu.add_command(label="New", command=self.menu_new)
        self.menu.add_command(label="Save", command=self.menu_save)
        self.menu.add_command(label="Save As...", command=self.menu_saveas)
        self.menu.add_command(label="Load", command=self.menu_load)
        self.menu.add_command(label="Help", command=lambda: menu_help_hub(self.root, self.restricted))
        self.root.config(menu=self.menu)
        self.root.resizable(False, True)

        "scrollable canvas"
        self.around_canvas_frame, self.canvas, self.scrollable_frame = create_scrollable_frame(self.root)
        self.root.rowconfigure(2, weight=1)
        self.around_canvas_frame.grid(sticky='nswe', row=2, column=0, columnspan=2, padx=5, pady=5)
        self.around_canvas_frame.configure(borderwidth=0)

        "frames"
        self.data_frame = LabelFrame(self.scrollable_frame, text=' Data ', bg="white")
        self.simple_clustering_frame = LabelFrame(self.scrollable_frame, text=' Simple Clustering ', bg="white")
        self.refined_clustering_frame = LabelFrame(self.scrollable_frame, text=' Refined Clustering ', bg="white")

        self.data_frame.grid(sticky='nswe', row=2, column=0, columnspan=2, padx=5, pady=5)
        self.simple_clustering_frame.grid(sticky='nswe', row=3, column=0, columnspan=2, padx=5, pady=5)
        self.refined_clustering_frame.grid(sticky='nswe', row=6, column=0, columnspan=2, padx=5, pady=5)

        "preconfigured abstraction choice"
        self.label_abstraction_preconfigured = Label(self.simple_clustering_frame, text="Preconfigured Aggregation:", bg="white")
        self.label_abstraction_preconfigured.grid(sticky='w', row=0, column=1, padx=(10,0), pady=10)

        if restricted:
            self.abstraction_options = [ABSTRACTION_OPTION_DEFAULT]
        else:
            self.abstraction_options = [ABSTRACTION_OPTION_CUSTOM, ABSTRACTION_OPTION_CASE_LETTERS_DIGITS,
                                        ABSTRACTION_OPTION_LETTERS_DIGITS, ABSTRACTION_OPTION_CASE_LETTER_DIGIT_SEQ,
                                        ABSTRACTION_OPTION_DEFAULT, ABSTRACTION_OPTION_WORDS_DIGIT_SEQ,
                                        ABSTRACTION_OPTION_WORDS_DECIMALS, ABSTRACTION_OPTION_SENTENCES_DIGIT_SEQ,
                                        ABSTRACTION_OPTION_MAX]
        self.selected_abstraction_option = StringVar()
        self.selected_abstraction_option.set(ABSTRACTION_OPTION_DEFAULT)
        self.option_menu_abstraction_choice = OptionMenu(self.simple_clustering_frame, self.selected_abstraction_option,
                                                 *self.abstraction_options, command=self.selected_abstraction_option_changed)
        self.option_menu_abstraction_choice.grid(sticky='wes', row=0, column=2, padx=(0,10), pady=10)
        self.option_menu_abstraction_choice.configure(width=26)
        if restricted:
            self.option_menu_abstraction_choice.configure(state="disabled")

        "distance method choice"
        self.label_distance_choice = Label(self.refined_clustering_frame, text="Separation Configuration Method:", bg="white")
        self.label_distance_choice.grid(sticky='w', row=10, column=1, padx=(10,0), pady=10)

        if restricted:
            self.distance_options = [DISTANCE_OPTION_SLIDERS]
        else:
            self.distance_options = [DISTANCE_OPTION_SLIDERS, DISTANCE_OPTION_BLOBS]
        self.selected_distance_option = StringVar()
        self.selected_distance_option.set(DISTANCE_OPTION_SLIDERS)
        self.option_menu_distance_choice = OptionMenu(self.refined_clustering_frame, self.selected_distance_option,
                                                 *self.distance_options, command=self.selected_distance_option_changed)
        self.option_menu_distance_choice.grid(sticky='wes', row=10, column=2, padx=(0,10), pady=10)
        self.option_menu_distance_choice.configure(width=15)
        if restricted:
            self.option_menu_distance_choice.configure(state="disabled")

        "buttons"
        button_width_part = 37
        button_width_full = 50
        button_height = 2
        self.button_data = Button(self.data_frame, text='Configure Data...', command=self.configure_data,
                                  width=button_width_full, height=button_height, bg='paleturquoise1')
        self.button_abstraction = Button(self.simple_clustering_frame, text='Configure Aggregation...', command=self.configure_abstraction,
                                         width=button_width_full, height=button_height, bg='paleturquoise1')
        self.button_distance = Button(self.refined_clustering_frame, text=CONFIG_DISSIMILARITIES_SLIDERS, command=self.configure_distance,
                                      width=button_width_full, height=button_height, state="disabled")
        self.button_clustering = Button(self.refined_clustering_frame, text=CONFIG_CLUSTERING, command=self.configure_clustering,
                                        width=button_width_part, height=button_height, state="disabled")

        self.button_data.grid(sticky='nwe', row=5, column=1, columnspan=2, padx=10, pady=10)
        self.button_abstraction.grid(sticky='nwe', row=8, column=1, columnspan=2, padx=10, pady=10)
        self.button_distance.grid(sticky='nwe', row=11, column=1, columnspan=2, padx=10, pady=10)
        self.button_clustering.grid(sticky='nwe', row=15, column=1, columnspan=2, padx=10, pady=10)

        CreateToolTip(self.button_data, "Specify which data you intend to analyse.")
        CreateToolTip(self.button_abstraction, "Specify which features of the data values you are not interested in.")
        CreateToolTip(self.button_distance, "Specify how certain features influence the dissimilarity between data values.")
        if self.restricted:
            CreateToolTip(self.button_clustering,
                          "Specify the parameters of the clustering algorithm.")
        else:
            CreateToolTip(self.button_clustering, "Specify which clustering algorithm should be applied.")

        self.button_distance_play = Button(self.refined_clustering_frame, text='???', command=self.execute_distance,
                                           width=4, height=2, state="disabled")
        self.button_distance_play.grid(sticky='ne', row=12, column=2, padx=10, pady=10, rowspan=2)
        self.button_clustering_play = Button(self.refined_clustering_frame, text='???', command=self.execute_clustering,
                                             width=4, height=2, state="disabled")
        self.button_clustering_play.grid(sticky='ne', row=16, column=2, padx=10, pady=10, rowspan=2)

        self.button_show_result = Button(self.scrollable_frame, text='Open Refined Clustering...', command=self.show_result, state="disabled",
                                         font=('Sans', '10', 'bold'), width=45, height=2)
        self.button_show_result.grid(sticky='nswe', row=7, column=0, columnspan=2, padx=10, pady=10)

        # self.button_save_result = Button(self.root, text='Save', command=self.menu_save,
        #                                  font=('Sans', '10', 'bold')) #, height=2)
        # self.button_save_result.grid(sticky='nswe', row=17, column=1, padx=10, pady=10)
        # self.button_save_result.grid(sticky='ne', row=0, column=1, padx=10, pady=10)

        self.label_expert_configuration = Label(self.refined_clustering_frame, text="Grouping Configuration Method:", bg="white")
        self.label_expert_configuration.grid(sticky='w', row=14, column=1, padx=(10,0), pady=10)
        self.checked_expert_clustering = IntVar(value=1)
        self.checkbutton_expert_clustering = Checkbutton(self.refined_clustering_frame,
                                                         variable=self.checked_expert_clustering, bg="white", command=self.update_expert_clustering, text="Default", state="disabled")
        self.checkbutton_expert_clustering.grid(sticky='ws', row=14, column=2, pady=10)

        # self.checkbutton_clustering_label = Label(self.refined_clustering_frame, text="Default", bg="white", width=7)
        # self.checkbutton_clustering_label.grid(sticky='nwe', row=14, column=1, columnspan=1, padx=10, pady=10)

        CreateToolTip(self.button_distance_play, "Execute separation.")
        CreateToolTip(self.button_clustering_play, "Execute grouping.")
        CreateToolTip(self.button_show_result, "Show calculated clustering and evaluation questionnaire.")
        # CreateToolTip(self.button_save_result, "Save configuration.")

        # "progress bars"
        # self.path_progress = Progressbar(self.root, orient=HORIZONTAL, length=100, mode='determinate')
        # self.data_progress = Progressbar(self.root, orient=HORIZONTAL, length=100, mode='determinate')
        # self.abstraction_progress = Progressbar(self.root, orient=HORIZONTAL, length=100, mode='determinate')
        # self.distance_progress = Progressbar(self.root, orient=HORIZONTAL, length=100, mode='determinate')
        # self.clustering_progress = Progressbar(self.root, orient=HORIZONTAL, length=100, mode='determinate')
        #
        # self.path_progress.grid(sticky='nwe', row=4, column=1, columnspan=1, padx=20, pady=10)
        # self.data_progress.grid(sticky='nwe', row=6, column=1, columnspan=1, padx=20, pady=10)
        # self.abstraction_progress.grid(sticky='nwe', row=8, column=1, columnspan=1, padx=20, pady=10)
        # self.distance_progress.grid(sticky='nwe', row=10, column=1, columnspan=1, padx=20, pady=10)
        # self.clustering_progress.grid(sticky='nwe', row=12, column=1, columnspan=1, padx=20, pady=10)

        self.original_button_color = self.button_show_result.cget("background")

        "progress labels"
        self.label_data_progress = Label(self.data_frame, text=DATA_NOT_CONFIGURED, bg="white", fg="red")
        self.label_abstraction_progress = Label(self.simple_clustering_frame, text=ABSTRACTION_NOT_CONFIGURED, bg="white", fg="red")
        self.label_distance_progress = Label(self.refined_clustering_frame, text=DISTANCE_NOT_CONFIGURED, bg="white", fg="red")
        self.label_clustering_progress = Label(self.refined_clustering_frame, text=CLUSTERING_NOT_CALC, bg="white", fg="red")

        self.label_data_progress.grid(sticky='nw', row=6, column=1, columnspan=2, padx=20, pady=2)
        self.label_abstraction_progress.grid(sticky='nw', row=9, column=1, columnspan=2, padx=20, pady=2)
        self.label_distance_progress.grid(sticky='nw', row=12, column=1, columnspan=2, padx=20, pady=2)
        self.label_clustering_progress.grid(sticky='nw', row=16, column=1, columnspan=2, padx=20, pady=2)

        CreateToolTip(self.label_data_progress, "Status of the data")
        CreateToolTip(self.label_abstraction_progress, "Status of the aggregation")
        CreateToolTip(self.label_distance_progress, "Status of the separation")
        CreateToolTip(self.label_clustering_progress, "Status of the grouping")

        "advice labels"
        self.label_data_advice = Label(self.data_frame, text="", bg="white", fg="blue")
        self.label_abstraction_advice = Label(self.simple_clustering_frame, text="", bg="white", fg="blue")
        self.label_distance_advice = Label(self.refined_clustering_frame, text="", bg="white", fg="blue")
        self.label_clustering_advice = Label(self.refined_clustering_frame, text="", bg="white", fg="blue")

        self.label_data_advice.grid(sticky='nw', row=7, column=1, columnspan=1, padx=20, pady=2)
        self.label_abstraction_advice.grid(sticky='nw', row=10, column=1, columnspan=1, padx=20, pady=2)
        self.label_distance_advice.grid(sticky='nw', row=13, column=1, columnspan=1, padx=20, pady=2)
        self.label_clustering_advice.grid(sticky='nw', row=17, column=1, columnspan=1, padx=20, pady=2)

        # CreateToolTip(self.label_data_advice, "Status of the data")
        # CreateToolTip(self.label_abstraction_advice, "Status of the abstraction")
        # CreateToolTip(self.label_distance_advice, "Status of the distances")
        # CreateToolTip(self.label_clustering_advice, "Status of the clustering")

        "preview frames"
        frame_width = button_width_full

        self.preview_data_outer, self.preview_data_canvas, self.preview_data = \
            create_scrollable_frame(self.data_frame, dynamic_height=False, surrounding_frame=self.scrollable_frame, surrounding_canvas=self.canvas)
        self.preview_abstraction_outer, self.preview_abstraction_canvas, self.preview_abstraction = \
            create_scrollable_frame(self.simple_clustering_frame, dynamic_height=False, surrounding_frame=self.scrollable_frame, surrounding_canvas=self.canvas)
        self.preview_distance_outer, self.preview_distance_canvas, self.preview_distance = \
            create_scrollable_frame(self.refined_clustering_frame, dynamic_height=False, surrounding_frame=self.scrollable_frame, surrounding_canvas=self.canvas)
        self.preview_clustering_outer, self.preview_clustering_canvas, self.preview_clustering = \
            create_scrollable_frame(self.refined_clustering_frame, dynamic_height=False, surrounding_frame=self.scrollable_frame, surrounding_canvas=self.canvas)

        self.preview_data_canvas.config(height=0, bg="grey90")
        self.preview_abstraction_canvas.config(height=0, bg="grey90")
        self.preview_distance_canvas.config(height=0, bg="grey90")
        self.preview_clustering_canvas.config(height=0, bg="grey90")

        self.preview_data.config(bg="grey90")
        self.preview_abstraction.config(bg="grey90")
        self.preview_distance.config(bg="grey90")
        self.preview_clustering.config(bg="grey90")

        self.preview_data_outer.config(bg="grey90")
        self.preview_abstraction_outer.config(bg="grey90")
        self.preview_distance_outer.config(bg="grey90")
        self.preview_clustering_outer.config(bg="grey90")

        self.preview_data_outer.grid(sticky='nswe', row=5, column=3, rowspan=3, columnspan=2, padx=10, pady=10)
        self.preview_abstraction_outer.grid(sticky='nswe', row=0, column=3, rowspan=11, columnspan=2, padx=10, pady=10)
        self.preview_distance_outer.grid(sticky='nswe', row=10, column=3, rowspan=4, columnspan=2, padx=10, pady=10)
        self.preview_clustering_outer.grid(sticky='nswe', row=14, column=3, rowspan=4, columnspan=2, padx=10, pady=10)

        "labels in preview frames"
        label_width = 40
        self.label_data_config_heading = Label(self.preview_data, text="Current Data Configuration:", bg="grey90", anchor="w", justify="left", width=label_width)
        self.label_abstraction_config_heading = Label(self.preview_abstraction, text="Current Aggregation Configuration:", bg="grey90", anchor="w", justify="left", width=label_width)
        self.label_distance_config_heading = Label(self.preview_distance, text="Current Separation Configuration:", bg="grey90", anchor="w", justify="left", width=label_width)
        self.label_clustering_config_heading = Label(self.preview_clustering, text="Current Grouping Configuration:", bg="grey90", anchor="w", justify="left", width=label_width)

        self.label_data_config_heading.grid(sticky='nw', row=0, column=0, rowspan=1)
        self.label_abstraction_config_heading.grid(sticky='nw', row=0, column=0)
        self.label_distance_config_heading.grid(sticky='nw', row=0, column=0)
        self.label_clustering_config_heading.grid(sticky='nw', row=0, column=0)

        # TODO: add scrollbars or use Text instead of Label
        self.label_data_config = Label(self.preview_data, text=NONE, bg="grey90", anchor="nw", justify="left", padx=10, width=label_width)
        self.label_abstraction_config = Label(self.preview_abstraction, text=NONE, bg="grey90", anchor="nw", justify="left", padx=10, width=label_width)
        self.label_distance_config = Label(self.preview_distance, text=NONE, bg="grey90", anchor="nw", justify="left", padx=10, width=label_width)
        self.label_distance_config2 = Label(self.preview_distance, text=NONE, bg="grey90", anchor="nw", justify="left", padx=10, width=0)
        self.label_clustering_config = Label(self.preview_clustering, text=NONE, bg="grey90", anchor="nw", justify="left", padx=10, width=label_width)

        self.label_data_config.grid(sticky='nwse', row=1, column=0, rowspan=1, columnspan=2)
        self.label_abstraction_config.grid(sticky='nwse', row=1, column=0, rowspan=1, columnspan=2)
        self.label_distance_config.grid(sticky='nwse', row=1, column=0, rowspan=1)
        self.label_distance_config2.grid(sticky='nse', row=1, column=0, rowspan=1)
        self.label_clustering_config.grid(sticky='nwse', row=1, column=0, rowspan=1, columnspan=2)

        CreateToolTip(self.label_data_config, "Name of the selected data set.")
        CreateToolTip(self.label_abstraction_config, "Abstracted details marked by 'True'.")
        CreateToolTip(self.label_distance_config, "The first column shows the character groups. Besides corresponding dissimilarity weights are shown.")
        CreateToolTip(self.label_clustering_config, "Selected clustering algorithm and specified parameters.")

        "Simple Clustering Hint"
        # self.label_abstraction_hint = Label(self.simple_clustering_frame, text="\n", bg="white", justify="left")
        # self.label_abstraction_hint.grid(sticky='nw', row=11, column=1, columnspan=1, padx=20, pady=10)
        # self.button_abstraction_excel = Button(self.simple_clustering_frame, text="Open Simple Clustering", width=20, height=2, command=self.open_simple_clustering)
        # self.button_abstraction_excel.grid(sticky='nw', row=11, column=3, columnspan=1, padx=10, pady=10)
        self.label_abstraction_hint = Label(self.scrollable_frame, text="\n", width=button_width_full, bg="white", justify="left")
        self.label_abstraction_hint.grid(sticky='w', row=4, column=0, padx=10, pady=10)
        self.button_abstraction_excel = Button(self.scrollable_frame, text="Open Simple Clustering", height=2, command=self.open_simple_clustering)
        self.button_abstraction_excel.grid(sticky='w', row=4, column=1, padx=10, pady=10)
        CreateToolTip(self.button_abstraction_excel, "Open Excel file showing simple clustering resulting from the aggregation.")
        self.hide_simple_clustering_hint()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.update()

        set_window_size_simple(self.root)

        self.root.attributes('-alpha', 1.0)

        self.root.after(1, lambda: self.root.focus_force())
        if loadpath is not None:
            self.load(loadpath)
            self.update()
        self.root.mainloop()

    def selected_abstraction_option_changed(self, *args):
        new_selection = self.selected_abstraction_option.get()
        if new_selection != ABSTRACTION_OPTION_CUSTOM:
            answers = preconfigured_abstraction_answers[np.where(preconfigured_abstraction_answers[:,0] == new_selection)[0][0], 1]
            if answers != self.configuration.get_abstraction_configuration():
                self.apply_abstraction(answers)
        else:
            self.apply_abstraction(None)

    def set_selected_distance_option(self, value):
        self.selected_distance_option.set(value)
        self.selected_distance_option_changed()

    def selected_distance_option_changed(self, *args):
        self.update_selected_distance_option()
        self.update_distance_button()

    def update_distance_button(self):
        current_selection = self.selected_distance_option.get()
        if current_selection == DISTANCE_OPTION_SLIDERS:
            self.button_distance.configure(text=CONFIG_DISSIMILARITIES_SLIDERS)
        elif current_selection == DISTANCE_OPTION_BLOBS:
            self.button_distance.configure(text=CONFIG_DISSIMILARITIES_BLOBS)
        else:
            self.button_distance.configure(text=CONFIG_DISSIMILARITIES_MATRIX)

    def update_selected_distance_option(self):
        new_selection = self.selected_distance_option.get()
        previous_method = self.configuration.get_distance_config_method()
        if new_selection == DISTANCE_OPTION_SLIDERS:
            if previous_method == DistanceView.MATRIX:
                if not messagebox.askokcancel("Potential Information Loss",
                                              "You previously configured the separation "
                                              "via Expert Mode, i.e. the matrix. This configuration will be "
                                              "lost if you configure the weights via the Sliders view.",
                                              icon=WARNING):
                    self.set_selected_distance_option(DISTANCE_OPTION_MATRIX)
            elif previous_method == DistanceView.BLOB:
                if not messagebox.askokcancel("Potential Information Loss",
                                              "You previously configured the separation "
                                              "via Blobs. This configuration will be "
                                              "lost if you configure the weights via the Sliders view.",
                                              icon=WARNING):
                    self.set_selected_distance_option(DISTANCE_OPTION_BLOBS)
        elif new_selection == DISTANCE_OPTION_BLOBS:
            if previous_method == DistanceView.MATRIX:
                if not messagebox.askokcancel("Potential Information Loss",
                                              "You previously configured the separation "
                                              "via Expert Mode, i.e. the matrix. This configuration will be "
                                              "lost if you configure the weights via the Blobs view.",
                                              icon=WARNING):
                    self.set_selected_distance_option(DISTANCE_OPTION_MATRIX)
            elif previous_method == DistanceView.SLIDER:
                if not messagebox.askokcancel("Potential Information Loss",
                                              "You previously configured the separation "
                                              "via Sliders. This configuration will be "
                                              "lost if you configure the weights via the Blobs view.",
                                              icon=WARNING):
                    self.set_selected_distance_option(DISTANCE_OPTION_SLIDERS)

    def set_saved(self, saved):
        self.configuration.json_saved = saved
        if not saved and self.root.title() != TITLE and not self.root.title().endswith("*"):
            self.root.title(self.root.title() + "*")
        if saved:
            self.root.title(self.configuration.json_save_path)

    def on_closing(self):
        if self.configuration.json_saved or \
                messagebox.askokcancel("Quit",
                                       "Closing the window without prior saving the configuration will delete the configuration."
                                       "\nDo you want to quit?",
                                       icon=WARNING):
            self.root.destroy()

    def open_simple_clustering(self):
        if self.configuration.excel_simple_save_path is None:
            self.configuration.excel_simple_save_path = getExcelSavePath()
            if self.logging:
                append_log_clustering(self.configuration, False, self.restricted)

        if self.configuration.excel_simple_save_path is not None:
            try:
                if not self.configuration.excel_simple_saved:
                    self.configuration.save_simple_as_excel()
                    self.configuration.excel_simple_saved = True
                os.startfile('"' + self.configuration.excel_simple_save_path + '"')
            except (PermissionError, xlsxwriter.exceptions.FileCreateError) as e:
                messagebox.showerror("Error",
                                       "Cannot save file at selected path since the file exists already and is currently open."
                                       " Please close the file first or select a different path.",
                                       icon=ERROR)
                self.configuration.excel_simple_save_path = None
            except subprocess.CalledProcessError as e:
                messagebox.showerror("Error", "File is already open.", icon=ERROR)
            # os.system('"' + self.configuration.excel_simple_save_path + '"')

    def data_path_from_name(self, data_name):
        if data_name is None:
            return None
        relative_path = "data\\" + data_name + ".txt"
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = Path(__file__).parent.parent
        return os.path.join(base_path, relative_path)

    def configure_data(self):
        self.label_data_progress.configure(text=DATA_CONFIG_IN_PROGRESS, fg='magenta2')
        previous_data_path = self.configuration.get_data_configuration()[0]
        previous_data_name = data_name_from_path(previous_data_path)

        data_name = select_data(self.root, previous_data_name, get_suggested_data(self.get_validation_answers()),
                                self.restricted)

        if data_name is None or previous_data_name == data_name:
            self.update()
            self.root.update()
            return

        self.set_saved(False)
        self.reset_validation_answers()
        self.configuration.set_data_configuration(self.data_path_from_name(data_name))

        # self.configuration.set_clustering_selection(None)
        # self.configuration.set_clustering_configuration(None)

        self.update()
        self.root.update()

        self.label_data_progress.configure(text=DATA_EXTRACTION_IN_PROGRESS, fg='RoyalBlue1')
        self.root.update()

        self.configuration.execute_data()

        self.update()

        if self.configuration.abstraction_configuration_valid():
            self.label_abstraction_progress.configure(text=ABSTRACTION_IN_PROGRESS, fg='RoyalBlue1')
            self.root.update()
            self.configuration.execute_abstraction()
            self.configuration.excel_simple_saved = False
            self.configuration.excel_simple_save_path = None
            self.update()

        # self.configuration.save_as_json()

    def configure_abstraction(self):
        self.label_abstraction_progress.configure(text=ABSTRACTION_CONFIG_IN_PROGRESS, fg='magenta2')
        # 1. get data from config
        previous_abstraction_answers = self.configuration.get_abstraction_configuration()
        # 2. put data into abstraction gui
        # 3. read from abstraction gui
        method, abstraction_answers = abstraction_configuration(self.root, self.configuration.data, previous_abstraction_answers, get_suggested_abstraction_modifications(self.get_validation_answers(), self.configuration), self.restricted)
        if abstraction_answers is None or previous_abstraction_answers == abstraction_answers:
            self.update()
            self.root.update()
            return

        self.apply_abstraction(abstraction_answers)
        # self.configuration.save_as_json()

    def apply_abstraction(self, abstraction_answers):
        self.set_saved(False)
        self.configuration.reset_abstraction()
        self.configuration.set_distance_configuration(None)
        # self.configuration.set_clustering_selection(None)
        # self.configuration.set_clustering_configuration(None)
        self.reset_validation_answers()
        self.configuration.set_abstraction_configuration(abstraction_answers)

        self.update()
        self.root.update()
        self.label_abstraction_progress.configure(text=ABSTRACTION_IN_PROGRESS, fg='RoyalBlue1')
        self.root.update()
        if self.configuration.data_configuration_valid() and self.configuration.abstraction_configuration_valid():
            self.configuration.execute_abstraction()

        self.configuration.excel_simple_saved = False
        self.configuration.excel_simple_save_path = None

        self.update()

    def show_simple_clustering_hint(self, i):
        self.label_abstraction_hint.configure(fg="black", text=SIMPLE_CLUSTERING_HINT_1 + str(i) + SIMPLE_CLUSTERING_HINT_2)
        self.button_abstraction_excel.configure(state="normal", bg='pale green')
        # if i and 0 < i:
        #     self.label_abstraction_hint.grid()
        #     self.button_abstraction_excel.grid()
        #     self.label_abstraction_hint.configure(fg="black", text=SIMPLE_CLUSTERING_HINT_1 + str(i) + SIMPLE_CLUSTERING_HINT_2)

    def hide_simple_clustering_hint(self):
        # self.label_abstraction_hint.grid_remove()
        # self.button_abstraction_excel.grid_remove()
        self.label_abstraction_hint.configure(fg="grey", text="You need to configure the data and the aggregation\nbefore you can access the simple clustering.")
        self.button_abstraction_excel.configure(state="disabled")
        self.button_abstraction_excel.configure(bg=self.original_button_color)

    def configure_distance(self):
        self.label_distance_progress.configure(text=DISTANCE_CONFIGURATION_IN_PROGRESS, fg='magenta2')
        previous_cost_map, blob_configuration = self.configuration.get_distance_configuration()

        self.set_saved(False)

        if self.selected_distance_option.get() == DISTANCE_OPTION_SLIDERS:
            config_method, cost_map = slider_view(self.root, abstraction=blob_configuration[1:, 0:4],
                                   texts=list(blob_configuration[1:,1]), costmap=previous_cost_map, suggestion=get_suggested_distance_modifications(self.get_validation_answers(), self.configuration), configuration=self.configuration, values_abstracted=self.configuration.values_abstracted, restricted=self.restricted)
            blob_configuration = None
        elif self.selected_distance_option.get() == DISTANCE_OPTION_BLOBS:
            config_method, cost_map, blob_configuration = input_blobs(self.root, blob_configuration, get_suggested_distance_modifications(self.get_validation_answers(), self.configuration), restricted=self.restricted)
        else:
            cost_map = input_costmap(self.root, regexes=list(blob_configuration[:, 1]), costmap=previous_cost_map,
                                         abstraction=blob_configuration[1:, 0:4], suggestion=get_suggested_distance_modifications(self.get_validation_answers(), self.configuration), configuration=self.configuration)
            blob_configuration = None
            config_method = DistanceView.MATRIX

        if cost_map is None or previous_cost_map == cost_map:
            self.configuration.blob_configuration = blob_configuration
            self.update()
            self.root.update()
            return

        self.configuration.set_distance_configuration(cost_map, blob_configuration)

        if config_method is not None:
            self.configuration.set_distance_config_method(config_method)

        self.reset_validation_answers()

        self.update()
        self.root.update()

    def update_option_menu_value_list(self):
        menu = self.option_menu_distance_choice["menu"]
        if menu:
            menu.delete(0, "end")
        for string in self.distance_options:
            menu.add_command(label=string,
                             command=lambda value=string: self.option_menu_command(value))

    def option_menu_command(self, value):
        self.set_selected_distance_option(value)

    def update_option_menu(self):
        method = self.configuration.get_distance_config_method()
        if method == DistanceView.MATRIX:
            # expert mode was used, thus add matrix option to menu
            self.distance_options = [DISTANCE_OPTION_SLIDERS, DISTANCE_OPTION_BLOBS, DISTANCE_OPTION_MATRIX]
            self.update_option_menu_value_list()
            self.set_selected_distance_option(DISTANCE_OPTION_MATRIX)
        else:
            # remove matrix option from menu
            self.distance_options = [DISTANCE_OPTION_SLIDERS, DISTANCE_OPTION_BLOBS]
            self.update_option_menu_value_list()
            if method is None or method == DistanceView.SLIDER:
                self.set_selected_distance_option(DISTANCE_OPTION_SLIDERS)
            else:
                self.set_selected_distance_option(DISTANCE_OPTION_BLOBS)

    def execute_distance(self):
        if not messagebox.askokcancel("Starting Distance Calculation", "Note that the separation may take up to multiple hours and cannot be interrupted. "
                                                                       "You will not be able to make any inputs to this application during the calculation. "
                                                                       "In order for the calculation to complete successfully, you must not close the application. "
                                                                       "Once the calculation is completed, the application icon in the taskbar will be highlighted and the status label will change."
                                                                       "\nDo you really want to start the separation now?",
                                       icon=WARNING):
            return

        self.label_distance_progress.configure(text=DISTANCE_CALC_IN_PROGRESS, fg='RoyalBlue1')
        self.root.update()
        try:
            self.configuration.execute_distance()
        except MemoryError:
            messagebox.showerror("Too many values",
                                   "The separation failed due to too many values. Please reconfigure the aggregation such that less values remain. "
                                   "Typically, checking the last question, i.e. allowing the removal of duplicates, is sufficient.",
                                   icon=ERROR)

        self.set_saved(False)

        self.update()
        # self.configuration.save_as_json()

        self.root.focus_force()

    def configure_clustering(self):
        self.label_clustering_progress.configure(text=CLUSTERING_CONFIG_IN_PROGRESS, fg='magenta2')
        prev_clustering_algorithm = self.configuration.get_clustering_selection()
        prev_parameters = self.configuration.get_clustering_configuration()
        suggested_algorithms = get_suggested_algorithms(self.get_validation_answers())

        # if self.checked_expert_clustering.get() == 1:#
        if True:
            cluster_config_f, clustering_algorithm = select_algorithm(self.root, prev_clustering_algorithm, suggested_algorithms)

            if clustering_algorithm is None:
                self.update()
                self.root.update()
                return

            if prev_clustering_algorithm != clustering_algorithm:
                prev_parameters = None
                suggested_parameter_modifications = None
            else:
                suggested_parameter_modifications = get_suggested_parameter_modifications(self.get_validation_answers(), self.configuration, expert=True)
            parameters = cluster_config_f(self.root, self.configuration.distance_matrix_map, self.configuration.values_abstracted, self.configuration.abstraction_dict, prev_parameters, suggestion=suggested_parameter_modifications, restricted=self.restricted)
        # else:
        #     clustering_algorithm = "Hierarchical"
        #
        #     if prev_clustering_algorithm != clustering_algorithm:
        #         prev_parameters = None
        #         suggested_parameter_modifications = None
        #     else:
        #         suggested_parameter_modifications = get_suggested_parameter_modifications(self.get_validation_answers(), self.configuration, expert=False)
        #     parameters = simple_cluster_hierarchical(self.root, self.configuration.distance_matrix_map, self.configuration.values_abstracted, self.configuration.abstraction_dict, prev_parameters, suggestion=suggested_parameter_modifications, restricted=self.restricted)

        if parameters is None or (prev_clustering_algorithm == clustering_algorithm and prev_parameters == parameters):
            self.update()
            self.root.update()
            return

        self.set_saved(False)
        self.configuration.excel_saved = False
        self.reset_validation_answers()
        self.configuration.set_clustering_selection(clustering_algorithm)
        self.configuration.set_clustering_configuration(parameters)

        self.update()
        self.root.update()

    def update_expert_clustering(self):
        self.configuration.clustering_default_mode = bool(self.checked_expert_clustering.get())
        self.button_clustering.configure(state="disabled")
        if self.configuration.clustering_default_mode:
            self.clustering_algorithm = "Hierarchical"
            self.configuration.set_clustering_selection(self.clustering_algorithm)
            self.clustering_parameters = {'method': 'single', 'n_clusters': None,
                                          'distance_threshold': 10, 'criterion': 'distance', 'depth': None}
            self.configuration.set_clustering_configuration(self.clustering_parameters)
        elif self.configuration.clustering_configuration_possible():
            self.button_clustering.configure(state="normal")
        self.update_advice()

    def get_validation_answers(self):
        return self.configuration.get_validation_answer_1(), self.configuration.get_validation_answer_2(), self.configuration.get_validation_answer_3(), self.configuration.get_validation_answer_4(),

    def execute_clustering(self):
        self.label_clustering_progress.configure(text=CLUSTERING_IN_PROGRESS, fg='RoyalBlue1')
        self.root.update()

        self.configuration.execute_clustering()

        self.set_saved(False)
        self.configuration.excel_saved = False
        self.configuration.excel_save_path = None

        # self.label_clustering_progress.configure(text="Saving in progress ...", fg='RoyalBlue1')
        # self.root.update()
        #
        # self.configuration.save_as_json()
        # self.configuration.save_as_excel()

        self.update()

        self.root.focus_force()

    def show_result(self):
        # validation_result = result_view(self.root, self.configuration.excel_save_path, self.configuration.num_data, self.configuration.num_abstracted_data, self.configuration.abstraction_rate, self.configuration.no_clusters, self.configuration.no_noise,
        #             self.configuration.timedelta_abstraction, self.configuration.timedelta_distance, self.configuration.timedelta_cluster, self.configuration.timedelta_total,
        #             self.configuration.values_abstracted, self.configuration.distance_matrix_map, self.configuration.clusters_abstracted)
        result_view(self.root, self.configuration, restricted=self.restricted, logging=self.logging)
        self.update()

    def update_advice(self):
        answers = self.get_validation_answers()
        self.label_data_advice.config(text="")
        self.label_abstraction_advice.config(text="")
        self.label_distance_advice.config(text="")
        self.label_clustering_advice.config(text="")
        if answers[0] is not None and answers[0] != ValidationAnswer.HAPPY:
            if not self.restricted:
                self.label_abstraction_advice.config(text=ABSTRACTION_ADVICE)
            self.label_distance_advice.config(text=DISTANCE_ADVICE)
            if self.configuration.get_clustering_selection() != HIERARCHICAL and self.configuration.get_clustering_selection() != OPTICS \
                    or not self.restricted and self.configuration.get_clustering_selection() == HIERARCHICAL and self.configuration.get_clustering_configuration()[METHOD] != 'average' and self.configuration.get_clustering_configuration()[METHOD] != 'weighted':
                self.label_clustering_advice.config(text=CLUSTERING_ADVICE)
        if answers[1] is not None and answers[1] == ValidationAnswer.MORE:
            if not self.restricted:
                if self.configuration.clustering_default_mode:
                    self.label_clustering_advice.config(text=CLUSTERING_ADVICE)
                else:
                    self.label_clustering_advice.config(text=CLUSTERING_ADVICE_EXPERT)
            self.label_distance_advice.config(text=DISTANCE_ADVICE)
        if answers[1] is not None and answers[1] == ValidationAnswer.LESS:
            if not self.restricted:
                if self.configuration.clustering_default_mode:
                    self.label_clustering_advice.config(text=CLUSTERING_ADVICE)
            self.label_distance_advice.config(text=DISTANCE_ADVICE)
        if answers[2] is not None and answers[2] != ValidationAnswer.HAPPY:
            if not self.restricted:
                self.label_abstraction_advice.config(text=ABSTRACTION_ADVICE)
                self.label_clustering_advice.config(text=CLUSTERING_ADVICE)
            self.label_distance_advice.config(text=DISTANCE_ADVICE)
        if answers[3] is not None and answers[3][0] is not None and answers[3][0] != ValidationAnswer.HAPPY:
            self.label_data_advice.config(text=DATA_ADVICE)

    # def abstraction_callback(self, percentage):
    #     self.abstraction_progress['value'] = percentage
    #     self.root.update()

    # def distance_callback(self, percentage):
    #     self.distance_progress['value'] = percentage
    #     self.root.update()

    def menu_load(self):
        load_path = getJsonLoadPath(self.configuration.json_save_path)
        if not load_path:
            self.update()
        else:
            self.load(load_path)

    def load(self, load_path):
        print("loading from " + load_path + " ...")
        self.configuration = load_hub_configuration(load_path)
        self.set_saved(True)
        if (self.configuration.clustering_default_mode or self.configuration.distance_config_method == DistanceView.MATRIX or self.configuration.distance_config_method == DistanceView.BLOB or self.configuration.get_abstraction_configuration() != sequence_abstraction_function()[1]) and self.restricted:
            if messagebox.showinfo("Loading failed",
                                   "You tried to load a configuration which uses expert mode while running the application in restricted mode. "
                                   "This is not possible. Please load another configuration or run the application in expert mode.",
                                   icon=WARNING):
                self.configuration = HubConfiguration()
                self.set_saved(False)
                self.root.title(TITLE)

        self.update()

    def menu_new(self):
        if self.configuration.json_saved or \
            messagebox.askokcancel("New Configuration",
                                   "Creating a new configuration without prior saving the current configuration will delete it."
                                   "\nDo you want to proceed?",
                                   icon=WARNING):
            self.configuration = HubConfiguration()
            self.configuration.set_abstraction_configuration(sequence_abstraction_function()[1])
            self.update()
            self.root.title(TITLE)

    def menu_save(self):
        if not self.configuration.json_saved:
            if messagebox.showinfo("Saving Configuration",
                                   "Note that saving the configuration may take up to a minute and cannot be interrupted.",
                                   icon=WARNING):
                self.save()

    def menu_saveas(self):
        if messagebox.showinfo("Saving Configuration",
                               "Note that saving the configuration may take up to a minute and cannot be interrupted.",
                               icon=WARNING):
            self.saveas()

    def save(self):
        if self.configuration.json_save_path is not None:
            self.root.title("Saving to " + self.configuration.json_save_path + " in progress ...")
            self.configuration.save_as_json()
            self.set_saved(True)
        else:
            self.saveas()
        self.update()
        self.root.focus_force()

    def saveas(self):
        self.configuration.json_save_path = getJsonSavePath()
        if self.configuration.json_save_path is not None:
            self.save()

    def reset_validation_answers(self):
        self.configuration.reset_validation_answers()

    def update(self):
        self.update_option_menu()

        if self.configuration.data_configuration_valid():
            self.label_data_progress.configure(text=DATA_DONE, fg='green')
            self.button_data.configure(bg=self.original_button_color)
        else:
            self.label_data_progress.configure(text=DATA_NOT_CONFIGURED, fg='red')
            self.button_data.configure(bg="paleturquoise1")

        if self.configuration.abstraction_configuration_valid():
            self.button_abstraction.configure(bg=self.original_button_color)
            self.selected_abstraction_option.set(get_predefined_option_from_answers(self.configuration.get_abstraction_configuration()))
            if self.configuration.data_configuration_valid():
                self.label_abstraction_progress.configure(text=ABSTRACTION_DONE, fg='green')
                self.show_simple_clustering_hint(self.configuration.no_values_abstracted)
            else:
                self.label_abstraction_progress.configure(text=ABSTRACTION_CONFIGURED, fg='DarkOrange2')
        else:
            self.button_abstraction.configure(bg='paleturquoise1')
            self.label_abstraction_progress.configure(text=ABSTRACTION_NOT_CONFIGURED, fg='red')
        if self.restricted:
            self.button_abstraction.configure(state="disabled")

        if self.configuration.distance_configuration_possible():
            if self.configuration.distance_configuration_valid():
                self.button_distance.configure(state="normal", bg=self.original_button_color)
            else:
                self.button_distance.configure(state="normal", bg='paleturquoise1')
            self.label_distance_choice.configure(state="normal")
            if not self.restricted:
                self.option_menu_distance_choice.configure(state="normal")
            # self.label_distance_progress.configure(state="normal")
        else:
            self.hide_simple_clustering_hint()
            self.button_distance.configure(state="disabled", bg=self.original_button_color)
            self.label_distance_progress.configure(fg='red')
            self.label_distance_choice.configure(state="disabled")
            self.option_menu_distance_choice.configure(state="disabled")

        if self.configuration.clustering_configuration_possible():
            self.label_distance_progress.configure(text=DISTANCE_DONE, fg='green')
            self.button_distance_play.configure(state="normal", bg=self.original_button_color)
            self.label_expert_configuration.configure(state="normal")
            if not self.restricted:
                self.checkbutton_expert_clustering.config(state="normal")
            if self.configuration.clustering_configuration_valid():
                self.button_clustering.configure(state="normal", bg=self.original_button_color)
            else:
                self.button_clustering.configure(state="normal", bg="paleturquoise1")
        else:
            self.button_clustering.configure(state="disabled", bg=self.original_button_color)
            self.label_clustering_progress.configure(fg='red')
            self.label_expert_configuration.configure(state="disabled")
            self.checkbutton_expert_clustering.configure(state="disabled")

            if self.configuration.distance_configuration_valid():
                self.label_distance_progress.configure(text=DISTANCE_NOT_CALC, fg='DarkOrange2')
                self.button_distance_play.configure(state="normal", bg='paleturquoise1')
            else:
                self.label_distance_progress.configure(text=DISTANCE_NOT_CONFIGURED, fg='red')
                self.button_distance_play.configure(state="disabled", bg=self.original_button_color)

        self.checked_expert_clustering.set(int(self.configuration.clustering_default_mode))

        if self.configuration.result_is_ready():
            self.button_show_result.configure(state="normal", bg='pale green')
            self.label_clustering_progress.configure(text=CLUSTERING_DONE, fg='green')
            self.button_clustering_play.configure(state="normal", bg=self.original_button_color)
        else:
            self.button_show_result.configure(state="disabled", bg=self.original_button_color)
            if self.configuration.clustering_execution_possible():
                # self.clustering_progress['value'] = 100
                self.label_clustering_progress.configure(text=CLUSTERING_NOT_CALC, fg='DarkOrange2')
                self.button_clustering_play.configure(state="normal", bg='paleturquoise1')
            else:
                # self.clustering_progress['value'] = 0
                if self.configuration.clustering_configuration_valid():
                    self.label_clustering_progress.configure(text=CLUSTERING_NOT_CALC, fg='DarkOrange2')
                else:
                    self.label_clustering_progress.configure(text=CLUSTERING_NOT_CONFIGURED, fg='red')
                self.button_clustering_play.configure(state="disabled", bg=self.original_button_color)

        # if self.configuration.json_saved:
        #     self.button_save_result.configure(state="normal", bg=self.original_button_color) # state="disabled"
        # else:
        #     self.button_save_result.configure(state="normal", bg='pale green')

        self.update_frame_data()
        self.update_frame_abstraction()
        self.update_frame_distance()
        self.update_frame_clustering()

        self.update_expert_clustering()

        self.update_advice()

        self.root.update()

    def update_frame_data(self):
        data_path, data_lower_limit, data_upper_limit = self.configuration.get_data_configuration()
        if data_path is None:
            self.label_data_config.configure(text=NONE)
        else:
            text = data_name_from_path(data_path)
            if data_lower_limit is not None:
                text += "[" + str(data_lower_limit) + ".."
            if data_upper_limit is not None:
                text += str(data_upper_limit)
            if data_lower_limit is not None or data_upper_limit is not None:
                text += "]"
            text += "\n" + str(self.configuration.num_data) + " values"
            self.label_data_config.configure(text=text)

    def update_frame_abstraction(self):
        answers = self.configuration.get_abstraction_configuration()
        if answers is None:
            self.label_abstraction_config.configure(text=NONE)
        else:
            abbreviations = np.array(abstraction_question_array, dtype=object)[:, 2]
            text = ""
            for i, abb in enumerate(abbreviations):
                if answers[i]:
                    text += abb + "\n"
            self.label_abstraction_config.configure(text=text)

    def update_frame_distance(self):

        def calculateFontSize(string):
            from PIL import ImageFont
            font = ImageFont.truetype('arial', 12)
            return font.getsize(string)[0]

        cost_map, blob_configuration = self.configuration.get_distance_configuration()
        if cost_map is None:
            self.label_distance_config.configure(text=NONE)
            self.label_distance_config2.configure(text="")
        else:
            labels, numbers = string_simplified_cost_map_split(cost_map, blob_configuration, self.configuration.distance_config_method)
            self.label_distance_config.configure(text=labels)
            self.label_distance_config2.configure(text=numbers)

    def update_frame_clustering(self):
        clustering_algorithm = self.configuration.get_clustering_selection()
        if clustering_algorithm is None:
            self.label_clustering_config.configure(text=NONE)
        else:
            clustering_parameters = self.configuration.get_clustering_configuration()
            text = "Algorithm: " + clustering_algorithm
            if clustering_parameters is None:
                self.label_clustering_config.configure(text=text)
            else:
                text += "\nParameters:"
                k = 0
                for i, key in enumerate(clustering_parameters.keys()):
                    parameter_value = clustering_parameters[key]
                    if parameter_value is not None:
                        text += "\n  " + key + " = " + str(parameter_value)
                self.label_clustering_config.configure(text=text)


if __name__ == "__main__":
    Hub(restricted=False, logging=False)
