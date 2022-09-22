from faulthandler import disable
import cv2
import PIL.Image, PIL.ImageTk
import numpy as np
import tkinter
from model import Calibration

from view import View


class Controller:
    def __init__(self, model: Calibration, view: View):
        self.model = model
        self.view = view
        self.messagebox = MessageBox(view)

        self.cvimage = model.image
        self.display_image = np.copy(self.cvimage)
        self.display_image_scale = None
        self.last_clicked_canvas = None
        self.mode_calibration_pick = False
        self.dummy_image = dummy_image = tkinter.PhotoImage(file="data/initial_image_500px.png")
        self.view.show_image(dummy_image)
        self.gathered_points = []
        self.disable_buttons()
        

    def save_calibration_file(self):
        self.model.save_calibration("calibration.xml")


    def load_calibration_file(self, file):
        self.model.read_calibration(file)
        self.view.btn_top_down["state"] = "normal"
        self.messagebox.show(f"Calibration file {self.model.calibration_file} loaded.")
        

    def disable_buttons(self):
         for button in self.view.calibration_buttons:
            button["state"] = "disabled"

    def set_image_file(self, file):

        self.model.image_path_to_cv(file)
        self.model.image_path = file
        print(self.model.image_path)
        self.display_image = np.copy(self.model.image)
        self.scale_display_image()
        self.show_image(self.display_image)
        self.view.btn_choose_points["state"] = "normal"
        self.view.btn_load_calib["state"] = "normal"
        self.messagebox.show(f"File: {self.model.image_path} loaded.")

    def scale_display_image(self):
        width, height = self.model.get_image_size(self.display_image)
        self.messagebox.show(f"display image width: {width}")
        self.messagebox.show(f"display image height: {height}")

        scale_h = self.view.image_height / height
        self.display_image_scale = scale_w = scale_h

        new_width = int(scale_w * width)
        new_height = int(scale_h * height)

        self.messagebox.show(f"display image scaled to: {new_width} X {new_height}")
        self.display_image = cv2.resize(self.display_image, (new_height, new_width), interpolation=cv2.INTER_CUBIC)


    def cvimage_to_image(self, cv_image):
        
        cvimg = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(cvimg))

        return photo

    def show_image(self, cv_image):

        image_to_show = self.cvimage_to_image(cv_image)
        self.view.update_image(image_to_show)

    def set_calibration_mode(self):
        if len(self.gathered_points):    
            self.model.srcPoints = None
            self.gathered_points = []
            self.set_image_file(self.model.image_path)
            self.view.btn_top_down["state"] = "disabled"
            self.messagebox.show("calibration picking reset!")

        self.mode_calibration_pick = True
        self.messagebox.show("calibration picking on!")

    def pick_calibration_points(self):

        if self.mode_calibration_pick:
            if self.last_clicked_canvas is not None:
                point = self.last_clicked_canvas
                
                self.gathered_points.append(point)
                print(f"Points selected: {self.gathered_points}")
                cv2.circle(self.display_image, point, radius=5, color=(0, 0, 255), thickness=-1)
                cv2.putText(self.display_image, f"{point[0]} {point[1]}", (point[0],point[1]),cv2.FONT_HERSHEY_SIMPLEX, 1, (0,10,255), 2)
                self.show_image(self.display_image)

            if len(self.gathered_points) == 4:
                self.mode_calibration_pick = False
                self.view.btn_top_down["state"] = "normal"
                self.view.btn_save_calib["state"] = "normal"
                self.messagebox.show("calibration picking done!")
            
            rescaled_points = self.rescale_picked_points(self.gathered_points)
            self.model.srcPoints = rescaled_points

    def rescale_picked_points(self, point_list):
        rescaled_list = []
        for point in point_list:
            x, y = point
            x = x * 1/self.display_image_scale
            y = y * 1/self.display_image_scale

            rescaled_list.append((x,y))
        return rescaled_list

    def top_down(self):
        matrix = self.model.setTopDownMatrix()
        self.messagebox.show(f"Perspective transformation matrix: {matrix}")
        self.model.topDown()
        self.show_image(self.model.top_down_image)
        self.gathered_points = []
        self.view.btn_top_down["state"] = "disabled"
        self.messagebox.show("Top Down correction done.")

    def canvas_click(self, event):

        self.last_clicked_canvas = (event.x, event.y)
        self.pick_calibration_points()

class MessageBox:
    def __init__(self, view) -> None:
        self.view = view

    def show(self, message):
        self.view.messagebox.configure(state="normal")
        self.view.messagebox.insert(tkinter.END, f"{message} \n")
        self.view.messagebox.see("end")
        self.view.messagebox.configure(state="disabled")
