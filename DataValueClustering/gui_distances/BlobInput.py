from math import sqrt
from tkinter import Tk, Button, Canvas, Menu
import numpy as np
from PIL import Image, ImageTk

from compression.compression import get_blob_configuration
from gui_distances.Blob import Blob
from gui_distances.blobinput_helper import create_coordinates, print_cost_matrix


class BlobInput:

    def __init__(self, chars_labels):

        """Parameters"""
        self.chars_labels = chars_labels
        self.labels = chars_labels[:, 0]
        self.regex = chars_labels[:, 1]
        self.resizable = chars_labels[:, 2]
        self.canceled = False

        """Root"""
        self.root = Tk()
        self.root.title('Distance Specification')

        """Frame"""
        self.w = int(3*self.root.winfo_screenwidth()/4)
        self.h = int(3*self.root.winfo_screenheight()/4)
        self.x = int(self.w / 2)
        self.y = int(self.h / 2)
        self.diagonal = int(sqrt(self.w * self.w + self.h * self.h))
        self.root.geometry(f"{self.w}x{self.h}+{int(self.w/6)}+{int(self.h/6)}")
        # self.root.geometry(f"{self.w}x{self.h}")
        # self.root.eval('tk::PlaceWindow . center')
        self.root.resizable(False, False)
        # self.root.minsize(400, 300)
        # self.root.maxsize(self.root.winfo_screenwidth(), self.root.winfo_screenheight())
        self.root.config(bg='white')

        """Images"""
        self.image_sizes = int(min(self.h, self.w) / 8)
        self.max_distance = 20
        self.max_self_dif = 5
        self.distance_factor = 1 / self.image_sizes  # self.max_distance / self.diagonal
        self.size_factor = 1.  # 2 / self.image_sizes  # self.max_distance / self.diagonal / 0.62
        self.distance_threshold = self.diagonal / 20
        self.coordinates = create_coordinates(self.x, self.y, self.labels)  # array: [label, x, y, size]

        """Canvas"""
        self.canvas = Canvas(width=self.w, height=self.h, background="alice blue")
        self.canvas.pack(fill="both", expand=True)

        # garbage collector defense mechanism
        img = Image.open("..\\blob_images\\background3.png")
        img = img.resize((self.w, self.h), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        self.background_image = img
        self.background = self.canvas.create_image(0, 0, image=img, anchor='nw')

        """Menu"""
        menu = Menu(self.root)
        # configMenu = Menu(menu)
        # configMenu.add_command(label="Configure1")
        # menu.add_cascade(label="Configure", menu=configMenu)
        menu.add_command(label="Help")
        self.root.config(menu=menu)

        """Dragging"""
        # this data is used to keep track of an item being dragged
        self._drag_data = {"x": 0, "y": 0, "item": None, "item_last": None}
        # add bindings for clicking, dragging and releasing over any object with the "token" tag
        self.canvas.tag_bind("token", "<ButtonPress-1>", self.drag_start)
        self.canvas.tag_bind("token", "<ButtonRelease-1>", self.drag_stop)
        self.canvas.tag_bind("token", "<B1-Motion>", self.drag)
        self.canvas.bind_all("<n>", self.scale_blob_normal)
        self.canvas.bind_all("<MouseWheel>", self.scale_a_blob)

        """Build Blobs"""
        self.blobs = np.empty(len(chars_labels), dtype=Blob)
        for i, c in reversed(list(enumerate(self.coordinates))):
        """OK Button"""
        Button(self.root, text='OK', command=self.close, width=int(self.w / 7.2), background='lime green'
               ).place(anchor='center', x=self.x, y=self.h - 50)

        Button(self.root, text='Restart', command=self.restart, width=int(self.w / 7.2), background='brown2'
               ).place(anchor='center', x=self.x, y=self.h - 20)

        self.root.mainloop()

    def find_nearest_blob(self, x, y):
        min_blob, min_distance = (None, self.distance_threshold)
        # min_blob, min_distance = (self.blobs[0], self.blobs[0].get_distance(x, y))
        for i, blob in enumerate(self.blobs):
            d = blob.get_distance(x, y) - blob.size
            if d < min_distance:
                min_blob, min_distance = blob, d
        return min_blob

    def drag_start(self, event):
        """Beginning drag of an object"""
        # record the item and its location
        nearest = self.find_nearest_blob(event.x, event.y)
        nearest.lift()
        self._drag_data["item"] = nearest
        self._drag_data["item_last"] = None
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

    def drag_stop(self, event):
        """End drag of an object"""
        # reset the drag information
        self._drag_data["item_last"] = self._drag_data["item"]
        self._drag_data["item"] = None
        self._drag_data["x"] = 0
        self._drag_data["y"] = 0

    def drag(self, event):
        """Handle dragging of an object"""
        # compute how much the mouse has moved
        delta_x = event.x - self._drag_data["x"]
        delta_y = event.y - self._drag_data["y"]
        # move the blob the appropriate amount
        self._drag_data["item"].move(delta_x, delta_y)
        # record the new position
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

    def scale_a_blob(self, event):
        """Handles scaling a Blob"""
        up = event.delta > 0
        nearest = self.find_nearest_blob(event.x, event.y)
        if nearest is not None:
            nearest.scale(up=up)

    def scale_blob_normal(self, event):
        nearest = self.find_nearest_blob(event.x, event.y)
        if nearest is not None:
            nearest.scale(reset=True)

    # calculate and return distance map
    def get(self):
        # TODO: () -> ?
        distance_map = {(()): 1.}

        for i, l in enumerate(self.labels):
            distance_map[i] = self.regex[i]

        # TODO: costs for insertion (:,0) and deletion (0,:)

        for i, label_i in enumerate(self.labels):
            for j, label_j in enumerate(self.labels):
                if i == j:
                    # (i,j), i==j -> blobsize(i)
                    distance_map[(i, i)] = round((self.blobs[i].get_size() * self.size_factor), 2)
                else:
                    # (i,j), i!=j -> distance ( blob(i), blob(j) )
                    distance_map[(i, j)] = round(
                        (self.blobs[i].get_distance(blob=self.blobs[j]) * self.distance_factor), 2)

        return distance_map

    def close(self):
        self.root.destroy()

    def restart(self):
        chars_labels = self.chars_labels
        self.root.destroy()
        self.__init__(chars_labels)


if __name__ == '__main__':
    min_blobs = [False, False, False, False, False, False, False, False, False,
        False, False, False,
        True, False, False, False, False, False]
    min_blob_config = get_blob_configuration(min_blobs)
    print_cost_matrix(BlobInput(min_blob_config).get())

    # max_blobs = [False, False, True, True, True, True, True, True, True,
    #     True, True, True,
    #     False, True, True, True, True, True]
    # max_blob_config = get_blob_configuration(max_blobs)
    # print(str(BlobInput(max_blob_config).get()))

