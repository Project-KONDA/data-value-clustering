from tkinter import Tk, Button

import numpy as np


class Blob:
    def __init__(self, frame, label, x, y, size):
        pass

    # size of a blob
    def get_size(self):
        pass

    # calculate distance between blobs
    def get_distance(self, blob2):
        pass


class BlobInput:

    def __init__(self, labels):
        self.root = Tk()
        self.root.title('Please enter Cost Matrix')
        self.root.configure(background='white')

        self.w = 900
        self.h = 700
        self.root.geometry(str(self.w) + "x" + str(self.h))
        self.x = int(self.w / 2)
        self.y = int(self.h / 2)

        self.labels = labels

        # array: [label, x, y, size]
        self.coordinates = self.create_coordinates(self.x, self.y)

        # TODO build blobs
        self.blobs = np.empty(len(labels), dtype=Blob)
        for i, c in enumerate(self.coordinates):
            self.blobs[i] = Blob(self.root, c[0], c[1], c[2], c[3])

        Button(self.root, text='OK', command=self.close, width=int(self.w/7.2), background='white'
               ).place(anchor='center', x=self.x, y=self.h - 20)
        self.root.mainloop()

    # create n coordinates of equal distance to middlepoint x|y clockwise
    def create_coordinates(self, x, y):
        # array: [label, x, y, size]
        array = np.empty((4, len(self.labels)), dtype=object)
        degree = 360 / len(self.labels)

        for i, l in enumerate(self.labels):
            deg = i * degree
            # TODO
            array[i, 0] = l
            array[i, 1] = 10
            array[i, 2] = 10
            array[i, 3] = 10
            # array[i] = [l, 10, 10, 10]

        return array

    # calculate and return distance map
    def get(self):
        # TODO: () -> ?
        distance_map = {(()): 1.}

        for i, l in enumerate(self.labels):
            distance_map[i] = l

        for i in enumerate(self.labels):
            for j in enumerate(self.labels):
                if i == j:
                    # (i,j), i==j -> blobsize(i)
                    distance_map[(i, i)] = self.blobs[i].get_size()
                else:
                    # (i,j), i!=j -> distance ( blob(i), blob(j) )
                    distance_map[(i, j)] = self.blobs[i].get_distance(self.blobs[j])

        return distance_map

    def close(self):
        self.root.destroy()


if __name__ == '__main__':
    names = ["Blib", "Blab", "Blob", "Blub"]
    print(str(BlobInput(names).get()))
