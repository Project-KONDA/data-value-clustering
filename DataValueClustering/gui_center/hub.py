import os
import subprocess
from math import floor, sqrt
from tkinter import Tk, Button, Label, Frame, messagebox, Menu, Checkbutton, IntVar, LabelFrame, \
    OptionMenu, StringVar
from pathlib import Path
from tkinter.messagebox import WARNING, ERROR
import numpy as np
import sys

import xlsxwriter

from clustering.hierarchical_clustering import hierarchical_method_config
from export.path import getJsonSavePath, getJsonLoadPath, getExcelSavePath
from gui_abstraction.AbstractionQuestionnaireResultInput import abstraction_configuration
from gui_abstraction.abstraction_questions import abstraction_question_array
from gui_center.hub_configuration import HubConfiguration, load_hub_configuration
from gui_cluster_configuration.cluster_algorithms_gui import simple_cluster_hierarchical
from gui_cluster_selection.select_algorithm import select_algorithm
from gui_data.select_data import select_data
from gui_distances.BlobInput import input_blobs
from gui_distances.CostMapInput import input_costmap
from gui_distances.costmapinput_helper import string_simplified_cost_map_split
from gui_distances.distance_choice import DistanceView
from gui_distances.slider_view import slider_view
from gui_general import CreateToolTip
from gui_general.help_popup_gui import menu_help_hub
from gui_general.scrollable_frame import create_scrollable_frame
from gui_general.window_size import set_window_size
from gui_result.ResultView import result_view
from gui_result.validation_questionnaire import get_suggested_algorithms, get_suggested_data, \
    get_suggested_abstraction_modifications, get_suggested_distance_modifications, \
    get_suggested_parameter_modifications, ValidationAnswer

DISTANCE_OPTION_MATRIX = "Matrix (expert)"
DISTANCE_OPTION_BLOBS = "Blobs (advanced)"
DISTANCE_OPTION_SLIDERS = "Sliders (easy)"


CONFIG_DISSIMILARITIES = 'Configure Dissimilarities...'
CONFIG_DISSIMILARITIES_SLIDERS = 'Configure Dissimilarities... (Sliders)'
CONFIG_DISSIMILARITIES_BLOBS = 'Configure Dissimilarities... (Blobs)'
CONFIG_DISSIMILARITIES_MATRIX = 'Configure Dissimilarities... (Matrix)'

CONFIG_CLUSTERING_SIMPLE = 'Configure Algorithm... (simple)'
CONFIG_CLUSTERING_EXPERT = 'Configure Algorithm... (expert)'


TITLE = "Clustering Configuration Hub"

STATUS = "Status: "
CLUSTERING_NOT_CALC = STATUS + 'Algorithm configured but not executed'
CLUSTERING_DONE = STATUS + 'Algorithm execution done'
DISTANCE_NOT_CALC = STATUS + 'Dissimilarities configured but not calculated'
DISTANCE_DONE = STATUS + 'Dissimilarity calculation done'
ABSTRACTION_CONFIGURED = STATUS + 'Abstraction configured'
ABSTRACTION_DONE = STATUS + 'Abstraction done'
DATA_DONE = STATUS + 'Data extraction done'
CLUSTERING_IN_PROGRESS = STATUS + "Algorithm execution in progress ..."
CLUSTERING_CONFIG_IN_PROGRESS = STATUS + "Algorithm configuration in progress ..."
DISTANCE_CALC_IN_PROGRESS = STATUS + "Dissimilarity calculation in progress ..."
DISTANCE_CONFIGURATION_IN_PROGRESS = STATUS + "Dissimilarity configuration in progress ..."
ABSTRACTION_CONFIG_IN_PROGRESS = STATUS + "Abstraction configuration in progress ..."
ABSTRACTION_IN_PROGRESS = STATUS + "Abstraction in progress ..."
DATA_EXTRACTION_IN_PROGRESS = STATUS + "Data extraction in progress ..."
DATA_CONFIG_IN_PROGRESS = STATUS + "Data configuration in progress ..."
CLUSTERING_NOT_CONFIGURED = STATUS + "Algorithm not configured"
DISTANCE_NOT_CONFIGURED = STATUS + "Dissimilarities not configured"
ABSTRACTION_NOT_CONFIGURED = STATUS + "Abstraction not configured"
DATA_NOT_CONFIGURED = STATUS + "Data not configured"

