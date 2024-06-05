from PIL import Image,ImageTk
import cv2
def bgr2tkPhoto(bgr):
    img_rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)  # 转换颜色空间
    img_pil = Image.fromarray(img_rgb)
    img_tk = ImageTk.PhotoImage(image=img_pil)
    return img_tk

