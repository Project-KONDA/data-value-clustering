import os
import subprocess
from enum import Enum
from tkinter import Tk, StringVar, Label, font, Frame, Button, Toplevel
import numpy as np

from export.path import getExcelSavePath
from gui_center.hub_configuration import HubConfiguration
from gui_result.result_gui import show_mds_scatter_plot_integrated
from gui_result.validation_frames.EnumIntValidationQuestion import create_enum_int_validation_question
from gui_result.validation_frames.EnumValidationQuestion import create_enum_validation_question


class ValidationAnswer(Enum):
    HAPPY = 1
    UNHAPPY = 2
    MORE = 3
    LESS = 4

# def result_view(master, excel_path, num_data, num_abstracted_data, abstraction_rate, no_clusters, no_noise, timedelta_abstraction, timedelta_distance, timedelta_clustering, timedelta_total, values_abstracted, distance_matrix_map, clusters_abstracted):
#     r = ResultView(master, excel_path, num_data, num_abstracted_data, abstraction_rate, no_clusters, no_noise, timedelta_abstraction, timedelta_distance, timedelta_clustering, timedelta_total, values_abstracted, distance_matrix_map, clusters_abstracted)
def result_view(master, configuration):
    res = ResultView(master, configuration)
    return res.get()

class ResultView:

    # def __init__(self, master, excel_path, num_data, num_abstracted_data, abstraction_rate, no_clusters, no_noise, timedelta_abstraction, timedelta_distance, timedelta_clustering, timedelta_total, values_abstracted, distance_matrix_map, clusters_abstracted):
    def __init__(self, master, configuration):
        self.root = Toplevel(master)
        self.root.title("Result")

        self.canceled = False

        self.configuration = configuration

        # self.excel_path = excel_path
        # self.num_data = num_data
        # self.num_abstracted_data = num_abstracted_data
        # self.abstraction_rate = abstraction_rate
        # self.no_clusters = no_clusters
        # self.no_noise = no_noise
        # self.timedelta_abstraction = timedelta_abstraction
        # self.timedelta_distance = timedelta_distance
        # self.timedelta_clustering = timedelta_clustering
        # self.timedelta_total = timedelta_total
        # self.values_abstracted = values_abstracted
        # self.distance_matrix_map = distance_matrix_map
        # self.clusters_abstracted = clusters_abstracted

        # summary:
        self.summary_frame = Frame(self.root, bg="white", padx=10, pady=10)
        self.summary_frame.grid(row=1, column=0, sticky='nwse', columnspan=1)

        # caption left side:
        self.summary_caption = StringVar()
        self.summary_caption.set("Result")
        self.summary_caption_label = Label(self.summary_frame, anchor='w', textvariable=self.summary_caption, text="test", bg='white',
                                            font=('TkDefaultFont', 14, 'bold'), padx=5)
        self.summary_caption_label.grid(row=0, column=0, sticky='wesn', columnspan=1)

        self.info_frame = Frame(self.summary_frame, bg="white", borderwidth=2, relief="sunken")
        self.info_frame.grid(row=1, column=0, sticky='nwse', columnspan=1)

        self.info_header_label = Label(self.info_frame, text="Meta-Information", bg='white', font=('TkDefaultFont', 12, 'bold'))
        self.info_header_label.grid(row=0, column=0, sticky='nwes', columnspan=1)

        s = self.get_info()
        self.info_label = Label(self.info_frame, text=s, justify="left", bg='white')
        self.info_label.grid(row=1, column=0, sticky='nwes', columnspan=1)

        # scatter plot in summary_frame
        show_mds_scatter_plot_integrated(self.summary_frame, self.configuration.values_abstracted, self.configuration.distance_matrix_map["distance_matrix"], self.configuration.clusters_abstracted)

        # excel button
        self.button = Button(self.summary_frame, text='Open Excel File Showing Clustering', command=self.open_excel,
                             bg='pale green')
        self.button.grid(row=3, column=0, sticky='we', columnspan=1)


        # questionnaire:
        self.questionnaire_frame = Frame(self.root, bg="white", padx=10, pady=10)
        self.questionnaire_frame.grid(row=1, column=1, sticky='nwse')

        # caption right side:
        self.questionnaire_caption = StringVar()
        self.questionnaire_caption.set("Validation")
        self.questionnaire_caption_label = Label(self.questionnaire_frame, anchor='w', textvariable=self.questionnaire_caption, text="test",
                                          bg='white',
                                          font=('TkDefaultFont', 14, 'bold'), padx=5)
        self.questionnaire_caption_label.grid(row=0, column=0, sticky='we', columnspan=2)

        self.questions_frame = Frame(self.questionnaire_frame, bg="white")
        self.questions_frame.grid(row=1, column=0, sticky='nsew')

        a1 = np.array([[ValidationAnswer.HAPPY, "I'm happy", "happy tip"],
                        [ValidationAnswer.UNHAPPY,"I’m not happy, a lot of values that seem pretty similar are in "
                                                  "different clusters and a lot of values that seem pretty "
                                                  "dissimilar are in the same cluster", "unhappy tip"]], dtype=object)
        q1 = create_enum_validation_question(self.questions_frame, "How do you feel about the meaningfulness of the "
                                                                     "clustering concerning the grouping of similar "
                                                                     "values in the same cluster?",
                                               "explanation", a1)
        q1.frame.grid(row=0, column=0, sticky='nsew')

        a2 = np.array([[ValidationAnswer.HAPPY, "I'm happy", "happy tip"],
                       [ValidationAnswer.MORE, "More noise please", "more tip"],
                       [ValidationAnswer.LESS, "Less noise please", "less tip"]], dtype=object)
        q2 = create_enum_validation_question(self.questions_frame, "How do you feel about the number of noisy values?", "explanation", a2)
        q2.frame.grid(row=1, column=0, sticky='nsew')

        a3 = np.array([[ValidationAnswer.HAPPY, "I'm happy", "happy tip"],
                       [ValidationAnswer.MORE, "More clusters please", "more tip"],
                       [ValidationAnswer.LESS, "Less clusters please", "less tip"]], dtype=object)
        q3 = create_enum_validation_question(self.questions_frame, "How do you feel about the overall level of detail of the clustering?", "explanation", a3)
        q3.frame.grid(row=2, column=0, sticky='nsew')

        a4 = np.array([[ValidationAnswer.HAPPY, "I'm happy", "happy tip", False],
                        [ValidationAnswer.UNHAPPY, "I'm unhappy, the following clusters are too heterogeneous:", "unhappy tip", True]], dtype=object)
        q4 = create_enum_int_validation_question(self.questions_frame, "Do you consider individual clusters too "
                                                                         "heterogeneous (i.e., level of detail too "
                                                                         "low) while the others are fine?",
                                                   "explanation", a4)
        q4.frame.grid(row=3, column=0, sticky='nsew')

        self.suggestion_frame = Frame(self.questionnaire_frame, bg="white")
        self.suggestion_frame.grid(row=1, column=1, sticky='nw')

        # ...

        # button:
        self.button = Button(self.root, text='Close', command=self.close, bg='azure')
        self.button.grid(row=2, column=0, sticky='we', columnspan=3)

        self.root.update_idletasks()
        midx = max(0, self.root.winfo_screenwidth() // 2 - self.root.winfo_reqwidth() // 2)
        midy = max(0, self.root.winfo_screenheight() // 3 - self.root.winfo_reqheight() // 2)
        self.root.geometry(f"+%s+%s" % (midx, midy))

        self.root.after(1, lambda: self.root.focus_force())
        self.root.protocol("WM_DELETE_WINDOW", self.cancel)

        self.root.mainloop()

    def open_excel(self):
        if self.configuration.excel_save_path is None:
            self.configuration.excel_save_path = getExcelSavePath()
            self.configuration.save_as_excel()
        if self.configuration.excel_save_path:
            # os.system(self.excel_path)
            os.system('"' + self.configuration.excel_save_path + '"')
            # subprocess.call([self.excel_path])
            # subprocess.run(['open', self.excel_path], check=True)

    def get_info(self):
        s = "Number of Data Values: " + str(self.configuration.num_data)
        s += "\nNumber of Abstracted Data Values: " + str(self.configuration.num_abstracted_data)
        s += "\nAbstraction Rate: " + str(self.configuration.abstraction_rate)
        s += "\n\nNumber of clusters: " + str(self.configuration.no_clusters)
        s += "\nNumber of noisy values: " + str(self.configuration.no_noise)

        s += "\n\nTime Abstraction: " + str(self.configuration.timedelta_abstraction)
        s += "\nTime Distance: " + str(self.configuration.timedelta_distance)
        s += "\nTime Clustering: " + str(self.configuration.timedelta_cluster)
        s += "\nTime Total: " + str(self.configuration.timedelta_total)

        # s += "wb-Index:                " + str(self.wb_index)
        # s += "Calinski-Harabasz Index: " + str(self.calinski_harabasz_index)
        # s += "Dunn Index:              " + str(self.dunn_index)
        return s

    def close(self):
        self.root.quit()
        self.root.destroy()

    def cancel(self):
        self.canceled = True
        self.close()

    def get(self):
        pass


if __name__ == '__main__':

    config = HubConfiguration()

    config.excel_path = "..\experiments\exports\study\\1_Attribution_Qualifier.xlsx"
    config.num_data = 0
    config.num_abstracted_data = 1
    config.abstraction_rate = 2
    config.no_clusters = 3
    config.no_noise = 4
    config.timedelta_abstraction = 5
    config.timedelta_distance = 6
    config.timedelta_clustering = 7
    config.timedelta_total = 8
    config.values_abstracted = ["a", "1", "?"]
    distance_matrix = np.array([
        [0, 1, 2],
        [0, 0, 1.5],
        [0, 0, 0]
    ])
    config.distance_matrix_map = {"distance_matrix": distance_matrix,
                                  "condensed_distance_matrix": None,
                                  "affinity_matrix": None,
                                  "min_distance": None,
                                  "max_distance": None}
    config.clusters_abstracted = [0, 1, 2]

    r = ResultView(Tk(), config)
