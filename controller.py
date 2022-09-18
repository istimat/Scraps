import cv2
import PIL.Image, PIL.ImageTk
import numpy as np
import tkinter


class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.cvimage = model.calibration_image
        self.display_image = np.copy(self.cvimage)
        self.last_clicked_canvas = None
        self.mode_calibration_pick = False
        self.dummy_image = dummy_image = tkinter.PhotoImage(file="data/initial_image.png")
        self.view.show_image(dummy_image)
        self.gathered_points = []
        #self.show_image(self.cvimage)

    def cvimage_to_image(self, cvimage):
        
        cvimg = cv2.cvtColor(cvimage, cv2.COLOR_BGR2RGB)
        photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(cvimg))

        return photo

    def set_calibration_mode(self):
        self.mode_calibration_pick = True
        print("calibration picking on!")

    def pick_calibration_points(self):

        if self.mode_calibration_pick:
            #gathered_points = []

            #point = self.model.pick_point(self.cvimage)
            if self.last_clicked_canvas is not None:
                point = self.last_clicked_canvas
                
                self.gathered_points.append(point)
                print(f"Points selected: {self.gathered_points}")
                cv2.circle(self.display_image, point, radius=5, color=(0, 0, 255), thickness=-1)
                cv2.putText(self.display_image, f"{point[0]} {point[1]}", (point[0],point[1]),cv2.FONT_HERSHEY_SIMPLEX, 1, (0,10,255), 2)
                self.show_image(self.display_image)

            if len(self.gathered_points) == 4:
                self.mode_calibration_pick = False
                print("calibration picking off!")

        
    def show_image(self, cvimage):

        image_to_show = self.cvimage_to_image(cvimage)
        self.view.update_image(image_to_show)

    def canvas_click(self, event):
        print ("clicked at", event.x, event.y)
        self.last_clicked_canvas = (event.x, event.y)
        self.pick_calibration_points()
