import os
import sys
from math import floor, sqrt
from tkinter import Tk, Button, Label, Frame, messagebox, HORIZONTAL, ttk, Menu, Checkbutton, IntVar
from pathlib import Path
from tkinter.messagebox import WARNING
from tkinter.ttk import Progressbar
import numpy as np

from distance.weighted_levenshtein_distance import get_costmap_num, split_cost_map
from export.path import getJsonSavePath, getJsonLoadPath, getExcelSavePath
from gui_abstraction.AbstractionQuestionnaireResultInput import abstraction_configuration
from gui_abstraction.abstraction_questions import abstraction_question_array
from gui_center.hub_configuration import HubConfiguration, load_hub_configuration
from gui_cluster_selection.ClusteringQuestionnaireResultInput import cluster_suggest
from gui_data.select_data import select_data
from gui_distances import input_blobs, input_costmap
from gui_distances.blobinput_helper import get_blob_configuration
from gui_distances.distance_choice import get_distance_choice, DistanceView
from gui_distances.slider_view import slider_view
from gui_general import CreateToolTip
from gui_general.help_popup_gui import menu_help_hub
from gui_result.ResultView import result_view
from gui_result.validation_questionnaire import get_suggested_algorithms, get_suggested_data, \
    get_suggested_abstraction_modifications, get_suggested_distance_modifications, \
    get_suggested_parameter_modifications, ValidationAnswer

TITLE = "Clustering Configuration Hub"

STATUS = "Status: "
CLUSTERING_NOT_CALC = STATUS + 'Clustering configured but not calculated'
CLUSTERING_DONE = STATUS + 'Clustering done'
DISTANCE_NOT_CALC = STATUS + 'Dissimilarities configured but not calculated'
DISTANCE_DONE = STATUS + 'Dissimilarity calculation done'
ABSTRACTION_CONFIGURED = STATUS + 'Abstraction configured'
ABSTRACTION_DONE = STATUS + 'Abstraction done'
DATA_DONE = STATUS + 'Data extraction done'
CLUSTERING_IN_PROGRESS = STATUS + "Clustering in progress ..."
CLUSTERING_CONFIG_IN_PROGRESS = STATUS + "Clustering configuration in progress ..."
DISTANCE_CALC_IN_PROGRESS = STATUS + "Dissimilarity calculation in progress ..."
DISTANCE_CONFIGURATION_IN_PROGRESS = STATUS + "Dissimilarity configuration in progress ..."
ABSTRACTION_CONFIG_IN_PROGRESS = STATUS + "Abstraction configuration in progress ..."
ABSTRACTION_IN_PROGRESS = STATUS + "Abstraction in progress ..."
DATA_EXTRACTION_IN_PROGRESS = STATUS + "Data extraction in progress ..."
DATA_CONFIG_IN_PROGRESS = STATUS + "Data configuration in progress ..."
CLUSTERING_NOT_CONFIGURED = STATUS + "Clustering not configured"
DISTANCE_NOT_CONFIGURED = STATUS + "Dissimilarities not configured"
ABSTRACTION_NOT_CONFIGURED = STATUS + "Abstraction not configured"
DATA_NOT_CONFIGURED = STATUS + "Data not configured"

NONE = "None"

CLUSTERING_ADVICE = "Advice based on the evaluation: reconfigure clustering"
DISTANCE_ADVICE = "Advice based on the evaluation: reconfigure dissimilarities"
ABSTRACTION_ADVICE = "Advice based on the evaluation: reconfigure abstraction"
DATA_ADVICE = "Advice based on the evaluation: reconfigure data"


def data_name_from_path(data_path):
    if data_path is None:
        return None
    data_path_split = data_path.split("\\")
    last = data_path_split[len(data_path_split) - 1]
    last_split = last.split(".")
    data_name = last_split[0]
    return data_name


