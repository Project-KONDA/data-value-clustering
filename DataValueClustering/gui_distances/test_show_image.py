from tkinter import Tk, PhotoImage, Canvas
import PIL
import PIL.Image
import PIL.ImageTk
from PIL import Image, ImageTk

if __name__ == '__main__':

    root = Tk()

    """Canvas"""
    canvas = Canvas(root, width=1000, heigh=1000, bg='white')
    canvas.pack(pady=20)

    """Image"""
    path = "..\\blob_images\Digits.png"
    img = Image.open(path)
    img = img.resize((119, 100), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)

    # img = PhotoImage(file="..\\blob_images\Digits.png")
    # img = img.resize((200, 200), resample=0)
    my_image = canvas.create_image(200, 200, image=img)

    root.mainloop()
