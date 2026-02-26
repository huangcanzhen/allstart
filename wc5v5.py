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
class Mumuplay:
    """docstring for Mumuplay"""
    def __init__(self, mu_path):
        self.logger = self.log()
        self.target_image = None
        os.putenv('path', mu_path)

    #日志
    def log(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        # 获取当前时间
        now = datetime.now()
        # 格式化时间
        formatted_now = now.strftime("%Y-%m-%d-%H-%M-%S")
        handler = logging.FileHandler(r'.\log\{}mumuplay.log'.format(formatted_now))
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        return self.logger

    # 启动 MuMu
    def start(self):
        try:
            self.sendcommand('MuMuManager.exe control -v 0 launch -pkg com.netease.allstar')
            self.logger.info('MuMu started successfully.')
            time.sleep(15)
        except Exception as e:
            self.logger.error(f'Failed to start MuMu: {e}')

    # 发送命令
    def sendcommand(self, command):
        try:
            process = subprocess.Popen(command, shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            process.stdout.read()
            self.logger.info(f'Command executed: {command}')
        except Exception as e:
            self.logger.error(f'Failed to execute command: {command}. Error: {e}')

    # 读取图片文件夹下所有文件
    @staticmethod
    def read_images(folder_path):
        images = []
        for filename in os.listdir(folder_path):
            if filename.endswith('.bmp'):
                image_path = os.path.join(folder_path, filename)
                images.append(image_path)
        return images

    # 操作界面 -合集
    def action_ui(self,path):
        time.sleep(5)
        list_bmp = self.read_images(path)
        delay_times = {
            r'.\pic\WC3V3\5.bmp': 8,
            r'.\pic\WC5V5\2.bmp': 8,
            r'.\pic\Login\1.bmp': 8,

        }

        for index, bmp_path in enumerate(list_bmp):
            # 尝试次数
            attempts = 1
            while True:
                delay_time = delay_times.get(bmp_path, 2)
                traget_value = self.identify_images(bmp_path)
                self.logger.info(f'{index + 1},tyr.{attempts} ,path: {bmp_path}')
                print(f'第{index + 1}张图片,尝试第{attempts}次，路径: {bmp_path}')
                print(traget_value)
                if traget_value is None:
                    time.sleep(delay_time)
                    attempts += 1
                    if attempts == 5:
                        self.logger.info(f'attempts:{attempts},break')
                        print(f'数字{attempts}退出')
                        break
                    continue
                break

        # 识别图像
    def identify_images(self, bmp_path):
        try:
            # 读取目标图像
            self.target_image = cv2.imread(bmp_path, 0)

            # 截取屏幕图像
            screen_image = np.array(pyautogui.screenshot())

            # 转换为灰度图像
            screen_image_gray = cv2.cvtColor(screen_image, cv2.COLOR_BGR2GRAY)

            # 使用模板匹配找到目标图像的位置
            result = cv2.matchTemplate(screen_image_gray, self.target_image, cv2.TM_CCOEFF_NORMED)

            # 筛选
            threshold = 0.7
            loc = np.where(result >= threshold)
            liebiao = list(zip(*loc[::-1]))

            if len(liebiao) > 0:
                # 使用 Counter 统计每个元组的出现次数
                counter = Counter(liebiao)
                # 找出出现次数最多的元组
                most_common_tuple = counter.most_common(1)[0][0]
                self.logger.info(f'Target found at location: {most_common_tuple}')
                return self.click_location(most_common_tuple, bmp_path)
            else:
                self.logger.info('Target not found.')
                today = datetime.now().strftime("%Y-%m-%d-%H-%M")
                os.makedirs(f"pic/found/{today}", exist_ok=True)
                pyautogui.screenshot().save(f"pic/found/{today}/screenshot_{datetime.now().strftime('%H%M%S')}.png")
                print('保存图片')
                return
        except Exception as e:
            self.logger.error(f'Error in identifying images: {e}')

    #   位置单个点击位置
    def click_location(self, location, bmp_path):

            try:
                x = location[0] + self.target_image.shape[1] // 2
                y = location[1] + self.target_image.shape[0] // 2
                pyautogui.moveTo(x, y,duration=1),pyautogui.click(),
                time.sleep(1)

                if bmp_path == r'.\pic\Card\3.bmp' or bmp_path == r'.\pic\WC5V5\2.bmp':
                    self.slide(location, bmp_path)
                self.logger.info(f'Clicked at location: {location}')
            except Exception as e:
                self.logger.error(f'Failed to click at location: {location}. Error: {e}')
            return True

    #特殊 滑动
    def slide(self,location,bmp_path):
            self.logger.info(f'Enter the sliding operation')
            try:
                # 移动鼠标到指定位置
                pyautogui.moveTo(location[0],location[1])

                # 滑动鼠标
                if bmp_path == r'.\pic\WC5V5\2.bmp':


                    pyautogui.moveTo(1400,800,duration=1),pyautogui.click()
                    # 按住左键
                    pyautogui.mouseDown()
                    pyautogui.moveRel(0, -600, duration=2)  #  向上滑动400像素，持续1秒
                    pyautogui.mouseUp()




                    pyautogui.moveTo(1600,360,duration=1),pyautogui.click() #5v5坐标


                    pyautogui.moveTo(1555,850,duration=1),pyautogui.click()
                    pyautogui.moveTo(1759,750,duration=1),pyautogui.click()

                #
                # elif bmp_path == r'.\pic\Card\3.bmp':
                #     pyautogui.moveRel(300, 0, duration=1)  # 向右滑动300像素，持续1秒
                else:
                    pass

                self.logger.info(f'Slided at location: {location}')
            except Exception as e:
                self.logger.error(f'Failed to slide at location: {location}. Error: {e}')


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini')
    Mumuconsole_path = config.get('Mumu', 'path')
    Login_ui_path=config.get('Login', 'path')
    Shop_ui_path=config.get('Shop', 'path')
    Card_ui_path=config.get('Card', 'path')
    WC3V3_ui_path=config.get('WC3V3', 'path')
    WC5V5_ui_path=config.get('WC5V5', 'path')

    Mumuconsole = Mumuplay(Mumuconsole_path)

    ###############启动Mumu模拟器，启动游戏#######
    Mumuconsole.start()

    # ##########登录界面点击
    Mumuconsole.action_ui( Login_ui_path)

    # WC5V5界面点击
    Mumuconsole.action_ui(WC5V5_ui_path)

