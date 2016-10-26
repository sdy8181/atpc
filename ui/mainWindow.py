# -*- coding:utf-8 -*-
import os
import shutil
import subprocess
import sys
import socket
import threading
import webbrowser
from datetime import datetime

import time

from PyQt5.QtGui import QBrush
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QFont
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import QAbstractItemView
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QSpinBox
from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QProgressBar
from PyQt5.QtCore import Qt
from ui.appConfig import AppConfig
from interface.get_data import getter
from ui.atConfig import AtConfig

from ui.editWindow import EditWindow
from ui.viewResult import ViewResult

class MainWidget(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setGeometry(30, 30, 1420, 800)
        self.setWindowTitle('QGATP')
        self.setWindowIcon(QIcon('./images/icon.jpg'))


        self.runFlag = False
        self.features_runned_cnt = 0
        self.selected_features_cnt = 0

        self.hide_flag = True   # 筛选项隐藏标识， 默认隐藏
        self.hide_row = 4  # 筛选项组数
        self.grid = QGridLayout()

        # 已经勾选的关键词

        self.filter_words = {'module_words': [], 'scen_words': [], 'author_words': []}

    def initUI(self):

        #  菜单设置
        appSettingAction = QAction('&应用设置', self)
        appSettingAction.setStatusTip('客户端设置')
        appSettingAction.triggered.connect(self.showAppConf)

        scriptSettingAction = QAction('&脚本配置', self)
        scriptSettingAction.setStatusTip('脚本配置')
        scriptSettingAction.triggered.connect(self.showScriptConf)

        refreshAutotestScriptAction = QAction('&获取最新测试脚本', self)
        refreshAutotestScriptAction.setStatusTip('获取最新测试脚本')
        refreshAutotestScriptAction.triggered.connect(self.getLatestScript)

        settingCasesFilterAction = QAction('&用例筛选设置', self)
        settingCasesFilterAction.setStatusTip('用例筛选设置')
        settingCasesFilterAction.triggered.connect(self.showFilterSetting)

        menubar = self.menuBar()
        settingMenu = menubar.addMenu('设置')
        settingMenu.addAction(appSettingAction)
        settingMenu.addAction(scriptSettingAction)
        # menubar.setFixedHeight(22)

        optionMenu = menubar.addMenu('操作')
        optionMenu.addAction(refreshAutotestScriptAction)
        optionMenu.addAction(settingCasesFilterAction)

        # 设置筛选隐藏动作
        self.hideBtn = QPushButton('筛选>>', self)
        self.hideBtn.clicked.connect(self.hide_case_filter)

        self.filter_type_table = QTableWidget()
        self.filter_type_table.horizontalHeader().setVisible(False)
        self.filter_type_table.verticalHeader().setVisible(False)
        self.filter_type_table.horizontalScrollBar().setVisible(False)

        self.filter_type_table.setShowGrid(False)
        self.filter_type_table.setFrameShape(QFrame.NoFrame)
        self.filter_type_table.resizeColumnsToContents()
        self.filter_type_table.resizeRowsToContents()

        self.filter_type_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.filter_type_table.setFixedHeight(self.height()/20*3.5)
        self.filter_type_table.setRowCount(4)
        self.filter_type_table.setColumnCount(21)
        self.filter_type_table.setItem(0, 0, QTableWidgetItem('模块名称:'))
        self.filter_type_table.setSpan(1, 0, 2, 1)
        self.filter_type_table.setItem(1, 0, QTableWidgetItem('用例类型:'))
        self.filter_type_table.item(1, 0).setTextAlignment(Qt.AlignTop)

        self.filter_type_table.setItem(3, 0, QTableWidgetItem('人员分类:'))


        self.filter_type_table.itemClicked.connect(self.show_features)

        #设置背景透明
        self.no_palette = QPalette()
        self.no_palette.setColor(QPalette.Base, QColor(255, 255, 255, 0))
        self.filter_type_table.setPalette(self.no_palette)


        self.jenkinsLink = QPushButton('持续集成>>')
        self.jenkinsLink.clicked.connect(self.openJenkinsBrowser)

        self.progressBar = QProgressBar(self)
        self.progressBar.setGeometry(30, 40, 200, 25)
        self.progressBar.setValue(30 / 55 * 100)
        self.progressBar.hide()


        self.search_txt = QLineEdit(self)
        self.search_txt.setMinimumHeight(40)
        self.search_txt.setPlaceholderText('请输入搜索关键字,即：用例名称包含的关键字')
        # self.search_txt.setFixedHeight(38)
        self.search_txt.textChanged[str].connect(self.show_features)

        self.runBtn = QPushButton('运行')
        self.runBtn.resize(self.runBtn.sizeHint())

        self.loopLabel = QLabel('次数')
        self.loopSpinbox = QSpinBox()
        self.loopLabel.setFont(QFont('sanserif', 18))

        self.loopSpinbox.setRange(1, 5000)
        self.loopSpinbox.setValue(1)
        self.loopSpinbox.setFont(QFont('sanserif', 18))

        self.runBtn.setFont(QFont('sanserif', 18))
        # 默认不可点击，只有选中用例才可以点击
        self.runBtn.setDisabled(True)
        self.runBtn.clicked.connect(self.run_tests)

        self.selectAllBtn = QPushButton('全选')
        self.selectAllBtn.resize(self.selectAllBtn.sizeHint())
        self.selectAllBtn.setFont(QFont('sanserif', 8))
        self.selectAllBtn.clicked.connect(self.selectAllFeatures)

        self.inverseAllBtn = QPushButton('反选')
        self.inverseAllBtn.resize(self.selectAllBtn.sizeHint())
        self.inverseAllBtn.setFont(QFont('sanserif', 8))
        self.inverseAllBtn.clicked.connect(self.inverseAllFeatures)

        self.addBtn = QPushButton('添加')
        self.addBtn.resize(self.addBtn.sizeHint())
        self.addBtn.setFont(QFont('sanserif', 8))
        self.addBtn.clicked.connect(self.editFeatureWin)

        self.delBtn = QPushButton('删除')
        self.delBtn.resize(self.delBtn.sizeHint())
        self.delBtn.setFont(QFont('sanserif', 8))
        self.delBtn.setDisabled(True)
        self.delBtn.clicked.connect(self.del_features)


        self.refreshBtn = QPushButton('刷新')
        self.refreshBtn.resize(self.refreshBtn.sizeHint())
        self.refreshBtn.setFont(QFont('sanserif', 8))
        self.refreshBtn.clicked.connect(self.show_features)

        self.pe_red = QPalette()
        self.pe_red.setColor(QPalette.WindowText, Qt.red)

        self.tipLabel = QLabel()
        self.tipLabel.setFont(QFont("Roman times", 14, QFont.Bold))

        self.featureLabel = QLabel('测试用例列表', self)
        self.featureTable = QTableWidget()
        self.featureTable.setColumnCount(4)
        self.featureTable.setHorizontalHeaderLabels(['名称', '模块', '用例类型', '作者'])

        self.featureTable.setColumnWidth(0, 800)
        self.featureTable.horizontalHeader().setStretchLastSection(True)
        self.featureTable.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.featureTable.itemClicked.connect(self.check_features)
        self.featureTable.itemDoubleClicked.connect(self.editFeatureWin)


        self.resultLabel = QLabel('执行历史列表', self)
        self.resultTable = QTableWidget()
        self.resultTable.setColumnCount(4)
        self.resultTable.setHorizontalHeaderLabels(['任务编号', '任务状态', '操作时间', '查看结果'])
        self.resultTable.setColumnWidth(0, 100)
        self.resultTable.setColumnWidth(1, 500)
        self.resultTable.setColumnWidth(2, 400)


        self.resultTable.itemClicked.connect(self.view_result)

        # 设置表格自动适应窗口
        self.resultTable.horizontalHeader().setStretchLastSection(True)
        self.resultTable.setEditTriggers(QAbstractItemView.NoEditTriggers)


        # 添加布局
        tmpLabel = QLabel()
        tmpLabel.setLayout(self.grid)
        self.setCentralWidget(tmpLabel)

        self.refresh_filter()
        self.hide_case_filter()


        self.selected_feature_ids = []

        # 启动socket服务，来接收已经执行的用例数量

        t_socket_server = threading.Thread(target=self.start_socket_server)
        t_socket_server.setDaemon(True)
        t_socket_server.start()


    def refresh_filter(self):
        '''
        刷新筛选信息
        :return:

        '''

        # 模块筛选
        module_type = getter.get_filter_module_type_all()
        for i in range(len(module_type)):
            item = QTableWidgetItem(module_type[i]['name'])
            item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            item.setCheckState(Qt.Unchecked)
            item.setTextAlignment(Qt.AlignTop)
            print(i)
            self.filter_type_table.setItem(0, i+1, item)

        # 用例类型筛选
        scen_type = getter.get_filter_scen_type_all()
        for i in range(len(scen_type)):
            item = QTableWidgetItem(scen_type[i]['name'])
            item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            item.setCheckState(Qt.Unchecked)
            item.setTextAlignment(Qt.AlignTop)
            if i > 10:
                self.filter_type_table.setItem(2, i - 10, item)
            else:
                self.filter_type_table.setItem(1, i + 1, item)

        # 人员分类

        self.filter_type_table.resizeColumnsToContents()

    # 刷新界面布局
    def refresh_widgets(self):

        self.grid.addWidget(self.hideBtn, 0, 1)

        self.grid.addWidget(self.filter_type_table, 1, 1, 4, 17)

        self.grid.addWidget(self.jenkinsLink, 5 - self.hide_row, 19)

        self.grid.addWidget(self.search_txt, 5 - self.hide_row, 1, 1, 10)

        self.grid.addWidget(self.runBtn, 5 - self.hide_row, 11, 1, 2)
        self.grid.addWidget(self.loopLabel, 5 - self.hide_row, 13, 1, 1)
        self.grid.addWidget(self.loopSpinbox, 5 - self.hide_row, 14, 1, 2)

        self.grid.addWidget(self.featureLabel, 7 - self.hide_row, 1, 1, 2)
        self.grid.addWidget(self.tipLabel, 7 - self.hide_row, 3, 1, 6)
        self.grid.addWidget(self.selectAllBtn, 7 - self.hide_row, 15)
        self.grid.addWidget(self.inverseAllBtn, 7 - self.hide_row, 16)
        self.grid.addWidget(self.addBtn, 7 - self.hide_row, 17)
        self.grid.addWidget(self.delBtn, 7 - self.hide_row, 18)
        self.grid.addWidget(self.refreshBtn, 7 - self.hide_row, 19)

        self.grid.addWidget(self.featureTable, 9 - self.hide_row, 1, 15 + self.hide_row, 19)
        self.grid.addWidget(self.resultLabel, 24, 1, 2, 2)
        self.grid.addWidget(self.progressBar, 24, 3, 2, 9)
        self.grid.addWidget(self.resultTable, 26, 1, 10, 19)

        self.grid.setColumnMinimumWidth(7, 200)
        self.grid.setRowStretch(20, 1)

        try:
            self.show_features()
            self.show_task_history()
        except Exception as e:
            print('连接错误，请检查服务器地址和端口并重新启动')
            self.tipLabel.setText('连接错误，请检查服务器地址和端口并重新启动')
            self.tipLabel.setPalette(self.pe_red)
            print(e)

        self.show()


    def hide_case_filter(self):

        if self.hide_flag:
            self.hideBtn.setText('筛选>>>')
            self.hide_row = 4
            self.filter_type_table.hide()

        else:
            self.hideBtn.setText('筛选<<<')
            self.hide_row = 0
            self.filter_type_table.show()


        self.refresh_widgets()
        self.hide_flag = not self.hide_flag


    # 打开用例编辑界面
    def editFeatureWin(self, item):

        self.editFeature = EditWindow()
        # 根据传递参数判断是新增还是修改
        if not item:
            self.editFeature.initUI()
            return
        sce_name = self.featureTable.item(item.row(), 0).text()
        if item.column() == 0:
            if sce_name:
                self.editFeature.initUI(sce_name=sce_name)

    # 展示 刷新测试用例
    def show_features(self):

        # 清空筛选数据
        self.filter_words['module_words'] = []
        self.filter_words['scen_words'] = []
        self.filter_words['author_words'] = []
        # 获取column值
        column = self.filter_type_table.columnCount()
        row = self.filter_type_table.rowCount()

        #获取选中的模块名称关键字
        for j in range(column):
            if j < 1:
                continue
            item = self.filter_type_table.item(0, j)

            if item is None:
                break

            if item.checkState() == Qt.Checked:
                self.filter_words['module_words'].append(item.text())


        #获取选中的模块名称关键字
        for j in range(column):
            if j < 1:
                continue
            if j > 10:
                item = self.filter_type_table.item(2, j)
            else:
                item = self.filter_type_table.item(1, j)

            if item is None:
                break

            if item.checkState() == Qt.Checked:
                self.filter_words['scen_words'].append(item.text())

        print(self.filter_words)


        # 设置数据展示
        key_word = self.search_txt.text()
        try:
            features = getter.get_feature_all()
        except Exception as e:
            self.tipLabel.setText('连接错误，请检查服务器地址和端口并重新启动')
            self.tipLabel.setPalette(self.pe_red)
            print(e)
            return
        i = 0
        self.featureTable.setRowCount(0)
        for f in features:

            if (not key_word in f['name']) or (not f['type'] in self.filter_words['module_words'] and len(self.filter_words['module_words']) > 0) or (not f['sce_type'] in self.filter_words['scen_words'] and len(self.filter_words['scen_words']) > 0):
                continue
            self.featureTable.insertRow(i)
            item = QTableWidgetItem(f['name'])
            item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            item.setCheckState(Qt.Unchecked)
            self.featureTable.setItem(i, 0, item)
            author = QTableWidgetItem(f['author'])

            self.featureTable.setItem(i, 1, QTableWidgetItem(f['type']))
            self.featureTable.setItem(i, 2, QTableWidgetItem(f['sce_type']))
            self.featureTable.setItem(i, 3, author)

            i += 1
        self.show_task_history()
    # 显示任务历史
    def show_task_history(self):
        # self.resultTable
        # 获取任务历史
        tasks = getter.get_task_history()
        self.resultTable.setRowCount(0)

        for i in range(len(tasks)):
            task = tasks[i]
            self.resultTable.insertRow(i)
            self.resultTable.setItem(i, 0, QTableWidgetItem(str(task['id'])))
            self.resultTable.setItem(i, 1, QTableWidgetItem(task['status']))
            self.resultTable.setItem(i, 2, QTableWidgetItem(task['date_time']))

            # viewResult = QLabel("#00ff00",'查看')
            # self.resultTable.setCellWidget(i, 4, viewResult)

            self.resultTable.setItem(i, 3, QTableWidgetItem('查看'))

    # 查看任务执行报告
    def view_result(self, item):
        cnt = item.row()
        taskid = self.resultTable.item(cnt, 0).text()
        if item.column() == 3:
            self.viewResult = ViewResult()
            self.viewResult.initUI(taskid)

    # 选中feature
    def check_features(self, item):
        it = self.featureTable.item(item.row(), 0)
        if item.column() == 0:
            # 获取选中的feature id
            self.selected_feature_ids.clear()
            # 遍历所有数据并把选中的数据放入列表
            row_count = self.featureTable.rowCount()
            for i in range(row_count):
                row = self.featureTable.item(i, 0)
                if row.checkState() == Qt.Checked:
                    id = getter.get_feature_info(row.text())['id']
                    self.selected_feature_ids.append(id)

        if len(self.selected_feature_ids) > 0:
            self.runBtn.setEnabled(True)
            self.delBtn.setEnabled(True)
        else:
            self.runBtn.setDisabled(True)
            self.delBtn.setDisabled(True)

    #  删除用例
    def del_features(self):
        for id in self.selected_feature_ids:
            getter.del_feature(id)
        self.selected_feature_ids.clear()
        self.show_features()

    # 获取最新测试脚本
    def getLatestScript(self):

        # 生成测试用例文件
        cf = getter.get_app_conf()
        projectPath = str(cf.get('baseconf', 'projectLocation'))
        # 删除原来的工程
        # 先删除.git文件夹
        git_dir_path = os.path.join(projectPath, '.git')
        git_url = str(cf.get('baseconf', 'gitUrlForScript'))

        if os.path.exists(git_dir_path):
            if sys.platform == 'linux':
                shutil.rmtree(git_dir_path)
            else:
                subprocess.call('rd /q/s ' + git_dir_path, shell=True)

        try:
            fileList = os.listdir(projectPath)
            for f in fileList:
                testProjPath = os.path.join(projectPath, f)
                if os.path.isfile(testProjPath):
                    os.remove(testProjPath)
                else:
                    shutil.rmtree(testProjPath)
        except Exception as e:
            self.tipLabel.setText(str(e))
            self.tipLabel.setPalette(self.pe_red)
        # 从git服务器上下载最新的测试工程
        from git import Repo
        try:
            t = threading.Thread(target=Repo.clone_from, args=(git_url, projectPath))
            t.setDaemon(True)
            t.start()
            t.join()

            # 复制配置文件
            homeDir = os.path.expanduser('~')
            shutil.copyfile(os.path.join(homeDir, '.config.ini'), os.path.join(projectPath,  'support', 'config.ini'))

            # Repo.clone_from('https://github.com/ouguangqian/autotestproject.git', projectPath)
        except Exception as e:
            print(e)
            self.tipLabel.setText('测试工程脚本下载失败，请联系相关负责人')
            self.tipLabel.setPalette(self.pe_red)
            return

        self.tipLabel.setText('测试脚本更新完成')
        self.tipLabel.setPalette(self.pe_red)

    # 执行测试
    def run_tests(self):
        global t
        # 设置运行按钮展示字符
        self.runFlag = not self.runFlag
        self.tipLabel.setText('')

        if self.runFlag:

            self.selected_features_cnt = len(self.selected_feature_ids)
            self.features_runned_cnt = 0
            print(self.selected_features_cnt)
            self.progressBar.show()
            self.progressBar.setValue(0)
            self.runBtn.setText('停止')

        else:
            self.progressBar.hide()
            self.runBtn.setText('运行')
            print('用例运行状态为: ' + str(t.is_alive()))
            if t.is_alive():
                if sys.platform == 'linux':
                    ret = subprocess.Popen('ps -ef | grep behave', stdout=subprocess.PIPE, shell=True).stdout.readlines()
                    for r in ret:
                        r = r.decode().strip()
                        if 'grep' in r:
                            continue

                        while '  ' in r:
                            r = r.replace('  ', ' ')
                        rlist = r.split(' ')

                        pid = rlist[1]
                        print('pid:' + pid)
                        try:
                            subprocess.call('kill -9 ' + pid, shell=True)
                        except Exception as e:
                            self.tipLabel.setText('用例停止失败，可以尝试重启应用解决')
                            print(e)
                else:
                    ret = subprocess.Popen('tasklist -V | findstr behave', stdout=subprocess.PIPE).stdout.readlines()
                    for r in ret:
                        r = r.decode('unicode_escape').strip()
                        while '  ' in r:
                            r = r.replace('  ', ' ')

                        rlist = r.split(' ')
                        pid = rlist[1]
                        try:
                            print(rlist[1])
                            subprocess.call('taskkill /T /F /pid ' + pid, shell=True)
                            break
                        except Exception as e:
                            self.tipLabel.setText('用例停止失败，可以尝试重启应用解决')
                            print(e)
            return


        # 获取用例循环次数
        loopCnt = self.loopSpinbox.value()

        date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
        status = '执行中'
        feature_ids = ''
        # 根据选中的用例保存用例信息
        for id in self.selected_feature_ids:
            if not len(feature_ids) == 0:
                feature_ids += ','
            feature_ids += str(id)

        data = {'status': status, 'date_time': date_time, 'feature_ids': feature_ids}
        ret_save = getter.save_task_history(data)
        self.show_task_history()


        # 生成测试用例文件
        cf = getter.get_app_conf()
        projectPath = str(cf.get('baseconf', 'projectLocation'))

        featurePath = os.path.join(projectPath, 'features')
        filelist = os.listdir(featurePath)

        if len(filelist) > 0:
            for f in filelist:
                if f.endswith('.feature'):
                    os.remove(os.path.join(featurePath, f))

        # 写feature文件
        for id in self.selected_feature_ids:
            fileName = os.path.join(featurePath, 'testcase-' + datetime.now().strftime('%Y_%m_%d%H_%M_%S_%f') + '.feature')
            print('要写入的文件为: ' + fileName)
            file = open(fileName, 'w', encoding='utf-8')
            print('写入文件的场景ID为: ' + str(id))
            # 根据id 获取场景的feature_name and sce_name
            feature = getter.get_feature_info_by_id(id)

            print('# language: zh-CN')
            print('功能: ' + feature['feature_name'])
            # print(feature['tags'])
            print('场景: ' + feature['sce_name'])
            file.writelines('# language: zh-CN')
            file.writelines('\n')
            file.writelines('功能: ' + feature['feature_name'])
            file.writelines('\n')
            # file.writelines(feature['tags'])
            # file.writelines('\n')
            file.writelines('场景: ' + feature['sce_name'])
            file.writelines('\n')
            # 根据名称 获取关联的步骤场景
            try:
                feature_steps_relationship = getter.get_featrue_step_relationship(feature['sce_name'])
            except:
                self.tipLabel.setText('获取步骤信息错误，可能步骤被删除')

            if len(feature_steps_relationship) > 0:
                feature_steps_info = []
                for fs in feature_steps_relationship:
                    step_id = fs['id']
                    step_info = getter.get_step_info_by_id(step_id)
                    step_name = step_info['name']
                    step_is_chk = step_info['is_chk']
                    step_idx = fs['idx']
                    params = fs['params']
                    st = {'name': step_name, 'is_chk':step_is_chk, 'params': params}
                    feature_steps_info.insert(step_idx, st)

                for fsi in feature_steps_info:
                    if fsi['is_chk']:
                        print('那么< ' + fsi['name'])
                        file.writelines('那么< ' + fsi['name'])
                        file.writelines('\n')
                    else:
                        print('当< ' + fsi['name'])
                        file.writelines('当< ' + fsi['name'])
                        file.writelines('\n')

                    if len(fsi['params']) > 0:
                        for p in fsi['params']:
                            print('|' + p['name'], end='')
                            file.writelines('|' + p['name'])
                        print('|')
                        file.writelines('|')
                        file.writelines('\n')
                        for v in fsi['params']:
                            print('|' + v['value'], end='')
                            file.writelines('|' + v['value'])
                        print('|')
                        file.writelines('|')
                        file.writelines('\n')
            file.close()
        print('文件生成完成')
        # 运行测试用例
        os.chdir(projectPath)
        # 调用运行测试用例函数
        t = threading.Thread(target=self.run_behave_cmd, args=(ret_save['id'], loopCnt))
        t.setDaemon(True)
        t.start()
    # 运行behave命令 并生成xml 报告文件
    def run_behave_cmd(self, id, loopCnt):
        cf = getter.get_app_conf()
        projectPath = str(cf.get('baseconf', 'projectLocation'))
        # reportPath = os.path.join(projectPath, 'reports', str(id))
        reportPath = os.path.join(projectPath, 'reports', str(id), 'report.log')

        # os.system('behave  -k --junit --junit-directory ' + reportPath)
        try:
            for i in range(int(loopCnt)):
                os.system('behave  -k --show-source --show-timings --format plain --outfile ' + reportPath)
        except:
            pass
        finally:
            self.progressBar.hide()
            self.runBtn.setText('运行')
            self.runBtn.setEnabled(True)

        # 上传logcat日志信息到服务器端
        print('执行结束,更新任务状态')
        try:
            getter.update_task_status(id)
            file = open(reportPath, 'r').read()
            data = {'id': id, 'result': file}
            getter.save_result_to_task_his(data)
        except Exception as e:
            raise Exception(e)
        finally:
            self.show_task_history()
            # 日志上传暂时停用,日志太多容易引起阻塞
            # getter.upload_logcat_file_to_server(id)

    # 启动查看报告服务 默认端口 9527
    # def run_http_server(self):
    #     cf = getter.get_app_conf()
    #     projectPath = str(cf.get('baseconf', 'projectLocation'))
    #     reportPath = os.path.join(projectPath, 'reports')
    #     # 判断目录不存在创建目录
    #     if not os.path.exists(reportPath):
    #         os.mkdir(reportPath)
    #
    #     os.chdir(reportPath)
    #     # 先杀掉进程
    #     if sys.platform == 'linux':
    #         ret = os.popen('netstat -anp | grep 9527').readlines()
    #         for r in ret:
    #             if '9527' in r:
    #                 while '  ' in r:
    #                     r = r.replace('  ', ' ')
    #
    #                 pid = (r.strip().split(' ')[6].split('/')[0])
    #                 os.system('kill -9 ' + pid)
    #                 break
    #         os.system('python3 -m http.server 9527')
    #     else:
    #         ret = os.popen('netstat -ano | findstr 9527').readlines()
    #         for r in ret:
    #             if '9527' in r:
    #                 while '  ' in r:
    #                     r = r.replace('  ', ' ')
    #
    #                 pid = r.strip().split(' ')[4]
    #                 os.system('taskkill /F /pid ' + pid)
    #                 break
    #         os.system('python -m http.server 9527')

    def start_socket_server(self):

        socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_server.bind(('localhost', 8899))
        socket_server.listen(1)
        while True:
            print('ready to accept')
            con, addr = socket_server.accept()
            try:
                buf = con.recv(1024).decode('utf-8')
                print(buf)
                self.features_runned_cnt += 1
                print(self.features_runned_cnt)
                self.progressBar.setValue(self.features_runned_cnt / self.selected_features_cnt * 100)
                print('aaa')
            except Exception as e:
                print(e)
                self.tipLabel.setText('读取用例执行进度数据异常')
                self.tipLabel.setPalette(self.pe_red)


    def selectAllFeatures(self):
        rowCnt = self.featureTable.rowCount()
        if rowCnt == 0:
            return
        for i in range(rowCnt):
            # self.featureTable.setCurrentItem(QTableWidgetItem(self.featureTable.itemAt(i+1,0)))
            item = self.featureTable.item(i, 0)
            if not item.checkState() == Qt.Checked:
                # item.setCheckState(Qt.Unchecked)
                item.setCheckState(Qt.Checked)
            if i == rowCnt - 1:
                self.check_features(item)

    def inverseAllFeatures(self):
        rowCnt = self.featureTable.rowCount()
        if rowCnt == 0:
            return
        for i in range(rowCnt):
            # self.featureTable.setCurrentItem(QTableWidgetItem(self.featureTable.itemAt(i+1,0)))
            item = self.featureTable.item(i, 0)
            if item.checkState() == Qt.Checked:
                item.setCheckState(Qt.Unchecked)
            else:
                item.setCheckState(Qt.Checked)

            if i == rowCnt - 1:
                self.check_features(item)
    # 打开应用配置
    def showAppConf(self):
        self.appConfig = AppConfig()
        self.appConfig.initUI()

    #打开过滤配置

    def showFilterSetting(self):
        from ui.caseFilterWords import CaseFilterWords
        self.filterWin = CaseFilterWords()

    # 打开脚本配置
    def showScriptConf(self):

        try:
            getter.get_app_conf()
        except Exception as e:
            self.tipLabel.setText(e)
            self.tipLabel.setPalette(self.pe_red)
            return
        self.atConfig = AtConfig()
        self.atConfig.initUI()

    def openJenkinsBrowser(self):
        webbrowser.open_new_tab('http://10.10.99.87:8080/job/OS2.0_AllTests/')
