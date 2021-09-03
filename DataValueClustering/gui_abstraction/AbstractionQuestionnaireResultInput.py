from tkinter import StringVar, Label, LEFT, OptionMenu, Tk, Menu, Button, Canvas, CENTER

import gui_abstraction.abstraction_questions
from gui_general import CreateToolTip
from gui_general.QuestionnaireResultInput import QuestionnaireResultInput
from abstraction.abstraction import *
from gui_general.help_popup_gui import menu_help_abstraction

SHOW = "▼     Preview     ▼"
HIDE = "▲     Preview     ▲"

# CAPTION_PART_TWO = " The resulting abstraction from the first 100 data values is shown on the right-hand side."
CAPTION_PART_ONE = "Answer the following questions to configure the abstraction from irrelevant details"

DEFAULT_CONFIG = "Letters & Digits (Default)"
MANUAL_CONFIG = "Custom Configuration"

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
        self.caption_text = CAPTION_PART_ONE
        self.hint_text = "Use your domain knowledge to abstract from features that you expect to find frequently in the data values\nand that do not alter the values’ meaning significantly.\nA preview of the simple clustering achieved through the abstraction is shown on demand."
        if suggestion is not None:
            suggestion = "Advice based on the clustering evaluation:" + suggestion
        super().__init__(master, "Abstraction Configuration", config, predefined_answers, 10, suggestion)

        # self.root.grid_columnconfigure((0, 1), minsize=self.root.winfo_screenwidth() / 3)

        self.menu = Menu(self.root)
        self.menu.add_command(label="Help", command=lambda: menu_help_abstraction(self.root))
        self.root.config(menu=self.menu)

        self.predefined_abstractions = np.array([
            [MANUAL_CONFIG, list(np.full(len(abstraction_question_array), False))],
            # [DEFAULT_CONFIG, self.config[:, 3]],
            ["Duplicate Removal", duplicate_removal_function()[1]],
            ["Case-Sensitive Letters & Digits", char_abstraction_case_sensitive_function()[1]],
            [DEFAULT_CONFIG, char_abstraction_function()[1]],
            ["Letter Sequences & Digits", letter_sequence_abstraction_function()[1]],
            ["Letters & Digit Sequences", number_sequence_abstraction_function()[1]],
            ["Case-Sensitive Letter Sequences & Digit Sequences", sequence_abstraction_case_sensitive_function()[1]],
            ["Letter Sequences & Digit Sequences", sequence_abstraction_function()[1]],
            ["Words & Digit Sequences", word_abstraction_function()[1]],
            ["Words & Decimals", word_decimal_abstraction_function()[1]],
            ["Sentences & Digit Sequences", word_sequence_abstraction_function()[1]],
            ["Maximum Abstraction", max_abstraction_function()[1]],

            # ["Custom Dictionary", lambda data: custom_dictionary()],
            # ["Custom Full", lambda data: custom_full()]
        ], dtype=object)

        self.label = Label(self.scrollable_questions_frame, text="You can start with one of the following predefined configurations:", bg="white")
        self.label.grid(sticky='nw', row=2, column=0)

        self.predefined_options = list(self.predefined_abstractions[:, 0])
        self.selected_predefined_option = StringVar()
        self.selected_predefined_option.set(DEFAULT_CONFIG)
        self.predefined_option_menu = OptionMenu(self.scrollable_questions_frame, self.selected_predefined_option, *self.predefined_options, command=self.option_changed)
        self.predefined_option_menu.grid(sticky='ne', row=2, column=0, padx=10)

        def canvas_preview_button_press(arg, press):
            if press:
                arg.widget.configure(relief="raised")
                self.canvas_preview_button.delete('all')
                if self.preview_shown:
                    self.canvas_preview_button.create_text((4, 50), angle="90", anchor="ne", text=SHOW, fill="SystemButtonText")
                    self.hide_preview()
                else:
                    self.canvas_preview_button.create_text((4, 50), angle="90", anchor="ne", text=HIDE, fill="SystemButtonText")
                    self.show_preview()
                self.preview_shown = not self.preview_shown
            else:
                arg.widget.configure(relief="sunken")

        self.canvas_preview_button = Canvas(self.root, width=14, background="SystemButtonFace", borderwidth=2, relief="raised")
        self.canvas_preview_button.grid(row=3, column=1, sticky='ns', pady=5, padx=1)
        self.canvas_preview_button.create_text((4, 50), angle="90", anchor="ne", text=SHOW, fill="SystemButtonText")

        self.canvas_preview_button.bind("<ButtonPress-1>", lambda ev: canvas_preview_button_press(ev, True))
        self.canvas_preview_button.bind("<ButtonRelease-1>", lambda ev: canvas_preview_button_press(ev, False))

        # CreateToolTip(self.button_show_hide, "Show/hide abstraction preview")

        self.data = data
        self.labels = []
        self.preview_shown = False
        super().selection_changed()
        if self.data is not None:
            self.hide_preview()

    def option_changed(self, *args):
        selected_option = self.selected_predefined_option.get()
        answers_of_selected_option = self.predefined_abstractions[np.where(self.predefined_abstractions[:, 0] == selected_option)][:, 1][0]
        self.update_check_buttons(answers_of_selected_option)

    def selection_changed(self):
        super().selection_changed()
        self.selected_predefined_option.set(MANUAL_CONFIG)

    def apply(self):
        if self.data is None:
            self.destroy_preview()
            return

        answers = self.get()
        abstraction_f = get_abstraction_method(answers)
        values_abstracted, abstraction_dict = abstraction_f(self.data[0:100])
        for i in range(len(self.labels)):
            self.labels[i].destroy()

        self.canvas_result.yview_moveto(0)

        self.w = self.root.winfo_screenwidth() / 2
        wrap_right = 1/3 * self.w

        abstraction_source_label = Label(self.scrollable_result_frame, anchor='c', text="Preview of Simple Clustering", bg='lemonchiffon',
                                         wraplength=wrap_right, justify=CENTER, font=('TkDefaultFont', 10, 'bold', 'underline'), padx=2)
        abstraction_source_label.grid(row=5, column=0, sticky='nwse', pady=(0,4))
        self.labels.append(abstraction_source_label)

        abstraction_source_explanation_label = Label(self.scrollable_result_frame, anchor='c', text="The application of the configured abstraction to the first 100 orginal data values resulted in " + str(len(abstraction_dict)) + " cluster" + ("s" if len(abstraction_dict) > 1 else "") + ".",
                                         bg='lemonchiffon', wraplength=wrap_right, justify=CENTER, padx=2)
        abstraction_source_explanation_label.grid(row=6, column=0, sticky='nwse', pady=(0, 4))
        self.labels.append(abstraction_source_explanation_label)

        delta = 7

        for i, key in enumerate(abstraction_dict):
            text = str(abstraction_dict[key])[1:len(str(abstraction_dict[key])) - 1]
            abstraction_source_content_label = Label(self.scrollable_result_frame, anchor='nw', text=text, bg='lemonchiffon',
                                             wraplength=wrap_right, justify=LEFT)
            abstraction_source_content_label.grid(row=i+delta, column=0, sticky='nwse', pady=4)
            self.labels.append(abstraction_source_content_label)

    # def toggle_show_hide(self):
    #     if self.preview_shown:
    #         self.button_show_hide.configure(text=SHOW)
    #         self.hide_preview()
    #     else:
    #         self.button_show_hide.configure(text=HIDE)
    #         self.show_preview()
    #     self.preview_shown = not self.preview_shown

    def show_preview(self):
        self.around_canvas_frame_result.grid()

    def hide_preview(self):
        self.around_canvas_frame_result.grid_remove()

    def destroy_preview(self):
        self.around_canvas_frame_result.destroy()
        self.canvas_preview_button.destroy()
        self.root.grid_columnconfigure((1), minsize=0)
        if self.label_suggested is not None:
            self.label_suggested.configure(wraplengt=800)


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
