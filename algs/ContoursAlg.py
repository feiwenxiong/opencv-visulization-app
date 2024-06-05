from .Alg import Alg
import cv2
import numpy as np
class ContoursAlg(Alg):
    #找轮廓
    def __init__(self,param_space,image):
        super().__init__(param_space,image)
        
    def process(self):
        cur_param = self.cur
        threshold = cur_param["threshold"] 
        minArea = cur_param["minArea"]
        gray = cv2.cvtColor(self.image,cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        image_new = self.image.copy()
        new_contours = []
        for contour in contours:
        #     area = cv2.contourArea(contour)
            rect = cv2.boundingRect(contour)
        #     print(contour)
            area_rect = rect[2] * rect[3]
            #area = cv2.contourArea(contour)
        #     print(area)
            if    area_rect >= minArea: # >16
                new_contours.append(contour)
                # area_lst.append(area_rect)
        cv2.drawContours(image_new,new_contours,-1,(0,0,255),1)  
        # cv2.drawContours(image_new, contours, -1, (255, 0, 0),1)
        return image_new