import cv2
import matplotlib.pyplot as plt
import numpy as np


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


    def pickCornerPoints(self):

        gathered_points = []
        image_with_selection_points = np.copy(self.calibration_image)

        def click_event(event, x, y, flags, params):
        
            if event == cv2.EVENT_LBUTTONDOWN and len(gathered_points) < 4:
                print(x, ' ',y)
                gathered_points.append((float(x), float(y)))
                cv2.circle(image_with_selection_points, (x, y), radius=5, color=(0, 0, 255), thickness=-1)
                cv2.putText(image_with_selection_points, f"{x} {y}", (x,y),cv2.FONT_HERSHEY_SIMPLEX, 1, (0,10,255), 2)
                cv2.imshow('image', image_with_selection_points)

        

        cv2.imshow('image', image_with_selection_points)

        cv2.setMouseCallback('image', click_event)

        cv2.waitKey(0)

        cv2.destroyAllWindows()

        print(f"Gathered points: {gathered_points}")    
        self.srcPoints = np.asarray(gathered_points, np.float32)

        return image_with_selection_points, len(gathered_points)

#im = cv2.imread("data/undistorted.png")
#w, h = im.shape[0], im.shape[1]
# We will first manually select the source points 
# we will select the destination point which will map the source points in
# original image to destination points in unwarped image



        self.dstPoints = np.float32([(600, 0),
                                     (0, 0),
                                     (0, 531),
                                     (600, 531)])
        print(f"srcPoints: {self.srcPoints}")
        print(f"dstPoints: {self.dstPoints}")

#calibration = Calibration("data/undistorted.png")

#calibration.pickCornerPoints()
#calibration.setTopDownMatrix()
#calibration.topDown()

#cv2.imshow("so", im)
#cv2.waitKey(0)
#cv2.destroyAllWindows()


 #       self.srcPoints = np.float32([(107,     0),
 #                                    (622,  125),
 #                                    (127,  364),
 #                                    (467,    443)])