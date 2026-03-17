import os
import sys
from mumu_play import Mumuplay
import configparser


if __name__ == '__main__':
    config = configparser.ConfigParser()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config.read(os.path.join(script_dir, 'config.ini'))
    Mumuconsole_path = config.get('Mumu', 'path')
    Login_ui_path=config.get('Login', 'path')
    Shop_ui_path=config.get('Shop', 'path')
    Card_ui_path=config.get('Card', 'path')
    WC3V3_ui_path=config.get('WC3V3', 'path')
    WC5V5_ui_path=config.get('WC5V5', 'path')

    Mumuconsole = Mumuplay(Mumuconsole_path)

    # # 启动Mumu模拟器，启动游戏
    Mumuconsole.start()

    # # 登录界面点击
    Mumuconsole.action_ui( Login_ui_path)
    #

    # WC3V3界面点击
    Mumuconsole.action_ui(WC3V3_ui_path)


