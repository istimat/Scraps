import cv2
import matplotlib.pyplot as plt
import numpy as np


class Calibration:

    def __init__(self, image_path) -> None:
        self.calibration_image = cv2.imread(image_path)
        self.perspectiveTransform = ''
        self.srcPoints = np.float32([(107,     0),
                                     (622,  125),
                                     (127,  364),
                                     (467,    443)])

        self.dstPoints = np.float32([(600, 0),
                                     (0, 0),
                                     (600, 531),
                                     (0, 531)])
        self.testing = True
        self.h, self.w = self.calibration_image.shape[:2]



    def setTopDownMatrix(self):
        
        # use cv2.getPerspectiveTransform() to get the transform matrix
        self.perspectiveTransformMatrix = cv2.getPerspectiveTransform(self.srcPoints, self.dstPoints)
        

    def topDown(self):
        unwarped_image = cv2.warpPerspective(self.calibration_image, self.perspectiveTransformMatrix, (self.w, self.h), flags=cv2.INTER_LINEAR)

        if self.testing:
            f, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))
            f.subplots_adjust(hspace=.2, wspace=.05)
            ax1.imshow(self.calibration_image)
            x = [self.srcPoints[0][0], self.srcPoints[2][0], self.srcPoints[3][0], self.srcPoints[1][0], self.srcPoints[0][0]]
            y = [self.srcPoints[0][1], self.srcPoints[2][1], self.srcPoints[3][1], self.srcPoints[1][1], self.srcPoints[0][1]]
            ax1.plot(x, y, color='red', alpha=0.4, linewidth=3, solid_capstyle='round', zorder=2)
            ax1.set_ylim([self.h, 0])
            ax1.set_xlim([0, self.w])
            ax1.set_title('Original Image', fontsize=30)
            ax2.imshow(cv2.flip(unwarped_image, 1))
            ax2.set_title('Unwarped Image', fontsize=30)
            plt.show()
        
        return unwarped_image


#im = cv2.imread("data/undistorted.png")
#w, h = im.shape[0], im.shape[1]
# We will first manually select the source points 
# we will select the destination point which will map the source points in
# original image to destination points in unwarped image


calibration = Calibration("data/undistorted.png")

calibration.setTopDownMatrix()
calibration.topDown()

#cv2.imshow("so", im)
cv2.waitKey(0)[[1]][1]
cv2.destroyAllWindows()