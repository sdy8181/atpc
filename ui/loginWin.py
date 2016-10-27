# -*- coding: utf-8 -*-
import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.Qt import Qt

class LoginWin(QWidget):

    def __init__(self):
        super().__init__()

    def initUI(self):
        self.setGeometry(512, 400, 400, 200)
        self.setWindowTitle('登录')
        self.setWindowFlags(Qt.ToolTip | Qt.WindowStaysOnTopHint)
        self.setWindowIcon(QIcon('./images/icon.jpg'))
        self.__grid = QGridLayout()

        self.__login_btn = QPushButton('登录', self)
        self.__login_btn.clicked.connect(self.login)

        self.__grid.addWidget(self.__login_btn, 0, 1)


        self.setLayout(self.__grid)
        self.show()

    def login(self):
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    lg = LoginWin()
    lg.initUI()
    sys.exit(app.exec_())
