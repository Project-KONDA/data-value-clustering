from tkinter import *


class ToolTip(object):
    """
    Class for GUI ToolTips
    binds text to objects, that are shown when hovering
    """

    def __init__(self, widget, color="#ffffe0"):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0
        self.color = color

    def showtip(self, text):
        "Display text in tooltip window"
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 57
        y = y + cy + self.widget.winfo_rooty() + 27
        self.tipwindow = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        # if self.text.startswith("Warning"):
        #     bg = "tomato"
        # else:
        #     bg="#ffffe0"
        label = Label(tw, text=self.text, justify=LEFT,
                      background=self.color, relief=SOLID, borderwidth=1,
                      font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()


def CreateToolTip(widget, text="", textfunction=None, color="#ffffe0"):
    toolTip = ToolTip(widget, color)
    if textfunction is None:
        textfunction = lambda: text

    def enter(event):
        toolTip.showtip(textfunction())

    def leave(event):
        toolTip.hidetip()

    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)

    return toolTip
