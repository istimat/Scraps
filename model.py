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

        
    def __repr__(self) -> str:
        return f"{self.image_path!r}"

    def save_calibration(self, filename):
        cv_file = cv2.FileStorage(filename, cv2.FILE_STORAGE_WRITE)
        cv_file.write("transformation_matrix", self.perspectiveTransformMatrix)
        cv_file.release()

    def read_calibration(self, filename):
        self.calibration_file = filename
        cv_file = cv2.FileStorage(filename, cv2.FILE_STORAGE_READ)
        matrix = cv_file.getNode("transformation_matrix").mat()
        print("read matrix\n", matrix)
        self.perspectiveTransformMatrix = matrix
        cv_file.release()


    def get_image_size(self, image):
        w, h = image.shape[:2]
        return w, h

    def image_path_to_cv(self, image_path):

        self.image = cv2.imread(image_path)
        _image = np.array(self.image).astype('uint8')
        #self.image = cv2.resize(_image, self.view_resolution, interpolation=cv2.INTER_CUBIC)
        
    def contour_detection(self):
        canny = cv2.Canny(self.top_down_image, 100, 200)
        self.detected_contours, hierarchy = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        contours_draw = cv2.drawContours(self.top_down_image, self.detected_contours, -1, (0, 255, 0), 2)
    
    def dxf_generate(self, horiz_meas, vert_meas):
        h = int(horiz_meas)
        v = int(vert_meas)
        dwg = ezdxf.new("R2000")
        msp = dwg.modelspace()
        dwg.layers.new(name="detected contours", dxfattribs={"color": 3})

        squeezed = [np.squeeze(cnt, axis=1) for cnt in self.detected_contours]

        msp.add_lwpolyline([(0, 0),(0, h),(v, h),(v, 0)])
        
        for ctr in squeezed:
            points = ctr
            msp.add_lwpolyline(points)      
            
            # for n in range(len(ctr)):
            #     if n >= len(ctr) - 1:
            #         n = 0
            #     try:
            #         msp.add_line(ctr[n], ctr[n + 1], dxfattribs={"layer": "greeny green lines", "lineweight": 20})
            #     except IndexError:
            #         pass

        dwg.saveas("output.dxf")

    def calculate_dest_points(self, horiz, vert):
        
        h = float(horiz)
        v = float(vert)
        
        aspect_ratio_of_measurement = h/v
        _, img_h = self.get_image_size(self.image)
        
        self.dest_x = int(img_h)
        self.dest_y = int(img_h / aspect_ratio_of_measurement)
        
        self.dstPoints = np.float32([(self.dest_x, 0),
                                     (0, 0),
                                     (0, self.dest_y),
                                     (self.dest_x, self.dest_y)])
        print(self.dstPoints)
        

    def setTopDownMatrix(self):
        self.srcPoints = np.asarray(self.srcPoints, np.float32)

        if self.perspectiveTransformMatrix is None:
            self.perspectiveTransformMatrix = cv2.getPerspectiveTransform(self.srcPoints, self.dstPoints)

        return self.perspectiveTransformMatrix

    def topDown(self):
        #w, h = self.image.shape[:2]
        unwarped_image = cv2.warpPerspective(self.image, self.perspectiveTransformMatrix, (self.dest_x, self.dest_y), flags=cv2.INTER_LINEAR)

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


    def pick_point(self, cvimage):

        gathered_point = None

        def click_event(event, x, y, flags, params):
        
            if event == cv2.EVENT_LBUTTONDOWN:
                print(x, ' ',y)
                gathered_point = (float(x), float(y))
                
        cv2.setMouseCallback('image', click_event)

        cv2.waitKey(0)

        print(f"Gathered point: {gathered_point}")    
        

        return cvimage, self.srcPoints
