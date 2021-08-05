from tkinter import StringVar, Label, LEFT, OptionMenu, Tk, Menu

import gui_abstraction.abstraction_questions
from gui_general import CreateToolTip
from gui_general.QuestionnaireResultInput import QuestionnaireResultInput
from abstraction.abstraction import *
from gui_general.help_popup_gui import menu_help_abstraction

CAPTION_PART_TWO = " The resulting abstraction from the first 100 data values is shown on the right-hand side."
CAPTION_PART_ONE = "Answer the following questions to configure the abstraction from irrelevant details."

DEFAULT_CONFIG = "Default Configuration"
MANUAL_CONFIG = "Manual Configuration"

def abstraction_configuration(master, data, predefined_answers=None, suggestion=None):
    answers = input_questionnaire_abstraction(master, abstraction_question_array, data, predefined_answers, suggestion)
    if answers is None:
        return None, None
    return get_abstraction_method(answers), answers


def input_questionnaire_abstraction(master, config, data, predefined_answers=None, suggestion=None):
    questionnaire = AbstractionQuestionnaireResultInput(master, config, data, predefined_answers, suggestion)
    questionnaire.run()
    answers = questionnaire.get()
    return answers


class AbstractionQuestionnaireResultInput(QuestionnaireResultInput):
    """ binary questionaire GUI for configuring the abstraction function """

    def __init__(self, master, config, data, predefined_answers=None, suggestion=None):
        self.caption_text = CAPTION_PART_ONE + CAPTION_PART_TWO
        self.hint_text = "Use your domain knowledge to abstract from features that you expect to find frequently in the data values and that do not alter the values’ meaning significantly."
        if suggestion is not None:
            suggestion = "Advice based on the clustering evaluation:" + suggestion
        super().__init__(master, "Abstraction Configuration", config, predefined_answers, 10, suggestion)

        self.root.grid_columnconfigure((0, 1), minsize=self.root.winfo_screenwidth() / 3)

        self.menu = Menu(self.root)
        self.menu.add_command(label="Help", command=lambda: menu_help_abstraction(self.root))
        self.root.config(menu=self.menu)

        self.predefined_abstractions = np.array([
            [MANUAL_CONFIG, list(np.full(len(abstraction_question_array), False))],
            [DEFAULT_CONFIG, self.config[:, 3]],
            ["Maximum Abstraction", max_abstraction_function()[1]],
            ["Duplicate Removal", duplicate_removal_function()[1]],
            ["letters, digits", char_abstraction_function()[1]],
            ["case-sensitive letters, digits", char_abstraction_case_sensitive_function()[1]],
            ["letter sequences and digit sequences", sequence_abstraction_function()[1]],
            ["case-sensitive letter sequences and digit sequences", sequence_abstraction_case_sensitive_function()[1]],
            ["letter sequences, digits", letter_sequence_abstraction_function()[1]],
            ["letters, number sequences", number_sequence_abstraction_function()[1]],
            ["words", word_abstraction_function()[1]],
            ["words and decimal", word_decimal_abstraction_function()[1]],
            ["sentence", word_sequence_abstraction_function()[1]],

            # ["Custom Dictionary", lambda data: custom_dictionary()],
            # ["Custom Full", lambda data: custom_full()]
        ], dtype=object)

        self.label = Label(self.question_frame, text="You can start with one of the following predefined configurations:", bg="white")
        self.label.grid(sticky='nw', row=2, column=0)

        self.predefined_options = list(self.predefined_abstractions[:, 0])
        self.selected_predefined_option = StringVar()
        self.selected_predefined_option.set(DEFAULT_CONFIG)
        self.predefined_option_menu = OptionMenu(self.question_frame, self.selected_predefined_option, *self.predefined_options, command=self.option_changed)
        self.predefined_option_menu.grid(sticky='ne', row=2, column=0, padx=10)

        self.data = data
        self.labels = []
        super().selection_changed()

    def option_changed(self, *args):
        selected_option = self.selected_predefined_option.get()
        answers_of_selected_option = self.predefined_abstractions[np.where(self.predefined_abstractions[:, 0] == selected_option)][:, 1][0]
        self.update_check_buttons(answers_of_selected_option)

    def selection_changed(self):
        super().selection_changed()
        self.selected_predefined_option.set(MANUAL_CONFIG)

    def apply(self):
        if self.data is None:
            self.scrollable_result_frame.destroy()
            self.canvas.destroy()
            self.scrollbar.destroy()
            self.root.grid_columnconfigure((1), minsize=0)
            self.question_caption_label.destroy()

            self.caption_text = CAPTION_PART_ONE

            self.question_caption = StringVar()
            self.question_caption.set(self.caption_text)
            self.question_caption_label = Label(self.root, anchor='c', justify="center",
                                                textvariable=self.question_caption, bg='white',
                                                font=('TkDefaultFont', 12, 'bold'), pady=10)
            self.question_caption_label.grid(row=0, column=0, sticky='nsew', columnspan=2)
            if self.label_suggested is not None:
                self.label_suggested.configure(wraplengt = 800)
            return
        answers = self.get()
        abstraction_f = get_abstraction_method(answers)
        values_abstracted, abstraction_dict = abstraction_f(self.data[0:100])
        for i in range(len(self.labels)):
            self.labels[i].destroy()

        s1 = StringVar()
        s1.set("Abstracted values")
        abstraction_target_label = Label(self.scrollable_result_frame, anchor='nw', textvariable=s1,
                                         bg='lemonchiffon', font=('TkDefaultFont', 10, 'bold', 'underline'), padx=2)
        abstraction_target_label.grid(row=5, column=0, sticky='nwse')
        self.labels.append(abstraction_target_label)

        s2 = StringVar()
        s2.set("Original values")
        abstraction_source_label = Label(self.scrollable_result_frame, anchor='nw', textvariable=s2, bg='ivory',
                                         wraplength=540, justify=LEFT, font=('TkDefaultFont', 10, 'bold', 'underline'), padx=2)  # TODO: calculate wraplength
        abstraction_source_label.grid(row=5, column=1, sticky='nwse')
        self.labels.append(abstraction_source_label)

        for i, key in enumerate(abstraction_dict):
            s1 = StringVar()
            s1.set(key)
            abstraction_target_label = Label(self.scrollable_result_frame, anchor='nw', textvariable=s1,
                                             bg='lemonchiffon')
            CreateToolTip(abstraction_target_label, "Abstracted data value representing all original values shown on the right hand side")
            abstraction_target_label.grid(row=i + 10, column=0, sticky='nwse')
            self.labels.append(abstraction_target_label)
            s2 = StringVar()
            s2.set(str(abstraction_dict[key])[1:len(str(abstraction_dict[key])) - 1])
            abstraction_source_label = Label(self.scrollable_result_frame, anchor='nw', textvariable=s2, bg='ivory',
                                             wraplength=540, justify=LEFT)  # TODO: calculate wraplength
            CreateToolTip(abstraction_source_label, "Original data values represented by the abstracted value shown on the left hand side")
            abstraction_source_label.grid(row=i + 10, column=1, sticky='nwse')
            self.labels.append(abstraction_source_label)


