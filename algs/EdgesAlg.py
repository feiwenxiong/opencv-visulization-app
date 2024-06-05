from .Alg import Alg
import cv2
class EdgesAlg(Alg):
    def __init__(self,param_space,image):
        super().__init__(param_space,image)
    
    def process(self):
        cur_param = self.cur
        threshold_low = cur_param["threshold_low"] 
        threshold_high = cur_param["threshold_high"] 
        apertureSize = cur_param["apertureSize"] 
        apertureSize = min(apertureSize if apertureSize % 2 else apertureSize + 1,self.param_space["apertureSize"][1])
        gray = cv2.cvtColor(self.image,cv2.COLOR_BGR2GRAY)
        image_new = cv2.Canny(gray, threshold_low, threshold_high,apertureSize=apertureSize)
        return image_new