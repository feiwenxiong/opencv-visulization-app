from .Alg import Alg
import cv2
class ThreshAlg(Alg):
    def __init__(self,param_space,image):
        super().__init__(param_space,image)

    def process(self):
        cur_param = self.cur
        threshold = cur_param["threshold"] 
        gray = cv2.cvtColor(self.image,cv2.COLOR_BGR2GRAY)
        _, image_new = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
        return image_new