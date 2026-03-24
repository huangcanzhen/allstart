import pyautogui,time
import pytesseract
from PIL import Image
import time
import os
# 春节版本
time.sleep(3)



pyautogui.moveTo(250, 500, duration=1), pyautogui.click()# 获取脚本所在目录                               
script_dir = os.path.dirname(os.path.abspath(__file__))      # 构建图片的绝对路                     
image_path = os.path.join(script_dir, 'pic', 'active', '7.bmp')
location = pyautogui.locateCenterOnScreen(image_path, confidence=0.7)           # 查找图片并返回中心坐标
pyautogui.moveTo(location.x, location.y), pyautogui.click(clicks=6, interval=0.5)