if __name__ == '__main__':
    q_config = np.array(
        # 0              1                 2     3        4         5             6
        # [dependencies, not-dependencies, name, default, question, explanation?, example?]
        [[[], [], "name0", False, "question0?"],
         [[], [], "name1", True, "question1?"],
         [[0], [], "name2", False, "question2?"],
         [[1], [], "name3", True, "question3?"],
         [[], [3], "name4", False, "question4?"],
         [[3], [], "name5", True, "question5?"],
         [[0], [1], "name6", False, "question6?"]],
        dtype=object)

    q_config2 = gui_abstraction.abstraction_questions.abstraction_question_array

    qc = AbstractionQuestionnaireResultInput(Tk(), q_config2,
                                             ["abcLBSDH", "bbbGDGD", "c", "a", "b", "c", "d", "e", "f", "g", "h", "i",
                                              "j",
                                              "k", "l", "m", "n", "o", "p", "q", "r", "a", "b", "c", "a", "b", "c", "a",
                                              "b",
                                              "c", "a", "b", "c", "a", "b", "c", "a", "b", "c", "a", "b", "c", "a", "b",
                                              "c",
                                              "a", "b", "c", "a", "b", "c", "a", "b", "c", "a", "b", "c", "a", "b", "c",
                                              "a",
                                              "b", "c", "?", "3", "1234"], None)
    qc.run()

    result = qc.get()
    print(result)
