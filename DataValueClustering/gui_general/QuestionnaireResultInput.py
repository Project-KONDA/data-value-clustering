from abc import ABC, abstractmethod
from tkinter import Label, Checkbutton, Button, IntVar, StringVar, NORMAL, DISABLED, Toplevel
from tkinter.font import Font

import numpy as np

from gui_general.ToolTip import CreateToolTip
from gui_general.scrollable_frame import create_scrollable_frame
from gui_general.window_size import set_window_size_simple


class QuestionnaireResultInput(ABC):

    # config: [dependencies, not-dependencies, name, default, question, notes?]

    def __init__(self, master, title, config, predefined_answers=None, start_row=0, suggestion=None):
        # Parameters
        self.config = np.array(config, dtype=object)
        self.n = len(config)
        self.m = len(self.config[0])
        self.check_config()
        self.start_row = start_row

        self.canceled = False

        self.checks = np.empty(self.n, dtype=Checkbutton)
        self.answers = np.empty(self.n, dtype=IntVar)

        # Variables
        self.config_dep = self.config[:, 0]
        self.config_notdep = self.config[:, 1]
        self.config_name = self.config[:, 2]
        if predefined_answers is None or len(predefined_answers) != self.n:
            self.config_default = self.config[:, 3]
        else:
            self.config_default = predefined_answers
        self.config_question = self.config[:, 4]
        self.config_notes = self.config[:, 5] if self.m > 5 else None

        # root:
        self.root = Toplevel(master)
        self.root.attributes('-alpha', 0.0)
        self.root.title(title)
        self.root.config(bg='white')
        self.root.resizable(False, True)
        # self.root.grid_rowconfigure(1, minsize=400)

        self.root.bind_all("<Return>", self.close)

        # caption:
        self.question_caption = StringVar()
        self.question_caption.set(self.caption_text)
        font = Font(family="TkDefaultFont", size=12, weight="bold")
        self.question_caption_label = Label(self.root, anchor='c', justify="center", textvariable=self.question_caption, bg='white',
                                            font=font)

        self.caption_width = font.measure(self.caption_text)

        self.hint_var = StringVar()
        self.hint_var.set(self.hint_text)
        self.hint_label = Label(self.root, anchor='c', justify="center", textvariable=self.hint_var, bg='white', wraplength=self.caption_width)

        self.label_suggested = None
        if suggestion is not None:
            self.label_suggested = Label(self.root, text=suggestion, bg="white", anchor='w', pady=10, fg='blue', justify='left', wraplength=self.caption_width)
            self.question_caption_label.grid(row=0, column=0, sticky='nsew', columnspan=4, pady=(10, 0))
            self.hint_label.grid(row=1, column=0, sticky='nsew', columnspan=3, pady=(0, 0))
            self.label_suggested.grid(row=2, column=0, sticky='senw', columnspan=3, padx=10)
        else:
            self.question_caption_label.grid(row=0, column=0, sticky='nsew', columnspan=3, pady=(10, 0))
            self.hint_label.grid(row=1, column=0, sticky='nsew', columnspan=3, pady=(0, 10))

        # scrollable question frame:
        self.around_canvas_frame_questions, self.canvas_questions, self.scrollable_questions_frame = create_scrollable_frame(self.root)
        self.root.rowconfigure(4, weight=1)
        self.around_canvas_frame_questions.grid(row=4, column=0, sticky='nsw', pady=5, padx=5)

        # question checkboxes:
        for i, question in enumerate(self.config_question):
            j = start_row + i
            self.answers[i] = IntVar()
            self.answers[i].set(int(self.config_default[i]))
            self.checks[i] = Checkbutton(self.scrollable_questions_frame, variable=self.answers[i], command=self.selection_changed, bg='white', text=question, anchor='nw', padx=20)
            self.checks[i].grid(row=j + 5, column=0, sticky='nw')
            if self.m > 5:
                message = str(self.config_notes[i])
                CreateToolTip(self.checks[i], text=message)
                # self.labels[i].bind("<Enter>", (lambda event, i2=i: self.on_label_enter(event, i2)))
                # self.labels[i].bind("<Leave>", (lambda event, i2=i: self.on_label_leave(event, i2)))

        self.visible = np.full(self.n, True)
        self.update_visibility()

        # caption right side:
        # self.result_caption = StringVar()
        # self.result_caption.set(self.help_text)
        # self.result_caption_label = Label(self.root, anchor='w', textvariable=self.result_caption, bg='white',
        #                                   font=('TkDefaultFont', 14, 'bold'), padx=5)
        # self.result_caption_label.grid(row=0, column=1, sticky='we', columnspan=2)

        # scrollable result frame:
        self.around_canvas_frame_result, self.canvas_result, self.scrollable_result_frame = create_scrollable_frame(self.root)
        self.root.rowconfigure(4, weight=1)
        self.around_canvas_frame_result.grid(row=4, column=2, sticky='nsw', pady=5, padx=5)

        # OK button:
        self.button = Button(self.root, text='OK', command=self.close, bg='white')
        self.button.grid(row=5, column=0, sticky='nswe', columnspan=6)


    def enter_scrollable_result_frame(self, *args):
        self.scrollable_result_frame.bind_all("<MouseWheel>", self.on_mousewheel_result_frame)

    def leave_scrollable_result_frame(self, *args):
        self.scrollable_result_frame.unbind_all("<MouseWheel>")

    def on_mousewheel_result_frame(self, event):
        if self.scrollable_result_frame.winfo_height() > self.canvas_result.winfo_height():
            self.canvas_result.yview_scroll(-1 * (event.delta // 120), "units")

    def run(self):

        set_window_size_simple(self.root)

        self.root.attributes('-alpha', 1.0)

        self.root.focus_force()
        self.root.grab_set()

        self.root.protocol("WM_DELETE_WINDOW", self.cancel)

        self.root.mainloop()

    def update_visibility(self):
        for i in range(self.n):
            is_visible = self.visible[i]
            should_visible = self.should_be_visible(i)
            if not is_visible and should_visible:
                self.checks[i].config(state=NORMAL)
                # self.checks[i].grid(row=i + 5, column=0, sticky='nw')
            if is_visible and not should_visible:
                self.checks[i].config(state=DISABLED)
                # self.checks[i].grid_forget()
                # self.answers[i].set(False)
            if not should_visible:
                self.answers[i].set(False)
            self.visible[i] = should_visible

    def selection_changed(self):
        self.update_visibility()
        self.apply()

    def should_be_visible(self, i):
        """ test if question i should be visible"""
        bool = True
        for d in self.config_dep[i]:
            bool &= self.answers[d].get() and self.visible[d]
        for nd in self.config_notdep[i]:
            bool &= not self.answers[nd].get()  # or not self.visible[nd]
        return bool

    def update_check_buttons(self, answers):
        for i, answer in enumerate(answers):
            self.answers[i].set(int(answer))
        self.update_visibility()
        self.apply()

    def check_questions(self):
        pass

    def get(self):
        if self.canceled is True:
            return None
        answers = []
        for i, v in enumerate(self.answers):
            answers.append(v.get() == 1)
        return answers

    def cancel(self):
        self.canceled = True
        self.close()

    def close(self, event=None):
        self.unbind_all()
        self.root.quit()
        self.root.destroy()

    def unbind_all(self):
        self.scrollable_result_frame.unbind_all("<MouseWheel>")
        self.scrollable_questions_frame.unbind_all("<MouseWheel>")
        self.root.unbind_all("<Return>")


    @abstractmethod
    def apply(self):
        pass

    def check_config(self):
        assert self.n > 0
        assert 5 <= self.m <= 6
        for i in range(self.n):
            assert self.m == len(self.config[i])
            assert isinstance(self.config[i, 0], list)
            assert isinstance(self.config[i, 1], list)
            assert isinstance(self.config[i, 2], str)
            assert isinstance(self.config[i, 3], bool)
            assert isinstance(self.config[i, 4], str)
            if self.m > 5:
                assert isinstance(self.config[i, 5], str)

            assert not self.config[i, 0] or max(self.config[i, 0]) < i
            assert not self.config[i, 1] or max(self.config[i, 1]) < i

    # def on_label_enter(self, event, i):
    #     message = str(self.config_notes[i])
    #
    #
    #     print("on index " + str(i) + " show message: " + message)
    #
    # def on_label_leave(self, event, i):
    #     print("hide")