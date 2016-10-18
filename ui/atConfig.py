# -×- coding -*-
import os
import shutil
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QWidget
from configparser import ConfigParser
from interface.get_data import getter
from PyQt5 import Qt

class AtConfig(QWidget):
    def __init__(self):
        super().__init__()

    def initUI(self):
        self.setGeometry(100, 100, 600, 500)
        self.setWindowTitle('脚本配置')
        self.setWindowFlags(Qt.Qt.SubWindow)
        grid = QGridLayout()

        self.playerLabel = QLabel('音频播放器路径: ')
        self.playerTxt = QLineEdit()

        self.voiceDirLabel = QLabel('音频文件路径: ')
        self.voiceDirTxt = QLineEdit()

        self.runLogDirLabel = QLabel('运行日志存放路径: ')
        self.runLogDirTxt = QLineEdit()

        self.deviceSerialLabel = QLabel('车机设备编号: ')
        self.deviceSerialTxt = QLineEdit()


        ##wifi或者热点
        self.deviceIPaddressLabel= QLabel('车机IP地址: ')
        self.deviceIPaddressTxt = QLineEdit()

        self.devicePcanBaudrate = QLabel('车机PCAN波特率: ')
        self.devicePcanBaudrateTxt = QLineEdit()


        self.phoneSerialLabel = QLabel('手机设备编号: ')
        self.phoneSerialTxt = QLineEdit()

        self.phoneBlueToothNameLabel = QLabel('手机蓝牙名称: ')
        self.phoneBlueToothNameTxt = QLineEdit()

        self.versionLabel = QLabel('测试版本编号: ')

        self.versionTxt = QLineEdit()
        self.versionTxt.setPlaceholderText('2.0 or 1.0')

        self.usbMusicLabel = QLabel('usb音乐名列表: ')

        self.usbMusicTxt = QLineEdit()
        self.usbMusicTxt.setPlaceholderText('usb音乐播放时展示的音乐名称，英文逗号分隔')

        self.socketIpLabel = QLabel('socketIp: ')

        self.socketIpTxt = QLineEdit()
        self.socketIpTxt.setPlaceholderText('用于控制logcat日志记录和停止,填写本机地址')

        self.socketPortLabel = QLabel('socketPort: ')

        self.socketPortTxt = QLineEdit()
        self.socketPortTxt.setPlaceholderText('本地socket端口,不冲突即可')


        self.okBtn = QPushButton('OK')
        self.okBtn.resize(self.okBtn.sizeHint())
        self.okBtn.clicked.connect(self.saveConfigs)

        self.cancelBtn = QPushButton('Cancel')
        self.cancelBtn.resize(self.cancelBtn.sizeHint())
        self.cancelBtn.clicked.connect(self.close)

        # 布局文件
        grid.addWidget(self.playerLabel, 1, 0)
        grid.addWidget(self.playerTxt, 1, 1, 1, 3)
        grid.addWidget(self.voiceDirLabel, 2, 0)
        grid.addWidget(self.voiceDirTxt, 2, 1, 1, 3)
        grid.addWidget(self.runLogDirLabel, 3, 0)
        grid.addWidget(self.runLogDirTxt, 3, 1, 1, 3)
        grid.addWidget(self.deviceSerialLabel, 4, 0)
        grid.addWidget(self.deviceSerialTxt, 4, 1, 1, 3)
        grid.addWidget(self.deviceIPaddressLabel, 5, 0)
        grid.addWidget(self.deviceIPaddressTxt, 5, 1, 1, 3)
        grid.addWidget(self.devicePcanBaudrate,6,0)
        grid.addWidget(self.devicePcanBaudrateTxt,6,1,1,3)


        grid.addWidget(self.phoneSerialLabel, 7, 0)
        grid.addWidget(self.phoneSerialTxt, 7, 1, 1, 3)
        grid.addWidget(self.phoneBlueToothNameLabel, 8, 0)
        grid.addWidget(self.phoneBlueToothNameTxt, 8, 1, 1, 3)
        grid.addWidget(self.versionLabel, 9, 0)
        grid.addWidget(self.versionTxt, 9, 1, 1, 3)
        grid.addWidget(self.usbMusicLabel, 10, 0)
        grid.addWidget(self.usbMusicTxt, 10, 1, 1, 3)
        # grid.addWidget(self.socketIpLabel, 9, 0)
        # grid.addWidget(self.socketIpTxt, 9, 1, 1, 3)
        # grid.addWidget(self.socketPortLabel, 10, 0)
        # grid.addWidget(self.socketPortTxt, 10, 1, 1, 3)
        grid.addWidget(self.okBtn, 12, 3)
        grid.addWidget(self.cancelBtn, 12, 4)
        grid.setRowMinimumHeight(13, 30)

        self.setLayout(grid)
        self.showConfigs()
        self.show()

    # 保存配置项
    def saveConfigs(self):

        cf = getter.get_app_conf()
        projectPath = str(cf.get('baseconf', 'projectLocation'))

        # atConfigPath = os.path.join(projectPath, 'support', 'config.ini')

        homeDir = os.path.expanduser('~')

        file = open(os.path.join(homeDir, '.config.ini'), 'w')

        # file = open(atConfigPath, 'w')
        file.writelines('[baseconf]')
        file.writelines('\n')
        file.writelines('player=' + self.playerTxt.text())
        file.writelines('\n')
        file.writelines('voiceDir=' + self.voiceDirTxt.text())
        file.writelines('\n')
        file.writelines('logPath=' + self.runLogDirTxt.text())
        file.writelines('\n')
        file.writelines('deviceSerial=' + self.deviceSerialTxt.text())
        file.writelines('\n')
        file.writelines('deviceIPaddress=' + self.deviceIPaddressTxt.text())
        file.writelines('\n')
        file.writelines('devicePcanBaudrate=' + self.devicePcanBaudrateTxt.text())
        file.writelines('\n')



        file.writelines('phoneSerial=' + self.phoneSerialTxt.text())
        file.writelines('\n')
        file.writelines('phoneBluetoothName=' + self.phoneBlueToothNameTxt.text())
        file.writelines('\n')
        file.writelines('version=' + self.versionTxt.text())
        file.writelines('\n')
        file.writelines('usbMusic=' + self.usbMusicTxt.text())
        file.writelines('\n')
        # file.writelines('socketIp=' + self.socketIpTxt.text())
        # file.writelines('\n')
        # file.writelines('socketPort=' + self.socketPortTxt.text())
        # file.writelines('\n')

        file.close()

        self.close()

       # 判断测试工程是否存在，存在就覆盖配置文件，不存在就什么都不做

        if os.path.exists(os.path.join(projectPath, 'support')):
            shutil.copyfile(os.path.join(homeDir, '.config.ini'), os.path.join(projectPath,  'support', 'config.ini'))

    #  显示配置项
    def showConfigs(self):

        # cf = getter.get_app_conf()
        # projectPath = str(cf.get('baseconf', 'projectLocation'))
        # atConfigPath = os.path.join(projectPath, 'support', 'config.ini')
        homeDir = os.path.expanduser('~')
        atConfigPath = os.path.join(homeDir, '.config.ini')

        cf = ConfigParser()
        cf.read(atConfigPath)
        try:
            self.playerTxt.setText(str(cf.get('baseconf', 'player')))
            self.voiceDirTxt.setText(str(cf.get('baseconf', 'voiceDir')))
            self.runLogDirTxt.setText(str(cf.get('baseconf', 'logPath')))
            self.deviceSerialTxt.setText(str(cf.get('baseconf', 'deviceSerial')))

            self.deviceIPaddressTxt.setText(str(cf.get('baseconf', 'deviceIPaddress')))
            self.devicePcanBaudrateTxt.setText(cf.get('baseconf','devicePcanBaudrate'))

            self.phoneSerialTxt.setText(str(cf.get('baseconf', 'phoneSerial')))
            self.phoneBlueToothNameTxt.setText(str(cf.get('baseconf', 'phoneBluetoothName')))
            self.versionTxt.setText(str(cf.get('baseconf', 'version')))
            self.usbMusicTxt.setText(str(cf.get('baseconf', 'usbMusic')))
            # self.socketIpTxt.setText(str(cf.get('baseconf', 'socketIp')))
            # self.socketPortTxt.setText(str(cf.get('baseconf', 'socketPort')))
        except:
            pass


