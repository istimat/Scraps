from __future__ import annotations
from symbol import yield_expr
from typing import Tuple
from faulthandler import disable
import cv2
import PIL.Image, PIL.ImageTk
import numpy as np
import tkinter
import math

#trick to avoid circular import but allow type hinting for intellisence
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from model import Calibration
    from view import View


class Controller:
    def __init__(self, model: Calibration, view: View):
        self.model = model
        self.view = view
        self.messagebox = MessageBox(view)
        self.measure = Measure(self, view, model)
        
        self.cvimage = model.image
        self.display_image = np.copy(self.cvimage)
        self.display_image_scaled = None
        self.display_image_scale = None
        self.last_clicked_canvas = None
        self.mode_calibration_pick = False
        self.dummy_image = dummy_image = tkinter.PhotoImage(file="data/initial_image_500px.png")
        self.view.show_image(dummy_image)
        self.view.horiz_measurement.insert(tkinter.END, "600")
        self.view.vert_measurement.insert(tkinter.END, "400")
        self.gathered_points = []
        self.disable_buttons()
        self.contour_toggle = False
        self.zoom_image_id = None
        self.zoom_image = None
    
    
    def show_zoom_image(self, image: cv2.Mat) -> Tuple(int, int):
        """Ahows unscaled image in smaller window, like a magnifying glass
           Adds a crosshair on top of image
        """
           
        self.zoom_image = self.cvimage_to_image(image)
        self.zoom_image_id = self.view.zoom_window.create_image(0, 0, image=self.zoom_image, anchor=tkinter.NW)
        self.crosshair = PIL.ImageTk.PhotoImage(file="data/crosshair_green_100px.png")
        self.crosshair_id = self.view.zoom_window.create_image(100,100, anchor=tkinter.CENTER, image=self.crosshair) 
        self.view.zoom_window.update()
        
        return self.zoom_image_id, self.crosshair_id
    
    def update_zoom_image(self, event: tkinter.Event):
        """ 
        Every mouse hover event on large image translates zoomed image
            Crosshair is translated in the opposite direction
        """
        
        if self.display_image_scale is not None:
            x = int(event.x*-self.display_image_scale)+100
            y = int(event.y*-self.display_image_scale)+100
            self.view.zoom_window.scan_dragto(x, y, gain=1)
            self.view.zoom_window.coords(self.crosshair_id, 
                                         int(event.x*self.display_image_scale),
                                         int(event.y*self.display_image_scale))

            self.view.zoom_window.update()

    
    def show_contour(self) -> bool:
        """ 
        Hides or shows the image underneath the detected contours
        for better visualization
        """
        
        if self.contour_toggle == True:
            self.set_display_image(self.model.image_with_contours)
            self.contour_toggle = False
        else:
            self.set_display_image(self.model.image_only_contours)
            self.contour_toggle = True
        
        return self.contour_toggle
    
    def detect_contours(self, min_thresh: int, max_thresh: int, blur_kernel: int) -> cv2.Mat:
        """ 
        Detects contours based on threshold values and blur kernel size
        """
        
        self.model.contour_detection(self.model.top_down_image,
                                     blur_kernel,
                                     min_thresh,
                                     max_thresh)
        self.set_display_image(self.model.image_with_contours)
        self.messagebox.show(f"Edge detection run with minimun threshold {min_thresh} and maximum {max_thresh}")
        
        return self.model.image_with_contours
    
    def set_dxf_path(self, path: str):
        
        self.model.dxf_path = path
        return path
        
    def save_dxf(self):
        self.model.dxf_generate(self.view.horiz_measurement.get("1.0",'end-1c'),
                                self.view.vert_measurement.get("1.0",'end-1c'))
        self.messagebox.show(f"DXF file saved!")
        

    def save_calibration_file(self, filename):
        self.model.save_calibration(filename)
        self.messagebox.show(f"Calibration file {filename} saved.")


    def load_calibration_file(self, file):
        self.model.read_calibration(file)
        self.view.btn_top_down["state"] = "normal"
        self.messagebox.show(f"Calibration file {self.model.calibration_file} loaded.")
        

    def disable_buttons(self):
         for button in self.view.calibration_buttons:
            button["state"] = "disabled"

    def set_display_image(self, image):
        self.display_image = np.copy(image)
        self.scale_display_image(image)
        self.show_image(self.display_image_scaled)
        self.show_zoom_image(self.display_image)
        

    def set_image_file(self, file):

        self.model.convert_image_to_cv(file)
        self.model.image_path = file
        self.set_display_image(self.model.image)
        self.view.btn_choose_points["state"] = "normal"
        self.view.btn_load_calib["state"] = "normal"
        self.messagebox.show(f"File: {self.model.image_path} loaded.")

    def scale_display_image(self, image):
        height, width = self.model.get_image_size(image)
        self.messagebox.show(f"display image width: {width}")
        self.messagebox.show(f"display image height: {height}")

        aspect_ratio_of_image = width / height
        
        new_width = int(self.view.display_image_height * aspect_ratio_of_image)
        new_height = self.view.display_image_height

        self.display_image_scale = height / new_height
        self.messagebox.show(f"display image scaled to: {new_width} X {new_height}")
        self.display_image_scaled = cv2.resize(self.display_image, (new_width, new_height), interpolation=cv2.INTER_CUBIC)


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
        self.model.perspectiveTransformMatrix = None
        self.messagebox.show("calibration picking on!")

    def pick_calibration_points(self):

        if self.mode_calibration_pick:
            if self.last_clicked_canvas is not None:
                point = self.last_clicked_canvas
                
                self.gathered_points.append(point)
                cv2.circle(self.display_image_scaled, point, radius=5, color=(0, 0, 255), thickness=-1)
                #cv2.putText(self.display_image_scaled, f"{point[0]} {point[1]}", (point[0],point[1]),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,10,255), 2)
                self.show_image(self.display_image_scaled)

            if len(self.gathered_points) == 4:
                self.mode_calibration_pick = False
                self.view.btn_top_down["state"] = "normal"
                self.view.btn_save_calib["state"] = "normal"
                self.messagebox.show("calibration picking done!")
            
            rescaled_points = self.rescale_picked_points(self.gathered_points)
            self.model.srcPoints = rescaled_points
            self.messagebox.show(f"Source points: \n {self.model.srcPoints}")

    def rescale_picked_points(self, point_list):
        rescaled_list = []
        for point in point_list:
            x, y = point
            x = x * self.display_image_scale
            y = y * self.display_image_scale

            rescaled_list.append((x,y))
        return rescaled_list



    def top_down(self):
        self.model.calculate_dest_points(self.view.horiz_measurement.get("1.0",'end-1c'),
                                         self.view.vert_measurement.get("1.0",'end-1c'))
        matrix = self.model.setTopDownMatrix()
        #self.messagebox.show(f"Perspective transformation matrix: {matrix}")
        self.model.topDown()
        self.set_display_image(self.model.top_down_image)
        self.gathered_points = []
        self.view.btn_top_down["state"] = "disabled"
        self.messagebox.show("Top Down correction done.")
        self.messagebox.show(f"destination points: {self.model.dstPoints}")

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

