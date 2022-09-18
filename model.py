import cv2
import matplotlib.pyplot as plt
import numpy as np


class Model:

    def __init__(self) -> None:
        pass



class Calibration:

    def __init__(self, image_path) -> None:
        self.image_path = image_path
        self.calibration_image = cv2.imread(image_path)
        self.h, self.w = self.calibration_image.shape[:2]

        self.unwarped_image = None
        self.perspectiveTransform = None
        self.srcPoints = None
        self.dstPoints = None

        self.testing = True
        
    def __repr__(self) -> str:
        return f"{self.image_path!r}"


    def setTopDownMatrix(self):
        
        # use cv2.getPerspectiveTransform() to get the transform matrix
        self.perspectiveTransformMatrix = cv2.getPerspectiveTransform(self.srcPoints, self.dstPoints)
        

    def topDown(self):
        unwarped_image = cv2.warpPerspective(self.calibration_image, self.perspectiveTransformMatrix, (self.w, self.h), flags=cv2.INTER_LINEAR)

        if self.testing:
            f, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))
            f.subplots_adjust(hspace=.2, wspace=.05)
            ax1.imshow(self.calibration_image)
            x = [self.srcPoints[0][0], self.srcPoints[1][0], self.srcPoints[2][0], self.srcPoints[3][0], self.srcPoints[0][0]]
            y = [self.srcPoints[0][1], self.srcPoints[1][1], self.srcPoints[2][1], self.srcPoints[3][1], self.srcPoints[0][1]]
            ax1.plot(x, y, color='red', alpha=0.4, linewidth=3, solid_capstyle='round', zorder=2)
            ax1.set_ylim([self.h, 0])
            ax1.set_xlim([0, self.w])
            ax1.set_title('Original Image', fontsize=30)
            ax2.imshow(cv2.flip(unwarped_image, 1))
            ax2.set_title('Unwarped Image', fontsize=30)
            plt.show()
        
        return unwarped_image


    def pick_point(self, cvimage):

        gathered_point = None

        def click_event(event, x, y, flags, params):
        
            if event == cv2.EVENT_LBUTTONDOWN:
                print(x, ' ',y)
                gathered_point = (float(x), float(y))
                
        cv2.setMouseCallback('image', click_event)

        cv2.waitKey(0)

        print(f"Gathered point: {gathered_point}")    
        self.srcPoints = np.asarray(gathered_point, np.float32)

        return cvimage, self.srcPoints