import os
from tkinter import Tk, StringVar, Label, Frame, Button, Toplevel, Menu
import numpy as np

from export.path import getExcelSavePath
from gui_center.hub_configuration import HubConfiguration
from gui_general.help_popup_gui import menu_help_result
from gui_result.result_gui import show_mds_scatter_plot_integrated
from gui_result.validation_frames.EnumIntValidationQuestion import create_enum_int_validation_question
from gui_result.validation_frames.EnumValidationQuestion import create_enum_validation_question
from gui_result.validation_questionnaire import question_1_answers, question_2_answers, question_3_answers, \
    question_4_answers, ValidationAnswer, question_2, question_3, question_4, question_1

# def result_view(master, excel_path, num_data, num_abstracted_data, abstraction_rate, no_clusters, no_noise, timedelta_abstraction, timedelta_distance, timedelta_clustering, timedelta_total, values_abstracted, distance_matrix_map, clusters_abstracted):
#     r = ResultView(master, excel_path, num_data, num_abstracted_data, abstraction_rate, no_clusters, no_noise, timedelta_abstraction, timedelta_distance, timedelta_clustering, timedelta_total, values_abstracted, distance_matrix_map, clusters_abstracted)
NOT_SATISFIED = "Based on your answers above, we suggest doing another iteration with a modified configuration.\nPay attention to the advice given in the configuration views in blue text."
SATISFIED = "According to your answers above, you are satisfied with the clustering.\nCongratulations, you are done!"


def result_view(master, configuration):
    res = ResultView(master, configuration)
    return res.get()


