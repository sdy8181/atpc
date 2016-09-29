# -*- coding: utf-8 -*-
import os
import subprocess

from urllib.parse import quote
from PyQt5.QtGui import QBrush
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QFont
from PyQt5.QtGui import QIcon

from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QInputDialog
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QTreeWidget
from PyQt5.QtWidgets import QTreeWidgetItem
from PyQt5.QtWidgets import QWidget
from PyQt5 import Qt

from interface.get_data import getter

class ViewResult(QWidget):
    def __init__(self, parent=None):
        super(ViewResult, self).__init__(parent)

    def initUI(self, id):
        self.setWindowTitle('结果查看')
        self.setWindowIcon(QIcon('./images/icon.jpg'))
        self.setGeometry(10, 10, 900, 800)
        # self.setMaximumSize()
        self.setWindowFlags(Qt.Qt.SubWindow)
        self.taskid = id
        grid = QGridLayout()

        closeBtn = QPushButton('关闭')
        downloadReportBtn = QPushButton('下载报告')
        downloadLogBtn = QPushButton('下载日志')
        closeBtn.resize(closeBtn.sizeHint())
        closeBtn.clicked.connect(self.close)

        downloadReportBtn.resize(downloadReportBtn.sizeHint())
        downloadReportBtn.clicked.connect(self.downloadReport)

        downloadLogBtn.resize(downloadLogBtn.sizeHint())
        downloadLogBtn.clicked.connect(self.downloadLog)

        self.tipLabel = QLabel()
        # self.tipLabel.(QColor(20,150,150))
        self.tipLabel.setFont(QFont('sanserif', 12))
        self.tipLabel.setText('')



        self.errMsgLabel = QLabel()
        self.errMsgLabel.setFont(QFont('sanserif', 16))
        self.errMsgLabel.setText('')
        self.pe_red = QPalette()
        self.pe_red.setColor(QPalette.WindowText, Qt.Qt.red)
        self.errMsgLabel.setPalette(self.pe_red)

        self.tree = QTreeWidget()
        self.tree.setColumnCount(1)
        self.tree.setHeaderLabels([''])
        self.tree.setColumnWidth(0, 750)
        self.featureTree = QTreeWidgetItem()


        grid.addWidget(closeBtn, 1, 9)
        grid.addWidget(downloadReportBtn, 1, 10)
        # grid.addWidget(downloadLogBtn, 1, 10) # 日志下载暂时停用
        grid.addWidget(self.tipLabel, 2, 0, 1, 5)
        grid.addWidget(self.errMsgLabel, 2, 5, 1, 3)
        grid.addWidget(self.tree, 3, 0, 20, 11)
        self.setLayout(grid)

        self.show()

        cf = getter.get_app_conf()
        projectPath = str(cf.get('baseconf', 'projectLocation'))
        reportPath = os.path.join(projectPath, 'reports', str(id), 'report.log')
        # 获取结果 数据库查询
        res = getter.get_task_his_by_id(self.taskid)
        result = res['result']

        if len(result) == 0:
            self.errMsgLabel.setText('没有生成报告，请确定是否执行结束')
            return

        step_flag = None
        scen_flag = None
        total_cnt = 0
        failed_cnt = 0
        for f in result.split('\n'):
            if f.strip().startswith('场景:'):
                total_cnt += 1
                step_flag = True
                scen_flag = True
                self.featureTree = QTreeWidgetItem(self.tree)
                self.featureTree.setText(0, f.strip()[len('场景:'):].strip())
            elif not f.strip().startswith('背景:') and not f.strip().startswith('功能:') and not f.strip() == '':
                backgroundTree = QTreeWidgetItem(self.featureTree)
                if '...' in f:
                    backgroundTree.setText(0, f.replace('\n', '')[: f.index('...')])
                else:
                    backgroundTree.setText(0, f.replace('\n', ''))
                if 'passed' in f:
                    # backgroundTree.setBackground(0, QBrush(QColor(0, 250, 0)))
                    step_flag = True

                if 'failed' in f:
                    backgroundTree.setForeground(0, QBrush(QColor(250, 0, 0)))
                    step_flag = False
                    scen_flag = False
                    failed_cnt += 1

                if step_flag:
                    pass
                    # backgroundTree.setBackground(0, QBrush(QColor(0, 250, 0)))
                else:
                    # backgroundTree.setBackground(0, QBrush(QColor(250, 0, 0)))
                    backgroundTree.setForeground(0, QBrush(QColor(250, 0, 0)))



                if scen_flag:
                    self.featureTree.setForeground(0, QBrush(QColor(0, 250, 0)))
                else:
                    self.featureTree.setForeground(0, QBrush(QColor(255, 0, 0)))

        # file.close()

        self.tipLabel.setText('全部用例:' + str(total_cnt) + '条, 通过用例:' + str(total_cnt - failed_cnt) + '条, 失败用例:' + str(failed_cnt) + '条')

    def downloadReport(self):
        text, ok = QInputDialog.getText(self, '下载报告', '请输入保存文件路径(含文件名)')

        if ok:
            res = getter.get_task_his_by_id(self.taskid)
            result = res['result']
            file = open(text, 'w')
            for line in result.split('\n'):
                if len(line.strip()) > 0:
                    file.writelines(line)
                    file.writelines('\n')
            file.close()

    def downloadLog(self):
        print(self.tree.currentItem())
        if self.tree.currentItem() == None:
            self.errMsgLabel.setText('请选中要下载日志的用例')
            return

        self.errMsgLabel.setText('')
        text, ok = QInputDialog.getText(self, '下载日志', '请输入保存日志目录')
        if ok:

            item = QTreeWidgetItem(self.tree.currentItem())

            while type(item.parent()).__name__ != 'NoneType':
                item = item.parent()

            if not os.path.exists(text):
                os.makedirs(text)
            log_name = item.text(0) + '.log'
            logcat_file_name = os.path.join(text, log_name)

            print('要下载的日志为' + logcat_file_name + ', 任务ID为: ' + str(self.taskid) + ', 下载路径为: ' + text)
            # os.chdir(text)
            cf = getter.get_app_conf()

            logcat_url = 'http://' + str(cf.get('baseconf', 'serverIp')) + ':9527/' + str(self.taskid) + '/' + quote(log_name)
            print(logcat_url)
            subprocess.call('wget ' + logcat_url + ' --output-document=' + logcat_file_name, shell=True)


# app = QApplication(sys.argv)
# te = ViewResult()
# te.initUI(14)
# te.show()
# sys.exit(app.exec_())