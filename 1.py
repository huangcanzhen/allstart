import os
import subprocess
import sys

import cv2
import numpy as np
import pyautogui
import time
from collections import Counter
import configparser
import logging
import logging.handlers
from datetime import datetime

time.sleep(2)
###----------------------------------###-----------------------------------宝箱
pyautogui.moveTo(120, 170, duration=0.5)
pyautogui.moveRel(0, 260, duration=1), pyautogui.click()  # 向下
pyautogui.moveTo(1300, 840, duration=3), pyautogui.click()
time.sleep(2)
pyautogui.mouseDown()
pyautogui.moveRel(-400, -500, duration=2)
pyautogui.mouseUp()
pyautogui.moveTo(1150, 820, duration=2), pyautogui.click()  # 返回
pyautogui.moveTo(120, 170, duration=1), pyautogui.click()  # 退出
###----------------------------------###----------------------------------活动
# 日常
pyautogui.moveTo(120, 170, duration=1)
pyautogui.moveRel(0, 330, duration=1), pyautogui.click()  # 向下
pyautogui.moveRel(0, -100, duration=2), pyautogui.click()  # 向上
pyautogui.moveTo(250, 300, duration=1), pyautogui.click()
pyautogui.moveTo(1600, 900, duration=1), pyautogui.click(clicks=2, interval=1)

# 每日签到
pyautogui.moveTo(250, 400, duration=1), pyautogui.click()
moveX = 650
moveY = 450
for x in range(7):
 pyautogui.moveTo(moveX, moveY, duration=0.1), pyautogui.click(clicks=2, interval=0.1),
 for y in range(2):
     moveY += 150
     pyautogui.moveTo(moveX, moveY, duration=0.1), pyautogui.click(clicks=2, interval=0.1),
 moveY = 450
 moveX += 170

# 冬日
pyautogui.moveTo(250, 500, duration=1), pyautogui.click()
pyautogui.moveTo(1730, 400, duration=1), pyautogui.click(clicks=6, interval=0.5)

pyautogui.moveTo(120, 170, duration=1), pyautogui.click()  # 退出

# time.sleep(2)
# pyautogui.mouseDown()
# pyautogui.moveRel(-400, -500, duration=2)
# pyautogui.mouseUp()
# pyautogui.moveTo(1150, 820, duration=2) , pyautogui.click() #返回
# pyautogui.moveTo(120, 170, duration=1), pyautogui.click()  # 退出

# pyautogui.moveRel(400, 0, duration=1), pyautogui.click() #向右
# pyautogui.moveTo(120,170, duration=1), pyautogui.click(clicks=2,interval=2),