SIMPLE_CLUSTERING_HINT_1 = "The simple clustering yielded "
SIMPLE_CLUSTERING_HINT_2 = " clusters. You can stop here \nor continue below to achieve a coarser clustering."
# SIMPLE_CLUSTERING_HINT_2 = " clusters.\nTo achieve a coarser clustering, go to 'Refined Clustering'."

NONE = "None"

CLUSTERING_ADVICE = "Advice: reconfigure algorithm"
DISTANCE_ADVICE = "Advice: reconfigure dissimilarities"
ABSTRACTION_ADVICE = "Advice: reconfigure abstraction"
DATA_ADVICE = "Advice: reconfigure data"


def data_name_from_path(data_path):
    if data_path is None:
        return None
    data_path_split = data_path.split("\\")
    last = data_path_split[len(data_path_split) - 1]
    last_split = last.split(".")
    data_name = last_split[0]
    return data_name


class Hub:

    def __init__(self, loadpath=None):

        "initialisation"
        self.root = Tk()
        self.root.attributes('-alpha', 0.0)
        self.root.title(TITLE)
        self.root.configure(background='white')

        self.configuration = HubConfiguration()

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
        self.menu.add_command(label="Help", command=lambda: menu_help_hub(self.root))
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

        "distance method choice"
        self.label_distance_choice = Label(self.refined_clustering_frame, text="Dissimilarities Configuration Method:", bg="white")
        self.label_distance_choice.grid(sticky='w', row=10, column=1, padx=(10,0), pady=10)

        self.distance_options = [DISTANCE_OPTION_SLIDERS, DISTANCE_OPTION_BLOBS]
        self.selected_distance_option = StringVar()
        self.selected_distance_option.set(DISTANCE_OPTION_SLIDERS)
        self.option_menu_distance_choice = OptionMenu(self.refined_clustering_frame, self.selected_distance_option,
                                                 *self.distance_options, command=self.selected_distance_option_changed)
        self.option_menu_distance_choice.grid(sticky='ws', row=10, column=2, pady=10)

        "buttons"
        button_width_part = 37
        button_width_full = 50
        button_height = 2
        self.button_data = Button(self.data_frame, text='Configure Data...', command=self.configure_data,
                                  width=button_width_full, height=button_height, bg='paleturquoise1')
        self.button_abstraction = Button(self.simple_clustering_frame, text='Configure Abstraction...', command=self.configure_abstraction,
                                         width=button_width_full, height=button_height, bg='paleturquoise1')
        self.button_distance = Button(self.refined_clustering_frame, text=CONFIG_DISSIMILARITIES_SLIDERS, command=self.configure_distance,
                                      width=button_width_full, height=button_height, state="disabled")
        self.button_clustering = Button(self.refined_clustering_frame, text=CONFIG_CLUSTERING_SIMPLE, command=self.configure_clustering,
                                        width=button_width_part, height=button_height, state="disabled")

        self.button_data.grid(sticky='nwe', row=5, column=1, columnspan=2, padx=10, pady=10)
        self.button_abstraction.grid(sticky='nwe', row=8, column=1, columnspan=2, padx=10, pady=10)
        self.button_distance.grid(sticky='nwe', row=11, column=1, columnspan=2, padx=10, pady=10)
        self.button_clustering.grid(sticky='nwe', row=15, column=1, columnspan=2, padx=10, pady=10)

        CreateToolTip(self.button_data, "Specify which data you intend to analyse.")
        CreateToolTip(self.button_abstraction, "Specify features of the data values that you are not interested in.")
        CreateToolTip(self.button_distance, "Specify how certain features influence the dissimilarity between data values.")
        CreateToolTip(self.button_clustering, "Specify which clustering algorithm should be applied.")

        self.button_distance_play = Button(self.refined_clustering_frame, text='▶', command=self.execute_distance,
                                           width=4, height=2, state="disabled")
        self.button_distance_play.grid(sticky='ne', row=12, column=2, padx=10, pady=10, rowspan=2)
        self.button_clustering_play = Button(self.refined_clustering_frame, text='▶', command=self.execute_clustering,
                                             width=4, height=2, state="disabled")
        self.button_clustering_play.grid(sticky='ne', row=16, column=2, padx=10, pady=10, rowspan=2)

        self.button_show_result = Button(self.scrollable_frame, text='Open Refined Clustering...', command=self.show_result, state="disabled",
                                         font=('Sans', '10', 'bold'), width=45, height=2)
        self.button_show_result.grid(sticky='nswe', row=7, column=0, columnspan=2, padx=10, pady=10)

        # self.button_save_result = Button(self.root, text='Save', command=self.menu_save,
        #                                  font=('Sans', '10', 'bold')) #, height=2)
        # self.button_save_result.grid(sticky='nswe', row=17, column=1, padx=10, pady=10)
        # self.button_save_result.grid(sticky='ne', row=0, column=1, padx=10, pady=10)

        self.label_expert_configuration = Label(self.refined_clustering_frame, text="Algorithm Configuration Method:", bg="white")
        self.label_expert_configuration.grid(sticky='w', row=14, column=1, padx=(10,0), pady=10)
        self.checked_expert_clustering = IntVar(value=1)
        self.checkbutton_expert_clustering = Checkbutton(self.refined_clustering_frame,
            variable=self.checked_expert_clustering, bg="white", command=self.trigger_expert_clustering, text="Expert")
        self.checkbutton_expert_clustering.grid(sticky='ws', row=14, column=2, pady=10)

        # self.checkbutton_clustering_label = Label(self.refined_clustering_frame, text="Default", bg="white", width=7)
        # self.checkbutton_clustering_label.grid(sticky='nwe', row=14, column=1, columnspan=1, padx=10, pady=10)

        CreateToolTip(self.button_distance_play, "Execute dissimilarity calculation.")
        CreateToolTip(self.button_clustering_play, "Execute clustering algorithm.")
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
        CreateToolTip(self.label_abstraction_progress, "Status of the abstraction")
        CreateToolTip(self.label_distance_progress, "Status of the dissimilarities")
        CreateToolTip(self.label_clustering_progress, "Status of the clustering")

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
            create_scrollable_frame(self.data_frame)
        self.preview_abstraction_outer, self.preview_abstraction_canvas, self.preview_abstraction = \
            create_scrollable_frame(self.simple_clustering_frame)
        self.preview_distance_outer, self.preview_distance_canvas, self.preview_distance = \
            create_scrollable_frame(self.refined_clustering_frame)
        self.preview_clustering_outer, self.preview_clustering_canvas, self.preview_clustering = \
            create_scrollable_frame(self.refined_clustering_frame)

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
        self.preview_abstraction_outer.grid(sticky='nswe', row=8, column=3, rowspan=3, columnspan=2, padx=10, pady=10)
        self.preview_distance_outer.grid(sticky='nswe', row=10, column=3, rowspan=4, columnspan=2, padx=10, pady=10)
        self.preview_clustering_outer.grid(sticky='nswe', row=14, column=3, rowspan=4, columnspan=2, padx=10, pady=10)

        "labels in preview frames"
        label_width = 40
        self.label_data_config_heading = Label(self.preview_data, text="Current Data Configuration:", bg="grey90", anchor="w", justify="left", width=label_width)
        self.label_abstraction_config_heading = Label(self.preview_abstraction, text="Current Abstraction Configuration:", bg="grey90", anchor="w", justify="left", width=label_width)
        self.label_distance_config_heading = Label(self.preview_distance, text="Current Dissimilarity Configuration:", bg="grey90", anchor="w", justify="left", width=label_width)
        self.label_clustering_config_heading = Label(self.preview_clustering, text="Current Algorithm Configuration:", bg="grey90", anchor="w", justify="left", width=label_width)

        self.label_data_config_heading.grid(sticky='nw', row=0, column=0, rowspan=1)
        self.label_abstraction_config_heading.grid(sticky='nw', row=0, column=0)
        self.label_distance_config_heading.grid(sticky='nw', row=0, column=0)
        self.label_clustering_config_heading.grid(sticky='nw', row=0, column=0)

        # TODO: add scrollbars or use Text instead of Label
        self.label_data_config = Label(self.preview_data, text=NONE, bg="grey90", anchor="nw", justify="left", padx=10, width=label_width)
        self.label_abstraction_config = Label(self.preview_abstraction, text=NONE, bg="grey90", anchor="nw", justify="left", padx=10, width=label_width)
        self.label_distance_config = Label(self.preview_distance, text=NONE, bg="grey90", anchor="nw", justify="left", padx=10, width=label_width)
        self.label_distance_config2 = Label(self.preview_distance, text=NONE, bg="grey90", anchor="nw", justify="right", padx=10, width=0)
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
        CreateToolTip(self.button_abstraction_excel, "Open Excel file showing simple clustering resulting from the abstraction.")
        self.hide_simple_clustering_hint()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.update()

        self.root.update_idletasks()

        # calculate and set window size:
        h_root = self.root.winfo_reqheight()
        h_scrollable = self.scrollable_frame.winfo_height()
        h_canvas_questionnaire = self.canvas.winfo_height()
        h_expanded = h_root - h_canvas_questionnaire + h_scrollable
        set_window_size(self.root, h_expanded)

        self.root.attributes('-alpha', 1.0)

        self.root.after(1, lambda: self.root.focus_force())
        if loadpath is not None:
            self.load(loadpath)
        self.root.mainloop()

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
                                              "You previously configured the dissimilarity "
                                              "calculation via Expert Mode, i.e. the matrix. This configuration will be "
                                              "lost if you configure the weights via the Sliders view.",
                                              icon=WARNING):
                    self.set_selected_distance_option(DISTANCE_OPTION_MATRIX)
            elif previous_method == DistanceView.BLOB:
                if not messagebox.askokcancel("Potential Information Loss",
                                              "You previously configured the dissimilarity "
                                              "calculation via Blobs. This configuration will be "
                                              "lost if you configure the weights via the Sliders view.",
                                              icon=WARNING):
                    self.set_selected_distance_option(DISTANCE_OPTION_BLOBS)
        elif new_selection == DISTANCE_OPTION_BLOBS:
            if previous_method == DistanceView.MATRIX:
                if not messagebox.askokcancel("Potential Information Loss",
                                              "You previously configured the dissimilarity "
                                              "calculation via Expert Mode, i.e. the matrix. This configuration will be "
                                              "lost if you configure the weights via the Blobs view.",
                                              icon=WARNING):
                    self.set_selected_distance_option(DISTANCE_OPTION_MATRIX)
            elif previous_method == DistanceView.SLIDER:
                if not messagebox.askokcancel("Potential Information Loss",
                                              "You previously configured the dissimilarity "
                                              "calculation via Sliders. This configuration will be "
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

        if self.configuration.excel_simple_save_path is not None:
            try:
                if not self.configuration.excel_simple_saved:
                    self.configuration.save_simple_as_excel()
                    self.configuration.excel_simple_saved = True
                subprocess.check_output('"' + self.configuration.excel_simple_save_path + '"', shell=True,
                                        stderr=subprocess.STDOUT)
            except (PermissionError, xlsxwriter.exceptions.FileCreateError) as e:
                messagebox.showerror("Error",
                                       "Cannot save file at selected path since the file exists already and is currently open."
                                       "Please close the file first or select a different path.",
                                       icon=ERROR)
                self.configuration.excel_simple_save_path = None
            except subprocess.CalledProcessError as e:
                messagebox.showerror("Error",
                                     "File is already open.",
                                     icon=ERROR)
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

        data_name = select_data(self.root, previous_data_name, get_suggested_data(self.get_validation_answers()))

        if data_name is None or previous_data_name == data_name:
            self.update()
            self.root.update()
            return

        self.set_saved(False)
        self.reset_validation_answers()
        self.configuration.set_data_configuration(self.data_path_from_name(data_name))

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
            self.update()

        # self.configuration.save_as_json()

    def configure_abstraction(self):
        self.label_abstraction_progress.configure(text=ABSTRACTION_CONFIG_IN_PROGRESS, fg='magenta2')
        # 1. get data from config
        previous_abstraction_answers = self.configuration.get_abstraction_configuration()
        # 2. put data into abstraction gui
        # 3. read from abstraction gui
        abstraction_answers = abstraction_configuration(self.root, self.configuration.data, previous_abstraction_answers, get_suggested_abstraction_modifications(self.get_validation_answers(), self.configuration))[1]
        if abstraction_answers is None or previous_abstraction_answers == abstraction_answers:
            self.update()
            self.root.update()
            return

        # 4. save abstraction into configuration
        self.set_saved(False)
        self.reset_validation_answers()
        self.configuration.set_abstraction_configuration(abstraction_answers)
        # 5. update self
        # 6. initiate execution of abstraction in config

        self.update()
        self.root.update()

        self.label_abstraction_progress.configure(text=ABSTRACTION_IN_PROGRESS, fg='RoyalBlue1')
        self.root.update()

        if self.configuration.data_configuration_valid():
            self.configuration.execute_abstraction()

        self.update()
        # self.configuration.save_as_json()

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
        self.label_abstraction_hint.configure(fg="grey", text="You need to configure the data and the abstraction\nbefore you can access the simple clustering.")
        self.button_abstraction_excel.configure(state="disabled")
        self.button_abstraction_excel.configure(bg=self.original_button_color)

    def configure_distance(self):
        self.label_distance_progress.configure(text=DISTANCE_CONFIGURATION_IN_PROGRESS, fg='magenta2')
        previous_cost_map, blob_configuration = self.configuration.get_distance_configuration()

        self.set_saved(False)

        if self.selected_distance_option.get() == DISTANCE_OPTION_SLIDERS:
            config_method, cost_map = slider_view(self.root, abstraction=blob_configuration[1:, 0:4],
                                   texts=list(blob_configuration[1:,1]), costmap=previous_cost_map, suggestion=get_suggested_distance_modifications(self.get_validation_answers(), self.configuration), configuration=self.configuration)
            blob_configuration = None
        elif self.selected_distance_option.get() == DISTANCE_OPTION_BLOBS:
            config_method, cost_map, blob_configuration = input_blobs(self.root, blob_configuration, get_suggested_distance_modifications(self.get_validation_answers(), self.configuration))
        else:
            cost_map = input_costmap(self.root, regexes=list(blob_configuration[:, 1]), costmap=previous_cost_map,
                                         abstraction=blob_configuration[1:, 0:4], suggestion=get_suggested_distance_modifications(self.get_validation_answers(), self.configuration), configuration=self.configuration)
            blob_configuration = None
            config_method = DistanceView.MATRIX

        self.reset_validation_answers()

        if cost_map is None or previous_cost_map == cost_map:
            self.configuration.blob_configuration = blob_configuration
        else:
            self.configuration.set_distance_configuration(cost_map, blob_configuration)

        if config_method is not None:
            self.configuration.set_distance_config_method(config_method)

        self.update()
        self.root.update()

    def update_option_menu_value_list(self):
        menu = self.option_menu_distance_choice["menu"]
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
        self.label_distance_progress.configure(text=DISTANCE_CALC_IN_PROGRESS, fg='RoyalBlue1')
        self.root.update()

        self.configuration.execute_distance()
        self.set_saved(False)

        self.update()
        # self.configuration.save_as_json()

    def configure_clustering(self):
        self.label_clustering_progress.configure(text=CLUSTERING_CONFIG_IN_PROGRESS, fg='magenta2')
        prev_clustering_algorithm = self.configuration.get_clustering_selection()
        prev_parameters = self.configuration.get_clustering_configuration()
        suggested_algorithms = get_suggested_algorithms(self.get_validation_answers())

        if self.checked_expert_clustering.get() == 1:
            cluster_config_f, clustering_algorithm = select_algorithm(self.root, prev_clustering_algorithm, suggested_algorithms)

            if clustering_algorithm is None:
                self.update()
                self.root.update()
                return

            if prev_clustering_algorithm != clustering_algorithm:
                prev_parameters = None
                suggested_parameter_modifications = None
            else:
                suggested_parameter_modifications = get_suggested_parameter_modifications(self.get_validation_answers(), self.configuration)
            parameters = cluster_config_f(self.root, self.configuration.distance_matrix_map, self.configuration.values_abstracted, prev_parameters, suggestion=suggested_parameter_modifications)
        else:
            clustering_algorithm = "Hierarchical"

            if prev_clustering_algorithm != clustering_algorithm:
                prev_parameters = None
                suggested_parameter_modifications = None
            else:
                suggested_parameter_modifications = get_suggested_parameter_modifications(self.get_validation_answers(), self.configuration)
            parameters = simple_cluster_hierarchical(self.root, self.configuration.distance_matrix_map, self.configuration.values_abstracted, prev_parameters, suggestion=suggested_parameter_modifications)

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

    def trigger_expert_clustering(self):
        self.configuration.clustering_expert_mode = bool(self.checked_expert_clustering.get())
        if self.configuration.clustering_expert_mode:
            self.button_clustering.configure(text=CONFIG_CLUSTERING_EXPERT)
        else:
            self.button_clustering.configure(text=CONFIG_CLUSTERING_SIMPLE)

    def get_validation_answers(self):
        return self.configuration.get_validation_answer_1(), self.configuration.get_validation_answer_2(), self.configuration.get_validation_answer_3(), self.configuration.get_validation_answer_4(),

    def execute_clustering(self):
        self.label_clustering_progress.configure(text=CLUSTERING_IN_PROGRESS, fg='RoyalBlue1')
        self.root.update()

        self.configuration.execute_clustering()

        self.set_saved(False)
        self.configuration.excel_saved = False

        # self.label_clustering_progress.configure(text="Saving in progress ...", fg='RoyalBlue1')
        # self.root.update()
        #
        # self.configuration.save_as_json()
        # self.configuration.save_as_excel()

        self.update()

    def show_result(self):
        # validation_result = result_view(self.root, self.configuration.excel_save_path, self.configuration.num_data, self.configuration.num_abstracted_data, self.configuration.abstraction_rate, self.configuration.no_clusters, self.configuration.no_noise,
        #             self.configuration.timedelta_abstraction, self.configuration.timedelta_distance, self.configuration.timedelta_cluster, self.configuration.timedelta_total,
        #             self.configuration.values_abstracted, self.configuration.distance_matrix_map, self.configuration.clusters_abstracted)
        result_view(self.root, self.configuration)
        self.update()

    def update_advice(self):
        answers = self.get_validation_answers()
        self.label_data_advice.config(text="")
        self.label_abstraction_advice.config(text="")
        self.label_distance_advice.config(text="")
        self.label_clustering_advice.config(text="")
        if answers[0] is not None and answers[0] != ValidationAnswer.HAPPY:
            self.label_abstraction_advice.config(text=ABSTRACTION_ADVICE)
            self.label_distance_advice.config(text=DISTANCE_ADVICE)
            self.label_clustering_advice.config(text=CLUSTERING_ADVICE)
        if answers[1] is not None and answers[1] != ValidationAnswer.HAPPY:
            self.label_clustering_advice.config(text=CLUSTERING_ADVICE)
        if answers[2] is not None and answers[2] != ValidationAnswer.HAPPY:
            self.label_abstraction_advice.config(text=ABSTRACTION_ADVICE)
            self.label_distance_advice.config(text=DISTANCE_ADVICE)
            self.label_clustering_advice.config(text=CLUSTERING_ADVICE)
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
        self.update()

    def menu_new(self):
        if self.configuration.json_saved or \
            messagebox.askokcancel("New Configuration",
                                   "Creating a new configuration without prior saving the current configuration will delete it."
                                   "\nDo you want to proceed?",
                                   icon=WARNING):
            self.configuration = HubConfiguration()
            self.update()
            self.root.title(TITLE)

    def menu_save(self):
        if not self.configuration.json_saved:
            if self.configuration.json_save_path is not None:
                self.configuration.save_as_json()
                self.set_saved(True)
            else:
                self.menu_saveas()
            self.update()

    def menu_saveas(self):
        self.configuration.json_save_path = getJsonSavePath()
        if self.configuration.json_save_path is not None:
            self.menu_save()

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
            if self.configuration.data_configuration_valid():
                self.label_abstraction_progress.configure(text=ABSTRACTION_DONE, fg='green')
                self.show_simple_clustering_hint(self.configuration.no_values_abstracted)
            else:
                self.label_abstraction_progress.configure(text=ABSTRACTION_CONFIGURED, fg='orange')
        else:
            self.button_abstraction.configure(bg='paleturquoise1')
            self.label_abstraction_progress.configure(text=ABSTRACTION_NOT_CONFIGURED, fg='red')


        if self.configuration.distance_configuration_possible():
            if self.configuration.distance_configuration_valid():
                self.button_distance.configure(state="normal", bg=self.original_button_color)
            else:
                self.button_distance.configure(state="normal", bg='paleturquoise1')
            self.label_distance_choice.configure(state="normal")
            self.option_menu_distance_choice.configure(state="normal")
            # self.label_distance_progress.configure(state="normal")
        else:
            self.button_distance.configure(state="disabled")
            self.label_distance_progress.configure(fg='red')
            self.label_distance_choice.configure(state="disabled")
            self.option_menu_distance_choice.configure(state="disabled")

        if self.configuration.clustering_configuration_possible():
            self.label_distance_progress.configure(text=DISTANCE_DONE, fg='green')
            self.button_distance_play.configure(state="normal", bg=self.original_button_color)
            self.label_expert_configuration.configure(state="normal")
            self.checkbutton_expert_clustering.configure(state="normal")
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
                self.label_distance_progress.configure(text=DISTANCE_NOT_CALC, fg='orange')
                self.button_distance_play.configure(state="normal", bg='paleturquoise1')
            else:
                self.label_distance_progress.configure(text=DISTANCE_NOT_CONFIGURED, fg='red')
                self.button_distance_play.configure(state="disabled", bg=self.original_button_color)

        self.checked_expert_clustering.set(int(self.configuration.clustering_expert_mode))

        if self.configuration.result_is_ready():
            self.button_show_result.configure(state="normal", bg='pale green')
            self.label_clustering_progress.configure(text=CLUSTERING_DONE, fg='green')
            self.button_clustering_play.configure(state="normal", bg=self.original_button_color)
        else:
            self.button_show_result.configure(state="disabled", bg=self.original_button_color)
            if self.configuration.clustering_execution_possible():
                # self.clustering_progress['value'] = 100
                self.label_clustering_progress.configure(text=CLUSTERING_NOT_CALC, fg='orange')
                self.button_clustering_play.configure(state="normal", bg='paleturquoise1')
            else:
                # self.clustering_progress['value'] = 0
                if self.configuration.clustering_configuration_valid():
                    self.label_clustering_progress.configure(text=CLUSTERING_NOT_CALC, fg='orange')
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
            labels, numbers = string_simplified_cost_map_split(cost_map, blob_configuration)
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
    Hub()