class Hub:

    def __init__(self):

        "initialisation"
        self.root = Tk()
        self.root.title(TITLE)
        self.root.configure(background='white')

        self.configuration = HubConfiguration()

        "labels"
        self.label_title = Label(self.root, text=TITLE, bg="white",
                                 font=('TkDefaultFont', 14, 'bold'), anchor="c", justify="center")
        self.label_title.grid(sticky='nswe', row=0, column=1, columnspan=4, pady=(10, 0))

        self.label_explanation = Label(self.root, text="Perform the following steps to obtain a clustering of your data.\nThe steps required next are highlighted in blue.", bg="white")
        self.label_explanation.grid(sticky='nswe', row=1, column=1, columnspan=4, pady=(0, 10))

        "menu"
        self.menu = Menu(self.root)
        self.menu.add_command(label="New", command=self.menu_new)
        self.menu.add_command(label="Save", command=self.menu_save)
        self.menu.add_command(label="Save As...", command=self.menu_saveas)
        self.menu.add_command(label="Load", command=self.menu_load)
        self.menu.add_command(label="Help", command=lambda: menu_help_hub(self.root))
        self.root.config(menu=self.menu)
        self.root.resizable(False, False)

        "buttons"
        button_width = 50
        self.button_data = Button(self.root, text='Configure Data...', command=self.configure_data,
                                  width=button_width, height=2, bg='paleturquoise1')
        self.button_abstraction = Button(self.root, text='Configure Abstraction...', command=self.configure_abstraction,
                                         width=button_width, height=2, bg='paleturquoise1')
        self.button_distance = Button(self.root, text='Configure Dissimilarities...', command=self.configure_distance,
                                      width=button_width, height=2, state="disabled")
        self.button_clustering = Button(self.root, text='Configure Clustering...', command=self.configure_clustering,
                                        width=button_width, height=2, state="disabled")

        self.button_data.grid(sticky='nwe', row=5, column=1, columnspan=2, padx=10, pady=10)
        self.button_abstraction.grid(sticky='nwe', row=8, column=1, columnspan=2, padx=10, pady=10)
        self.button_distance.grid(sticky='nwe', row=11, column=1, columnspan=2, padx=10, pady=10)
        self.button_clustering.grid(sticky='nwe', row=14, column=2, columnspan=1, padx=10, pady=10)

        CreateToolTip(self.button_data, "Specify which data you intend to analyse.")
        CreateToolTip(self.button_abstraction, "Specify features of the data values that you are not interested in.")
        CreateToolTip(self.button_distance, "Specify how certain features influence the dissimilarity between data values.")
        CreateToolTip(self.button_clustering, "Specify which clustering algorithm should be applied.")

        self.button_distance_play = Button(self.root, text='▶', command=self.execute_distance,
                                           width=4, height=2, state="disabled")
        self.button_distance_play.grid(sticky='ne', row=12, column=2, padx=10, pady=10, rowspan=2)
        self.button_clustering_play = Button(self.root, text='▶', command=self.execute_clustering,
                                             width=4, height=2, state="disabled")
        self.button_clustering_play.grid(sticky='ne', row=15, column=2, padx=10, pady=10, rowspan=2)

        self.button_show_result = Button(self.root, text='Show Result...', command=self.show_result, state="disabled",
                                         font=('Sans', '10', 'bold'), width=45, height=2)
        self.button_show_result.grid(sticky='nswe', row=17, column=1, columnspan=3, padx=10, pady=10)

        self.button_save_result = Button(self.root, text='Save', command=self.menu_save,
                                         font=('Sans', '10', 'bold'), height=2)
        self.button_save_result.grid(sticky='nswe', row=17, column=4, padx=10, pady=10)

        self.checked_clustering = IntVar(value=1)
        self.checkbutton_clustering = Checkbutton(self.root, variable=self.checked_clustering, state="disabled",
                                                  bg="white", command=self.check_default_clustering)
        self.checkbutton_clustering.grid(sticky='swe', row=14, column=1, columnspan=1, padx=10, pady=10)
        self.checkbutton_clustering_label = Label(self.root, text="Default", bg="white", width=7)
        self.checkbutton_clustering_label.grid(sticky='nwe', row=14, column=1, columnspan=1, padx=10, pady=10)

        CreateToolTip(self.button_distance_play, "Execute dissimilarity calculation.")
        CreateToolTip(self.button_clustering_play, "Execute clustering.")
        CreateToolTip(self.button_show_result, "Show calculated clustering and evaluation questionnaire.")
        CreateToolTip(self.button_save_result, "Save configuration.")

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
        self.label_data_progress = Label(self.root, text=DATA_NOT_CONFIGURED, bg="white", fg="red")
        self.label_abstraction_progress = Label(self.root, text=ABSTRACTION_NOT_CONFIGURED, bg="white", fg="red")
        self.label_distance_progress = Label(self.root, text=DISTANCE_NOT_CONFIGURED, bg="white", fg="red")
        self.label_clustering_progress = Label(self.root, text=CLUSTERING_NOT_CALC, bg="white", fg="red")

        self.label_data_progress.grid(sticky='nw', row=6, column=1, columnspan=2, padx=20, pady=2)
        self.label_abstraction_progress.grid(sticky='nw', row=9, column=1, columnspan=2, padx=20, pady=2)
        self.label_distance_progress.grid(sticky='nw', row=12, column=1, columnspan=2, padx=20, pady=2)
        self.label_clustering_progress.grid(sticky='nw', row=15, column=1, columnspan=2, padx=20, pady=2)

        CreateToolTip(self.label_data_progress, "Status of the data")
        CreateToolTip(self.label_abstraction_progress, "Status of the abstraction")
        CreateToolTip(self.label_distance_progress, "Status of the dissimilarities")
        CreateToolTip(self.label_clustering_progress, "Status of the clustering")

        "advice labels"
        self.label_data_advice = Label(self.root, text="", bg="white", fg="blue")
        self.label_abstraction_advice = Label(self.root, text="", bg="white", fg="blue")
        self.label_distance_advice = Label(self.root, text="", bg="white", fg="blue")
        self.label_clustering_advice = Label(self.root, text="", bg="white", fg="blue")

        self.label_data_advice.grid(sticky='nw', row=7, column=1, columnspan=1, padx=20, pady=2)
        self.label_abstraction_advice.grid(sticky='nw', row=10, column=1, columnspan=1, padx=20, pady=2)
        self.label_distance_advice.grid(sticky='nw', row=13, column=1, columnspan=1, padx=20, pady=2)
        self.label_clustering_advice.grid(sticky='nw', row=16, column=1, columnspan=1, padx=20, pady=2)

        # CreateToolTip(self.label_data_advice, "Status of the data")
        # CreateToolTip(self.label_abstraction_advice, "Status of the abstraction")
        # CreateToolTip(self.label_distance_advice, "Status of the distances")
        # CreateToolTip(self.label_clustering_advice, "Status of the clustering")

        "frames"
        self.frame_data = Frame(self.root, bg="grey90", width=200, height=100)
        self.frame_abstraction = Frame(self.root, bg="grey90", width=200, height=100)
        self.frame_distance = Frame(self.root, bg="grey90", width=200, height=100)
        self.frame_clustering = Frame(self.root, bg="grey90", width=200, height=100)

        self.frame_data.configure(highlightbackground="grey", highlightthickness=1)
        self.frame_abstraction.configure(highlightbackground="grey", highlightthickness=1)
        self.frame_distance.configure(highlightbackground="grey", highlightthickness=1)
        self.frame_clustering.configure(highlightbackground="grey", highlightthickness=1)

        self.frame_data.grid(sticky='nswe', row=5, column=3, rowspan=3, columnspan=2, padx=10, pady=10)
        self.frame_abstraction.grid(sticky='nswe', row=8, column=3, rowspan=3, columnspan=2, padx=10, pady=10)
        self.frame_distance.grid(sticky='nswe', row=11, column=3, rowspan=3, columnspan=2, padx=10, pady=10)
        self.frame_clustering.grid(sticky='nswe', row=14, column=3, rowspan=3, columnspan=2, padx=10, pady=10)

        "labels in frames"
        self.label_data_config_heading = Label(self.frame_data, text="Current Data Configuration:", bg="grey90", anchor="w", justify="left")
        self.label_abstraction_config_heading = Label(self.frame_abstraction, text="Current Abstraction Configuration:", bg="grey90", anchor="w",
                                              justify="left")
        self.label_distance_config_heading = Label(self.frame_distance, text="Current Dissimilarity Configuration:", bg="grey90", anchor="w", justify="left")
        self.label_clustering_config_heading = Label(self.frame_clustering, text="Current Clustering Configuration:", bg="grey90", anchor="w", justify="left")

        self.label_data_config_heading.grid(sticky='nwse', row=0, column=0, rowspan=1, columnspan=2)
        self.label_abstraction_config_heading.grid(sticky='nwse', row=0, column=0, rowspan=1, columnspan=2)
        self.label_distance_config_heading.grid(sticky='nwse', row=0, column=0, rowspan=1, columnspan=2)
        self.label_clustering_config_heading.grid(sticky='nwse', row=0, column=0, rowspan=1, columnspan=2)

        self.label_data_config = Label(self.frame_data, text=NONE, bg="grey90", anchor="w", justify="left", padx=10)
        self.label_abstraction_config = Label(self.frame_abstraction, text=NONE, bg="grey90", anchor="w", justify="left", padx=10)
        self.label_distance_config = Label(self.frame_distance, text=NONE, bg="grey90", anchor="w", justify="left", padx=10)
        self.label_clustering_config = Label(self.frame_clustering, text=NONE, bg="grey90", anchor="w", justify="left", padx=10)

        self.label_data_config.grid(sticky='nwse', row=1, column=0, rowspan=1, columnspan=2)
        self.label_abstraction_config.grid(sticky='nwse', row=1, column=0, rowspan=1, columnspan=2)
        self.label_distance_config.grid(sticky='nwse', row=1, column=0, rowspan=1, columnspan=2)
        self.label_clustering_config.grid(sticky='nwse', row=1, column=0, rowspan=1, columnspan=2)

        CreateToolTip(self.label_data_config, "Name of the selected data set.")
        CreateToolTip(self.label_abstraction_config, "Abstracted details marked by 'True'.")
        CreateToolTip(self.label_distance_config, "The first column shows the character groups. Besides corresponding dissimilarity weights are shown.")
        CreateToolTip(self.label_clustering_config, "Selected clustering algorithm and specified parameters.")

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.update()
        self.root.after(1, lambda: self.root.focus_force())
        self.root.mainloop()

    def set_saved(self, saved):
        self.configuration.json_saved = saved
        if not saved and self.root.title() != TITLE and not self.root.title().endswith("*"):
            self.root.title(self.root.title() + "*")

    def on_closing(self):
        if self.configuration.json_saved or \
                messagebox.askokcancel("Quit",
                                       "Closing the window without prior saving the configuration will delete the configuration."
                                       "\nDo you want to quit?",
                                       icon=WARNING):
            self.root.destroy()

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
        self.root.update()
        self.disable()
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
        self.root.update()
        # 1. get data from config
        self.disable()
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

    def configure_distance(self):
        self.label_distance_progress.configure(text=DISTANCE_CONFIGURATION_IN_PROGRESS, fg='magenta2')
        self.root.update()
        self.disable()
        previous_cost_map, previous_blob_configuration = self.configuration.get_distance_configuration()
        distance_choice = get_distance_choice(self.root)
        if distance_choice is None:
            self.update()
            self.root.update()
            return

        cost_map = None
        blob_configuration = None

        self.set_saved(False)

        if distance_choice == DistanceView.SLIDER:
            blob_configuration = self.configuration.create_blob_configuration()
            cost_map = slider_view(self.root, abstraction=blob_configuration[1:, 0:4],
                                   texts=list(blob_configuration[1:,1]), costmap=previous_cost_map, suggestion=get_suggested_distance_modifications(self.get_validation_answers(), self.configuration), configuration=self.configuration)
            blob_configuration = None
        elif distance_choice == DistanceView.BLOB:
            if previous_blob_configuration is None:
                if previous_cost_map is None or \
                    messagebox.askokcancel("Potential Information Loss",
                                           "You previously configured the dissimilarity "
                                           "calculation via a different method. This configuration will be "
                                           "lost upon opening the Blob Configuration View. Do you want to proceed?",
                                           icon=WARNING):
                    blob_configuration = self.configuration.create_blob_configuration()
                else:
                    self.configure_distance()
            else:
                blob_configuration = previous_blob_configuration
            cost_map, blob_configuration = input_blobs(self.root, blob_configuration, get_suggested_distance_modifications(self.get_validation_answers(), self.configuration))
        elif distance_choice == DistanceView.MATRIX:
            blob_configuration = self.configuration.create_blob_configuration()
            cost_map = input_costmap(self.root, regexes=list(blob_configuration[:, 1]), costmap=previous_cost_map,
                                         abstraction=blob_configuration[1:, 0:4], suggestion=get_suggested_distance_modifications(self.get_validation_answers(), self.configuration), configuration=self.configuration)
            blob_configuration = None

        self.reset_validation_answers()

        if cost_map is None or previous_cost_map == cost_map:
            self.configuration.blob_configuration = previous_blob_configuration
        else:
            self.configuration.set_distance_configuration(cost_map, blob_configuration)

        self.update()
        self.root.update()

    def execute_distance(self):
        self.label_distance_progress.configure(text=DISTANCE_CALC_IN_PROGRESS, fg='RoyalBlue1')
        self.root.update()

        self.configuration.execute_distance()
        self.set_saved(False)

        self.update()
        # self.configuration.save_as_json()

    def configure_clustering(self):
        self.label_clustering_progress.configure(text=CLUSTERING_CONFIG_IN_PROGRESS, fg='magenta2')
        self.root.update()
        self.disable()
        prev_clustering_algorithm, prev_answers = self.configuration.get_clustering_selection()
        prev_parameters = self.configuration.get_clustering_configuration()
        answers, cluster_config_f, clustering_algorithm = cluster_suggest(self.root, prev_answers, prev_clustering_algorithm, get_suggested_algorithms(self.get_validation_answers()))
        if clustering_algorithm is None:
            self.update()
            self.root.update()
            return

        if prev_clustering_algorithm != clustering_algorithm:
            prev_parameters = None
        parameters = cluster_config_f(self.root, answers, self.configuration.distance_matrix_map, self.configuration.values_abstracted, prev_parameters, suggestion=get_suggested_parameter_modifications(self.get_validation_answers(), self.configuration))
        if parameters is None or (prev_clustering_algorithm == clustering_algorithm and prev_parameters == parameters):
            self.update()
            self.root.update()
            return

        self.set_saved(False)
        self.configuration.excel_saved = False
        self.reset_validation_answers()
        self.configuration.set_clustering_selection(clustering_algorithm, answers)
        self.configuration.set_clustering_configuration(parameters)

        self.update()
        self.root.update()

    def check_default_clustering(self):
        self.set_clustering_config_default()
        self.update()
        self.root.update()

    def set_clustering_config_default(self):
        from clustering.hierarchical_clustering import hierarchical_n_clusters_config
        self.checked_clustering.set(1)
        clustering_algorithm = "Hierarchical"
        answers = [False, False, False, True, True, True]
        n_clusters_new = hierarchical_n_clusters_config(self.configuration.num_abstracted_data)[4]
        parameters = {'method': 'single',
                      'n_clusters': n_clusters_new,
                      'distance_threshold': None,
                      'criterion': 'maxclust',
                      'depth': None}
        self.configuration.set_clustering_selection(clustering_algorithm, answers)
        self.configuration.set_clustering_configuration(parameters)

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
        self.disable()
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
        self.disable()
        load_path = getJsonLoadPath(self.configuration.json_save_path)
        if not load_path:
            self.update()
        else:
            self.load(load_path)

    def load(self, load_path):
        self.disable()
        print("loading from " + load_path + " ...")
        self.configuration = load_hub_configuration(load_path)
        self.root.title(self.configuration.json_save_path)
        self.set_saved(True)
        self.update()

    def menu_new(self):
        if self.configuration.json_saved or \
            messagebox.askokcancel("New Configuration",
                                   "Creating a new configuration without prior saving the configuration will delete the configuration."
                                   "\nDo you want to restart?",
                                   icon=WARNING):
            self.configuration = HubConfiguration()
            self.set_clustering_config_default()
            self.update()
            self.root.title(TITLE)

    def menu_save(self):
        if not self.configuration.json_saved:
            self.disable()
            if self.configuration.json_save_path:
                self.configuration.save_as_json()
                self.set_saved(True)
            else:
                self.menu_saveas()
            self.update()

    def menu_saveas(self):
        self.configuration.json_save_path = getJsonSavePath()
        self.root.title(self.configuration.json_save_path)
        if self.configuration.json_save_path:
            self.menu_save()

    def disable(self):
        self.button_data.configure(state="disabled")
        self.button_abstraction.configure(state="disabled")
        self.button_distance.configure(state="disabled")
        self.button_clustering.configure(state="disabled")
        self.button_distance_play.configure(state="disabled")
        self.button_clustering_play.configure(state="disabled")
        self.button_show_result.configure(state="disabled")
        self.button_save_result.configure(state="disabled")

    def reset_validation_answers(self):
        self.configuration.reset_validation_answers()

    def update(self):
        self.button_data.configure(state="normal")
        self.button_abstraction.configure(state="normal")

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
            # self.label_distance_progress.configure(state="normal")
        else:
            self.button_distance.configure(state="disabled")
            self.label_distance_progress.configure(fg='red')

        if self.configuration.clustering_configuration_possible():
            self.label_distance_progress.configure(text=DISTANCE_DONE, fg='green')
            self.button_distance_play.configure(state="normal", bg=self.original_button_color)
            if self.configuration.clustering_configuration_valid():
                self.button_clustering.configure(state="normal", bg=self.original_button_color)
            else:
                self.button_clustering.configure(state="normal", bg="paleturquoise1")
        else:
            self.button_clustering.configure(state="disabled", bg=self.original_button_color)
            self.label_clustering_progress.configure(fg='red')

            if self.configuration.distance_configuration_valid():
                self.label_distance_progress.configure(text=DISTANCE_NOT_CALC, fg='orange')
                self.button_distance_play.configure(state="normal", bg='paleturquoise1')
            else:
                self.label_distance_progress.configure(text=DISTANCE_NOT_CONFIGURED, fg='red')
                self.button_distance_play.configure(state="disabled", bg=self.original_button_color)

        if self.configuration.clustering_configuration_is_default():
            self.checked_clustering.set(1)
            self.checkbutton_clustering.configure(state="disabled")
        else:
            self.checkbutton_clustering.configure(state="normal")
            self.checked_clustering.set(0)

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

        if self.configuration.json_saved:
            self.button_save_result.configure(state="normal", bg=self.original_button_color) # state="disabled"
        else:
            self.button_save_result.configure(state="normal", bg='pale green')

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
            count = 0
            for i, abb in enumerate(abbreviations):
                # if i > 0:
                #     text += ", "
                #     if i % 3 == 0:
                #         text += "\n"
                # text += abb + "=" + str(answers[i])
                if answers[i]:
                    count += 1
                    if count > 1:
                        if count % 5 == 1:
                            text += ",\n"
                        else:
                            text += ",  "
                    text += abb
            self.label_abstraction_config.configure(text=text)

    def update_frame_distance(self):

        def calculateFontSize(string):
            from PIL import ImageFont
            font = ImageFont.truetype('arial', 12)
            return font.getsize(string)[0]


        cost_map, blob_configuration = self.configuration.get_distance_configuration()
        if cost_map is None:
            self.label_distance_config.configure(text=NONE)
        else:
            n = int(floor(sqrt(len(cost_map))))
            text = ""
            for i in range(n):
                # if type(cost_map[i])
                s = "[" + str(cost_map[i]) + "]:\t"
                if calculateFontSize(s) < 53:
                    s += "\t"
                for j in range(n):
                    s2 = str(cost_map[(j, i)]) + "  "
                    while calculateFontSize(s2) < 35:
                        s2 += " "
                    s += s2
                if text == "":
                    text = s
                else:
                    text += "\n" + s

            # costmap_case, regex_np, costmap_weights = split_cost_map(cost_map)
            # text = "["
            # for i, v in enumerate(regex_np):
            #     if i > 0:
            #         text += ", "
            #     s = ""
            #     for j, c in enumerate(v):
            #         s += c
            #     text += str(s)
            # text += "]"
            # text += "\n" + str(costmap_weights)
            self.label_distance_config.configure(text=text)

    def update_frame_clustering(self):

        clustering_algorithm, clustering_answers = self.configuration.get_clustering_selection()
        if clustering_algorithm is None:
            self.label_clustering_config.configure(text=NONE)
        else:
            clustering_parameters = self.configuration.get_clustering_configuration()
            text = "Algorithm: " + clustering_algorithm
            if clustering_parameters is None:
                self.label_clustering_config.configure(text=text)
            else:
                text += "\nParameters:\n\t"
                for i, key in enumerate(clustering_parameters.keys()):
                    if i > 0:
                        text += ", "
                        if i % 3 == 0:
                            text += "\n\t"
                    text += key + "=" + str(clustering_parameters[key])
                self.label_clustering_config.configure(text=text)



if __name__ == "__main__":
    Hub()
