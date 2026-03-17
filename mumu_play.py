import os
import subprocess
import cv2
import numpy as np
import pyautogui
import time
from collections import Counter
import configparser
import logging
from datetime import datetime

class Mumuplay:
    """MuMu模拟器自动化操作类"""
    def __init__(self, mu_path):
        # 获取脚本目录
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.logger = self._setup_logger()
        self.target_image = None
        os.putenv('path', mu_path)
        self.config = configparser.ConfigParser()
        self.config.read(os.path.join(self.script_dir, 'config.ini'))
    
    def _setup_logger(self):
        """设置日志"""
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        
        # 确保log目录存在
        log_dir = os.path.join(self.script_dir, 'log')
        os.makedirs(log_dir, exist_ok=True)
        
        # 获取当前时间
        now = datetime.now()
        formatted_now = now.strftime("%Y-%m-%d-%H-%M-%S")
        handler = logging.FileHandler(os.path.join(log_dir, f"{formatted_now}mumuplay.log"))
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger
    
    def start(self):
        """启动 MuMu 模拟器"""
        try:
            rule_json_path = os.path.join(self.script_dir, 'rule.json')
            self.send_command(f'MuMuManager.exe setting -v 0 -p "{rule_json_path}"')
            time.sleep(5)
            self.send_command('MuMuManager.exe control -v 0 launch -pkg com.netease.allstar')
            self.logger.info('MuMu started successfully.')
            time.sleep(15)
        except Exception as e:
            self.logger.error(f'Failed to start MuMu: {e}')
    
    def send_command(self, command):
        """发送命令到 MuMu 管理器"""
        try:
            process = subprocess.Popen(command, shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            process.stdout.read()
            self.logger.info(f'Command executed: {command}')
        except Exception as e:
            self.logger.error(f'Failed to execute command: {command}. Error: {e}')
    
    @staticmethod
    def read_images(folder_path):
        """读取图片文件夹下所有文件"""
        images = []
        for filename in os.listdir(folder_path):
            if filename.endswith('.bmp'):
                image_path = os.path.join(folder_path, filename)
                images.append(image_path)
        return images
    
    def action_ui(self, path):
        """操作界面 - 合集"""
        time.sleep(5)
        # Ensure path is relative to script directory
        # Handle paths that start with backslash
        if path.startswith('\\'):
            path = path[1:]  # Remove leading backslash
        # Convert to absolute path using script directory as base
        path = os.path.join(self.script_dir, path)
        list_bmp = self.read_images(path)
        delay_times = {
            os.path.join(self.script_dir, 'pic', 'Login', '1.bmp'): 5,
            os.path.join(self.script_dir, 'pic', 'Card', '3.bmp'): 0.5,
            os.path.join(self.script_dir, 'pic', 'WC3V3', '2.bmp'): 2,
        }
        
        for index, bmp_path in enumerate(list_bmp):
            attempts = 1
            while True:
                delay_time = delay_times.get(bmp_path, 2)
                target_value = self.identify_images(bmp_path)
                self.logger.info(f'{index + 1},try.{attempts} ,path: {bmp_path}')
                print(f'第{index + 1}张图片,尝试第{attempts}次，路径: {bmp_path}')
                print(target_value)
                time.sleep(delay_time)
                if target_value is None:
                    attempts += 1
                    if attempts == 5:
                        self.logger.info(f'attempts:{attempts},break')
                        print(f'数字{attempts}退出')
                        if bmp_path == os.path.join(self.script_dir, 'pic', 'WC3V3', '2.bmp'):
                            py = 'G_run.py'
                        elif bmp_path == os.path.join(self.script_dir, 'pic', 'WC5V5', '2.bmp'):
                            py = 'wc5v5.py'
                        elif bmp_path == os.path.join(self.script_dir, 'pic', 'active', '0.bmp'):
                            py = 'active.py'
                        else:
                            py = None
                            
                        if py:
                            print('退出重来')
                            self.send_command('MuMuManager.exe control -v all shutdown')
                            time.sleep(1)
                            g_run_path = os.path.join(self.script_dir, py)
                            self.send_command(f'python "{g_run_path}"')
                            self.send_command('taskkill /im python.exe')
                            time.sleep(1)
                        break
                    continue
                break
    
    def identify_images(self, bmp_path):
        """识别图像"""
        try:
            # 读取目标图像
            self.target_image = cv2.imread(bmp_path, 0)
            if self.target_image is None:
                self.logger.error(f'Failed to read image: {bmp_path}')
                return None
            
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
                found_dir = os.path.join(self.script_dir, 'pic', 'found', today)
                os.makedirs(found_dir, exist_ok=True)
                screenshot_path = os.path.join(found_dir, f"screenshot_{datetime.now().strftime('%H%M%S')}.png")
                pyautogui.screenshot().save(screenshot_path)
                print('保存图片')
                return None
        except Exception as e:
            self.logger.error(f'Error in identifying images: {e}')
            return None
    
    def click_location(self, location, bmp_path):
        """点击位置"""
        bmp_path = os.path.normpath(bmp_path)

        try:
            x = location[0] + self.target_image.shape[1] // 2
            y = location[1] + self.target_image.shape[0] // 2
            pyautogui.moveTo(x, y, duration=2), pyautogui.click()
            self.logger.info(f'Clicked at location: {location}')
            if bmp_path == os.path.join(self.script_dir, 'pic', 'Card', '3.bmp') or \
                bmp_path == os.path.join(self.script_dir, 'pic', 'WC3V3', '2.bmp') or \
                bmp_path == os.path.join(self.script_dir, 'pic', 'active', '0.bmp') or \
                bmp_path == os.path.join(self.script_dir, 'pic', 'active', '3.bmp') or \
                bmp_path == os.path.join(self.script_dir, 'pic', 'WC5V5', '2.bmp'):
                self.slide(location, bmp_path)
            
        except Exception as e:
            self.logger.error(f'Failed to click at location: {location}. Error: {e}')
        return True
    
    def slide(self, location, bmp_path):
        """滑动操作"""
        self.logger.info(f'Enter the sliding operation')
        try:
            time.sleep(1)
            if bmp_path == os.path.join(self.script_dir, 'pic', 'active', '0.bmp'):
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
                pyautogui.moveTo(120, 170, duration=1)
                pyautogui.moveRel(0, 330, duration=2), pyautogui.click()  # 向下


            elif bmp_path == os.path.join(self.script_dir, 'pic', 'active', '3.bmp'):
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
                pyautogui.moveTo(120, 170, duration=1), pyautogui.click()  # 退出
                # pyautogui.moveTo(1780, 825, duration=2), pyautogui.click()
                # pyautogui.moveTo(120, 170, duration=1), pyautogui.click(clicks=2,interval=0.5)  # 退出
            elif bmp_path == os.path.join(self.script_dir, 'pic', 'WC3V3', '2.bmp'):
                pyautogui.moveTo(1400, 400, duration=1), pyautogui.click()
                pyautogui.moveTo(1700, 520, duration=1), pyautogui.click()
                pyautogui.moveTo(1555, 850, duration=1), pyautogui.click()
                pyautogui.moveTo(1759, 750, duration=1), pyautogui.click()
            elif bmp_path == os.path.join(self.script_dir, 'pic', 'Card', '3.bmp'):
                pyautogui.moveRel(300, 0, duration=1)  # 向右滑动300像素，持续1秒
            elif bmp_path == os.path.join(self.script_dir, 'pic', 'WC5V5', '2.bmp'):
                pyautogui.moveTo(1600, 550, duration=1)
                pyautogui.mouseDown()
                pyautogui.moveRel(0, -600, duration=2)  # 向上滑动600像素，持续2秒
                pyautogui.mouseUp()
                # pyautogui.moveTo(1600, 360, duration=1), pyautogui.click()  # 5v5坐标
                pyautogui.moveTo(1600, 550, duration=1), pyautogui.click()  # 5v5坐标
                pyautogui.moveTo(1555, 850, duration=1), pyautogui.click()  #连续匹配

                pyautogui.moveTo(1759, 750, duration=1), pyautogui.click()
            self.logger.info(f'Slided at location: {location}')
        except Exception as e:
            self.logger.error(f'Failed to slide at location: {location}. Error: {e}')
