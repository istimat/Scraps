from tokenize import String
from typing import Tuple
import cv2
import matplotlib.pyplot as plt
import numpy as np
import ezdxf

class Calibration:

    def __init__(self) -> None:
        self.image_path = None
        self.image = None

        self.calibration_file = None
        self.perspectiveTransformMatrix = None

        self.unwarped_image = None
        self.perspectiveTransform = None
        self.srcPoints = None
        self.dstPoints = None

        self.testing = False
        self.top_down_image = None
        
        self.detected_contours = None
        self.image_with_contours = None
        self.image_only_contours = None
    

    def save_calibration(self, filename: str):
        
        """saves transformation matrix to xml file.

        Args:
            filename (str): full path and file name.
        """
        cv_file = cv2.FileStorage(filename, cv2.FILE_STORAGE_WRITE)
        cv_file.write("transformation_matrix", self.perspectiveTransformMatrix)
        cv_file.release()


    def read_calibration(self, filename: str):
        
        """loads transformation matrix from xml file.

        Args:
            filename (str): full path and file name.
        """
        self.calibration_file = filename
        cv_file = cv2.FileStorage(filename, cv2.FILE_STORAGE_READ)
        matrix = cv_file.getNode("transformation_matrix").mat()
        #print("read matrix\n", matrix)
        self.perspectiveTransformMatrix = matrix
        cv_file.release()


    def get_image_size(self, image: cv2.Mat) -> Tuple[str, str]:
        
        """Gets the image size of a cv2 image matrix

        Args:
            image (cv2.Mat): cv2 image matrix

        Returns:
            (str, str): width and height of image
        """
        w, h = image.shape[:2]
        return w, h


    def convert_image_to_cv(self, image_path: str):
        
        """Reads an image and creates a cv2 image matrix

        Args:
            image_path (str): path to image
        """
        self.image = cv2.imread(image_path)

        
    def contour_detection(self, image: cv2.Mat, blur_kernel: int, min_thresh: int, max_thresh: int):
        """Draws canny detection contours on given image. 

        Args:
            image (cv2.Mat): cv2 image matrix
        """
        image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(image_gray, (blur_kernel, blur_kernel), 0)
        
        canny = cv2.Canny(blurred, min_thresh, max_thresh)
        self.detected_contours, _ = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        
        self.image_with_contours = np.copy(image)
        width, height = self.get_image_size(image)
        self.image_only_contours = np.zeros((width, height, 3), dtype = "uint8")
        
        _ = cv2.drawContours(self.image_with_contours, self.detected_contours, -1, (0, 255, 0), 2)
        _ = cv2.drawContours(self.image_only_contours, self.detected_contours, -1, (0, 255, 0), 2)
    
    def dxf_generate(self, horiz_meas: str, vert_meas: str):
        """generates dxf file based on previously detected canny edges

        Args:
            horiz_meas (str): horizontal measurement between calibration points
            vert_meas (str): vertical measurement between calibration points
        """
        
        h = int(horiz_meas)
        v = int(vert_meas)
        image_height, image_width = self.get_image_size(self.top_down_image)
        x_scale = h / image_width
        y_scale = v / image_height
        
        dwg = ezdxf.new("R2000")
        msp = dwg.modelspace()
        dwg.layers.new(name="detected contours", dxfattribs={"color": 3})

        squeezed = [np.squeeze(cnt, axis=1) for cnt in self.detected_contours]
        #inversion mirrors along the horizontal axis
        inverted_squeezed = [arr * [1, -1] for arr in squeezed]

        msp.add_lwpolyline([(0, 0),(h, 0),(h, v),(0, v),(0, 0)])
        
        for ctr in inverted_squeezed:
            points = ctr
            scaled_points = []
            for point in points:
                x, y = point
                scaled_x = x * x_scale
                # + v because after mirroring drawing needs to be shifted upwards.
                scaled_y = y * y_scale + v
                scaled_points.append((scaled_x, scaled_y))
                
            msp.add_lwpolyline(scaled_points)      
            
        dwg.saveas("output.dxf")

    def calculate_dest_points(self, horiz_meas: str, vert_meas: str):
        """determines the destination points coordinates for top-down matrix calculation
           Uses the height of the original image and the aspect ratio of measurements
           to determine size of final image.

        Args:
            horiz_meas (str): horizontal measurement between calibration points
            vert_meas (str): vertical measurement between calibration points
        """
        
        h = float(horiz_meas)
        v = float(vert_meas)
        
        aspect_ratio_of_measurement = h/v
        _, img_h = self.get_image_size(self.image)
        
        self.dest_x = int(img_h)
        self.dest_y = int(img_h / aspect_ratio_of_measurement)
        
        self.dstPoints = np.float32([(self.dest_x, 0),
                                     (0, 0),
                                     (0, self.dest_y),
                                     (self.dest_x, self.dest_y)])
        

    def setTopDownMatrix(self) -> cv2.Mat:
        """calculates the top down transformation matrix based on source points 
        and destination points

        Returns:
            cv2.Mat: perspective transform matrix
        """
        self.srcPoints = np.asarray(self.srcPoints, np.float32)

        if self.perspectiveTransformMatrix is None:
            self.perspectiveTransformMatrix = cv2.getPerspectiveTransform(self.srcPoints, self.dstPoints)

        return self.perspectiveTransformMatrix

    def topDown(self):
        """applies the transformation matrix onto the cv2 image.
            ideally creates a top down corrected view.
        """
        unwarped_image = cv2.warpPerspective(self.image, self.perspectiveTransformMatrix,
                                             (self.dest_x, self.dest_y), flags=cv2.INTER_LINEAR)

        if self.testing:
            f, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))
            f.subplots_adjust(hspace=.2, wspace=.05)
            ax1.imshow(self.image)
            x = [self.srcPoints[0][0], self.srcPoints[1][0], self.srcPoints[2][0], self.srcPoints[3][0], self.srcPoints[0][0]]
            y = [self.srcPoints[0][1], self.srcPoints[1][1], self.srcPoints[2][1], self.srcPoints[3][1], self.srcPoints[0][1]]
            ax1.plot(x, y, color='red', alpha=0.4, linewidth=3, solid_capstyle='round', zorder=2)
            ax1.set_ylim([self.h, 0])
            ax1.set_xlim([0, self.w])
            ax1.set_title('Original Image', fontsize=30)
            ax2.imshow(cv2.flip(unwarped_image, 1))
            ax2.set_title('Unwarped Image', fontsize=30)
            plt.show()
        
        self.top_down_image = unwarped_image



