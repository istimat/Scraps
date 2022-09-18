import cv2
import PIL.Image, PIL.ImageTk
import numpy as np


class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.cvimage = model.calibration_image
        #self.show_image(self.cvimage)

    def cvimage_to_image(self, cvimage):
        
        cvimg = cv2.cvtColor(cvimage, cv2.COLOR_BGR2RGB)
        photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(cvimg))

        return photo

    def pick_calibration_points(self):

        gathered_points = []
        point = None
        image_with_points = np.copy(self.cvimage)
        while len(gathered_points) > 4:
            #point = self.model.pick_point(self.cvimage)
            print(f"Point selected: {point}")
            gathered_points.append(point)

            cv2.circle(image_with_points, point, radius=5, color=(0, 0, 255), thickness=-1)
            cv2.putText(image_with_points, f"{point(0)} {point(1)}", (point(0),point(1)),cv2.FONT_HERSHEY_SIMPLEX, 1, (0,10,255), 2)
            self.show_image(image_with_points)

        
    def show_image(self, cvimage):

        image_to_show = self.cvimage_to_image(cvimage)
        self.view.show_image(image_to_show)


    def save(self, email):
        """
        Save the email
        :param email:
        :return:
        """
        try:

            # save the model
            self.model.email = email
            self.model.save()

            # show a success message
            self.view.show_success(f'The email {email} saved!')

        except ValueError as error:
            # show an error message
            self.view.show_error(error)     