#实现你的算法
from  .Alg import Alg
import cv2
import numpy as np
class HsvAlg(Alg):
    def __init__(self,param_space,image):
        super().__init__(param_space,image)
        self.image = image  
        self.param_space = param_space
    
    def process(self):
        cur_param = self.cur
        hue,sat,val = cur_param['hue'], cur_param['saturation'], cur_param['value']
        H, S, V = cv2.split(self.image)
        image_new = cv2.merge([np.uint8(H /180 * hue) , np.uint8(S / 255 * sat)  , np.uint8(V / 255 * val)])
        # cv2.imwrite("t.png",image_new)
        return image_new

class HsvAlg2(Alg):
    '''param:{hue_min,hue_max,saturation_min,saturation_max,value_min,value_max}
    '''
    def __init__(self,param_space,image):
        super().__init__(param_space,image)
        self.image = image  
        self.param_space = param_space
    def process(self):
        cur_param = self.cur
        
        lowerbH = cur_param['hue_min']
        lowerbS = cur_param['saturation_min']
        lowerbV = cur_param['value_min']
        upperbH = cur_param['hue_max']
        upperbS = cur_param['saturation_max']
        upperbV = cur_param['value_max']
        mask=cv2.inRange(self.image,(lowerbH,lowerbS,lowerbV),(upperbH,upperbS,upperbV))
        #输入图像与输入图像在掩模条件下按位与，得到掩模范围内的原图像
        image_new=cv2.bitwise_and(self.image,self.image,mask=mask)
        return image_new