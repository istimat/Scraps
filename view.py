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

        self.button_width = 15

        self.image_id = None
        self.current_image = None
 

        imageFrame = tkinter.Frame(self, width = self.image_width, height = self.image_height, highlightbackground="blue", highlightthickness=1,)
        imageFrame.grid(row = 0, column = 1, padx = 10, pady = 10, rowspan=3)

        load_image_buttons_frame = tkinter.Frame(self, width = 200, height = 100, highlightbackground="blue", highlightthickness=1,)
        load_image_buttons_frame.grid(row = 0, column = 0, padx = 10, pady = 10)
        tkinter.Label(load_image_buttons_frame, text="Load an image").grid(row=0, column=0, padx=10, pady=2, columnspan=3)

        config_buttons_frame = tkinter.Frame(self, width = 200, height = 100, highlightbackground="blue", highlightthickness=1,)
        config_buttons_frame.grid(row = 1, column = 0, padx= 10, pady = 10)
        tkinter.Label(config_buttons_frame, text="Calibration").grid(row=0, column=0, padx=10, pady=2, columnspan=3)

        self.canvas = tkinter.Canvas(imageFrame, width = self.image_width, height = self.image_height)
        self.canvas.bind("<Button-1>", self.canvas_click)
        self.canvas.pack()

        self.btn_blur=tkinter.Button(load_image_buttons_frame, text="Blur", width=self.button_width, command=self.blur_image)
        self.btn_blur.grid(row=1, column=0, padx=5, pady=5)

        self.btn_get_image=tkinter.Button(load_image_buttons_frame, text="Browse", width=self.button_width, command=self.get_image_file)
        self.btn_get_image.grid(row=1, column=2, padx=5, pady=5)

        self.btn_choose_points=tkinter.Button(config_buttons_frame, text='Choose points', width=self.button_width, command=self.pick_calibration_points)
        self.btn_choose_points.grid(row=1, column=0, padx=5, pady=5)

        self.btn_top_down=tkinter.Button(config_buttons_frame, text='Top Down', width=self.button_width, command=self.top_down)
        self.btn_top_down.grid(row=1, column=1, padx=5, pady=5)

        self.btn_load_calib=tkinter.Button(config_buttons_frame, text='Load Calibration', width=self.button_width, command=self.load_calibration)
        self.btn_load_calib.grid(row=2, column=0, padx=5, pady=5)

        self.btn_save_calib=tkinter.Button(config_buttons_frame, text='Save Calibration', width=self.button_width, command=self.save_calibration)
        self.btn_save_calib.grid(row=2, column=1, padx=5, pady=5)


        self.calibration_buttons = [self.btn_choose_points, self.btn_top_down, self.btn_load_calib, self.btn_save_calib]
        
        self.messagebox = tkinter.Text(self, height = 10, width = 50)
        self.messagebox.grid(row=2, column=0, padx=5, pady=5)
        #self.messagebox.insert(tkinter.END,"Message Box")

        
    def load_calibration(self):
        pass

    def save_calibration(self):
        pass    

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
        file = tkinter.filedialog.askopenfilename(parent=self,title='Choose a file', filetypes = (("Image files",
                                                        "*.png"),
                                                       ("all files",
                                                        "*.*")))
        if self.controller:
            self.controller.set_image_file(file)

    def pick_calibration_points(self):
        if self.controller:
            self.controller.set_calibration_mode()

    def top_down(self):
        if self.controller:
            self.controller.top_down()

    def canvas_click(self, event):
        if self.controller:
            self.controller.canvas_click(event)


