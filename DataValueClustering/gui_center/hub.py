from tkinter import Tk, Button, Label, Frame
from pathlib import Path


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

        self.button_path.configure(width=20, height=2)
        self.button_data.configure(width=20, height=2, state="disabled")
        self.button_abstraction.configure(width=20, height=2, state="disabled")
        self.button_distance.configure(width=20, height=2, state="disabled")
        self.button_clustering.configure(width=20, height=2, state="disabled")

        self.button_load.grid(sticky='ne', row=1, column=4, columnspan=1, padx=10, pady=10)
        self.button_save.grid(sticky='nw', row=1, column=1, columnspan=1, padx=10, pady=10)
        self.button_path.grid(sticky='we', row=2, column=1, columnspan=2, padx=10, pady=10)
        self.button_data.grid(sticky='we', row=3, column=1, columnspan=2, padx=10, pady=10)
        self.button_abstraction.grid(sticky='we', row=4, column=1, columnspan=2, padx=10, pady=10)
        self.button_distance.grid(sticky='we', row=5, column=1, columnspan=2, padx=10, pady=10)
        self.button_clustering.grid(sticky='we', row=6, column=1, columnspan=2, padx=10, pady=10)

        self.button_show_result = Button(self.root, text='Show Result...', command=self.show_result, state="disabled", font = ('Sans','10','bold'))
        # self.button_save = Button(self.root, text='Save', command=self.save)

        self.button_show_result.configure(width=20, height=2)

        self.button_show_result.grid(sticky='nswe', row=7, column=1, columnspan=4, padx=10, pady=10)
        # self.button_save.grid(sticky='nswe', row=6, column=2, columnspan=1)

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

        self.frame_path.grid(sticky='nswe', row=2, column=3, columnspan=2, padx=10, pady=10)
        self.frame_data.grid(sticky='nswe', row=3, column=3, columnspan=2, padx=10, pady=10)
        self.frame_abstraction.grid(sticky='nswe', row=4, column=3, columnspan=2, padx=10, pady=10)
        self.frame_distance.grid(sticky='nswe', row=5, column=3, columnspan=2, padx=10, pady=10)
        self.frame_clustering.grid(sticky='nswe', row=6, column=3, columnspan=2, padx=10, pady=10)

        # self.frame_config = Frame(self.root, bg="grey90", width=200, height=200)  # pass this frame as root
        # self.frame_config.configure(highlightbackground="grey", highlightthickness=1)
        # self.frame_config.grid(sticky='nswe', row=1, column=5, columnspan=2, rowspan=4)



        self.root.after(1, lambda: self.root.focus_force())
        self.root.mainloop()

    def configure_path(self):
        self.configuration.json_save_path = getJsonSavePath(self.configuration.json_save_path)
        self.configuration.excel_save_path = self.configuration.json_save_path[0:len(self.configuration.json_save_path)-len(".json")] + ".xlsx"
        # if not save_path: return
        # print("saving to " + save_path + " ...")
        # self.configuration.save(save_path)

        self.update()
        # self.configuration.save_as_json()

    def configure_data(self):
        data_name = select_data(self.root)
        self.configuration.set_data_configuration(str(Path(__file__).parent.parent) + "\\data\\" + data_name + ".txt")

        self.configuration.execute_data()

        self.update()
        # self.configuration.save_as_json()

    def configure_abstraction(self):
        # 1. get data from config
        config = self.configuration.get_abstraction_configuration()
        # 2. put data into abstraction gui
        # 3. read from abstraction gui
        abstraction_answers = abstraction_configuration(self.root, self.configuration.data, config)[1]
        # 4. save abstraction into configuration
        self.configuration.set_abstraction_configuration(abstraction_answers)
        # 5. update self
        # 6. initiate execution of abstraction in config
        self.configuration.execute_abstraction()

        self.update()
        # self.configuration.save_as_json()

    def configure_distance(self):
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
                # TODO: warn user that cost map will be reset if previously specified with other view
                blob_configuration = self.configuration.create_blob_configuration()
            cost_map, blob_configuration = input_blobs(self.root, blob_configuration)
        elif distance_choice == DistanceView.MATRIX:
            if cost_map is None:
                blob_configuration = self.configuration.create_blob_configuration()
                cost_map = input_costmap(self.root, regexes=list(blob_configuration[1:,1]))
            else:
                cost_map = input_costmap(self.root, costmap=cost_map)
            blob_configuration = None
        self.configuration.set_distance_configuration(cost_map, blob_configuration)
        self.configuration.execute_distance()
        # TODO: show percentage

        self.update()
        # self.configuration.save_as_json()

    def configure_clustering(self):
        clustering_algorithm, answers = self.configuration.get_clustering_selection()
        parameters = self.configuration.get_clustering_configuration()
        answers, cluster_config_f, clustering_algorithm = cluster_suggest(self.root, answers, clustering_algorithm)
        self.configuration.set_clustering_selection(clustering_algorithm, answers)
        parameters = cluster_config_f(self.root, answers, self.configuration.distance_matrix_map, self.configuration.values_abstracted, parameters)  # TODO: pass self.root
        self.configuration.set_clustering_configuration(parameters)
        self.configuration.execute_clustering()

        self.update()
        self.configuration.save_as_json()
        self.configuration.save_as_excel()

    def show_result(self):
        validation_result = result_view(self.root, self.configuration.excel_save_path, self.configuration.num_data, self.configuration.num_abstracted_data, self.configuration.abstraction_rate, self.configuration.no_clusters, self.configuration.no_noise,
                    self.configuration.timedelta_abstraction, self.configuration.timedelta_distance, self.configuration.timedelta_cluster, self.configuration.timedelta_total,
                    self.configuration.values_abstracted, self.configuration.distance_matrix_map, self.configuration.clusters_abstracted)
        # TODO: save validation into configuration

        self.update()

    def load(self):
        load_path = getJsonLoadPath(self.configuration.json_save_path)
        if not load_path: return
        print("loading from " + load_path + " ...")
        self.configuration = load_hub_configuration(load_path)
        self.update()

    def save(self):
        self.configuration.save_as_json()

    def update(self):
        if self.configuration.saving_possible():
            self.button_save.configure(state="normal")
        else:
            self.button_save.configure(state="disabled")

        if self.configuration.data_configuration_possible():
            self.button_data.configure(state="normal")
        else:
            self.button_data.configure(state="disabled")

        if self.configuration.abstraction_configuration_possible():
            self.button_abstraction.configure(state="normal")
        else:
            self.button_abstraction.configure(state="disabled")

        if self.configuration.distance_configuration_possible():
            self.button_distance.configure(state="normal")
        else:
            self.button_distance.configure(state="disabled")

        if self.configuration.clustering_configuration_possible():
            self.button_clustering.configure(state="normal")
        else:
            self.button_clustering.configure(state="disabled")

        if self.configuration.execute_possible():
            self.button_show_result.configure(state="normal", bg='pale green')
        else:
            self.button_show_result.configure(state="disabled")

        self.update_frame_data()
        self.update_frame_abstraction()
        self.update_frame_distance()
        self.update_frame_clustering()

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
