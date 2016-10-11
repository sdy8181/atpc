# -*- coding:utf-8 -*-
import os
import shutil
import subprocess
import sys
import threading
import webbrowser
from datetime import datetime

from PyQt5.QtGui import QFont
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import QAbstractItemView
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QSpinBox
from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtCore import Qt
from ui.appConfig import AppConfig
from interface.get_data import getter
from ui.atConfig import AtConfig
from ui.editWindow import EditWindow
from ui.viewResult import ViewResult

class MainWidget(QMainWindow):
    def __init__(self):
        super().__init__()

    def initUI(self):
        # 设置布局方式
        grid = QGridLayout()

        #  菜单设置
        appSettingAction = QAction('&应用设置', self)
        appSettingAction.setStatusTip('客户端设置')
        appSettingAction.triggered.connect(self.showAppConf)

        scriptSettingAction = QAction('&脚本配置', self)
        scriptSettingAction.setStatusTip('脚本配置')
        scriptSettingAction.triggered.connect(self.showScriptConf)

        menubar = self.menuBar()
        settingMenu = menubar.addMenu('设置')
        settingMenu.addAction(appSettingAction)
        settingMenu.addAction(scriptSettingAction)
        # menubar.setFixedHeight(22)

        # 测试用例筛选
        appLabel = QLabel('模块名称:', self)
        self.audioCheckbox = QCheckBox('音乐', self)
        self.radioCheckbox = QCheckBox('电台', self)
        self.ivokaCheckbox = QCheckBox('语音', self)
        self.videoCHeckbox = QCheckBox('视频', self)

        self.audioCheckbox.stateChanged.connect(self.show_features)
        self.radioCheckbox.stateChanged.connect(self.show_features)
        self.ivokaCheckbox.stateChanged.connect(self.show_features)
        self.videoCHeckbox.stateChanged.connect(self.show_features)


        tagLabel = QLabel('用例类型:', self)
        self.baseScenCheckbox = QCheckBox('基本场景', self)
        self.mutiScenCheckbox = QCheckBox('复杂场景', self)
        self.btScenCheckbox = QCheckBox('蓝牙电话场景', self)
        self.ivokaScenCheckbox = QCheckBox('语音场景', self)

        self.baseScenCheckbox.stateChanged.connect(self.show_features)
        self.mutiScenCheckbox.stateChanged.connect(self.show_features)
        self.btScenCheckbox.stateChanged.connect(self.show_features)
        self.ivokaScenCheckbox.stateChanged.connect(self.show_features)

        self.jenkinsLink = QPushButton('持续集成>>')
        self.jenkinsLink.clicked.connect(self.openJenkinsBrowser)


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

        selectAllBtn = QPushButton('全选')
        selectAllBtn.resize(selectAllBtn.sizeHint())
        selectAllBtn.setFont(QFont('sanserif', 8))
        selectAllBtn.clicked.connect(self.selectAllFeatures)

        inverseAllBtn = QPushButton('反选')
        inverseAllBtn.resize(selectAllBtn.sizeHint())
        inverseAllBtn.setFont(QFont('sanserif', 8))
        inverseAllBtn.clicked.connect(self.inverseAllFeatures)

        addBtn = QPushButton('添加')
        addBtn.resize(addBtn.sizeHint())
        addBtn.setFont(QFont('sanserif', 8))
        addBtn.clicked.connect(self.editFeatureWin)

        self.delBtn = QPushButton('删除')
        self.delBtn.resize(self.delBtn.sizeHint())
        self.delBtn.setFont(QFont('sanserif', 8))
        self.delBtn.setDisabled(True)
        self.delBtn.clicked.connect(self.del_features)


        refreshBtn = QPushButton('刷新')
        refreshBtn.resize(refreshBtn.sizeHint())
        refreshBtn.setFont(QFont('sanserif', 8))
        refreshBtn.clicked.connect(self.show_features)

        self.pe_red = QPalette()
        self.pe_red.setColor(QPalette.WindowText, Qt.red)

        self.tipLabel = QLabel()
        self.tipLabel.setFont(QFont("Roman times", 14, QFont.Bold))

        featureLabel = QLabel('测试用例列表', self)
        self.featureTable = QTableWidget()
        self.featureTable.setColumnCount(4)
        self.featureTable.setHorizontalHeaderLabels(['名称', '模块', '用例类型', '作者'])

        self.featureTable.setColumnWidth(0, 800)
        self.featureTable.horizontalHeader().setStretchLastSection(True)
        self.featureTable.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.featureTable.itemClicked.connect(self.check_features)
        self.featureTable.itemDoubleClicked.connect(self.editFeatureWin)



        resultLabel = QLabel('执行历史列表', self)
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

        grid.setRowMinimumHeight(0,20)

        grid.addWidget(appLabel, 1, 1)
        grid.addWidget(self.audioCheckbox, 1, 2)
        grid.addWidget(self.radioCheckbox, 1, 3)
        grid.addWidget(self.ivokaCheckbox, 1, 4)
        grid.addWidget(self.videoCHeckbox, 1, 5)

        grid.addWidget(tagLabel, 1, 6)
        grid.addWidget(self.baseScenCheckbox, 1, 7)
        grid.addWidget(self.mutiScenCheckbox, 1, 8)
        grid.addWidget(self.btScenCheckbox, 1, 9)
        grid.addWidget(self.ivokaScenCheckbox, 1, 10)
        grid.addWidget(self.jenkinsLink, 1, 19)

        grid.addWidget(self.search_txt, 2, 1, 1, 10)

        grid.addWidget(self.runBtn, 2, 11, 1, 2)
        grid.addWidget(self.loopLabel, 2, 13, 1, 1)
        grid.addWidget(self.loopSpinbox, 2, 14, 1, 2)

        grid.addWidget(featureLabel, 5, 1, 1, 2)
        grid.addWidget(self.tipLabel, 5, 3, 1, 6)
        grid.addWidget(selectAllBtn, 5, 15)
        grid.addWidget(inverseAllBtn, 5, 16)
        grid.addWidget(addBtn, 5, 17)
        grid.addWidget(self.delBtn, 5, 18)
        grid.addWidget(refreshBtn, 5, 19)

        grid.addWidget(self.featureTable, 7, 1, 15, 19)
        grid.addWidget(resultLabel, 22, 1, 2, 19)
        grid.addWidget(self.resultTable, 24, 1, 10, 19)

        grid.setColumnMinimumWidth(5, 200)
        grid.setRowStretch(18, 1)

        tmpLabel = QLabel()
        tmpLabel.setLayout(grid)
        # self.setLayout(grid)
        self.setCentralWidget(tmpLabel)

        self.setGeometry(30, 30, 1420, 800)
        self.setWindowTitle('QGATP')
        self.setWindowIcon(QIcon('./images/icon.jpg'))
        try:
            self.show_features()
            self.show_task_history()
        except Exception as e:
            print('连接错误，请检查服务器地址和端口并重新启动')
            self.tipLabel.setText('连接错误，请检查服务器地址和端口并重新启动')
            self.tipLabel.setPalette(self.pe_red)

        self.selected_feature_ids = []

        # global t_http
        # t_http = threading.Thread(target=self.run_http_server)
        # t_http.setDaemon(True)
        # t_http.start()

        self.show()

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
        self.tipLabel.clear()
        sce_type_filter=[]
        if self.baseScenCheckbox.isChecked():
            sce_type_filter.append(self.baseScenCheckbox.text())
        if self.mutiScenCheckbox.isChecked():
            sce_type_filter.append(self.mutiScenCheckbox.text())
        if self.btScenCheckbox.isChecked():
            sce_type_filter.append(self.btScenCheckbox.text())
        if self.ivokaScenCheckbox.isChecked():
            sce_type_filter.append(self.ivokaScenCheckbox.text())

        type_filter = []
        if self.audioCheckbox.isChecked():
            type_filter.append(self.audioCheckbox.text())
        if self.videoCHeckbox.isChecked():
            type_filter.append(self.videoCHeckbox.text())
        if self.radioCheckbox.isChecked():
            type_filter.append(self.radioCheckbox.text())
        if self.ivokaCheckbox.isChecked():
            type_filter.append(self.ivokaCheckbox.text())

        # 设置数据展示
        key_word = self.search_txt.text()
        features = []
        try:
            features = getter.get_feature_all()
        except:
            self.tipLabel.setText('连接错误，请检查服务器地址和端口并重新启动')
            self.tipLabel.setPalette(self.pe_red)
            return
        i = 0
        self.featureTable.setRowCount(0)
        for f in features:
            '''
            type = ''
            sce_type = ''

            # 暂时有些多余，先这样处理，以防后续扩展

            if f['type'] == 'ivoka':
                type = '语音'
            elif f['type'] == 'music':
                type = '音乐'
            elif f['type'] == 'radio':
                type = '电台'
            elif f['type'] == 'video':
                type = '视频'

            if f['sce_type'] == '@baseScen':
                sce_type = '基本场景'
            elif f['sce_type'] == '@complexScen':
                sce_type = '复杂场景'
            elif f['sce_type'] == '@btScen':
                sce_type = '蓝牙场景'
            elif f['sce_type'] == '@ivokaScen':
                sce_type = '语音场景'
                '''
            if (not key_word in f['name']) or (not f['type'] in type_filter and len(type_filter) > 0) or (not f['sce_type'] in sce_type_filter and len(sce_type_filter) > 0):
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

    # 执行测试
    def run_tests(self):

        self.tipLabel = ''
        self.runBtn.setText('运行中')
        self.runBtn.setEnabled(False)

        # 获取用例循环次数
        loopCnt = self.loopSpinbox.value()

        date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
        status = '执行中'
        feature_ids = ''
        # 根据选中的用例保存用例信息
        for id in  self.selected_feature_ids:
            if not len(feature_ids) == 0:
                feature_ids += ','
            feature_ids += str(id)

        data = {'status': status, 'date_time': date_time, 'feature_ids': feature_ids}
        ret_save = getter.save_task_history(data)
        self.show_task_history()


        # 生成测试用例文件
        cf = getter.get_app_conf()
        projectPath = str(cf.get('baseconf', 'projectLocation'))
        # 删除原来的工程
        # 先删除.git文件夹
        git_dir_path = os.path.join(projectPath, '.git')

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
            Repo.clone_from('https://github.com/ouguangqian/autotestproject.git', projectPath)
        except:
            self.tipLabel.setText('测试工程脚本下载失败，请联系相关负责人')
            self.tipLabel.setPalette(self.pe_red)
            return

        # 复制配置文件
        homeDir = os.path.expanduser('~')
        shutil.copyfile(os.path.join(homeDir, '.config.ini'), os.path.join(projectPath,  'support', 'config.ini'))

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
            feature_steps_relationship = getter.get_featrue_step_relationship(feature['sce_name'])
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
        global t
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
