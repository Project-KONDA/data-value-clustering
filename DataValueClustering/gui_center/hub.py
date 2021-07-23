from tkinter import Tk, Button, Label, Frame, messagebox, HORIZONTAL, ttk, Menu
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
from gui_result.ResultView import result_view

CLUSTERING_NOT_CONFIGURED = "Clustering not configured"
DISTANCE_NOT_CONFIGURED = "Distance not configured"
ABSTRACTION_NOT_CONFIGURED = "Abstraction not configured"
DATA_NOT_CONFIGURED = "Data not configured"
PATH_NOT_CONFIGURED = "Save path not configured"
NONE = "None"


class Hub:

    def __init__(self):

        "initialisation"
        self.root = Tk()
        self.root.title("Clustering Configuration Hub")
        self.root.configure(background='white')

        self.configuration = HubConfiguration()
        self.saved = False

        "keys"
        self.root.bind_all("<Return>", self.show_result)

        "labels"
        self.label_title = Label(self.root, text="Clustering Configuration Hub", bg="white",
                                 font=('Helvatical bold', 19))
        self.label_title.grid(sticky='nswe', row=0, column=1, columnspan=3)

        "menu"

        self.menu = Menu(self.root)
        self.menu.add_command(label="Save", command=self.menu_save)
        self.menu.add_command(label="Save As ..", command=self.menu_saveas)
        self.menu.add_command(label="Load", command=self.menu_load)
        self.root.config(menu=self.menu)

        "buttons"
        self.button_data = Button(self.root, text='Configure Data...', command=self.configure_data,
                                  width=42, height=2, bg='paleturquoise1')
        self.button_abstraction = Button(self.root, text='Configure Abstraction...', command=self.configure_abstraction,
                                         width=42, height=2, bg='paleturquoise1')
        self.button_distance = Button(self.root, text='Configure Distance...', command=self.configure_distance,
                                      width=42, height=2, state="disabled")
        self.button_clustering = Button(self.root, text='Configure Clustering...', command=self.configure_clustering,
                                        width=42, height=2, state="disabled")

        self.button_data.grid(sticky='nwe', row=5, column=1, columnspan=2, padx=10, pady=10)
        self.button_abstraction.grid(sticky='nwe', row=7, column=1, columnspan=2, padx=10, pady=10)
        self.button_distance.grid(sticky='nwe', row=9, column=1, columnspan=2, padx=10, pady=10)
        self.button_clustering.grid(sticky='nwe', row=11, column=1, columnspan=2, padx=10, pady=10)

        self.button_distance_play = Button(self.root, text='▶', command=self.execute_distance,
                                           width=4, height=2, state="disabled")
        self.button_distance_play.grid(sticky='ne', row=10, column=2, padx=10, pady=10)
        self.button_clustering_play = Button(self.root, text='▶', command=self.execute_clustering,
                                             width=4, height=2, state="disabled")
        self.button_clustering_play.grid(sticky='ne', row=12, column=2, padx=10, pady=10)

        self.button_show_result = Button(self.root, text='Show Result...', command=self.show_result, state="disabled",
                                         font=('Sans', '10', 'bold'), width=45, height=2)
        self.button_show_result.grid(sticky='nswe', row=14, column=1, columnspan=3, padx=10, pady=10)

        self.button_save_result = Button(self.root, text='Save Excel', command=self.save_excel, state="disabled",
                                         font=('Sans', '10', 'bold'), height=2)
        self.button_save_result.grid(sticky='nswe', row=14, column=4, padx=10, pady=10)

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
        self.label_distance_progress = Label(self.root, text=DISTANCE_NOT_CONFIGURED, bg="white")
        self.label_clustering_progress = Label(self.root, text=CLUSTERING_NOT_CONFIGURED, bg="white")

        self.label_data_progress.grid(sticky='nw', row=6, column=1, columnspan=1, padx=20, pady=10)
        self.label_abstraction_progress.grid(sticky='nw', row=8, column=1, columnspan=1, padx=20, pady=10)
        self.label_distance_progress.grid(sticky='nw', row=10, column=1, columnspan=1, padx=20, pady=10)
        self.label_clustering_progress.grid(sticky='nw', row=12, column=1, columnspan=1, padx=20, pady=10)

        "frames"
        self.frame_data = Frame(self.root, bg="grey90", width=200, height=100)
        self.frame_abstraction = Frame(self.root, bg="grey90", width=200, height=100)
        self.frame_distance = Frame(self.root, bg="grey90", width=200, height=100)
        self.frame_clustering = Frame(self.root, bg="grey90", width=200, height=100)

        self.frame_data.configure(highlightbackground="grey", highlightthickness=1)
        self.frame_abstraction.configure(highlightbackground="grey", highlightthickness=1)
        self.frame_distance.configure(highlightbackground="grey", highlightthickness=1)
        self.frame_clustering.configure(highlightbackground="grey", highlightthickness=1)

        self.frame_data.grid(sticky='nswe', row=5, column=3, rowspan=2, columnspan=2, padx=10, pady=10)
        self.frame_abstraction.grid(sticky='nswe', row=7, column=3, rowspan=2, columnspan=2, padx=10, pady=10)
        self.frame_distance.grid(sticky='nswe', row=9, column=3, rowspan=2, columnspan=2, padx=10, pady=10)
        self.frame_clustering.grid(sticky='nswe', row=11, column=3, rowspan=2, columnspan=2, padx=10, pady=10)

        "labels in frames"
        self.label_data_config_heading = Label(self.frame_data, text="Current Data Configuration:", bg="grey90", anchor="w", justify="left")
        self.label_abstraction_config_heading = Label(self.frame_abstraction, text="Current Abstraction Configuration:", bg="grey90", anchor="w",
                                              justify="left")
        self.label_distance_config_heading = Label(self.frame_distance, text="Current Distance Configuration:", bg="grey90", anchor="w", justify="left")
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

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.root.after(1, lambda: self.root.focus_force())
        self.root.mainloop()

    def on_closing(self):
        if self.saved or messagebox.askokcancel("Quit", "Closing the window without prior saving the configuration will delete the configuration. Do you want to quit?", icon=WARNING):
            self.root.destroy()

    def data_path_from_name(self, data_name):
        if data_name is None:
            return None
        return str(Path(__file__).parent.parent) + "\\data\\" + data_name + ".txt"

    def data_name_from_path(self, data_path):
        if data_path is None:
            return None
        data_path_split = data_path.split("\\")
        last = data_path_split[len(data_path_split)-1]
        last_split = last.split(".")
        data_name = last_split[0]
        return data_name

    def configure_data(self):
        self.label_data_progress.configure(text="Data configuration in progress ...", fg='magenta2')
        self.root.update()
        self.disable()
        previous_data_path = self.configuration.get_data_configuration()[0]
        previous_data_name = self.data_name_from_path(previous_data_path)

        data_name = select_data(self.root, previous_data_name)

        if data_name is None:
            self.update()
            self.root.update()
            return

        self.saved = False
        self.configuration.set_data_configuration(self.data_path_from_name(data_name))

        self.update()
        self.root.update()

        # TODO: execute only if configuration was changed
        self.label_data_progress.configure(text="Data extraction in progress ...", fg='RoyalBlue1')
        self.root.update()

        self.configuration.execute_data()

        self.update()

        # TODO: execute only if configuration was changed
        if self.configuration.abstraction_configuration_valid():
            self.label_abstraction_progress.configure(text="Abstraction in progress ...", fg='RoyalBlue1')
            self.root.update()
            self.configuration.execute_abstraction()
            self.update()

        # self.configuration.save_as_json()

    def configure_abstraction(self):
        self.label_abstraction_progress.configure(text="Abstraction configuration in progress ...", fg='magenta2')
        self.root.update()
        # 1. get data from config
        self.disable()
        config = self.configuration.get_abstraction_configuration()
        # 2. put data into abstraction gui
        # 3. read from abstraction gui
        abstraction_answers = abstraction_configuration(self.root, self.configuration.data, config)[1]
        if abstraction_answers is None:
            self.update()
            self.root.update()
            return

        # 4. save abstraction into configuration
        self.saved = False
        self.configuration.set_abstraction_configuration(abstraction_answers)
        # 5. update self
        # 6. initiate execution of abstraction in config

        self.update()
        self.root.update()

        # TODO: execute only if configuration was changed
        self.label_abstraction_progress.configure(text="Abstraction in progress ...", fg='RoyalBlue1')
        self.root.update()

        if self.configuration.data_configuration_valid():
            self.configuration.execute_abstraction()

        self.update()
        # self.configuration.save_as_json()

    def configure_distance(self):
        self.label_distance_progress.configure(text="Distance configuration in progress ...", fg='magenta2')
        self.root.update()
        self.disable()
        cost_map, blob_configuration = self.configuration.get_distance_configuration()
        distance_choice = get_distance_choice(self.root)
        if distance_choice is None:
            self.update()
            self.root.update()
            return

        self.saved = False
        if distance_choice == DistanceView.SLIDER:
            if cost_map is None:
                blob_configuration = self.configuration.create_blob_configuration()
                cost_map = slider_view(self.root, texts=list(blob_configuration[1:,1]))
            else:
                cost_map = slider_view(self.root, costmap=cost_map)
            blob_configuration = None
        elif distance_choice == DistanceView.BLOB:
            if blob_configuration is None:
                if cost_map is None or messagebox.askokcancel("Potential Information Loss", "You previously configured the distance "
                                                                "calculation via a different method. This configuration will be "
                                                                "lost upon opening the Blob Configuration View. Do you want to proceed?", icon=WARNING):
                    blob_configuration = self.configuration.create_blob_configuration()
                else:
                    self.configure_distance()
            cost_map, blob_configuration = input_blobs(self.root, blob_configuration)
        elif distance_choice == DistanceView.MATRIX:
            if cost_map is None:
                blob_configuration = self.configuration.create_blob_configuration()
                cost_map = input_costmap(self.root, regexes=list(blob_configuration[1:,1]))
            else:
                cost_map = input_costmap(self.root, costmap=cost_map)
            blob_configuration = None

        if cost_map is None:
            self.update()
            self.root.update()
            return

        self.configuration.set_distance_configuration(cost_map, blob_configuration)

        self.update()
        self.root.update()

    def execute_distance(self):
        # TODO: execute only if configuration was changed
        self.label_distance_progress.configure(text="Distance calculation in progress ...", fg='RoyalBlue1')
        self.root.update()

        self.configuration.execute_distance()

        # TODO: show percentage

        self.update()
        # self.configuration.save_as_json()

    def configure_clustering(self):
        self.label_clustering_progress.configure(text="Clustering configuration in progress ...", fg='magenta2' )
        self.root.update()
        self.disable()
        prev_clustering_algorithm, prev_answers = self.configuration.get_clustering_selection()
        prev_parameters = self.configuration.get_clustering_configuration()
        answers, cluster_config_f, clustering_algorithm = cluster_suggest(self.root, prev_answers, prev_clustering_algorithm)
        if clustering_algorithm is None:
            self.update()
            self.root.update()
            return

        self.saved = False
        self.configuration.set_clustering_selection(clustering_algorithm, answers)
        if prev_clustering_algorithm != clustering_algorithm:
            prev_parameters = None
        parameters = cluster_config_f(self.root, answers, self.configuration.distance_matrix_map, self.configuration.values_abstracted, prev_parameters)
        if parameters is None:
            self.update()
            self.root.update()
            return
        self.configuration.set_clustering_configuration(parameters)

        self.update()
        self.root.update()

    def execute_clustering(self):
        # TODO: execute only if configuration was changed
        self.label_clustering_progress.configure(text="Clustering in progress ...", fg='RoyalBlue1')
        self.root.update()

        self.configuration.execute_clustering()

        # self.update()

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

    # def abstraction_callback(self, percentage):
    #     self.abstraction_progress['value'] = percentage
    #     self.root.update()

    # def distance_callback(self, percentage):
    #     self.distance_progress['value'] = percentage
    #     self.root.update()

    def menu_load(self):
        load_path = getJsonLoadPath(self.configuration.json_save_path)
        if not load_path: return
        print("loading from " + load_path + " ...")
        self.configuration = load_hub_configuration(load_path)
        self.update()
        self.saved = True

    def menu_save(self):
        if self.configuration.json_save_path:
            self.configuration.save_as_json()
            self.saved = True
        else:
            self.menu_saveas()

    def menu_saveas(self):
        self.configuration.json_save_path = getJsonSavePath()
        if self.configuration.json_save_path:
            self.menu_save()

    def save_excel(self):
        self.configuration.excel_save_path = getExcelSavePath()
        self.configuration.save_as_excel()

    def disable(self):
        self.button_data.configure(state="disabled")
        self.button_abstraction.configure(state="disabled")
        self.button_distance.configure(state="disabled")
        self.button_clustering.configure(state="disabled")
        self.button_distance_play.configure(state="disabled")
        self.button_clustering_play.configure(state="disabled")
        self.button_show_result.configure(state="disabled")
        self.button_save_result.configure(state="disabled")

    def update(self):
        self.button_data.configure(state="normal")
        self.button_abstraction.configure(state="normal")

        if self.configuration.data_configuration_valid():
            self.label_data_progress.configure(text='Data extraction done', fg='green')
            self.button_data.configure(bg=self.original_button_color)
        else:
            self.label_data_progress.configure(text=DATA_NOT_CONFIGURED, fg='red')
            self.button_data.configure(bg="paleturquoise1")

        if self.configuration.abstraction_configuration_valid():
            self.button_abstraction.configure(bg=self.original_button_color)
            if self.configuration.data_configuration_valid():
                self.label_abstraction_progress.configure(text='Abstraction done', fg='green')
            else:
                self.label_abstraction_progress.configure(text='Abstraction configured', fg='orange')
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
            self.label_distance_progress.configure(text='Distance calculation done', fg='green')
            self.button_distance_play.configure(state="normal", bg=self.original_button_color)
            if self.configuration.clustering_configuration_valid():
                self.button_clustering.configure(state="normal", bg=self.original_button_color)
            else:
                self.button_clustering.configure(state="normal", bg="paleturquoise1")
        else:
            self.button_clustering.configure(state="disabled", bg=self.original_button_color)
            self.label_clustering_progress.configure(fg='red')

            if self.configuration.distance_configuration_valid():
                self.label_distance_progress.configure(text='Distance configured but not calculated', fg='orange')
                self.button_distance_play.configure(state="normal", bg='paleturquoise1')
            else:
                self.label_distance_progress.configure(text=DISTANCE_NOT_CONFIGURED, fg='red')
                self.button_distance_play.configure(state="disabled", bg=self.original_button_color)

        if self.configuration.result_is_ready():
            self.button_show_result.configure(state="normal", bg='pale green')
            self.button_save_result.configure(state="normal", bg='pale green')
            self.label_clustering_progress.configure(text='Clustering done', fg='green')
            self.button_clustering_play.configure(state="normal", bg=self.original_button_color)
        else:
            self.button_show_result.configure(state="disabled", bg=self.original_button_color)
            self.button_save_result.configure(state="disabled", bg=self.original_button_color)
            if self.configuration.clustering_execution_possible():
                # self.clustering_progress['value'] = 100
                self.label_clustering_progress.configure(text='Clustering configured but not calculated', fg='orange')
                self.button_clustering_play.configure(state="normal", bg='paleturquoise1')
            else:
                # self.clustering_progress['value'] = 0
                self.label_clustering_progress.configure(text=CLUSTERING_NOT_CONFIGURED, fg='red')
                self.button_clustering_play.configure(state="disabled", bg=self.original_button_color)

        self.update_frame_data()
        self.update_frame_abstraction()
        self.update_frame_distance()
        self.update_frame_clustering()

        self.root.update()

    def update_frame_data(self):
        data_path, data_lower_limit, data_upper_limit = self.configuration.get_data_configuration()
        if data_path is None:
            self.label_data_config.configure(text=NONE)
        else:
            text = self.data_name_from_path(data_path)
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
                if i>0:
                    text += ", "
                    if i % 3 == 0:
                        text += "\n"
                text += abb + "=" + str(answers[i])
            self.label_abstraction_config.configure(text=text)

    def update_frame_distance(self):
        cost_map, blob_configuration = self.configuration.get_distance_configuration()
        if cost_map is None:
            self.label_distance_config.configure(text=NONE)
        else:
            costmap_case, regex_np, costmap_weights = split_cost_map(cost_map)
            text = str(regex_np) + "\n" + str(costmap_weights)
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
                text += "\nParameters: "
                for i, key in enumerate(clustering_parameters.keys()):
                    if i>0:
                        text += ", "
                        if i % 3 == 0:
                            text += "\n\t"
                    text += key + "=" + str(clustering_parameters[key])
                self.label_clustering_config.configure(text=text)



if __name__ == "__main__":
    Hub()