class ResultView:

    # def __init__(self, master, excel_path, num_data, num_abstracted_data, abstraction_rate, no_clusters, no_noise, timedelta_abstraction, timedelta_distance, timedelta_clustering, timedelta_total, values_abstracted, distance_matrix_map, clusters_abstracted):
    def __init__(self, master, configuration):
        self.root = Toplevel(master)
        self.root.title("Clustering Result & Evaluation")
        self.root.resizable(False, False)

        self.menu = Menu(self.root)
        self.menu.add_command(label="Help", command=lambda: menu_help_result(self.root))
        self.root.config(menu=self.menu)

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

        self.caption = StringVar()
        self.caption.set("Explore the calculated clustering and perform the clustering evaluation via the questionnaire")
        self.caption = Label(self.root, anchor='c', textvariable=self.caption,
                                           text="test", bg='white',
                                           font=('TkDefaultFont', 12, 'bold'), pady=10)
        self.caption.grid(row=0, column=0, sticky='wesn', columnspan=2)

        # summary:
        self.summary_frame = Frame(self.root, bg="white", padx=10, pady=10, borderwidth=2, relief="groove")
        self.summary_frame.grid(row=1, column=0, sticky='nwse', columnspan=1)

        # # caption left side:
        # self.summary_caption = StringVar()
        # self.summary_caption.set("Clustering Result")
        # self.summary_caption_label = Label(self.summary_frame, anchor='w', textvariable=self.summary_caption,
        #                                    text="test", bg='white',
        #                                    font=('TkDefaultFont', 12, 'bold'), pady=10)
        # self.summary_caption_label.grid(row=0, column=0, sticky='wesn', columnspan=1)

        self.info_frame = Frame(self.summary_frame, bg="white")
        self.info_frame.grid(row=1, column=0, sticky='nwse', columnspan=1)

        # self.info_header_label = Label(self.info_frame, text="Meta-Information", bg='white',
        #                                font=('TkDefaultFont', 12, 'bold'))
        # self.info_header_label.grid(row=0, column=0, sticky='nwes', columnspan=1)

        s = self.get_info()
        self.info_label = Label(self.info_frame, text=s, justify="left", bg='white')
        self.info_label.grid(row=1, column=0, sticky='nwes', columnspan=1)

        # scatter plot in summary_frame
        show_mds_scatter_plot_integrated(self.summary_frame, self.configuration.values_abstracted,
                                         self.configuration.distance_matrix_map["distance_matrix"],
                                         self.configuration.clusters_abstracted)

        # excel button
        self.button = Button(self.summary_frame, text='Open Excel File Showing Clustering', command=self.open_excel,
                             bg='pale green')
        self.button.grid(row=3, column=0, sticky='we', columnspan=1, pady=20)

        # questionnaire:
        self.questionnaire_frame = Frame(self.root, bg="white", padx=10, borderwidth=2, relief="groove")
        self.questionnaire_frame.grid(row=1, column=1, sticky='nwse')

        # # caption right side:
        # self.questionnaire_caption = StringVar()
        # self.questionnaire_caption.set("Clustering Validation")
        # self.questionnaire_caption_label = Label(self.questionnaire_frame, anchor='w',
        #                                          textvariable=self.questionnaire_caption, text="test",
        #                                          bg='white', font=('TkDefaultFont', 12, 'bold'), pady=10)
        # self.questionnaire_caption_label.grid(row=0, column=0, sticky='we', columnspan=2)

        # self.questionnaire_note_label = Label(self.questionnaire_frame, anchor='w', text="After having familiarized yourself with the clustering via the MDS Scatter Plot and the Excel file,\nanswer the following questions to perform the validation of the calculated clustering.", bg='white', justify='left')
        # self.questionnaire_note_label.grid(row=1, column=0, sticky='we', columnspan=2)

        self.questions_frame = Frame(self.questionnaire_frame, bg="white")
        self.questions_frame.grid(row=1, column=0, sticky='nsew')

        self.q1 = create_enum_validation_question(self.questions_frame, question_1, question_1_answers, self.update_suggestion, self.configuration.get_validation_answer_1())
        self.q1.frame.grid(row=0, column=0, sticky='nsew')

        self.q2 = create_enum_validation_question(self.questions_frame, question_2, question_2_answers, self.update_suggestion, self.configuration.get_validation_answer_2())
        self.q2.frame.grid(row=1, column=0, sticky='nsew')

        self.q3 = create_enum_validation_question(self.questions_frame,
                                             question_3, question_3_answers, self.update_suggestion, self.configuration.get_validation_answer_3())
        self.q3.frame.grid(row=2, column=0, sticky='nsew')

        self.q4 = create_enum_int_validation_question(self.questions_frame, question_4, question_4_answers, self.update_suggestion, self.configuration.get_validation_answer_4()[0], (None, self.configuration.get_validation_answer_4()[1]))
        self.q4.frame.grid(row=3, column=0, sticky='nsew')

        self.suggestion_frame = Frame(self.questionnaire_frame, bg="white")
        self.suggestion_frame.grid(row=3, column=0, sticky='nw', columnspan=2)

        self.advice_label = Label(self.suggestion_frame, text="", bg='white',
                                  font=('TkDefaultFont', 12, 'bold'), fg='blue', pady=10, justify='left')
        self.advice_label.grid(row=0, column=0, sticky='nwes', columnspan=1)

        # ...

        # close button:
        self.button = Button(self.root, text='Close', command=self.close, bg='azure')
        self.button.grid(row=2, column=0, sticky='we', columnspan=3)

        self.root.update_idletasks()
        midx = max(0, self.root.winfo_screenwidth() // 2 - self.root.winfo_reqwidth() // 2)
        midy = max(0, self.root.winfo_screenheight() // 3 - self.root.winfo_reqheight() // 2)
        self.root.geometry(f"+%s+%s" % (midx, midy))

        self.root.after(1, lambda: self.root.focus_force())
        self.root.protocol("WM_DELETE_WINDOW", self.cancel)

        self.update_suggestion()
        self.root.mainloop()

    def update_suggestion(self):
        if self.q1.get_result() is None and self.q2.get_result() is None and self.q3.get_result() is None and \
                self.q4.get_result()[0] is None:
            self.advice_label.config(text="", fg="blue")
        elif (self.q1.get_result() == ValidationAnswer.HAPPY or self.q1.get_result() is None) \
                and (self.q2.get_result() == ValidationAnswer.HAPPY or self.q2.get_result() is None) \
                and (self.q3.get_result() == ValidationAnswer.HAPPY or self.q3.get_result() is None)\
                and (self.q4.get_result()[0] == ValidationAnswer.HAPPY or self.q4.get_result()[0] is None):
            self.advice_label.config(text=SATISFIED, fg="green")
        else:
            self.advice_label.config(text=NOT_SATISFIED, fg="red")


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
        if self.answers_valid():
            self.root.quit()
            self.root.destroy()
        else:
            self.canceled = False

    def answers_valid(self):
        q4_result = self.q4.get_result()
        if q4_result[0] == ValidationAnswer.UNHAPPY:
            return q4_result[1] is not None and len(q4_result[1]) > 0
        return True

    def cancel(self):
        self.canceled = True
        self.close()

    def get(self):
        if self.canceled:
            return
        self.configuration.set_validation_answer_1(self.q1.get_result())
        self.configuration.set_validation_answer_2(self.q2.get_result())
        self.configuration.set_validation_answer_3(self.q3.get_result())
        self.configuration.set_validation_answer_4(self.q4.get_result())


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
