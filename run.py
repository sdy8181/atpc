# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QApplication

from ui.mainWindow import MainWidget

app = QApplication(sys.argv)
mw = MainWidget()
mw.initUI()
sys.exit(app.exec_())
