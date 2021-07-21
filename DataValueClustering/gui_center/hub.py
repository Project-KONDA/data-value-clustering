from tkinter import Tk, Button, Label, Frame, messagebox, HORIZONTAL, ttk
from pathlib import Path
from tkinter.messagebox import WARNING
from tkinter.ttk import Progressbar

from export.path import getJsonSavePath, getJsonLoadPath
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

        "buttons"
        self.button_load = Button(self.root, text='Load Configuration...', command=self.load)
        self.button_save = Button(self.root, text='Save Configuration', command=self.save, state="disabled")
        self.button_path = Button(self.root, text='Configure Save Path...', command=self.configure_path)
        self.button_data = Button(self.root, text='Configure Data...', command=self.configure_data)
        self.button_abstraction = Button(self.root, text='Configure Abstraction...', command=self.configure_abstraction)
        self.button_distance = Button(self.root, text='Configure Distance...', command=self.configure_distance)
        self.button_clustering = Button(self.root, text='Configure Clustering...', command=self.configure_clustering)

        self.orig_button_color = self.button_load.cget("background")

        self.button_path.configure(width=20, height=2)
        self.button_data.configure(width=20, height=2, state="disabled")
        self.button_abstraction.configure(width=20, height=2, state="disabled")
        self.button_distance.configure(width=20, height=2, state="disabled")
        self.button_clustering.configure(width=20, height=2, state="disabled")

        self.button_load.grid(sticky='ne', row=1, column=4, columnspan=1, padx=10, pady=10)
        self.button_save.grid(sticky='nw', row=1, column=1, columnspan=1, padx=10, pady=10)
        self.button_path.grid(sticky='nwe', row=3, column=1, columnspan=2, padx=10, pady=10)
        self.button_data.grid(sticky='nwe', row=5, column=1, columnspan=2, padx=10, pady=10)
        self.button_abstraction.grid(sticky='nwe', row=7, column=1, columnspan=2, padx=10, pady=10)
        self.button_distance.grid(sticky='nwe', row=9, column=1, columnspan=2, padx=10, pady=10)
        self.button_clustering.grid(sticky='nwe', row=11, column=1, columnspan=2, padx=10, pady=10)

        self.button_show_result = Button(self.root, text='Show Result...', command=self.show_result, state="disabled", font = ('Sans','10','bold'))
        # self.button_save = Button(self.root, text='Save', command=self.save)

        self.button_show_result.configure(width=20, height=2)

        self.button_show_result.grid(sticky='nswe', row=14, column=1, columnspan=4, padx=10, pady=10)
        # self.button_save.grid(sticky='nswe', row=6, column=2, columnspan=1)

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
        self.label_path_progress = Label(self.root, text=PATH_NOT_CONFIGURED, bg="white", fg='red')
        self.label_data_progress = Label(self.root, text=DATA_NOT_CONFIGURED, bg="white", state="disabled")
        self.label_abstraction_progress = Label(self.root, text=ABSTRACTION_NOT_CONFIGURED, bg="white", state="disabled")
        self.label_distance_progress = Label(self.root, text=DISTANCE_NOT_CONFIGURED, bg="white", state="disabled")
        self.label_clustering_progress = Label(self.root, text=CLUSTERING_NOT_CONFIGURED, bg="white", state="disabled")

        self.label_path_progress.grid(sticky='nw', row=4, column=1, columnspan=1, padx=20, pady=10)
        self.label_data_progress.grid(sticky='nw', row=6, column=1, columnspan=1, padx=20, pady=10)
        self.label_abstraction_progress.grid(sticky='nw', row=8, column=1, columnspan=1, padx=20, pady=10)
        self.label_distance_progress.grid(sticky='nw', row=10, column=1, columnspan=1, padx=20, pady=10)
        self.label_clustering_progress.grid(sticky='nw', row=12, column=1, columnspan=1, padx=20, pady=10)


        "frames"
        self.frame_path = Frame(self.root, bg="grey90", width=200, height=100)
        self.frame_data = Frame(self.root, bg="grey90", width=200, height=100)
        self.frame_abstraction = Frame(self.root, bg="grey90", width=200, height=100)
        self.frame_distance = Frame(self.root, bg="grey90", width=200, height=100)
        self.frame_clustering = Frame(self.root, bg="grey90", width=200, height=100)

        self.frame_path.configure(highlightbackground="grey", highlightthickness=1)
        self.frame_data.configure(highlightbackground="grey", highlightthickness=1)
        self.frame_abstraction.configure(highlightbackground="grey", highlightthickness=1)
        self.frame_distance.configure(highlightbackground="grey", highlightthickness=1)
        self.frame_clustering.configure(highlightbackground="grey", highlightthickness=1)

        self.frame_path.grid(sticky='nswe', row=3, column=3, rowspan=2, columnspan=2, padx=10, pady=10)
        self.frame_data.grid(sticky='nswe', row=5, column=3, rowspan=2, columnspan=2, padx=10, pady=10)
        self.frame_abstraction.grid(sticky='nswe', row=7, column=3, rowspan=2, columnspan=2, padx=10, pady=10)
        self.frame_distance.grid(sticky='nswe', row=9, column=3, rowspan=2, columnspan=2, padx=10, pady=10)
        self.frame_clustering.grid(sticky='nswe', row=11, column=3, rowspan=2, columnspan=2, padx=10, pady=10)

        # self.frame_config = Frame(self.root, bg="grey90", width=200, height=200)  # pass this frame as root
        # self.frame_config.configure(highlightbackground="grey", highlightthickness=1)
        # self.frame_config.grid(sticky='nswe', row=1, column=5, columnspan=2, rowspan=4)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.root.after(1, lambda: self.root.focus_force())
        self.root.mainloop()

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Closing the window without prior saving the configuration will delete the configuration. Do you want to quit?", icon=WARNING):
            self.root.destroy()

    def configure_path(self):
        self.label_path_progress['text'] = "Path configuration in progress ..."
        self.label_path_progress['fg'] = 'DarkOrange1'
        self.root.update()
        self.configuration.json_save_path = getJsonSavePath(self.configuration.json_save_path)
        self.configuration.excel_save_path = self.configuration.json_save_path[0:len(self.configuration.json_save_path)-len(".json")] + ".xlsx"
        # if not save_path: return
        # print("saving to " + save_path + " ...")
        # self.configuration.save(save_path)

        self.update()
        # self.configuration.save_as_json()

    def configure_data(self):
        self.label_data_progress['text'] = "Data configuration in progress ..."
        self.label_data_progress['fg'] = 'DarkOrange1'
        self.root.update()
        data_name = select_data(self.root)
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
        clustering_algorithm, answers = self.configuration.get_clustering_selection()
        parameters = self.configuration.get_clustering_configuration()
        answers, cluster_config_f, clustering_algorithm = cluster_suggest(self.root, answers, clustering_algorithm)
        self.configuration.set_clustering_selection(clustering_algorithm, answers)
        parameters = cluster_config_f(self.root, answers, self.configuration.distance_matrix_map, self.configuration.values_abstracted, parameters)  # TODO: pass self.root
        self.configuration.set_clustering_configuration(parameters)

        self.update()
        self.root.update()

        # TODO: execute only if configuration was changed
        self.label_clustering_progress['text'] = "Clustering in progress ..."
        self.label_clustering_progress['fg'] = 'RoyalBlue1'
        self.root.update()

        self.configuration.execute_clustering()

        # self.update()

        self.label_clustering_progress['text'] = "Saving in progress ..."
        self.label_clustering_progress['fg'] = 'RoyalBlue1'
        self.root.update()

        self.configuration.save_as_json()
        self.configuration.save_as_excel()

        self.update()

    def show_result(self):
        validation_result = result_view(self.root, self.configuration.excel_save_path, self.configuration.num_data, self.configuration.num_abstracted_data, self.configuration.abstraction_rate, self.configuration.no_clusters, self.configuration.no_noise,
                    self.configuration.timedelta_abstraction, self.configuration.timedelta_distance, self.configuration.timedelta_cluster, self.configuration.timedelta_total,
                    self.configuration.values_abstracted, self.configuration.distance_matrix_map, self.configuration.clusters_abstracted)
        # TODO: save validation into configuration

        self.update()

    # def abstraction_callback(self, percentage):
    #     self.abstraction_progress['value'] = percentage
    #     self.root.update()

    # def distance_callback(self, percentage):
    #     self.distance_progress['value'] = percentage
    #     self.root.update()

    def load(self):
        load_path = getJsonLoadPath(self.configuration.json_save_path)
        if not load_path: return
        print("loading from " + load_path + " ...")
        self.configuration = load_hub_configuration(load_path)
        self.update()

    def save(self):
        self.configuration.save_as_json()

    def update(self):
        if self.configuration.path_configuration_valid():
            # self.path_progress['value'] = 100
            self.label_path_progress['text'] = "Path saving done"
            self.label_path_progress['fg'] = 'green'
        else:
            # self.path_progress['value'] = 0
            self.label_path_progress['text'] = PATH_NOT_CONFIGURED
            self.label_path_progress['fg'] = 'red'

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
            self.label_distance_progress['text'] = CLUSTERING_NOT_CONFIGURED
            self.label_clustering_progress['fg'] = 'red'


        if self.configuration.saving_possible():
            self.button_save.configure(state="normal")
        else:
            self.button_save.configure(state="disabled")

        if self.configuration.data_configuration_possible():
            self.button_data.configure(state="normal")
            self.label_data_progress.configure(state="normal")
        else:
            self.button_data.configure(state="disabled")
            self.label_data_progress.configure(state="disabled")

        if self.configuration.abstraction_configuration_possible():
            self.button_abstraction.configure(state="normal")
            self.label_abstraction_progress.configure(state="normal")
        else:
            self.button_abstraction.configure(state="disabled")
            self.label_abstraction_progress.configure(state="disabled")

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
            self.button_show_result.configure(state="disabled", bg=self.orig_button_color)

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
