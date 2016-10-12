# -*- coding: utf-8 -*-
import os
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QWidget
from configparser import ConfigParser
from PyQt5 import Qt


class AppConfig(QWidget):
    def __init__(self):
        super().__init__()

    def initUI(self):

        self.setGeometry(100, 100, 400, 300)
        self.setWindowTitle('应用配置')
        self.setWindowFlags(Qt.Qt.SubWindow)

        grid = QGridLayout()


        self.scriptLocationLabel = QLabel('脚本目录: ')
        self.scriptLocationTxt = QLineEdit()

        self.serverIpLabel = QLabel('服务器IP: ')
        self.serverIpTxt = QLineEdit()

        self.serverPortLabel = QLabel('服务器Port: ')
        self.serverPortTxt = QLineEdit()

        self.gitUrlLabel = QLabel('测试脚本git地址: ')
        self.gitUrlForScript = QLineEdit()
        self.gitUrlForScript.setText('https://github.com/ouguangqian/autotestproject.git')


        self.okBtn = QPushButton('OK')
        self.okBtn.resize(self.okBtn.sizeHint())
        self.okBtn.clicked.connect(self.saveConfigs)

        self.cancelBtn = QPushButton('Cancel')
        self.cancelBtn.resize(self.cancelBtn.sizeHint())
        self.cancelBtn.clicked.connect(self.close)


        # 布局管理

        grid.addWidget(self.scriptLocationLabel, 1, 0)
        grid.addWidget(self.scriptLocationTxt, 1, 1, 1, 3)
        grid.addWidget(self.serverIpLabel, 2, 0)
        grid.addWidget(self.serverIpTxt, 2, 1, 1, 3)
        grid.addWidget(self.serverPortLabel, 3, 0)
        grid.addWidget(self.serverPortTxt, 3, 1, 1, 3)
        grid.addWidget(self.gitUrlLabel, 4, 0)
        grid.addWidget(self.gitUrlForScript, 4, 1, 1, 3)
        grid.addWidget(self.okBtn, 8,2)
        grid.addWidget(self.cancelBtn, 8, 3)
        grid.setRowMinimumHeight(9, 30)
        grid.setRowStretch(4, 1)


        self.setLayout(grid)
        self.showConfigs()
        self.show()

    # 保存配置项
    def saveConfigs(self):
        location = self.scriptLocationTxt.text()
        ip = self.serverIpTxt.text()
        port = self.serverPortTxt.text()
        gitUrl = self.gitUrlForScript.text()

        print('要保存的配置信息为：', location, ip, port)
        # 获取当前用户目录并判断是否存在.atp.ini文件
        curDir = os.path.expanduser('~')

        file = open(os.path.join(curDir, '.atp.ini'), 'w')
        file.writelines('[baseconf]')
        file.writelines('\n')
        file.writelines('projectLocation=' + location)
        file.writelines('\n')
        file.writelines('serverIp=' + ip)
        file.writelines('\n')
        file.writelines('serverPort=' + port)
        file.writelines('\n')
        file.writelines('gitUrlForScript=' + gitUrl)
        file.writelines('\n')


        file.close()

        self.close()

    # 显示配置项
    def showConfigs(self):
        # 获取当前用户目录并判断是否存在.atp.ini文件
        curDir = os.path.expanduser('~')
        iniPath = os.path.join(curDir, '.atp.ini')

        if os.path.exists(iniPath):
            cf = ConfigParser()
            cf.read(iniPath)
            try:
                self.scriptLocationTxt.setText(str(cf.get('baseconf', 'projectLocation')))
                self.serverIpTxt.setText(str(cf.get('baseconf', 'serverIp')))
                self.serverPortTxt.setText(str(cf.get('baseconf', 'serverPort')))
                self.gitUrlForScript.setText(str(cf.get('baseconf','gitUrlForScript')))
            except:
                pass

