import numpy as np
from abc import ABC,abstractmethod
import tkinter as tk
from tkinter import ttk,messagebox
import cv2
from PIL import Image,ImageTk
from algs import *
from utils import bgr2tkPhoto
################################################################################################################
################################################################################################################
################################################################################################################
################################################################################################################
#utils
'''
通过参数空间生成滑块
这事处理后的图片
'''

def open_image():
    path = entry.get()
    if path:
        try:
            global image
            img = cv2.imread(path)
            MAX_WIDTH = 800
            MAX_HEIGHT = 600
            width, height = img.shape[1], img.shape[0]
            scale_factor = min(MAX_WIDTH / width, MAX_HEIGHT / height)
            new_width, new_height = int(width * scale_factor), int(height * scale_factor)
            resized_img = cv2.resize(img, (new_width, new_height))
            img = resized_img
            image = img.copy()
            if img is not None:
                img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                img_pil = Image.fromarray(img_rgb)
                img_tk = ImageTk.PhotoImage(image=img_pil)
                image_label.config(image=img_tk)
                image_label.image = img_tk  # 保持引用，防止图像被垃圾回收
                
                # 遍历所有Tab并更新图片显示
                for tab_id in notebook.tabs():
                    tab_frame = notebook.nametowidget(tab_id)
                    sliders_container = tab_frame.winfo_children()[0]
                    print(f"Updating image for Tab: {tab_id}")
                    if isinstance(sliders_container, Sliders):  # 现在这应该为True
                        # sliders_container.image = image
                        # sliders_container.updateImage()
                        sliders_container.updateOriginalImage(image)
            else:
                messagebox.showerror("Error", "无法打开图片，请检查路径是否正确！")
        except Exception as e:
            messagebox.showerror("Error", f"错误：{str(e)}")
    else:
        messagebox.showerror("Error", "请输入图片路径！")
    
# class Alg(ABC):
#     def __init__(self, param_space,image):
#         self.param_space= param_space
#         self.default = { k:(v[0] + v[1]) // 2 for k,v in param_space.items()} #default
#         self.cur = self.default.copy()
#         self.image = image
    
    
#     @abstractmethod
#     def process(self,):
#         pass

class SlidersContainer(ABC,ttk.Frame):
    def __init__(self, master, alg,):
        super().__init__(master)
        self.alg = alg
        self.varaibles = {}
        self.labels = {}
        self.sliders = {}
        self.image = self.alg.image
        self.param_space = self.alg.param_space
        self.tk_image = bgr2tkPhoto(self.image)
        # self.image_label = ttk.Label(self,image=self.tk_image ) 
        # self.image_label.grid(row=len(self.alg.default)+1, column=0, columnspan=2)
        # print(self.alg.default.items())
        for i,(param_name,initValue) in enumerate(self.alg.default.items()):
            # i = i+1
            self.varaibles[param_name] = tk.IntVar(value=initValue)

            # 创建一个标签来显示标题
            self.labels[param_name] = ttk.Label(self, text=param_name)
            self.labels[param_name].grid(row=i , column= 0,sticky='e')

            # 创建滑块
            self.sliders[param_name] = ttk.Scale(self, 
                               from_=self.param_space[param_name][0], 
                               to=self.param_space[param_name][1], 
                               variable=self.varaibles[param_name], 
                               orient=tk.HORIZONTAL,
                               command=self.onChange,
                               )
            self.sliders[param_name].grid(row=i , column=1, sticky='ew')
        
    @abstractmethod
    def onChange(self,_=None):
        #update all variables dict
        # print(self.alg.cur)
        # for i,(param_name,value )in enumerate(self.alg.cur.items()):
        #     self.alg.cur[param_name] = self.varaibles[param_name].get()
        # self.updateImage()
        pass

    @abstractmethod
    def updateImage(self):
        pass
    
    def updateOriginalImage(self, new_image):
        """更新显示的图片"""
        # 这里假设每个子类都有自己的方式来处理图片更新
        # 例如，重新调用自己的process方法并更新界面
        # self.image = new_image
        # self.updateImage()      
        pass

