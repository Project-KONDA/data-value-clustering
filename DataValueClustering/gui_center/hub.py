from tkinter import Tk, Button, Label, Frame, messagebox, HORIZONTAL, ttk, Menu
from pathlib import Path
from tkinter.messagebox import WARNING
from tkinter.ttk import Progressbar

from export.path import getJsonSavePath, getJsonLoadPath, getExcelSavePath
from gui_abstraction.AbstractionQuestionnaireResultInput import abstraction_configuration
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


class Hub:

    def __init__(self):

        "initialisation"
        self.root = Tk()
        self.root.title("Clustering Configuration Hub")
        self.root.configure(background='white')

        self.configuration = HubConfiguration()

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
        self.button_data = Button(self.root, text='Configure Data...', command=self.configure_data)
        self.button_abstraction = Button(self.root, text='Configure Abstraction...', command=self.configure_abstraction)
        self.button_distance = Button(self.root, text='Configure Distance...', command=self.configure_distance)
        self.button_clustering = Button(self.root, text='Configure Clustering...', command=self.configure_clustering)

        self.button_data.configure(width=35, height=2)
        self.button_abstraction.configure(width=35, height=2)
        self.button_distance.configure(width=35, height=2, state="disabled")
        self.button_clustering.configure(width=35, height=2, state="disabled")

        self.button_data.grid(sticky='nwe', row=5, column=1, columnspan=2, padx=10, pady=10)
        self.button_abstraction.grid(sticky='nwe', row=7, column=1, columnspan=2, padx=10, pady=10)
        self.button_distance.grid(sticky='nwe', row=9, column=1, columnspan=2, padx=10, pady=10)
        self.button_clustering.grid(sticky='nwe', row=11, column=1, columnspan=2, padx=10, pady=10)

        self.button_show_result = Button(self.root, text='Show Result...', command=self.show_result, state="disabled",
                                         font=('Sans', '10', 'bold'))

        self.button_show_result.configure(width=20, height=2)

        self.button_show_result.grid(sticky='nswe', row=14, column=1, columnspan=4, padx=10, pady=10)

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

        "progress labels"
        self.label_data_progress = Label(self.root, text=DATA_NOT_CONFIGURED, bg="white", state="disabled")
        self.label_abstraction_progress = Label(self.root, text=ABSTRACTION_NOT_CONFIGURED, bg="white", state="disabled")
        self.label_distance_progress = Label(self.root, text=DISTANCE_NOT_CONFIGURED, bg="white", state="disabled")
        self.label_clustering_progress = Label(self.root, text=CLUSTERING_NOT_CONFIGURED, bg="white", state="disabled")

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

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.root.after(1, lambda: self.root.focus_force())
        self.root.mainloop()

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Closing the window without prior saving the configuration will delete the configuration. Do you want to quit?", icon=WARNING):
            self.root.destroy()

    def configure_data(self):
        self.label_data_progress['text'] = "Data configuration in progress ..."
        self.label_data_progress['fg'] = 'DarkOrange1'
        self.root.update()
        data_name = select_data(self.root)

        if data_name is None:
            self.update()
            self.root.update()
            return

        self.configuration.set_data_configuration(str(Path(__file__).parent.parent) + "\\data\\" + data_name + ".txt")

        self.update()
        self.root.update()

        # TODO: execute only if configuration was changed
        self.label_data_progress['text'] = "Data extraction in progress ..."
        self.label_data_progress['fg'] = 'RoyalBlue1'
        self.root.update()

        self.configuration.execute_data()

        self.update()
        # self.configuration.save_as_json()

    def configure_abstraction(self):
        self.label_abstraction_progress['text'] = "Abstraction configuration in progress ..."
        self.label_abstraction_progress['fg'] = 'DarkOrange1'
        self.root.update()
        # 1. get data from config
        config = self.configuration.get_abstraction_configuration()
        # 2. put data into abstraction gui
        # 3. read from abstraction gui
        abstraction_answers = abstraction_configuration(self.root, self.configuration.data, config)[1]
        if abstraction_answers is None:
            self.update()
            self.root.update()
            return

        # 4. save abstraction into configuration
        self.configuration.set_abstraction_configuration(abstraction_answers)
        # 5. update self
        # 6. initiate execution of abstraction in config

        self.update()
        self.root.update()

        # TODO: execute only if configuration was changed
        self.label_abstraction_progress['text'] = "Abstraction in progress ..."
        self.label_abstraction_progress['fg'] = 'RoyalBlue1'
        self.root.update()

        self.configuration.execute_abstraction()

        self.update()
        # self.configuration.save_as_json()

    def configure_distance(self):
        self.label_distance_progress['text'] = "Distance configuration in progress ..."
        self.label_distance_progress['fg'] = 'DarkOrange1'
        self.root.update()
        cost_map, blob_configuration = self.configuration.get_distance_configuration()
        distance_choice = get_distance_choice(self.root)
        if distance_choice is None:
            self.update()
            self.root.update()
            return

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

        # TODO: execute only if configuration was changed
        self.label_distance_progress['text'] = "Distance calculation in progress ..."
        self.label_distance_progress['fg'] = 'RoyalBlue1'
        self.root.update()

        self.configuration.execute_distance()

        # TODO: show percentage

        self.update()
        # self.configuration.save_as_json()

    def configure_clustering(self):
        self.label_clustering_progress['text'] = "Clustering configuration in progress ..."
        self.label_clustering_progress['fg'] = 'DarkOrange1'
        self.root.update()
        prev_clustering_algorithm, prev_answers = self.configuration.get_clustering_selection()
        prev_parameters = self.configuration.get_clustering_configuration()
        answers, cluster_config_f, clustering_algorithm = cluster_suggest(self.root, prev_answers, prev_clustering_algorithm)
        if clustering_algorithm is None:
            self.update()
            self.root.update()
            return

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

        # TODO: execute only if configuration was changed
        self.label_clustering_progress['text'] = "Clustering in progress ..."
        self.label_clustering_progress['fg'] = 'RoyalBlue1'
        self.root.update()

        self.configuration.execute_clustering()

        # self.update()

        # self.label_clustering_progress['text'] = "Saving in progress ..."
        # self.label_clustering_progress['fg'] = 'RoyalBlue1'
        # self.root.update()
        #
        # self.configuration.save_as_json()
        # self.configuration.save_as_excel()

        self.update()

    def show_result(self):
        # validation_result = result_view(self.root, self.configuration.excel_save_path, self.configuration.num_data, self.configuration.num_abstracted_data, self.configuration.abstraction_rate, self.configuration.no_clusters, self.configuration.no_noise,
        #             self.configuration.timedelta_abstraction, self.configuration.timedelta_distance, self.configuration.timedelta_cluster, self.configuration.timedelta_total,
        #             self.configuration.values_abstracted, self.configuration.distance_matrix_map, self.configuration.clusters_abstracted)
        validation_result = result_view(self.root, self.configuration)
        # TODO: save validation into configuration

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

    def menu_save(self):
        if self.configuration.json_save_path:
            self.configuration.save_as_json()
        else:
            self.menu_saveas()

    def menu_saveas(self):
        self.configuration.json_save_path = getJsonSavePath()
        self.menu_save()


    def update(self):
        if self.configuration.data_configuration_valid():
            # self.data_progress['value'] = 100
            self.label_data_progress['text'] = "Data extraction done"
            self.label_data_progress['fg'] = 'green'
        else:
            # self.data_progress['value'] = 0
            self.label_data_progress['text'] = DATA_NOT_CONFIGURED
            self.label_data_progress['fg'] = 'red'

        if self.configuration.abstraction_configuration_valid():
            # self.abstraction_progress['value'] = 100
            self.label_abstraction_progress['text'] = "Abstraction done"
            self.label_abstraction_progress['fg'] = 'green'
        else:
            # self.abstraction_progress['value'] = 0
            self.label_abstraction_progress['text'] = ABSTRACTION_NOT_CONFIGURED
            self.label_abstraction_progress['fg'] = 'red'

        if self.configuration.distance_configuration_valid():
            # self.distance_progress['value'] = 100
            self.label_distance_progress['text'] = "Distance calculation done"
            self.label_distance_progress['fg'] = 'green'
        else:
            # self.distance_progress['value'] = 0
            self.label_distance_progress['text'] = DISTANCE_NOT_CONFIGURED
            self.label_distance_progress['fg'] = 'red'

        if self.configuration.clustering_configuration_valid():
            # self.clustering_progress['value'] = 100
            self.label_clustering_progress['text'] = "Clustering done"
            self.label_clustering_progress['fg'] = 'green'
        else:
            # self.clustering_progress['value'] = 0
            self.label_clustering_progress['text'] = CLUSTERING_NOT_CONFIGURED
            self.label_clustering_progress['fg'] = 'red'

        if self.configuration.distance_configuration_possible():
            self.button_distance.configure(state="normal")
            self.label_distance_progress.configure(state="normal")
        else:
            self.button_distance.configure(state="disabled")
            self.label_distance_progress.configure(state="disabled")

        if self.configuration.clustering_configuration_possible():
            self.button_clustering.configure(state="normal")
            self.label_clustering_progress.configure(state="normal")
        else:
            self.button_clustering.configure(state="disabled")
            self.label_clustering_progress.configure(state="disabled")

        if self.configuration.execute_possible():
            self.button_show_result.configure(state="normal", bg='pale green')
        else:
            self.button_show_result.configure(state="disabled") #, bg=self.orig_button_color)

        self.update_frame_data()
        self.update_frame_abstraction()
        self.update_frame_distance()
        self.update_frame_clustering()

        self.root.update()

    def update_frame_data(self):

        pass

    def update_frame_abstraction(self):
        pass

    def update_frame_distance(self):
        pass

    def update_frame_clustering(self):
        pass


if __name__ == "__main__":
    Hub()
