import tkinter
import tkinter.filedialog
from turtle import width
import cv2
import PIL.Image, PIL.ImageTk
from calibrate import Calibration

calibration = Calibration("data/undistorted.png")
 
class App:
    def __init__(self, window, window_title, image_path=calibration.image_path):
        self.window = window
        self.window.title(window_title)
        self.window_height = 600
        self.window_width = 800

        # Load an image using OpenCV
        self.cv_img = cv2.cvtColor(calibration.calibration_image, cv2.COLOR_BGR2RGB)
        self.image_height, self.image_width, no_channels = self.cv_img.shape



        imageFrame = tkinter.Frame(window, width = self.image_width, height = self.image_height, highlightbackground="blue", highlightthickness=1,)
        imageFrame.grid(row = 0, column = 1, padx = 10, pady = 10, rowspan=2)

        load_image_buttons_frame = tkinter.Frame(window, width = 200, height = 100, highlightbackground="blue", highlightthickness=1,)
        load_image_buttons_frame.grid(row = 0, column = 0, padx = 10, pady = 10)
        tkinter.Label(load_image_buttons_frame, text="Load an image").grid(row=0, column=0, padx=10, pady=2, columnspan=3)

        config_buttons_frame = tkinter.Frame(window, width = 200, height = 100, highlightbackground="blue", highlightthickness=1,)
        config_buttons_frame.grid(row = 1, column = 0, padx= 10, pady = 10)

        # Create a canvas that can fit the above image
        self.canvas = tkinter.Canvas(imageFrame, width = self.image_width, height = self.image_height)
        self.canvas.pack()

        # Use PIL (Pillow) to convert the NumPy ndarray to a PhotoImage
        self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(self.cv_img))

        # Add a PhotoImage to the Canvas
        self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)

        

        # Button that lets the user blur the image
        self.btn_blur=tkinter.Button(load_image_buttons_frame, text="Blur", width=10, command=self.blur_image)
        self.btn_blur.grid(row=1, column=0, padx=5, pady=5)

        self.btn_get_image=tkinter.Button(load_image_buttons_frame, text="Browse", width=10, command=self.get_image_file)
        self.btn_get_image.grid(row=1, column=2, padx=5, pady=5)

        self.btn_choose_points=tkinter.Button(config_buttons_frame, text='Choose points', width=10, command=calibration.pickCornerPoints)
        self.btn_choose_points.grid(row=1, column=0, padx=5, pady=5)

        self.window.mainloop()

    # Callback for the "Blur" button
    def blur_image(self):
        self.cv_img = cv2.blur(self.cv_img, (3, 3))
        self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(self.cv_img))
        self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)

    def get_image_file(self):
        file = tkinter.filedialog.askopenfile(parent=self.window,mode='rb',title='Choose a file')
        return file

    def pick_calibration_points(self):
        image, nr_of_gathered_points = calibration.pickCornerPoints()


# Create a window and pass it to the Application object
App(tkinter.Tk(), "Tkinter and OpenCV")