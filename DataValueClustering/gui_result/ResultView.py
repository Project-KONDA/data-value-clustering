import os
import subprocess
from tkinter import Tk, StringVar, Label, font, Frame, Button, Toplevel
import numpy as np

from gui_result.result_gui import show_mds_scatter_plot_integrated


def result_view(root, excel_path, num_data, num_abstracted_data, abstraction_rate, no_clusters, no_noise, timedelta_abstraction, timedelta_distance, timedelta_clustering, timedelta_total, values_abstracted, distance_matrix_map, clusters_abstracted):
    r = ResultView(excel_path, num_data, num_abstracted_data, abstraction_rate, no_clusters, no_noise, timedelta_abstraction, timedelta_distance, timedelta_clustering, timedelta_total, values_abstracted, distance_matrix_map, clusters_abstracted)
    return r.get()


class ResultView:

    def __init__(self, master, excel_path, num_data, num_abstracted_data, abstraction_rate, no_clusters, no_noise, timedelta_abstraction, timedelta_distance, timedelta_clustering, timedelta_total, values_abstracted, distance_matrix_map, clusters_abstracted):
        self.root = Toplevel(master)
        self.root.title("Result")

        self.excel_path = excel_path

        self.num_data = num_data
        self.num_abstracted_data = num_abstracted_data
        self.abstraction_rate = abstraction_rate
        self.no_clusters = no_clusters
        self.no_noise = no_noise
        self.timedelta_abstraction = timedelta_abstraction
        self.timedelta_distance = timedelta_distance
        self.timedelta_clustering = timedelta_clustering
        self.timedelta_total = timedelta_total

        self.values_abstracted = values_abstracted
        self.distance_matrix_map = distance_matrix_map
        self.clusters_abstracted = clusters_abstracted

        # summary:
        self.summary_frame = Frame(self.root, padx=10, bg="white", pady=10)
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
        show_mds_scatter_plot_integrated(self.summary_frame, self.values_abstracted, self.distance_matrix_map["distance_matrix"], self.clusters_abstracted)

        # excel button
        self.button = Button(self.summary_frame, text='Open Excel File Showing Clustering', command=self.open_excel,
                             bg='pale green')
        self.button.grid(row=3, column=0, sticky='we', columnspan=1)


        # questionnaire:
        self.questionnaire_frame = Frame(self.root, bg="white")
        self.questionnaire_frame.grid(row=1, column=1, sticky='nwse')

        # caption right side:
        self.questionnaire_caption = StringVar()
        self.questionnaire_caption.set("Validation")
        self.questionnaire_caption_label = Label(self.questionnaire_frame, anchor='w', textvariable=self.questionnaire_caption, text="test",
                                          bg='white',
                                          font=('TkDefaultFont', 14, 'bold'), padx=5)
        self.questionnaire_caption_label.grid(row=0, column=1, sticky='we', columnspan=2)

        self.questions_frame = Frame(self.questionnaire_frame, bg="white")
        self.questions_frame.grid(row=1, column=0, sticky='nw')

        # ...
        # cluster_no: more/less/ok
        # ...

        self.suggestion_frame = Frame(self.questionnaire_frame, bg="white")
        self.suggestion_frame.grid(row=1, column=1, sticky='nw')

        # ...

        # button:
        self.button = Button(self.root, text='Go to Configuration Hub', command=self.close, bg='azure')
        self.button.grid(row=2, column=0, sticky='we', columnspan=3)

        self.root.update_idletasks()
        midx = max(0, self.root.winfo_screenwidth() // 2 - self.root.winfo_reqwidth() // 2)
        midy = max(0, self.root.winfo_screenheight() // 3 - self.root.winfo_reqheight() // 2)
        self.root.geometry(f"+%s+%s" % (midx, midy))

        self.root.after(1, lambda: self.root.focus_force())
        self.root.mainloop()

    def open_excel(self):
        os.system(self.excel_path)
        # os.system('"' + self.excel_path + '"')
        # subprocess.call([self.excel_path])
        # subprocess.run(['open', self.excel_path], check=True)

    def get_info(self):
        s = "Number of Data Values: " + str(self.num_data)
        s += "\nNumber of Abstracted Data Values: " + str(self.num_abstracted_data)
        s += "\nAbstraction Rate: " + str(self.abstraction_rate)
        s += "\n\nNumber of clusters: " + str(self.no_clusters)
        s += "\nNumber of noisy values: " + str(self.no_noise)

        s += "\n\nTime Abstraction: " + str(self.timedelta_abstraction)
        s += "\nTime Distance: " + str(self.timedelta_distance)
        s += "\nTime Clustering: " + str(self.timedelta_clustering)
        s += "\nTime Total: " + str(self.timedelta_total)

        # s += "wb-Index:                " + str(self.wb_index)
        # s += "Calinski-Harabasz Index: " + str(self.calinski_harabasz_index)
        # s += "Dunn Index:              " + str(self.dunn_index)
        return s

    def close(self):
        self.root.quite()
        self.root.destroy()

    def get(self):
        pass


if __name__ == '__main__':
    values_compressed = ["a", "1", "?"]
    distance_matrix = np.array([
        [0, 1, 2],
        [0, 0, 1.5],
        [0, 0, 0]
    ])

    d = {"distance_matrix": distance_matrix,
     "condensed_distance_matrix": None,
     "affinity_matrix": None,
     "min_distance": None,
     "max_distance": None}

    clusters_compressed = [0, 1, 2]
    r = ResultView(Tk(),"..\experiments\exports\study\\1_Attribution_Qualifier.xlsx",0,1,2,3,4,5,6,7,8,values_compressed, d, clusters_compressed)
    # r = ResultView("C:\\Users\Viola^ Wenz\Documents\Repositories\data-value-clustering\DataValueClustering\experiments\exports\study\\1_Attribution_Qualifier.xlsx",0,1,2,3,4,5,6,7,8,values_compressed, distance_matrix, clusters_compressed)