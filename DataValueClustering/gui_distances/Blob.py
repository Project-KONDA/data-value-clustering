from math import sqrt
from PIL import Image, ImageTk


class Blob:
    def __init__(self, blob_input, label, x, y, size, resizable=True, info=""):
        self.blob_input = blob_input
        self.label = label
        self.info = info
        self.path = "blob_images\\" + (lambda: "" if resizable else "fixed\\")() + label + ".png"
        self.x = x
        self.y = y

        self.resizable = resizable
        self.min_size = 50
        self.default_size = size
        self.size = (lambda: size if resizable else self.min_size)()
        self.step_size = self.default_size // 20
        self.min_size = size - 10 * self.step_size
        self.max_size = size * 5

        self.photo_image = None
        self.image = self.create_image()

    # size of a blob
    def get_size(self):
        if self.resizable:
            return (self.size - self.min_size) / (10 * self.step_size)
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

    def scale(self, up=None, reset=False):
        self.lift()
        if self.resizable:
            if reset is True:
                self.size = self.default_size

            elif up is True:
                self.size = min(self.max_size, self.size + self.step_size)
                # self.size = int(round(self.size * 1.251))
            elif up is False:
                self.size = max(self.min_size, self.size - self.step_size)
                # self.size = int(round(self.size / 1.251))
            self.update_image()

    def create_image(self):
        img = Image.open(self.path)
        img_h, img_w = img.size
        img_w2 = self.size * img_h // img_w
        img = img.resize((img_w2, self.size), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        # garbage collector defense mechanism
        self.photo_image = img
        return self.blob_input.canvas.create_image(self.x, self.y, image=img, anchor='center', tags="token")

    def update_image(self):
        if self.image is not None:
            img = Image.open(self.path)
            img = img.resize((self.size, self.size), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(img)
            self.photo_image = img  # garbage collector defense mechanism
            self.blob_input.canvas.itemconfig(self.image, image=img)

    def lift(self):
        self.blob_input.canvas.lift(self.image)
