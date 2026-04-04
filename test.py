import pyautogui,time
import pytesseract
from PIL import Image
import time
import os
# 春节版本
time.sleep(3)



pyautogui.moveTo(120, 170, duration=0.5)
pyautogui.moveRel(0, 260, duration=1), pyautogui.click()  # 向下
pyautogui.moveTo(1300, 840, duration=3), pyautogui.click()

script_dir = os.path.dirname(os.path.abspath(__file__))      # 构建图片的绝对路                     
image_path = os.path.join(script_dir, 'pic', 'active', '8.bmp')
try:
    location = pyautogui.locateCenterOnScreen(image_path, confidence=0.9)       # 查找图片并返回中心坐标
    if location:
        pyautogui.moveTo(1234,758,duration=1), pyautogui.click()
        pyautogui.moveTo(1500, 770, duration=1), pyautogui.click()  # 返回
except Exception as e:
    pass
time.sleep(2)
pyautogui.moveTo(1300, 840, duration=2), pyautogui.click()
pyautogui.mouseDown()
pyautogui.moveRel(-400, -500, duration=2)
pyautogui.mouseUp()
pyautogui.moveTo(1150, 820, duration=2), pyautogui.click()  # 返回
pyautogui.moveTo(120, 170, duration=1), pyautogui.click()  # 退出