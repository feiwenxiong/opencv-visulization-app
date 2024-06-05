import cv2
import numpy as np
from .Alg import Alg
class ConnectionsAlg(Alg):
    #连通域
    def __init__(self,param_space,image):
        super().__init__(param_space,image)
    
    def process(self):
        cur_param = self.cur
        binary_threshold = cur_param["binary_threshold"] 
        minArea = cur_param["minArea"] 
        gray = cv2.cvtColor(self.image,cv2.COLOR_BGR2GRAY)
        _, binary_image = cv2.threshold(gray, binary_threshold, 255, cv2.THRESH_BINARY)
        # 使用connectedComponents函数找到连通域
        num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(binary_image, connectivity=8)
        colors = np.random.randint(0, 255, size=(num_labels, 3), dtype=np.uint8)
        output = np.zeros(self.image.shape, dtype=np.uint8)
        # 遍历每个连通域并用不同的颜色填充
        # print(stats[1:])
        for label, (x, y, w, h, ele_cnts) in zip(range(1, num_labels), stats[1:]):
            if ele_cnts >= minArea:
                color = colors[label]
                output[y:y+h, x:x+w] = color
        return output