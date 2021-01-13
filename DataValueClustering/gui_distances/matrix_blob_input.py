from math import sin, cos, radians, sqrt
from tkinter import Tk, Button, Canvas

from PIL import Image, ImageTk

import numpy as np


class Blob:
    def __init__(self, blobinput, label, x, y, size):
        self.blobinput = blobinput
        self.label = label
        self.path = "..\\blob_images\\" + self.label + ".png"
        self.x = x
        self.y = y
        self.size = size
        self.min_size = 50
        self.max_size = 550
        self.photoimage = None
        self.image = self.create_image()

    # size of a blob
    def get_size(self):

        return self.size - self.min_size

    # calculate distance to point or blob
    def get_distance(self, x=0, y=0, blob=None):
        if blob is None:
            return sqrt((self.x - x) ** 2 + (self.y - y) ** 2)
        else:
            return sqrt((self.x - blob.x) ** 2 + (self.y - blob.y) ** 2)

    def move(self, dx=0, dy=0):
        self.x += dx
        self.y += dy
        # self.canvas.move(self.oval, dx, dy)
        self.blobinput.canvas.move(self.image, dx, dy)

    def set_position(self, x=0, y=0):
        self.x = x
        self.y = y

    def scale(self, up=True):
        if up:
            self.size = min(self.max_size, self.size + 5)
            # self.size = int(round(self.size * 1.251))
        else:
            self.size = max(self.min_size, self.size - 5)
            # self.size = int(round(self.size / 1.251))
        self.update_image()

    def create_oval(self, color):
        return self.blobinput.canvas.create_oval(
            self.x - 25,
            self.y - 25,
            self.x + 25,
            self.y + 25,
            outline=color,
            fill=color,
            tags=("token",),
        )

    def create_image(self):
        img = Image.open(self.path)
        img = img.resize((int(self.size * 1.2), self.size), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        print ('fail')
        self.photoimage = img
        return self.blobinput.canvas.create_image(self.x, self.y, image=img, anchor='center', tags=("token",))

    def update_image(self):
        if self.image is not None:
            img = Image.open(self.path)
            img = img.resize((int(self.size * 1.2), int(self.size)), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(img)
            self.photoimage = img
            # self.image =
            self.blobinput.canvas.itemconfig(self.image, image=img)


class BlobInput:

    def __init__(self, chars_labels):

        self.chars_labels = chars_labels
        self.labels = chars_labels[:, 1]
        self.chars = chars_labels[:, 0]

        """ROOT"""
        self.root = Tk()
        self.root.title('Distance Specification')

        """Frame"""
        self.w = 1000
        self.h = 800
        self.root.geometry(str(self.w) + "x" + str(self.h))
        self.root.config(bg='white')
        self.x = int(self.w / 2)
        self.y = int(self.h / 2)
        self.diagonal = int(sqrt(self.w * self.w + self.h * self.h))

        """Images"""
        print(self.diagonal)
        self.image_sizes = int(min(self.h, self.w) / 8)
        self.max_distance = 20
        self.distance_factor = self.max_distance / self.diagonal
        self.size_factor = self.max_distance / self.diagonal
        self.distance_threashold = self.diagonal/20
        self.coordinates = self.create_coordinates()  # array: [label, x, y, size]

        """Canvas"""
        self.canvas = Canvas(width=400, height=400, background="alice blue")
        self.canvas.pack(fill="both", expand=True)

        """Dragging"""
        # this data is used to keep track of an item being dragged
        self._drag_data = {"x": 0, "y": 0, "item": None, "item_last": None}
        # add bindings for clicking, dragging and releasing over any object with the "token" tag
        self.canvas.tag_bind("token", "<ButtonPress-1>", self.drag_start)
        self.canvas.tag_bind("token", "<ButtonRelease-1>", self.drag_stop)
        self.canvas.tag_bind("token", "<B1-Motion>", self.drag)
        self.canvas.bind_all("<MouseWheel>", self.scale_a_blob)

        """Build Blobs"""
        self.blobs = np.empty(len(chars_labels), dtype=Blob)
        for i, c in enumerate(self.coordinates):
            self.blobs[i] = Blob(self, c[0], c[1], c[2], c[3])

        """OK Button"""
        Button(self.root, text='OK', command=self.close, width=int(self.w / 7.2), background='lime green'
               ).place(anchor='center', x=self.x, y=self.h - 50)

        Button(self.root, text='Restart', command=self.restart, width=int(self.w / 7.2), background='brown2'
               ).place(anchor='center', x=self.x, y=self.h - 20)

        self.root.mainloop()

    # create n coordinates of equal distance to middlepoint x|y clockwise
    def create_coordinates(self):
        distance_to_center = min(self.w, self.h) / 4
        # array: [label, x, y, size]
        array = np.empty((len(self.labels), 4), dtype=object)
        degree_delta = 360 / len(self.labels)

        for i, l in enumerate(self.labels):
            degree = i * degree_delta
            g = sin(radians(degree)) * distance_to_center
            a = cos(radians(degree)) * distance_to_center
            array[i, 0] = l
            array[i, 1] = self.x + a
            array[i, 2] = self.y + g
            array[i, 3] = self.image_sizes

        return array

    def find_nearest_blob(self, x, y):
        min_blob, min_distance = (None, self.distance_threashold)
        #min_blob, min_distance = (self.blobs[0], self.blobs[0].get_distance(x, y))
        for i, blob in enumerate(self.blobs):
            d = blob.get_distance(x, y) - blob.size
            if d < min_distance:
                min_blob, min_distance = blob, d
        return min_blob

    def drag_start(self, event):
        """Begining drag of an object"""
        # record the item and its location
        self._drag_data["item"] = self.find_nearest_blob(event.x, event.y)
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
            nearest.scale(up)
            print(nearest.label + " " + str(nearest.size))
        else:
            print("None")

    # calculate and return distance map
    def get(self):
        # TODO: () -> ?
        distance_map = {(()): 1.}

        for i, l in enumerate(self.labels):
            distance_map[i] = "[^" + self.chars[i] + "$]"

        # TODO: costs for insertion (:,0) and deletion (0,:)

        for i, label_i in enumerate(self.labels):
            for j, label_j in enumerate(self.labels):
                if i == j:
                    # (i,j), i==j -> blobsize(i)
                    distance_map[(i + 1, i + 1)] = round((self.blobs[i].get_size() * self.size_factor), 2)
                else:
                    # (i,j), i!=j -> distance ( blob(i), blob(j) )
                    distance_map[(i + 1, j + 1)] = round(
                        (self.blobs[i].get_distance(blob=self.blobs[j]) * self.distance_factor), 2)

        return distance_map

    def close(self):
        self.root.destroy()

    def restart(self):
        chars_labels = self.chars_labels
        self.root.destroy()
        self.__init__(chars_labels)


if __name__ == '__main__':
    # , ["2", "Blab"], ["3", "Blob"], ["4", "Blub"], ["5", "Blöb"], ["6", "Bläb"], ["7", "Blüb"]
    names = np.array([["1", "Digits"], ["1", "Letters"], ["1", "Integers"]], dtype=object)
    print(str(BlobInput(names).get()))
