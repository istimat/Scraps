from faulthandler import disable
import cv2
import PIL.Image, PIL.ImageTk
import numpy as np
import tkinter


class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.cvimage = model.image
        self.display_image = np.copy(self.cvimage)
        self.last_clicked_canvas = None
        self.mode_calibration_pick = False
        self.dummy_image = dummy_image = tkinter.PhotoImage(file="data/initial_image.png")
        self.view.show_image(dummy_image)
        self.gathered_points = []
        self.disable_buttons()
        #self.show_image(self.cvimage)

    def disable_buttons(self):
         for button in self.view.calibration_buttons:
            button["state"] = "disabled"

    def set_image_file(self, file):

        self.model.image_path_to_cv(file)
        self.model.image_path = file
        print(self.model.image_path)
        self.display_image = np.copy(self.model.image)
        self.show_image(self.display_image)
        self.view.btn_choose_points["state"] = "normal"
        self.view.btn_load_calib["state"] = "normal"

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
            print("calibration picking reset!")

        self.mode_calibration_pick = True
        print("calibration picking on!")

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
                print("calibration picking off!")
            
            self.model.srcPoints = self.gathered_points
    
    def top_down(self):
        self.model.setTopDownMatrix()
        self.model.topDown()
        self.show_image(self.model.top_down_image)
        self.gathered_points = []
        self.view.btn_top_down["state"] = "disabled"

    def canvas_click(self, event):

        self.last_clicked_canvas = (event.x, event.y)
        self.pick_calibration_points()
