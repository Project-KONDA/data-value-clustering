from math import sqrt
from PIL import Image, ImageTk



class Blob:
    def __init__(self, blob_input, label, x, y, size, resizable=True):
        self.blob_input = blob_input
        self.label = label
        self.path = "..\\blob_images\\" + (lambda: "" if resizable else "fixed\\")() + label + ".png"
        self.x = x
        self.y = y

        self.resizable = resizable
        self.min_size = 50
        self.default_size = size
        self.size = size
        self.max_size = size * 3

        self.photoimage = None
        self.image = self.create_image()

    # size of a blob
    def get_size(self):
        if self.resizable:
            return self.size - self.min_size
        else:
            return 0.

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
        self.blob_input.canvas.move(self.image, dx, dy)

    def set_position(self, x=0, y=0):
        self.x = x
        self.y = y

    def scale(self, up=True):
        if self.resizable:
            if up:
                self.size = min(self.max_size, self.size + 5)
                # self.size = int(round(self.size * 1.251))
            else:
                self.size = max(self.min_size, self.size - 5)
                # self.size = int(round(self.size / 1.251))
            self.update_image()

    def create_oval(self, color):
        return self.blob_input.canvas.create_oval(
            self.x - 25,
            self.y - 25,
            self.x + 25,
            self.y + 25,
            outline=color,
            fill=color,
            tags="token"
        )

    def create_image(self):
        img = Image.open(self.path)
        img = img.resize((int(self.size * 1.2), self.size), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        # garbage collector defense mechanism
        self.photoimage = img
        return self.blob_input.canvas.create_image(self.x, self.y, image=img, anchor='center', tags=("token",))

    def update_image(self):
        if self.image is not None:
            img = Image.open(self.path)
            img = img.resize((int(self.size * 1.2), int(self.size)), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(img)
            self.photoimage = img  # garbage collector defense mechanism
            self.blob_input.canvas.itemconfig(self.image, image=img)