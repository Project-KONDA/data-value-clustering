from math import sqrt
from tkinter import Tk, Button, Canvas, Menu, FLAT, Toplevel
import numpy as np
from PIL import Image, ImageTk

from gui_general.help_popup_gui import menu_help_blob_input
from gui_distances.Blob import Blob
from gui_distances.blobinput_helper import get_blob_configuration, \
    create_coordinates_relative
from gui_distances.costmapinput_helper import print_cost_map


def input_blobs(root, config):
    blobs = BlobInput(root, config)
    cost_map, new_config = blobs.get()
    return cost_map, new_config


class BlobInput:
    """
    GUI for indirect input of the weight matrix for configuring the weighted levenstein distance function
    by moving and resizing objects on a canvas
    """

    def __init__(self, master, config):
        """
        :param config: array
            config is array of form [label, regex, resizable, info, x, y, size]
        """

        """Parameters"""
        self.configuration = config
        self.labels = config[:, 0]
        self.n = len(self.labels)
        self.regexes = config[:, 1]
        self.resizable = config[:, 2]
        self.chars_info = config[:, 3]
        self.coordinates = config[:, (4, 5)]
        self.sizes = config[:, 6]

        """Root"""
        self.master = master
        self.root = Toplevel(self.master)
        self.root.title('Distance Specification')
        self.canceled = False

        """Frame"""
        self.window_size = 3/4
        self.w = int(self.root.winfo_screenwidth() * self.window_size)
        self.h = int(self.root.winfo_screenheight() * self.window_size)
        self.x = self.w // 2
        self.y = self.h // 2
        self.diagonal = int(sqrt(self.w * self.w + self.h * self.h))
        self.root.geometry(f"{self.w}x{self.h}+{self.w // 6}+{self.h // 6}")
        self.root.resizable(False, False)
        # self.root.minsize(400, 300)
        # self.root.maxsize(self.root.winfo_screenwidth(), self.root.winfo_screenheight())
        self.root.config(bg='black')
        self.root.bind_all("<Escape>", lambda event: self.close(event, True))
        self.root.bind_all("<Return>", self.close)

        """Menu"""
        self.menu = Menu(self.root)
        # configMenu = Menu(menu)
        # configMenu.add_command(label="Configure1")
        # menu.add_cascade(label="Configure", menu=configMenu)
        self.menu.add_command(label="Help", command=menu_help_blob_input)
        self.root.config(menu=self.menu)

        """Images"""
        self.image_sizes = min(self.h, self.w) // 8
        self.max_distance = 20
        self.max_self_dif = 5
        self.gui_spacing = 5
        self.distance_factor = 1 / self.image_sizes  # self.max_distance / self.diagonal
        self.size_factor = 1.  # 2 / self.image_sizes  # self.max_distance / self.diagonal / 0.62

        """Canvas"""
        self.canvas_h = 17 * self.h // 18 - 4 * self.gui_spacing
        self.canvas_w = self.w - 3 * self.gui_spacing
        self.canvas = Canvas(self.root, width=self.canvas_w, height=self.canvas_h,
                             highlightbackground="black")  # , background="alice blue")
        self.canvas.place(anchor='nw', x=self.gui_spacing, y=self.gui_spacing)

        # garbage collector defense mechanism
        self.img = Image.open("..\\gui_distances\\blob_images\\background4.png")
        self.img = self.img.resize((self.canvas_w, self.canvas_h), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(self.img)
        self.background_image = self.img
        self.background = self.canvas.create_image(0, 0, image=self.img, anchor='nw')

        """Dragging"""
        # this data is used to keep track of an item being dragged
        self._drag_data = {"x": 0, "y": 0, "item": None, "item_last": None, "nearest": None, "last_nearest": None}
        # add bindings for clicking, dragging and releasing over any object with the "token" tag
        self.canvas.tag_bind("token", "<ButtonPress-1>", self.drag_start)
        self.canvas.tag_bind("token", "<ButtonRelease-1>", self.drag_stop)
        self.canvas.tag_bind("token", "<B1-Motion>", self.drag)

        """Scale"""
        self.canvas.bind_all("<n>", self.scale_blob_normal)
        self.canvas.bind_all("<MouseWheel>", self.scale_a_blob)

        """Info"""
        self.canvas.bind("<Motion>", self.canvas_blob_info)
        self.canvas.text = self.canvas.create_text(10, 10, text="", anchor="nw")

        """Build Blobs"""
        self.blobs = np.empty(len(config), dtype=Blob)
        for i, c in reversed(list(enumerate(self.coordinates))):
            self.blobs[i] = Blob(self, label=self.labels[i], regex=self.regexes[i], resizable=self.resizable[i],
                                 info=self.chars_info[i], rel_x=self.coordinates[i, 0], rel_y=self.coordinates[i, 1],
                                 rel_size=self.sizes[i])

        """Buttons"""
        self.button_h = self.h // 18
        self.button_w = self.x - 2 * self.gui_spacing

        self.button_image_restart = Image.open("..\\gui_distances\\blob_images\\button_restart.png")
        self.button_image_restart = self.button_image_restart.resize((self.button_w, self.button_h), Image.ANTIALIAS)
        self.button_image_restart = ImageTk.PhotoImage(self.button_image_restart)
        self.button_image_ok = Image.open("..\\gui_distances\\blob_images\\button_ok.png")
        self.button_image_ok = self.button_image_ok.resize((self.button_w, self.button_h), Image.ANTIALIAS)
        self.button_image_ok = ImageTk.PhotoImage(self.button_image_ok)

        self.button_restart = Button(self.root, text='Restart', command=self.restart,
                                     width=self.button_w, height=self.button_h, bg='black', border=0,
                                     image=self.button_image_restart)
        # self.button_restart.place(anchor='center', x=self.x // 2, y=self.h - self.button_h // 2 - self.gui_spacing)
        self.button_restart.place(anchor='sw', x=self.gui_spacing + 1, y=self.h - self.gui_spacing)

        self.button_ok = Button(self.root, text='OK', command=self.close,
                                width=self.button_w, height=self.button_h, bg='black', border=0,
                                image=self.button_image_ok)
        # self.button_ok.place(anchor='center', x=3 * self.x // 2, y=self.h - self.button_h // 2 - self.gui_spacing)
        self.button_ok.place(anchor='se', x=self.w - self.gui_spacing - 1, y=self.h - self.gui_spacing)

        self.root.after(1, lambda: self.root.focus_force())
        self.root.protocol("WM_DELETE_WINDOW", self.cancel)
        self.root.mainloop()

    def unbind_all(self):
        self.root.unbind_all("<Return>")
        self.root.unbind_all("<Escape>")
        self.canvas.unbind_all("<MouseWheel>")
        self.canvas.unbind_all("<Motion>")
        self.canvas.unbind_all("<n>")
        self.canvas.unbind_all("<ButtonPress-1>")
        self.canvas.unbind_all("<ButtonRelease-1>")
        self.canvas.unbind_all("<B1-Motion>")
        self.canvas.unbind_all("<ButtonPress-1>")


    def canvas_blob_info(self, event):
        """On mouse over show Information of Blob in Canvas"""
        self.find_nearest_blob(event.x, event.y)
        if isinstance(self._drag_data["nearest"], Blob):
            text = self._drag_data["nearest"].info
            # text += f"\ndist.: {str(blob.get_distance(event.x, event.y))}"
            # text += f"\nposition: ({event.x:>4},{event.y:>4})"
            text += f"\nregex: {self._drag_data['nearest'].regex}"
            if self._drag_data["nearest"].resizable:
                text += f"\nsize : {str(self._drag_data['nearest'].get_size() * self.size_factor)}"
            if self._drag_data['last_nearest'] is not None \
                    and self._drag_data['last_nearest'] is not self._drag_data['nearest']:
                text += f"\n    distance from: {self._drag_data['last_nearest'].label}"
                text += f"\n    " + str(round(self._drag_data['nearest'].get_distance(
                    blob=self._drag_data['last_nearest']) * self.distance_factor, 2))
            self.canvas.itemconfigure(self.canvas.text, text=text)
        else:
            self.canvas.itemconfigure(self.canvas.text, text="")

    def find_nearest_blob(self, x, y):
        """Finds the nearest blob to (x|y)"""
        min_blob, min_distance = (None, 0.)
        for i, blob in enumerate(self.blobs):
            d = (blob.get_distance(x, y) - blob.get_abs_size() / 2) / blob.get_abs_size()
            if d < min_distance:
                min_blob, min_distance = blob, d

        if not self._drag_data["nearest"] is min_blob:
            if min_blob is not self._drag_data["nearest"] and isinstance(self._drag_data["nearest"], Blob):
                self._drag_data["last_nearest"] = self._drag_data["nearest"]
            self._drag_data["nearest"] = min_blob

    def drag_start(self, event):
        """Beginning drag of an object"""
        # record the item and its location
        if isinstance(self._drag_data["nearest"], Blob):
            self._drag_data["nearest"].lift()
        self._drag_data["item"] = self._drag_data["nearest"]
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

    def drag_stop(self, event):
        """End drag of an object"""
        # reset the drag information
        self._drag_data["item"] = None
        self._drag_data["x"] = 0
        self._drag_data["y"] = 0

    def drag(self, event):
        """Handle dragging of an object"""
        # compute how much the mouse has moved
        delta_x = event.x - self._drag_data["x"]
        delta_y = event.y - self._drag_data["y"]
        # move the blob the appropriate amount
        if isinstance(self._drag_data["item"], Blob):
            self._drag_data["item"].move(delta_x, delta_y)
        # record the new position
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

    def scale_a_blob(self, event):
        """Handles scaling a Blob"""
        up = event.delta > 0
        # self._drag_data["nearest"] = self.find_nearest_blob(event.x, event.y)
        if self._drag_data["nearest"] is not None:
            self._drag_data["nearest"].scale(up=up)
        self.canvas_blob_info(event)

    def scale_blob_normal(self, event):
        """Set Blob to normal size"""
        # nearest = self.find_nearest_blob(event.x, event.y)
        if self._drag_data["nearest"] is not None:
            self._drag_data["nearest"].scale(reset=True)
        self.canvas_blob_info(event)

    def get_distance_map(self):
        """Calculate and return distance map"""
        if self.canceled:
            return {}
        distance_map = {(()): 1.}

        for i, blob_i in enumerate(self.blobs):
            distance_map[i] = blob_i.regex

            for j, blob_j in enumerate(self.blobs):
                if i == j:  # (i,j), i==j -> blobsize(i)
                    distance_map[(i, i)] = round((blob_i.get_size() * self.size_factor), 2)

                else:  # (i,j), i!=j -> distance ( blob(i), blob(j) )
                    distance_map[(i, j)] = round(
                        (blob_i.get_distance(blob=blob_j) * self.distance_factor), 2)

        return distance_map  # TODO: return modified blob_configuration

    def get(self):
        if self.canceled:
            return None, None
        return self.get_distance_map(), self.get_config()

    def cancel(self):
        self.canceled = True
        self.close(canceled=True)

    def close(self, event=None, canceled=False):
        """Close Tk Window"""
        self.canceled = canceled
        self.unbind_all()
        self.root.quit()
        self.root.destroy()

    def restart(self):
        """Reopen the window, inclusive positions and sizes."""
        configuration = self.get_config()
        new_coordinates = create_coordinates_relative(self.n)

        for i in range(self.n):
            for j in range(3):
                configuration[i, j+4] = new_coordinates[i, j]

        self.root.destroy()
        self.__init__(self.master, configuration)

    def get_absolute_coordinate_value(self, relative_value, x=True):
        # ca. (-0.2, 1.2) -> (0-1920)
        factor = min(self.h, self.w)
        difference = abs(self.h - self.w) // 2
        result = relative_value * factor
        if x != (self.w <= self.h):  # longer axis
            result += difference
        return result

    def get_relative_coordinate_value(self, absolute_value, x=True):
        # ca. (0-1920) -> (-0.2, 1.2)
        factor = min(self.h, self.w)
        difference = abs(self.h - self.w) // 2
        if x != (self.w <= self.h):  # longer axis
            absolute_value -= difference
        result = absolute_value / factor
        return result

    def get_config(self):
        # [label, regex, resizable, info, x, y, size]
        config = list()
        for blob in self.blobs:
            blob_config = [blob.label, blob.regex, blob.resizable, blob.info, blob.rel_x, blob.rel_y, blob.rel_size]
            config.append(blob_config)
        return np.array(config, dtype=object)


if __name__ == '__main__':
    min_blobs = [False, False, False, False, False, False, False, False, False,
                 False, False, False,
                 True, False, False, False, False, False,
                 True]
    min_config = get_blob_configuration(min_blobs)
    # print(len(min_config), min_config)
    costmap, config = BlobInput(Tk(),min_config).get()
    print_cost_map(costmap)

    # max_blobs = [False, False, True, True, True, True, True, True, True,
    #              True, True, True,
    #              False, True, True, True, True, True,
    #              True]
    # max_config = get_blob_configuration(max_blobs)
    # max_blob_config = get_blob_configuration(max_blobs)
    # print(str(BlobInput(max_blob_config).get()))