class Sliders(SlidersContainer):
    def __init__(self, master, alg):
        super().__init__(master, alg)
        self.alg = alg
        self.varaibles = {}
        self.labels = {}
        self.sliders = {}
        self.labels_value = {}  # 新增：存储滑块值的标签
        self.image = self.alg.image
        self.param_space = self.alg.param_space
        self.tk_image = bgr2tkPhoto(self.image)
        self.image_label = ttk.Label(self, image=self.tk_image)
        self.image_label.grid(row=len(self.alg.default) + 1, column=1, columnspan=1)
        for i, (param_name, initValue) in enumerate(self.alg.default.items()):
            self.varaibles[param_name] = tk.IntVar(value=initValue)

            # 创建一个标签来显示标题
            self.labels[param_name] = ttk.Label(self, text=param_name + ": ")
            self.labels[param_name].grid(row=i, column=0, sticky='e')

            # 创建滑块
            self.sliders[param_name] = ttk.Scale(
                self,
                from_=self.param_space[param_name][0],
                to=self.param_space[param_name][1],
                variable=self.varaibles[param_name],
                orient=tk.HORIZONTAL,
                command=self.onChange,
            )
            self.sliders[param_name].grid(row=i, column=1, sticky='ew')

            # 创建一个标签来显示滑块的值
            self.labels_value[param_name] = ttk.Label(self, text=str(initValue))  # 初始值
            self.labels_value[param_name].grid(row=i, column=2, sticky='e')

    def onChange(self, _=None):
        for param_name, value in self.alg.cur.items():
            self.alg.cur[param_name] = self.varaibles[param_name].get()
            self.labels_value[param_name].config(text=str(value))  # 更新滑块值的标签
        self.updateImage()

    def updateImage(self):
        self.image = self.alg.process()
        self.tk_image = bgr2tkPhoto(self.image)
        self.image_label.config(image=self.tk_image)
        self.image_label.grid(row=len(self.alg.default) + 1, column=1, columnspan=1)

    def updateOriginalImage(self, new_image):
        """更新显示的图片"""
        # 这里假设每个子类都有自己的方式来处理图片更新
        # 例如，重新调用自己的process方法并更新界面
        #self.image = new_image
        self.alg.image = new_image
        self.updateImage()
################################################################################################################
################################################################################################################
################################################################################################################
################################################################################################################
################################################################################################################