class Measure:
    def __init__(self, controller: Controller, view: View, model: Calibration) -> None:
        self.controller = controller
        self.view = view
        self.model = model
        self.measuring = False
        self.picked_points = []
        self.measurement_points = []
        self.image_with_measurement = None
        
    def mode_toggle(self):
        if not self.measuring:
            self.measuring = True
            self.image_with_measurement =  np.copy(self.controller.display_image_scaled)
            self.controller.show_image(self.image_with_measurement)
            self.controller.messagebox.show(f"Measurement mode on!")
        else:
            self.measuring = False
            self.controller.show_image(self.controller.display_image_scaled)
            self.reset_measurement()
            self.controller.messagebox.show(f"Measurement mode off!")
    
    def reset_measurement(self):
        self.picked_points = []
        self.measurement_points = []
        self.image_with_measurement = None
        
    def get_picked_point(self, event: tkinter.Event):
        if self.measuring:
            x, y = self.rescale_point(int(event.x), (event.y))
            self.picked_points.append((event.x, event.y))
            
            x_coord, y_coord = self.point_to_mm(self.controller.display_image, x, y)
            self.measurement_points.append((x_coord,y_coord))
            #print(f"x: {x_coord}, y: {y_coord}")
            
            distance = self.calculate_measurement()
            self.draw_measurement(self.image_with_measurement, self.picked_points, distance)
            
            cv2.circle(self.image_with_measurement, (event.x, event.y), radius=5, color=(0, 0, 255), thickness=-1)
            self.controller.show_image(self.image_with_measurement)
            
            return x_coord, y_coord
        
    def draw_measurement(self, image, points, distance):
        cv2.circle(image, points[-1], radius=5, color=(0, 0, 255), thickness=-1)
        if len(points) > 1:
            cv2.line(image, points[-1], points[-2], (0, 255, 0), 2, 1)
            cv2.getTextSize()
            midpoint = self.calculate_half_way_point(points[-1],points[-2])
            cv2.putText(image, f"{distance:.1f} mm",
                                 midpoint,
                                 cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,10,255), 2)
            self.controller.messagebox.show(f"Last measurement = {distance:.1f} mm")
        self.controller.show_image(image)
    
    @staticmethod
    def calculate_half_way_point(point_a: Tuple, point_b: Tuple) -> Tuple:
        x1, y1 = point_a
        x2, y2 = point_b
        
        x = (x1 + x2)/2
        y = (y1 + y2)/2

        return (int(x), int(y))
    
    def calculate_measurement(self):
        if len(self.measurement_points) > 1:
            distance = math.dist(self.measurement_points[-1],self.measurement_points[-2])
            print(distance)

            return distance
            
            
    
    def rescale_point(self, x, y):
        x = x * self.controller.display_image_scale
        y = y * self.controller.display_image_scale
        
        return int(x), int(y)
    
    def point_to_mm(self, image, x, y):
        image_height, image_width = self.model.get_image_size(image)
        
        h = self.view.horiz_measurement.get("1.0",'end-1c')
        v = self.view.vert_measurement.get("1.0",'end-1c')
        
        x_scale = int(h) / image_width
        y_scale = int(v) / image_height
        
        return x * x_scale, y * y_scale