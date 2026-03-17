import pyautogui,time
import pytesseract
from PIL import Image
import time
# 春节版本
time.sleep(3)

pyautogui.moveRel(320, 0, duration=2), pyautogui.click()
# 会员
pyautogui.moveTo(200, 700, duration=2), pyautogui.click()
pyautogui.moveTo(1420, 840, duration=1), pyautogui.click()
pyautogui.moveTo(1420, 840, duration=1), pyautogui.click()
# 联赛币
pyautogui.moveTo(200, 640, duration=1)
pyautogui.mouseDown()
time.sleep(1)
pyautogui.moveRel(0, -1000, duration=1)
pyautogui.mouseUp()
pyautogui.moveRel(0, 300, duration=1), pyautogui.click()  # 向下
pyautogui.moveRel(400, 0, duration=1), pyautogui.click(clicks=2, interval=2)  # 向右
pyautogui.moveTo(120, 170, duration=1), pyautogui.click()  # 退出

# 宝箱
pyautogui.moveTo(120, 170, duration=0.5)
pyautogui.moveRel(0, 260, duration=1), pyautogui.click()  # 向下
pyautogui.moveTo(1300, 840, duration=3), pyautogui.click()
time.sleep(2)
pyautogui.mouseDown()
pyautogui.moveRel(-400, -500, duration=2)
pyautogui.mouseUp()
pyautogui.moveTo(1150, 820, duration=2), pyautogui.click()  # 返回
pyautogui.moveTo(120, 170, duration=1), pyautogui.click()  # 退出
# 活动
pyautogui.moveTo(120, 170, duration=2)


if bmp_path == os.path.join(self.script_dir, 'pic', 'active', '3.bmp'):
	pyautogui.moveRel(0, 330, duration=1), pyautogui.click()  # 向下
	pyautogui.moveRel(0, -10, duration=2), pyautogui.click()  # 向上
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
	    moveX += 158
	# 冬日
	pyautogui.moveTo(250, 500, duration=1), pyautogui.click()
	pyautogui.moveTo(1630, 400, duration=1), pyautogui.click(clicks=6, interval=0.5)
	pyautogui.moveTo(120, 170, duration=1), pyautogui.click()  # 退出
	#日常领取
	pyautogui.moveTo(250, 360, duration=2), pyautogui.click()
	pyautogui.moveTo(250, 800, duration=2), pyautogui.click()
	pyautogui.moveTo(1600, 760, duration=2), pyautogui.click()
	pyautogui.moveTo(1667, 221, duration=2), pyautogui.click(clicks=2,interval=0.5)
	pyautogui.moveTo(1780, 825, duration=2), pyautogui.click()
	pyautogui.moveTo(120, 170, duration=1), pyautogui.click(clicks=2,interval=0.5)  # 退出