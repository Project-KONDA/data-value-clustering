from tkinter import Frame, Canvas, Scrollbar, LabelFrame


def create_scrollable_label_frame(root, text, dynamic=False, dynamic_height=True):
    outer_frame = LabelFrame(root, bg="white", relief="groove", borderwidth=2, text=text)
    outer_frame.grid_rowconfigure(0, weight=1)
    return _create_scrollable_frame_in_outer_frame(outer_frame, dynamic, dynamic_height)


def create_scrollable_frame(root, dynamic=False, dynamic_height=True):
    outer_frame = Frame(root, bg="white", relief="groove", borderwidth=2)
    outer_frame.grid_rowconfigure(0, weight=1)
    return _create_scrollable_frame_in_outer_frame(outer_frame, dynamic, dynamic_height)


def _create_scrollable_frame_in_outer_frame(outer_frame, dynamic=False, dynamic_height=True):
    canvas = Canvas(outer_frame, bg="white", highlightthickness=0)
    canvas.grid(row=0, column=0, sticky='nswe')

    scrollbar = Scrollbar(outer_frame, orient="vertical",
                                         command=canvas.yview)
    scrollbar.grid(row=0, column=1, sticky='nswe')

    def scrollbarSet(low, high):
        if float(low) <= 0.0 and float(high) >= 1.0:
            scrollbar.grid_remove()
        else:
            scrollbar.grid()
        scrollbar.set(low, high)

    if dynamic:
        canvas.configure(yscrollcommand=scrollbarSet)
    else:
        canvas.configure(yscrollcommand=scrollbar.set)
    canvas.xview_moveto(0)
    canvas.yview_moveto(0)

    scrollable_frame = Frame(canvas, bg="white")
    scrollable_frame.bind('<Enter>', lambda args: _enter_scrollable_frame(args, scrollable_frame=scrollable_frame, canvas=canvas))
    scrollable_frame.bind('<Leave>', lambda args: _leave_scrollable_frame(args, scrollable_frame=scrollable_frame))

    canvas_id = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    scrollable_frame.bind('<Configure>', lambda event: _configure_scrollable_frame(event, scrollable_frame, canvas, outer_frame, dynamic_height))
    canvas.bind('<Configure>', lambda event: _configure_canvas(event, scrollable_frame, canvas, outer_frame, canvas_id))

    return outer_frame, canvas, scrollable_frame


def _enter_scrollable_frame(*args, scrollable_frame, canvas):
    scrollable_frame.bind_all("<MouseWheel>", lambda event: _on_mousewheel_scrollable_frame(event, scrollable_frame, canvas))


def _leave_scrollable_frame(*args, scrollable_frame):
    scrollable_frame.unbind_all("<MouseWheel>")


def _on_mousewheel_scrollable_frame(event, scrollable_frame, canvas):
    if scrollable_frame.winfo_height() > canvas.winfo_height():
        canvas.yview_scroll(-1 * (event.delta // 120), "units")

def _configure_scrollable_frame(event, scrollable_frame, canvas, outer_frame, dynamic_height):
    size = (scrollable_frame.winfo_reqwidth(), scrollable_frame.winfo_reqheight())
    canvas.config(scrollregion="0 0 %s %s" % size)
    if scrollable_frame.winfo_reqwidth() != canvas.winfo_width():
        canvas.config(width=scrollable_frame.winfo_reqwidth())
        outer_frame.config(width=scrollable_frame.winfo_reqwidth())
    if dynamic_height and scrollable_frame.winfo_reqheight() != canvas.winfo_height():
        canvas.config(height=scrollable_frame.winfo_reqheight())
        # outer_frame.config(height=scrollable_frame.winfo_reqheight())


def _configure_canvas(event, scrollable_frame, canvas, outer_frame, canvas_id):
    if scrollable_frame.winfo_reqwidth() != canvas.winfo_width():
        canvas.itemconfigure(canvas_id, width=canvas.winfo_width())
        outer_frame.config(width=canvas.winfo_width())
    # if scrollable_frame.winfo_reqheight() != canvas.winfo_height():
    #     canvas.itemconfigure(canvas_id, height=canvas.winfo_height())
        # outer_frame.config(height=canvas.winfo_height())