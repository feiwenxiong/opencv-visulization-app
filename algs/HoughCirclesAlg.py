from .Alg import Alg
import cv2
import numpy as np
class HoughCirclesAlg(Alg):
    def __init__(self,param_space,image):
        super().__init__(param_space,image)
    
    def process(self):
        cur_param = self.cur
        gray = cv2.cvtColor(self.image,cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (3, 3), 0)
        minDist = cur_param["minDist"]
        param1 = cur_param["canny_high_threshold"]
        param2 = cur_param["votes"]
        minRadius = cur_param["minRadius"]
        maxRadius = cur_param["maxRadius"]
        # 使用HoughCircles函数检测圆
        circles = cv2.HoughCircles(blurred, 
                                   cv2.HOUGH_GRADIENT, 
                                   dp=1, 
                                   minDist=minDist,
                                   param1=param1,
                                   param2=param2, 
                                   minRadius=minRadius, 
                                   maxRadius=maxRadius)
        # 确保有圆被检测到
        img_new = self.image.copy()
        if circles is not None:
            # 转换为uint16类型并重塑为(-1, 3)，以便于遍历
            circles = np.round(circles[0, :]).astype("uint16")
            
            # 在原图上画出检测到的圆
            for (x, y, r) in circles:
                cv2.circle(img_new, (x, y), r, (0, 255, 0), 1)
                cv2.circle(img_new, (x, y), 2, (0, 0, 255), 2)
        return  img_new
