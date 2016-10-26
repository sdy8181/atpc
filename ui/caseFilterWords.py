# -*- coding: utf-8 -*-
import sys

from PyQt5.QtGui import QFont
from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QListWidget
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QWidget
from PyQt5.Qt import Qt
from interface.get_data import getter


class CaseFilterWords(QWidget):

    def __init__(self):
        super().__init__()

        self.setGeometry(100, 100, 800, 600)
        self.setWindowFlags(Qt.SubWindow)
        self.setWindowTitle('用例筛选管理')
        grid = QGridLayout(self)

        self.tipTxt = QLabel(self)
        self.tipTxt.setFont(QFont("Roman times", 16, QFont.Bold))

        self.pe_red = QPalette()
        self.pe_red.setColor(QPalette.WindowText, Qt.red)
        self.tipTxt.setPalette(self.pe_red)

        self.closeBtn = QPushButton('关闭', self)
        self.closeBtn.clicked.connect(self.close)

        self.moduleLabel = QLabel('用例模块名称:', self)
        self.moduleEdit = QLineEdit(self)
        self.moduleAddBtn = QPushButton('添加', self)
        self.moduleDelBtn = QPushButton('删除', self)

        self.moduleAddBtn.clicked.connect(self.add_module_type)
        self.moduleDelBtn.clicked.connect(self.del_module_type)

        self.moduleList = QListWidget(self)


        self.scenLabel = QLabel('用例类型名称:', self)
        self.scenEdit = QLineEdit(self)
        self.scenAddBtn = QPushButton('添加', self)
        self.scenDelBtn = QPushButton('删除', self)

        self.scenAddBtn.clicked.connect(self.add_scen_type)
        self.scenDelBtn.clicked.connect(self.del_scen_type)

        self.scenList = QListWidget(self)


        grid.addWidget(self.tipTxt, 7, 2, 1, 3)
        grid.addWidget(QLabel('重启生效!', self), 7, 6)

        grid.addWidget(self.moduleLabel, 1, 0)
        grid.addWidget(self.moduleEdit, 1, 1)
        grid.addWidget(self.moduleAddBtn, 1, 2)
        grid.addWidget(self.moduleDelBtn, 1, 3)

        grid.addWidget(self.moduleList, 2, 0, 5, 4)

        grid.addWidget(self.scenLabel, 1, 4)
        grid.addWidget(self.scenEdit, 1, 5)
        grid.addWidget(self.scenAddBtn, 1, 6)
        grid.addWidget(self.scenDelBtn, 1, 7)

        grid.addWidget(self.scenList, 2, 4, 5, 4)

        grid.addWidget(self.closeBtn, 7, 7)

        grid.setRowStretch(7, 1)

        self.setLayout(grid)

        self.show()

        self.refresh_scen_type()
        self.refresh_module_type()

    def add_scen_type(self):
        self.tipTxt.clear()
        scen_type = self.scenEdit.text().strip()
        if scen_type == '':
            self.tipTxt.setText('请填写用例类型')
        else:
            # 查询scen_type是否存在
            isExists = getter.check_scen_type_exists(scen_type)
            if isExists['result']:
                self.tipTxt.setText('用例类型已经存在')
            else:
                #存入数据库
                try:
                    res = getter.save_scen_type({'name': scen_type})
                    if res['result']:
                        self.tipTxt.setText('用例类型添加成功')
                    else:
                        self.tipTxt.setText('用例类型添加失败')
                except Exception as e:
                    self.tipTxt.setText('用例类型添加异常')
                    print(e)
        self.refresh_scen_type()
        self.scenEdit.clear()

    def add_module_type(self):
        self.tipTxt.clear()
        module_type = self.moduleEdit.text().strip()
        if module_type == '':
            self.tipTxt.setText('请填写用例模块')
        else:
            # 查询scen_type是否存在
            isExists = getter.check_module_type_exists(module_type)
            if isExists['result']:
                self.tipTxt.setText('用例模块已经存在')
            else:
                #存入数据库
                try:
                    res = getter.save_module_type({'name': module_type})
                    if res['result']:
                        self.tipTxt.setText('模块类型添加成功')
                    else:
                        self.tipTxt.setText('模块类型添加失败')
                except Exception as e:
                    self.tipTxt.setText('用例模块添加异常')
                    print(e)

        self.refresh_module_type()
        self.moduleEdit.clear()

    def del_module_type(self):
        self.tipTxt.clear()
        item = self.moduleList.currentItem()
        if item is None:
            self.tipTxt.setText('请选择要删除的模块类型')
        else:
            try:
                res = getter.del_module_type(item.text())
                if res['result']:
                    self.tipTxt.setText('删除成功')
                else:
                    self.tipTxt.setText('删除失败')
            except Exception as e:
                self.tipTxt.setText('模块类型删除异常, 请联系负责人')
                print(e)

        self.refresh_module_type()


    def del_scen_type(self):
        self.tipTxt.clear()
        item = self.scenList.currentItem()
        if item is None:
            self.tipTxt.setText('请选择要删除的用例类型')
        else:
            try:
                res = getter.del_scen_type(item.text())
                if res['result']:
                    self.tipTxt.setText('删除成功')
                else:
                    self.tipTxt.setText('删除失败')
            except Exception as e:
                self.tipTxt.setText('用例类型删除异常, 请联系负责人')
                print(e)

        self.refresh_scen_type()

    def refresh_scen_type(self):
        self.scenList.clear()
        data = getter.get_filter_scen_type_all()
        for i in range(len(data)):
            self.scenList.insertItem(i, QListWidgetItem(data[i]['name']))


    def refresh_module_type(self):
        self.moduleList.clear()
        data = getter.get_filter_module_type_all()
        for i in range(len(data)):
            self.moduleList.insertItem(i, QListWidgetItem(data[i]['name']))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    csw = CaseFilterWords()
    sys.exit(app.exec_())
