from tkinter import *
from PIL import ImageTk, Image
from tkinter import ttk

output = [(),(),(),()]

class ClusterApp():
    root = Tk()
    input = [[], [], [], []]
    looping = True

    def config(self, options_data, options_comp, options_dist, options_clus):
        self.input = [options_data, options_comp, options_dist, options_clus]
        output[0].set(options_data[0])
        output[1].set(options_comp[0])
        output[2].set(options_dist[0])
        output[3].set(options_clus[0])

    def end(self):
        quit()

    def start(self):
        Label(self.root, text="Data: ").grid(row=0, column=0)
        OptionMenu(self.root, output[0], *self.input[0]).grid(row=0, column=1)

        Label(self.root, text="Compression: ").grid(row=1, column=0)
        OptionMenu(self.root, output[1], *self.input[1]).grid(row=1, column=1)

        Label(self.root, text="Distance: ").grid(row=2, column=0)
        OptionMenu(self.root, output[2], *self.input[2]).grid(row=2, column=1)

        Label(self.root, text="Cluster: ").grid(row=3, column=0)
        OptionMenu(self.root, output[3], *self.input[3]).grid(row=3, column=1)

        button = Button(self.root, text='OK', command=lambda: self.end(self))
        button.grid(row=5, column=0)

        Label(self.root, text=self.looping).grid(row=5, column=2)

        self.root.mainloop()


if __name__ == "__main__":
    output = [StringVar(), StringVar(), StringVar(), StringVar()]
    print(output)
    app = ClusterApp
    app.config(app, [0, 1], [0, 1], [0, 1], [0, 1])
    app.start(app)
    print("a")
    print(output)



# window = Tk()
# window.title('Title')
#
# # Drop Down Boxes
# def clicker(event): ()
#
#
# # myLabel = Label(root, text=clicked.get()).pack()
#
# options = range(3)
#
# clicked = StringVar()
# clicked.set(options[0])
#
# drop = OptionMenu(window, clicked, *options, command=clicker)
# drop.pack()
#
#
# def quit(self):
#     self.root.destroy()
#
#
# myButton = Button(window, text="Click Me!", command=window.quit())
# myButton.pack()
#
# window.mainloop()
#
# print(clicked.get())