if __name__ == "__main__":
    #bgr
    file_name  = "fk.jpg"
    image = cv2.imread(file_name)
    # image = np.zeros((600,600,3),dtype=np.uint8)
    #界面
    root = tk.Tk()
    root.title("opencv")
    root.geometry("1000x800")
    notebook = ttk.Notebook(root)
    
    tab0 = tk.Frame()
    entry_text = tk.StringVar(value="whole1.png")
    entry = ttk.Entry(tab0, width=50,textvariable=entry_text)
    entry.grid(row=0, column=0, padx=10, pady=10)
    entry.focus_set()  # 设置焦点到输入框
    entry.bind('<Return>', lambda event: open_image())  # 绑定回车事件
    open_button = ttk.Button(tab0, text="Open", command=open_image)
    open_button.grid(row=1, column=0, padx=10, pady=10)
    image_label = ttk.Label(tab0)
    image_label.grid(row=2, column=0, padx=10, pady=10, sticky='nswe')  # 填充整个区域
    notebook.add(tab0,text="打开图片")
    
    
    
    # 创建两个选项卡，每个都是一个Frame
    tab1 = tk.Frame()
    #算法+对应的滑块
    param_space1 = {"hue":(0, 180),
                   "saturation":(0, 255),
                   "value":(0, 255)}
    hsv_alg1 = HsvAlg(param_space1,image)
    sliders_container1 = Sliders(tab1,hsv_alg1)
    sliders_container1.pack(fill=tk.BOTH, expand=True)  # 使容器填充窗口
    notebook.add(tab1, text='hsv调色')
    
    
    
    tab2 = tk.Frame()
    #算法+对应的滑块
    param_space2 = {"hue_min":(0,180),
                   'saturation_min':(0, 255),
                   'value_min':(0, 255)
                   ,
                   'hue_max':(0, 180),
                   'saturation_max':(0, 255),
                   'value_max':(0, 255)
                   }
    hsv_alg2 = HsvAlg2(param_space2,image)
    sliders_container2 = Sliders(tab2,hsv_alg2)
    sliders_container2.pack(fill=tk.BOTH, expand=True)  # 使容器填充窗口
    notebook.add(tab2, text='hsv mask')
   
    
    
    
    tab3 = tk.Frame()
    #算法+对应的滑块
    param_space_thresh = {"threshold":(0,255)
                          }
    th_alg = ThreshAlg(param_space_thresh,image)
    sc3 = Sliders(tab3,th_alg)
    sc3.pack(fill=tk.BOTH, expand=True)  # 使容器填充窗口
    notebook.add(tab3, text='二值化-手动阈值')
    
    
    
    
    #算法+对应的滑块
    tab4 = ttk.Frame()
    param_space_canny = {"threshold_low":(0,255),
                          "threshold_high":(0,255),
                          "apertureSize":(3,9)
                          }
    canny_alg = EdgesAlg(param_space_canny,image)
    sc4 = Sliders(tab4,canny_alg)
    sc4.pack(fill=tk.BOTH, expand=True)  # 使容器填充窗口
    notebook.add(tab4, text='边缘检测')
    
    #算法+对应的滑块
    tab5 = ttk.Frame()
    param_space_contours = {"threshold":(0,255),
                            "minArea":(0,1e4)
                          }
    contours_alg = ContoursAlg(param_space_contours,image)
    sc5 = Sliders(tab5,contours_alg)
    sc5.pack(fill=tk.BOTH, expand=True)  # 使容器填充窗口
    notebook.add(tab5, text='轮廓检测')

    
    #算法+对应的滑块
    tab6 = ttk.Frame()
    param_space_circles = {"canny_high_threshold":(1,255),
                           "votes":(10,500),
                           "minDist":(1,1000),
                           "minRadius":(0,1000),
                           "maxRadius":(0,1000),
                           
                          }
    houghcircles_alg = HoughCirclesAlg(param_space_circles,image)
    sc6 = Sliders(tab6,houghcircles_alg)
    sc6.pack(fill=tk.BOTH, expand=True)  # 使容器填充窗口
    notebook.add(tab6, text='Hough圆检测')
    
    
    
    #算法+对应的滑块
    tab7 = ttk.Frame()
    param_space_lines = {"canny_low_threshold":(0,255),
                         "canny_high_threshold":(1,255),
                         "votes":(10,500),
                          }
    houghlines_alg = HoughLinesAlg(param_space_lines,image)
    sc7 = Sliders(tab7,houghlines_alg)
    sc7.pack(fill=tk.BOTH, expand=True)  # 使容器填充窗口
    notebook.add(tab7, text='Hough线检测')
    
    
    
    #算法+对应的滑块
    tab8 = ttk.Frame()
    param_space_connections = {"binary_threshold":(0,255),
                               "minArea":(0,1e4)
                          }
    connections_alg = ConnectionsAlg(param_space_connections,image)
    sc8 = Sliders(tab8,connections_alg)
    sc8.pack(fill=tk.BOTH, expand=True)  # 使容器填充窗口
    notebook.add(tab8, text='连通域检测')
    
    
    #算法+对应的滑块
    tab9 = ttk.Frame()
    param_space_corners = {"GradBlockSize":(3,11),
                            "sobelksize":(3,11),
                            "binary_threshold":(0,255)
                          }
    corners_alg = CornersAlg(param_space_corners,image)
    sc9 = Sliders(tab9,corners_alg)
    sc9.pack(fill=tk.BOTH, expand=True)  # 使容器填充窗口
    notebook.add(tab9, text='Hariss角点检测')
    
    
    
    notebook.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
    root.mainloop()