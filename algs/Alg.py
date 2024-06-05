from abc import ABC,abstractmethod
class Alg(ABC):
    def __init__(self, param_space,image):
        self.param_space= param_space
        self.default = { k:(v[0] + v[1]) // 2 for k,v in param_space.items()} #default
        self.cur = self.default.copy()
        self.image = image
    
    
    @abstractmethod
    def process(self,):
        pass
