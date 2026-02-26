import pyautogui,time
import pytesseract
from PIL import Image

# 春节版本
pyautogui.moveTo(120, 170, duration=1)
pyautogui.moveRel(0, 330, duration=1), pyautogui.click()  # 向下
pyautogui.moveRel(0, -10, duration=2), pyautogui.click()  # 向上
pyautogui.moveTo(250, 300, duration=1), pyautogui.click()
pyautogui.moveTo(1600, 900, duration=1), pyautogui.click(clicks=2, interval=1)