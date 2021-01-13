from math import sin, cos, radians, sqrt
from tkinter import Tk, Button, Canvas, PhotoImage

import numpy as np


class Blob:
    def __init__(self, frame, canvas, label, x, y, size):
        self.frame = frame
        self.canvas = canvas
        self.label = label
        self.x = x
        self.y = y
        self.size = size
        self.oval = self.create_oval("white")
        # self.image = self.create_image()

    # size of a blob
    def get_size(self):
        pass

    # calculate distance to point or blob
    def get_distance(self, x=0, y=0, blob=None):
        if blob is None:
            return sqrt((self.x - x) ** 2 + (self.y - y) ** 2)
        else:
            return sqrt((self.x - blob.x) ** 2 + (self.y - blob.y) ** 2)

    def move(self, dx=0, dy=0):
        self.x += dx
        self.y += dy
        self.canvas.move(self.oval, dx, dy)
        # self.canvas.move(self.image, dx, dy)

    def set_position(self, x=0, y=0):
        self.x = x
        self.y = y

    def scale_up(self):
        pass

    def scale_down(self):
        pass

    def create_oval(self, color):
        return self.canvas.create_oval(
            self.x - 25,
            self.y - 25,
            self.x + 25,
            self.y + 25,
            outline=color,
            fill=color,
            tags=("token",),
        )

    def create_image(self):
        image = PhotoImage(file='...')  # TODO
        return self.canvas.create_image(50, 50, image=image, anchor='center')


class BlobInput:

    def __init__(self, chars_labels):

        self.labels = chars_labels[:, 1]
        self.chars = chars_labels[:, 0]

        self.root = Tk()
        self.root.title('Distance Specification')
        self.root.configure(background='white')

        self.w = 900
        self.h = 700
        self.root.geometry(str(self.w) + "x" + str(self.h))
        self.x = int(self.w / 2)
        self.y = int(self.h / 2)

        # create a canvas
        self.canvas = Canvas(width=400, height=400, background="bisque")
        self.canvas.pack(fill="both", expand=True)

        # this data is used to keep track of an
        # item being dragged
        self._drag_data = {"x": 0, "y": 0, "item": None, "item_last": None}

        # add bindings for clicking, dragging and releasing over
        # any object with the "token" tag
        self.canvas.tag_bind("token", "<ButtonPress-1>", self.drag_start)
        self.canvas.tag_bind("token", "<ButtonRelease-1>", self.drag_stop)
        self.canvas.tag_bind("token", "<B1-Motion>", self.drag)

        # array: [label, x, y, size]
        self.coordinates = self.create_coordinates()
        #print(self.coordinates)

        # build blobs
        self.blobs = np.empty(len(chars_labels), dtype=Blob)
        for i, c in enumerate(self.coordinates):
            self.blobs[i] = Blob(self.root, self.canvas, c[0], c[1], c[2], c[3])

        Button(self.root, text='OK', command=self.close, width=int(self.w/7.2), background='white'
               ).place(anchor='center', x=self.x, y=self.h - 20)

        self.root.mainloop()

    # create n coordinates of equal distance to middlepoint x|y clockwise
    def create_coordinates(self):
        distance_to_center = min(self.w, self.h)/4
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
            array[i, 3] = 10

        return array

    def find_nearest_blob(self, x, y):
        min_blob, min_distance = (self.blobs[0], self.blobs[0].get_distance(x, y))
        for i, blob in enumerate(self.blobs):
            d = blob.get_distance(x,y)
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

    # calculate and return distance map
    def get(self):
        # TODO: () -> ?
        distance_map = {(()): 1.}

        for i, l in enumerate(self.labels):
            distance_map[(i)] = "[^" + self.chars[i] + "$]"

        # TODO: costs for insertion (:,0) and deletion (0,:)

        for i, label_i in enumerate(self.labels):
            for j, label_j in enumerate(self.labels):
                if i == j:
                    # (i,j), i==j -> blobsize(i)
                    distance_map[(i+1, i+1)] = self.blobs[i].get_size()
                else:
                    # (i,j), i!=j -> distance ( blob(i), blob(j) )
                    distance_map[(i+1, j+1)] = self.blobs[i].get_distance(blob=self.blobs[j])

        return distance_map

    def close(self):
        self.root.destroy()


if __name__ == '__main__':
    names = np.array([["1", "Blib"], ["2", "Blab"], ["3", "Blob"], ["4", "Blub"], ["5", "Blöb"], ["6", "Bläb"], ["7", "Blüb"]], dtype=object)
    print(str(BlobInput(names).get()))
