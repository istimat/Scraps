import cv2
import matplotlib.pyplot as plt
import numpy as np


class Calibration:

    def __init__(self) -> None:
        self.image_path = None
        self.image = None

        self.calibration_file = None
        self.perspectiveTransformMatrix = None

        self.unwarped_image = None
        self.perspectiveTransform = None
        self.srcPoints = None
        self.dstPoints = np.float32([(600, 0),
                                     (0, 0),
                                     (0, 531),
                                     (600, 531)])

        self.testing = False
        self.top_down_image = None

        
    def __repr__(self) -> str:
        return f"{self.image_path!r}"

    def save_calibration(self, filename):
        cv_file = cv2.FileStorage(filename, cv2.FILE_STORAGE_WRITE)
        cv_file.write("my_matrix", self.perspectiveTransformMatrix)
        cv_file.release()

    def read_calibration(self, filename):
        self.calibration_file = filename
        cv_file = cv2.FileStorage(filename, cv2.FILE_STORAGE_READ)
        matrix = cv_file.getNode("my_matrix").mat()
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
        

    def setTopDownMatrix(self):
        self.srcPoints = np.asarray(self.srcPoints, np.float32)

        if self.perspectiveTransformMatrix is None:
            self.perspectiveTransformMatrix = cv2.getPerspectiveTransform(self.srcPoints, self.dstPoints)

        return self.perspectiveTransformMatrix

    def topDown(self):
        w, h = self.image.shape[:2]
        unwarped_image = cv2.warpPerspective(self.image, self.perspectiveTransformMatrix, (w, h), flags=cv2.INTER_LINEAR)

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
