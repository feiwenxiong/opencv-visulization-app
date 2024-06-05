import cv2
import numpy as np
from .Alg import Alg
class HoughLinesAlg(Alg):
    
    def __init__(self,param_space,image):
        super().__init__(param_space,image)
    
    def process(self):
        image_new = self.image.copy()
        cur_param = self.cur
        gray = cv2.cvtColor(self.image,cv2.COLOR_BGR2GRAY)
        # blurred = cv2.GaussianBlur(gray, (3, 3), 0)
        canny_high_threshold = cur_param["canny_high_threshold"]
        canny_low_threshold = cur_param["canny_low_threshold"]
        votes = cur_param["votes"]
        
        edges = cv2.Canny(gray,
                          canny_low_threshold,
                          canny_high_threshold,
                          apertureSize=3)

        # 使用HoughLines函数检测直线
        lines = cv2.HoughLines(edges,
                               rho=1,
                               theta=np.pi/180,
                               threshold=votes)

        # 确保有直线被检测到
        if lines is not None:
            for line in lines:
                rho, theta = line[0]
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a * rho
                y0 = b * rho
                # 计算直线两端点
                x1 = int(x0 + 1000 * (-b))
                y1 = int(y0 + 1000 * (a))
                x2 = int(x0 - 1000 * (-b))
                y2 = int(y0 - 1000 * (a))

                # 在原图上画出检测到的直线
                cv2.line(image_new, (x1, y1), (x2, y2), (0, 0, 255), 1)
        return  image_new