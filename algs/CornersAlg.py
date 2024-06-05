from .Alg import Alg 
import cv2
import numpy as np
class CornersAlg(Alg):
    #角点特征
    def __init__(self,param_space,image):
        super().__init__(param_space,image)
    
    def process(self):
        cur_param = self.cur
        blockSize = cur_param["GradBlockSize"]
        # blockSize = min(blockSize if blockSize % 2  else blockSize + 1,self.param_space["GradBlockSize"][1])
        ksize = cur_param["sobelksize"]
        ksize = min(ksize if ksize % 2  else ksize + 1,self.param_space["sobelksize"][1])
        k = 0.04
        binary_threshold = cur_param["binary_threshold"]
        
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        method = "harris"
        if method == 'harris':
            corners = cv2.cornerHarris(gray, blockSize, ksize, k)
        elif method == 'shi-tomasi':
            corners = cv2.cornerMinEigenVal(gray, blockSize, ksize)
        # 将响应值转换为0-255的范围，便于可视化
        corners = cv2.convertScaleAbs(corners)
        # 应用阈值来筛选角点
        _, corners = cv2.threshold(corners, binary_threshold, 255, cv2.THRESH_BINARY)
        # print(corners)
        #np.where(corners > 0)
        x, y = np.where(corners > 0)
        # 在原图上标出角点
        copy = self.image.copy()
        for pt in zip(x, y):
            cv2.circle(copy, (pt[1], pt[0]), 1, (0, 0, 255), -1)
        return copy