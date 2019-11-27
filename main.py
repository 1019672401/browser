import random
import socket
import sys
import os
import configparser

if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']

import pymysql
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtCore import QUrl, QTimer
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon

from models.db_connect import db_session
from models.model import PrjScreen


class Controler():
    def __init__(self):
        self._app = QApplication(sys.argv)
        self.browser = QWebEngineView()
        self.browser.setWindowIcon(QIcon(r'./browser.ico'))
        self.browser.setWindowTitle('大屏显示')
        self.browser.zoomFactor()
        self.ip = self.get_host_ip()
        self.url = " "
        self.browser.load(QUrl(" "))

    def change_url(self):
        target = db_session.query(
            PrjScreen.screen_content,
            PrjScreen.parameter
        ).filter(
            PrjScreen.screen_ip == self.ip
        ).first()
        if not target:
            new_url = " "  # "https://www.easyicon.net/"
        else:
            if PrjScreen.screen_content:
                if PrjScreen.parameter:
                    new_url = target.screen_content + target.parameter
                else:
                    new_url = target.screen_content
            else:
                pass
                new_url = " "
        if new_url != self.url:
            self.url = new_url
            self.browser.load(QUrl(new_url))
            print(new_url)
        else:
            print("url is same", self.url)
            print(self.ip)

    def timer_start(self):
        self.timer = QTimer()
        # 一次刷新会调用一次showTime函数
        self.timer.timeout.connect(self.change_url)
        # 一秒钟更新一次
        config_dir = os.path.abspath('./configs/')
        cf = configparser.ConfigParser()
        cf_file_name = config_dir + "/config.ini"
        if os.path.exists(cf_file_name):
            cf.read(cf_file_name)
            secs = cf.sections()
            if "Timeout" in secs:
                config_options = cf.options("Timeout")
                if "t" in config_options:
                    timeout_time = cf.get("Timeout", "t")
                    if timeout_time == '':
                        timeout_time = 5
                    else:
                        timeout_time = int(timeout_time)
                else:
                    timeout_time = 5
            else:
                timeout_time = 5
        timeout_time = timeout_time * 1000
        self.timer.start(timeout_time)

    def get_host_ip(self):
        '''
        myname = socket.getfqdn(socket.gethostname())
        myaddr = socket.gethostbyname(myname)
        return  myaddr
        '''
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
        finally:
            s.close()

        return ip


    def run(self):
        self.browser.show()
        self.timer_start()
        return self._app.exec_()


if __name__ == '__main__':
    c = Controler()
    sys.exit(c.run())
