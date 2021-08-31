from abc import ABC, abstractmethod
from tkinter import Label, Checkbutton, Button, Tk, IntVar, StringVar, Frame, LEFT, RIGHT, BOTH, GROOVE, font, Canvas, \
    Scrollbar, FLAT, NORMAL, DISABLED, Toplevel

import numpy as np

from gui_general.ToolTip import CreateToolTip


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
        self.root.title(title)
        self.root.config(bg='white')
        self.root.resizable(False, False)
        # self.root.grid_rowconfigure(1, minsize=400)

        self.root.bind_all("<Return>", self.close)

        # caption:
        self.question_caption = StringVar()
        self.question_caption.set(self.caption_text)
        self.question_caption_label = Label(self.root, anchor='c', justify="center", textvariable=self.question_caption, bg='white',
                                            font=('TkDefaultFont', 12, 'bold'))

        self.hint_var = StringVar()
        self.hint_var.set(self.hint_text)
        self.hint_label = Label(self.root, anchor='c', justify="center", textvariable=self.hint_var, bg='white')

        self.label_suggested = None
        if suggestion is not None:
            self.label_suggested = Label(self.root, text=suggestion, bg="white", anchor='w', pady=10, fg='blue', justify='left')
            self.question_caption_label.grid(row=0, column=0, sticky='nsew', columnspan=4, pady=(10, 0))
            self.hint_label.grid(row=1, column=0, sticky='nsew', columnspan=3, pady=(0, 0))
            self.label_suggested.grid(row=2, column=0, sticky='senw', columnspan=3, padx=10)
        else:
            self.question_caption_label.grid(row=0, column=0, sticky='nsew', columnspan=3, pady=(10, 0))
            self.hint_label.grid(row=1, column=0, sticky='nsew', columnspan=3, pady=(0, 10))


        # question checkboxes:
        self.root.rowconfigure(3, weight=1)
        self.question_frame = Frame(self.root, bg="white", borderwidth=2, relief="groove")
        self.question_frame.grid(row=3, column=0, sticky='nsew', padx=5, pady=5)

        for i, question in enumerate(self.config_question):
            j = start_row + i
            self.answers[i] = IntVar()
            self.answers[i].set(int(self.config_default[i]))
            self.checks[i] = Checkbutton(self.question_frame, variable=self.answers[i], command=self.selection_changed, bg='white', text=question, anchor='nw', padx=20)
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


        # scrollable result:
        self.around_canvas_frame = Frame(self.root, bg="white", relief="groove", borderwidth=2)
        self.around_canvas_frame.grid_rowconfigure(0, weight=1)
        self.around_canvas_frame.grid(row=3, column=2, sticky='nsw', pady=5, padx=5)

        self.canvas = Canvas(self.around_canvas_frame, bg="white", highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky='nswe')
        self.scrollbar = Scrollbar(self.around_canvas_frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar.grid(row=0, column=5, sticky='nswe')
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)

        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)

        self.scrollable_result_frame = Frame(self.canvas, bg="white")

        self.canvas_frame = self.canvas.create_window((0, 0), window=self.scrollable_result_frame, anchor="nw")

        def _configure_scrollable_frame(event):
            size = (self.scrollable_result_frame.winfo_reqwidth(), self.scrollable_result_frame.winfo_reqheight())
            self.canvas.config(scrollregion="0 0 %s %s" % size)
            if self.scrollable_result_frame.winfo_reqwidth() != self.canvas.winfo_width():
                self.canvas.config(width=self.scrollable_result_frame.winfo_reqwidth())
                self.around_canvas_frame.config(width=self.scrollable_result_frame.winfo_reqwidth())

        self.scrollable_result_frame.bind('<Configure>', _configure_scrollable_frame)

        def _configure_canvas(event):
            if self.scrollable_result_frame.winfo_reqwidth() != self.canvas.winfo_width():
                self.canvas.itemconfigure(self.canvas_frame, width=self.canvas.winfo_width())
                self.around_canvas_frame.config(width=self.canvas.winfo_width())

        self.canvas.bind('<Configure>', _configure_canvas)

        # button:
        self.button = Button(self.root, text='OK', command=self.close, bg='white')
        self.button.grid(row=4, column=0, sticky='nswe', columnspan=6)

    def on_mousewheel(self, event):
        if self.scrollable_result_frame.winfo_height() > self.canvas.winfo_height():
            self.canvas.yview_scroll(-1 * (event.delta // 120), "units")

    def run(self):
        # Center Window on Screen
        self.root.update_idletasks()
        midx = max(0, self.root.winfo_screenwidth() // 2 - self.root.winfo_reqwidth() // 2)
        midy = max(0, self.root.winfo_screenheight() // 3 - self.root.winfo_reqheight() // 2)
        self.root.geometry(f"+%s+%s" % (midx, midy))

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
        self.canvas.unbind_all("<MouseWheel>")
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