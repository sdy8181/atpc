# -*- coding: utf-8 -*-
import sys

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLineEdit, QTextEdit, QProgressBar
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QListWidget
from PyQt5.QtGui import QPalette
from PyQt5 import Qt

from interface.get_data import getter


class StepManager(QWidget):
    def __init__(self):
        super(StepManager, self).__init__()

    def initUI(self):
        self.setGeometry(10, 10, 900, 600)
        self.setWindowTitle('用例管理')

        grid = QGridLayout()
        self.stepList = QListWidget()
        self.stepList.clicked.connect(self.show_step)

        self.moduleLabel = QLabel('所属模块', self)
        self.moduleCombo = QComboBox()
        self.moduleCombo.addItem('--')
        self.moduleCombo.addItem('音乐')
        self.moduleCombo.addItem('电台')
        self.moduleCombo.addItem('视频')
        self.moduleCombo.addItem('导航')
        self.moduleCombo.addItem('语音')
        self.moduleCombo.addItem('协议')
        self.moduleCombo.addItem('公共')
        self.moduleCombo.addItem('其他')

        self.stepDescLabel = QLabel('步骤信息:', self)
        self.stepDescValue = QTextEdit(self)

        self.paramNameLabel = QLabel('参数名称:', self)
        self.paramNameValue = QLineEdit(self)
        self.paramNameValue.setEnabled(False)

        self.saveBtn = QPushButton('保存', self)
        self.saveBtn.clicked.connect(self.save)
        self.delBtn = QPushButton('删除', self)
        self.delBtn.clicked.connect(self.del_step)
        self.closeBtn = QPushButton('退出', self)
        self.closeBtn.clicked.connect(self.close)

        self.tipText = QLabel(self)
        self.tipText.setFont(QFont('Roman times', 16, QFont.Bold))
        self.pe_red = QPalette()
        self.pe_red.setColor(QPalette.WindowText, Qt.Qt.red)

        self.bar = QProgressBar(self)
        self.bar.setGeometry(30, 40, 200, 25)
        self.bar.setValue(30 / 55 * 100)

        grid.addWidget(self.stepList, 0, 1, 5, 3)
        grid.addWidget(self.moduleLabel, 0, 5, 1, 1)
        grid.addWidget(self.moduleCombo, 0, 6, 1, 1)

        grid.addWidget(self.stepDescLabel, 1, 5, 1, 1)
        grid.addWidget(self.stepDescValue, 1, 6, 2, 4)

        grid.addWidget(self.paramNameLabel, 3, 5, 1, 1)
        grid.addWidget(self.paramNameValue, 3, 6, 1, 4)

        grid.addWidget(self.bar, 4, 5, 1, 4)

        grid.addWidget(self.tipText, 5, 7, 1, 2)

        grid.addWidget(self.saveBtn, 7, 5, 1, 1)
        grid.addWidget(self.delBtn, 7, 7, 1, 1)
        grid.addWidget(self.closeBtn, 7, 6, 1, 1)

        self.setLayout(grid)

        self.showSteps()
        self.show()

    def showSteps(self):
        self.stepList.clear()
        steps = getter.get_step_all()
        for i in range(len(steps)):
            self.stepList.insertItem(i, steps[i]['name'])

    def save(self):
        if self.stepList.currentRow() == -1:
            self.tipText.setText('请选择步骤')
            self.tipText.setPalette(self.pe_red)
            return
        if self.moduleCombo.currentIndex() == 0:
            self.tipText.setText('请选择模块')
            self.tipText.setPalette(self.pe_red)
            return

        self.tipText.clear()
        data = {'name': self.stepList.item(self.stepList.currentRow()).text(),
                'type': self.moduleCombo.currentText(),
                'step_desc': self.stepDescValue.toPlainText(),
                }

        res = getter.update_step_info(data)
        if res['result'] == 'true':
            self.tipText.setText('保存成功')
            self.tipText.setPalette(self.pe_red)

    def show_step(self):
        self.tipText.clear()
        self.stepDescValue.clear()
        self.paramNameValue.clear()

        step_name = self.stepList.item(self.stepList.currentRow()).text()
        st_info = getter.get_step_info_by_name(step_name)

        if st_info['type']:
            self.moduleCombo.setCurrentText(st_info['type'])
        else:
            self.moduleCombo.setCurrentIndex(0)

        if st_info['step_desc']:
            self.stepDescValue.setText(st_info['step_desc'])

        if st_info['param_name'] is not None:  # and len(st_info['param_name']) > 0:
            self.paramNameValue.setText(st_info['param_name'])
        else:
            self.paramNameValue.clear()

    def del_step(self):
        if self.stepList.currentRow() == -1:
            self.tipText.setText('请选择步骤')
            self.tipText.setPalette(self.pe_red)
            return
        step_name = self.stepList.item(self.stepList.currentRow()).text()
        getter.del_step_by_name(step_name)
        self.showSteps()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    sm = StepManager()
    sm.initUI()
    sys.exit(app.exec_())
