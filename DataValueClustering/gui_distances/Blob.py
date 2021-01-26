from math import sqrt
from PIL import Image, ImageTk


class Blob:
    def __init__(self, blob_input, label, regex="", resizable=True, info="", rel_x=0, rel_y=0, rel_size=1):
        self.blob_input = blob_input
        self.label = label
        self.regex = regex
        self.resizable = resizable
        self.info = info
        self.rel_x = rel_x
        self.rel_y = rel_y

        self.sizefactor = min(blob_input.canvas_h, blob_input.canvas_w)
        self.image_sizefactor = self.sizefactor // 8
        self.min_size = 0.5
        self.default_size = 1.0
        self.rel_size = (lambda: rel_size if resizable else 0.5)()
        self.step_size = 0.05
        self.max_size = 5.5  # self.min_size + 100 * self.step_size

        self.path = "..\\gui_distances\\blob_images\\" + (lambda: "" if self.resizable else "fixed\\")() + self.label + ".png"
        self.photo_image = None
        self.image = self.create_image()

    # get matix-value of a blob to itself
    def get_size(self):
        return round((self.rel_size - 0.5) * 2, 1)

    def get_abs_size(self):
        return int(self.rel_size * self.image_sizefactor)

    def get_abs_x(self):
        return self.blob_input.get_absolute_coordinate_value(self.rel_x, True)

    def get_abs_y(self):
        return self.blob_input.get_absolute_coordinate_value(self.rel_y, False)

    # calculate distance to point or blob
    def get_distance(self, abs_x1=0, abs_y1=0, blob=None):
        if blob is None:
            return sqrt((self.get_abs_x() - abs_x1) ** 2 + (self.get_abs_y() - abs_y1) ** 2)
        else:
            return sqrt((self.get_abs_x() - blob.get_abs_x()) ** 2 + (self.get_abs_y() - blob.get_abs_y()) ** 2)

    def move(self, dx=0, dy=0):
        # geht v1
        # self.rel_x += self.blob_input.get_relative_coordinate_value(dx, True, delta=True)
        # self.rel_y += self.blob_input.get_relative_coordinate_value(dy, False, delta=True)

        # geht v2
        # self.rel_x += self.blob_input.get_relative_coordinate_value(0+dx, True)
        # self.rel_x -= self.blob_input.get_relative_coordinate_value(0, True)
        # self.rel_y += self.blob_input.get_relative_coordinate_value(0+dy, False)
        # self.rel_y -= self.blob_input.get_relative_coordinate_value(0, False)

        # geht v3
        self.rel_x = self.blob_input.get_relative_coordinate_value(self.get_abs_x() + dx, x=True)
        self.rel_y = self.blob_input.get_relative_coordinate_value(self.get_abs_y() + dy, x=False)

        self.blob_input.canvas.move(self.image, dx, dy)

    def set_position(self, x=0, y=0):
        self.rel_x = self.blob_input.get_relative_coordinate_value(x, True, diff=False)
        self.rel_y = self.blob_input.get_relative_coordinate_value(y, False, diff=False)

    def scale(self, up=None, reset=False):
        self.lift()
        if self.resizable:
            if reset is True:
                self.rel_size = self.default_size

            elif up is True:
                self.rel_size = min(self.max_size, self.rel_size + self.step_size)
                # self.size = int(round(self.size * 1.251))
            elif up is False:
                self.rel_size = max(self.min_size, self.rel_size - self.step_size)
                # self.size = int(round(self.size / 1.251))
            self.update_image()

    def create_image(self):
        img = Image.open(self.path)
        # img_h, img_w = img.size
        size = self.get_abs_size()
        img = img.resize((size, size), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        self.photo_image = img  # garbage collector defense mechanism
        abs_x = self.blob_input.get_absolute_coordinate_value(self.rel_x)
        abs_y = self.blob_input.get_absolute_coordinate_value(self.rel_y, False)
        return self.blob_input.canvas.create_image(abs_x, abs_y, image=img, anchor='center', tags="token")

    def update_image(self):
        if self.image is not None:
            img = Image.open(self.path)
            size = self.get_abs_size()
            img = img.resize((size, size), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(img)
            self.photo_image = img  # garbage collector defense mechanism
            self.blob_input.canvas.itemconfig(self.image, image=img)

    def lift(self):
        self.blob_input.canvas.lift(self.image)
