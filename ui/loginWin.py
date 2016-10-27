# -*- coding: utf-8 -*-
import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QPushButton

class LoginWin(QWidget):

    def __init__(self):
        super().__init__()

    def initUI(self):
        self.setGeometry(512, 400, 400, 200)
        self.setWindowTitle('登录')
        self.setWindowIcon(QIcon('./images/icon.jpg'))
        self.__grid = QGridLayout()

        self.__login_btn = QPushButton('登录', self)
        self.__login_btn.clicked.connect(self.login)


        self.setLayout(self.grid)
        self.show()

    def login(self):
        self.close()

        from .mainWindow import MainWidget
        self.mw = MainWidget()
        self.mw.initUI()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    lg = LoginWin()
    lg.initUI()
    sys.exit(app.exec_())
