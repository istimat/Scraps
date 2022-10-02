import tkinter
import tkinter.filedialog
from tkinter import ttk
import os

from controller import Controller


 
class View(ttk.Frame):
    def __init__(self,parent):
    
        super().__init__(parent)
        
        self.controller: Controller = None
        self.window_height = 800
        self.window_width = 800
        self.display_image_width = 750
        self.display_image_height = 500

        self.button_width = 15

        self.image_id = None
        self.current_image = None
 

        imageFrame = tkinter.Frame(self, 
                                   width = self.display_image_width,
                                   height = self.display_image_height,
                                   highlightbackground="blue",
                                   highlightthickness=1,)
        imageFrame.grid(row = 0, column = 1, padx = 10, pady = 10, rowspan=4)

        load_image_buttons_frame = tkinter.Frame(self, width = 200, height = 100,
                                                 highlightbackground="blue",
                                                 highlightthickness=1,)
        load_image_buttons_frame.grid(row = 0, column = 0, padx = 10, pady = 10)
        tkinter.Label(load_image_buttons_frame, text="Load an image").grid(row=0,
                                                                           column=0,
                                                                           padx=10,
                                                                           pady=2,
                                                                           columnspan=3)

        measurement_frame = tkinter.Frame(self, width=200, height=100,
                                          highlightbackground="blue", 
                                          highlightthickness=1,)
        measurement_frame.grid(row=1, column=0, padx=10, pady=10)
        tkinter.Label(measurement_frame, text="Measurements").grid(row=0, 
                                                                     column=0,
                                                                     padx=10,
                                                                     pady=2,
                                                                     columnspan=3)

        config_buttons_frame = tkinter.Frame(self, width = 200, height = 100, 
                                             highlightbackground="blue", 
                                             highlightthickness=1)
        config_buttons_frame.grid(row = 2, column = 0, padx= 10, pady = 10)
        tkinter.Label(config_buttons_frame, text="Calibration").grid(row=0, 
                                                                     column=0,
                                                                     padx=10,
                                                                     pady=2,
                                                                     columnspan=3)
        
        dxf_buttons_frame = tkinter.Frame(self, width = 200, height = 100, 
                                             highlightbackground="blue", 
                                             highlightthickness=1)
        dxf_buttons_frame.grid(row = 3, column = 0, padx= 10, pady = 10, rowspan=2)
        tkinter.Label(dxf_buttons_frame, text="DXF").grid(row=0,
                                                                     column=0,
                                                                     padx=10,
                                                                     pady=2,
                                                                     columnspan=3)

        self.canvas = tkinter.Canvas(imageFrame, width = self.display_image_width, 
                                                 height = self.display_image_height)
        self.canvas.bind("<Button-1>", self.canvas_click)
        self.canvas.bind("<Motion>", self.moved)
        self.canvas.pack()

        self.btn_blur=tkinter.Button(load_image_buttons_frame, text="Blur",
                                     width=self.button_width, command=self.blur_image)
        self.btn_blur.grid(row=1, column=0, padx=5, pady=5)

        self.btn_get_image=tkinter.Button(load_image_buttons_frame, text="Browse",
                                          width=self.button_width, command=self.get_image_file)
        self.btn_get_image.grid(row=1, column=2, padx=5, pady=5)

        tkinter.Label(measurement_frame, text="Horizontal").grid(row=1, 
                                                                   column=0,
                                                                   padx=10,
                                                                   pady=2,
                                                                   columnspan=1)
        tkinter.Label(measurement_frame, text="Vertical").grid(row=1, 
                                                                   column=1,
                                                                   padx=10,
                                                                   pady=2,
                                                                   columnspan=1)

        self.horiz_measurement=tkinter.Text(measurement_frame, height=1, width=10,
                                            highlightbackground="blue",
                                            highlightthickness=1)
        self.horiz_measurement.grid(row=2, column=0,padx=5, pady=1)

        self.vert_measurement=tkinter.Text(measurement_frame, height=1, width=10,
                                           highlightbackground="blue",
                                           highlightthickness=1)
        self.vert_measurement.grid(row=2, column=1,padx=5, pady=1)


        self.btn_choose_points=tkinter.Button(config_buttons_frame, text='Choose points', width=self.button_width, command=self.pick_calibration_points)
        self.btn_choose_points.grid(row=1, column=0, padx=5, pady=5)

        self.btn_top_down=tkinter.Button(config_buttons_frame, text='Top Down', width=self.button_width, command=self.top_down)
        self.btn_top_down.grid(row=1, column=1, padx=5, pady=5)

        self.btn_load_calib=tkinter.Button(config_buttons_frame, text='Load Calibration', width=self.button_width, command=self.load_calibration)
        self.btn_load_calib.grid(row=2, column=0, padx=5, pady=5)

        self.btn_save_calib=tkinter.Button(config_buttons_frame, text='Save Calibration', width=self.button_width, command=self.save_calibration)
        self.btn_save_calib.grid(row=2, column=1, padx=5, pady=5)

        self.btn_contour_detect=tkinter.Button(dxf_buttons_frame, text='Contour', width=self.button_width, command=self.detect_contour)
        self.btn_contour_detect.grid(row=2, column=0, padx=5, pady=5)

        self.btn_dxf=tkinter.Button(dxf_buttons_frame, text='Save DXF', width=self.button_width, command=self.save_dxf)
        self.btn_dxf.grid(row=6, column=0, padx=5, pady=5, columnspan=2)

        self.btn_show_contour=tkinter.Button(dxf_buttons_frame, text='Show Contour', width=self.button_width, command=self.show_contour)
        self.btn_show_contour.grid(row=2, column=1, padx=5, pady=5)

        self.blur_kernel = tkinter.Scale(dxf_buttons_frame, from_=1, to=30,
                                         orient=tkinter.HORIZONTAL, length=180)
        self.blur_kernel.grid(row=3, column=1, columnspan=1)
        self.blur_kernel.set(11)
        tkinter.Label(dxf_buttons_frame, text="Blur Kernel:").grid(row=3, 
                                                                   column=0,
                                                                   padx=1,
                                                                   pady=1)
        self.max_thresh = tkinter.Scale(dxf_buttons_frame, from_=0, to=255, orient=tkinter.HORIZONTAL, length=180)
        self.min_thresh = tkinter.Scale(dxf_buttons_frame, from_=0, to=255, orient=tkinter.HORIZONTAL, length=180)
        self.min_thresh.grid(row=4, column=1, columnspan=1)
        self.min_thresh.set(100)
        tkinter.Label(dxf_buttons_frame, text="Max thresh:").grid(row=4, 
                                                                   column=0,
                                                                   padx=1,
                                                                   pady=1)
        self.max_thresh.grid(row=5, column=1, columnspan=1)
        self.max_thresh.set(200)
        tkinter.Label(dxf_buttons_frame, text="Min thresh:").grid(row=5, 
                                                                   column=0,
                                                                   padx=1,
                                                                   pady=1)

        self.calibration_buttons = [self.btn_choose_points, self.btn_top_down, self.btn_load_calib, self.btn_save_calib]
        
        self.messagebox = tkinter.Text(self, height = 10, width = 105)
        self.messagebox.grid(row=4, column=1, padx=5, pady=5)
        self.messagebox.bind("<1>", lambda event: self.messagebox.focus_set())




    def moved(self, event):
        pass
        #print(f"{event.x}, {event.y}")


    def detect_contour(self):
        if self.controller:
            self.controller.detect_contours()
    
    def save_dxf(self):
        if self.controller:
            self.controller.save_dxf()
        
    def load_calibration(self):
        file = tkinter.filedialog.askopenfilename(parent=self,title='Choose a configuration file', 
                                                  filetypes = (("XML files", "*.xml"),
                                                               ("all files","*.*")), 
                                                  initialdir=os.curdir)
        if self.controller:
            self.controller.load_calibration_file(file)


    def save_calibration(self):
        
        files = [('All Files', '*.*'), 
                 ('XML File', '*.xml')]
                 
        filename = tkinter.filedialog.asksaveasfilename(filetypes = files, defaultextension = files[1])
        
        if self.controller:
            self.controller.save_calibration_file(filename)
            


    def set_controller(self, controller: Controller):
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
                                                        "*.*"),
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
            
    def show_contour(self):
        if self.controller:
            self.controller.show_contour()


