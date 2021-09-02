from win32api import GetMonitorInfo, MonitorFromPoint


def set_window_size(root, h_expanded=None):
    root.update_idletasks()
    width = root.winfo_reqwidth()
    frame_width = root.winfo_rootx() - root.winfo_x()
    window_width = width + 2 * frame_width
    x = root.winfo_screenwidth() // 2 - window_width // 2
    # screen_height = self.root.winfo_screenheight()
    # app = QApplication(sys.argv)
    # dw = app.desktop()
    # taskbar_height = dw.screenGeometry().height() - dw.availableGeometry().height()
    # work_area_height = screen_height - taskbar_height - titlebar_height
    monitor_info = GetMonitorInfo(MonitorFromPoint((0, 0)))
    work_area = monitor_info.get("Work")  # work area does not include task bar
    work_area_height = work_area[3]
    title_bar_height = root.winfo_rooty() - root.winfo_y()
    max_height_inner = work_area_height - title_bar_height + frame_width
    h_expanded = h_expanded + frame_width
    if h_expanded is None:
        height_inner = max_height_inner
    else:
        height_inner = min(max_height_inner, h_expanded)
    height_outer = height_inner + title_bar_height - frame_width
    y = work_area_height // 2 - height_outer // 2
    root.maxsize(width, max_height_inner)
    root.geometry('{}x{}+{}+{}'.format(width, height_inner, x, y))
    root.deiconify()