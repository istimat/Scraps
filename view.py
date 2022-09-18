import tkinter
import tkinter.filedialog
from tkinter import ttk
from turtle import width
import cv2

from model import Calibration

#calibration = Calibration("data/undistorted.png")
 
class View(ttk.Frame):
    #def __init__(self,parent, window, window_title, image_path):
    def __init__(self,parent):
    
        super().__init__(parent)
        
        self.controller = None
        #self.window.title(window_title)
        self.window_height = 600
        self.window_width = 800
        #self.image_path = image_path
        self.image_width = 600
        self.image_height = 400

        self.image_id = None
        self.current_image = None
        # Load an image using OpenCV
        
        #self.image_height, self.image_width, no_channels = self.cv_img.shape



        imageFrame = tkinter.Frame(self, width = self.image_width, height = self.image_height, highlightbackground="blue", highlightthickness=1,)
        imageFrame.grid(row = 0, column = 1, padx = 10, pady = 10, rowspan=2)

        load_image_buttons_frame = tkinter.Frame(self, width = 200, height = 100, highlightbackground="blue", highlightthickness=1,)
        load_image_buttons_frame.grid(row = 0, column = 0, padx = 10, pady = 10)
        tkinter.Label(load_image_buttons_frame, text="Load an image").grid(row=0, column=0, padx=10, pady=2, columnspan=3)

        config_buttons_frame = tkinter.Frame(self, width = 200, height = 100, highlightbackground="blue", highlightthickness=1,)
        config_buttons_frame.grid(row = 1, column = 0, padx= 10, pady = 10)

        self.canvas = tkinter.Canvas(imageFrame, width = self.image_width, height = self.image_height)
        self.canvas.bind("<Button-1>", self.canvas_click)
        self.canvas.pack()

        self.btn_blur=tkinter.Button(load_image_buttons_frame, text="Blur", width=10, command=self.blur_image)
        self.btn_blur.grid(row=1, column=0, padx=5, pady=5)

        self.btn_get_image=tkinter.Button(load_image_buttons_frame, text="Browse", width=10, command=self.get_image_file)
        self.btn_get_image.grid(row=1, column=2, padx=5, pady=5)

        self.btn_choose_points=tkinter.Button(config_buttons_frame, text='Choose points', width=10, command=self.pick_calibration_points)
        self.btn_choose_points.grid(row=1, column=0, padx=5, pady=5)

        #self.dummy_image = dummy_image = tkinter.PhotoImage(file="data/initial_image.png")
        #self.show_image(dummy_image)
        

    def set_controller(self, controller):
        """
        Set the controller
        :param controller:
        :return:
        """
        self.controller = controller

    def show_image(self, image):
        self.current_image = image
        self.image_id = self.canvas.create_image(0, 0, image=image, anchor=tkinter.NW)
        self.canvas.update()

    def update_image(self, new_image):
        self.current_image = new_image
        self.canvas.itemconfig(self.image_id, image = new_image)
        self.canvas.update()
        print(self.image_id)

    # Callback for the "Blur" button
    def blur_image(self):
        pass

    def get_image_file(self):
        file = tkinter.filedialog.askopenfile(parent=self,mode='rb',title='Choose a file')
        return file

    def pick_calibration_points(self):
        if self.controller:
            self.controller.set_calibration_mode()

    def canvas_click(self, event):
        if self.controller:
            self.controller.canvas_click(event)


