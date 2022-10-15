import tkinter as tk
from model import Calibration
from view import View
from controller import Controller

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Scraps')
        self.testing = False
        # create a model
        model = Calibration()

        # create a view and place it on the root window
        view = View(self)
        view.grid(row=0, column=0, padx=10, pady=10)

        # create a controller
        controller = Controller(model, view)

        # set the controller to view
        view.set_controller(controller)

        if self.testing:
            controller.set_image_file("/Users/istimat/Projects/Scraps/data/IMG_2001.jpeg")
            controller.load_calibration_file("/Users/istimat/Projects/Scraps/calibration_2001.xml")
            controller.top_down()

if __name__ == '__main__':
    app = App()
    app.mainloop()  