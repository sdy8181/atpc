# -*- coding: utf-8 -*-

from PyQt5.QtGui import QFont
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import QAbstractItemView
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QListWidget
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QSpinBox
from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtWidgets import QWidget
from PyQt5 import Qt

from interface.get_data import getter


class EditWindow(QWidget):
    def __init__(self):
        super(EditWindow, self).__init__()

    def initUI(self,  sce_name=''):
        # 用例信息存放list
        self.feature_steps_info = []
        self.feature_info = {}

        self.setGeometry(10, 10, 900, 600)
        self.setWindowTitle('编辑用例')
        self.setWindowIcon(QIcon('./images/icon.jpg'))
        self.setWindowFlags(Qt.Qt.SubWindow)
        # self.setMaximumSize()

        grid = QGridLayout()

        featureLabel = QLabel('用例名称:')
        self.featureName = QLineEdit()
        self.featureName.setMinimumHeight(50)
        self.featureName.setPlaceholderText('用例名称保持唯一性')

        if not sce_name == '':
            self.featureName.setText(sce_name)
            self.featureName.setDisabled(True)

        self.featureName.textChanged[str].connect(self.chk_sce_name)

        self.flagLabel = QLabel(self)
        self.flagLabel.setFont(QFont("Roman times", 16, QFont.Bold))

        self.pe_red = QPalette()
        self.pe_red.setColor(QPalette.WindowText, Qt.Qt.red)
        self.pe_green = QPalette()
        self.pe_green.setColor(QPalette.WindowText, Qt.Qt.green)


        appLabel = QLabel('所属模块：', self)

        self.appCombo = QComboBox()
        self.appCombo.addItem('--请选择--')
        try:
            module_type = getter.get_filter_module_type_all()
            for mt in module_type:
                self.appCombo.addItem(mt['name'])
        except Exception as e:
            print(e)

        self.appCombo.activated[str].connect(self.add_module_to_feature)

        tagLabel = QLabel('用例类型:', self)

        self.tagCombo = QComboBox()
        self.tagCombo.addItem('--请选择--')
        try:
            scen_type = getter.get_filter_scen_type_all()
            for st in scen_type:
                self.tagCombo.addItem(st['name'])
        except Exception as e:
            print(e)

        self.tagCombo.activated[str].connect(self.add_tags_to_feature)

        self.tipLabel = QLabel(self)
        self.tipLabel.setFont(QFont("Roman times", 12))

        self.stepCombo = QComboBox()
        self.stepCombo.addItem('所有')
        self.stepCombo.addItem('公共')
        self.stepCombo.addItem('协议')
        try:
            module_type = getter.get_filter_module_type_all()
            for mt in module_type:
                self.stepCombo.addItem(mt['name'])
        except Exception as e:
            print(e)

        self.stepCombo.setCurrentIndex(0)
        self.stepCombo.currentTextChanged.connect(self.show_steps)

        self.search_step = QLineEdit()
        self.search_step.setPlaceholderText('请输入关键字')
        self.search_step.textChanged.connect(self.show_steps)
        self.step_list = QListWidget()

        upBtn = QPushButton('上移')
        downBtn = QPushButton('下移')
        delBtn = QPushButton('删除')


        upBtn.clicked.connect(self.up_step_in_feature)
        downBtn.clicked.connect(self.down_step_in_feature)
        delBtn.clicked.connect(self.del_step_from_feature)
        # saveStepBtn.clicked.connect(self.save_step_to_feature)

        # 创建用例步骤列表
        self.featureview = QTableWidget()
        self.featureview.setColumnCount(1)
        self.featureview.setHorizontalHeaderLabels(['用例步骤'])
        self.featureview.horizontalHeader().setStretchLastSection(True)
        self.featureview.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.featureview.clicked.connect(self.get_step_params)

         # 创建用例步骤参数列表
        self.stepParamview = QTableWidget()
        self.stepParamview.setColumnCount(2)
        self.stepParamview.setHorizontalHeaderLabels(['参数名', '参数值'])
        self.stepParamview.setColumnWidth(0, 180)
        self.stepParamview.horizontalHeader().setStretchLastSection(True)
        # 单元格发生变化就触发保存操作
        self.stepParamview.cellChanged.connect(self.save_step_to_feature)

        self.stepLabel = QLabel(self)
        self.stepLabel.setText('步骤信息:')

        self.stepTip = QTextEdit(self)
        self.stepTip.setEnabled(False)

        # 保存和取消按钮
        saveBtn = QPushButton('保存')
        cancelBtn = QPushButton('取消')
        cancelBtn.clicked.connect(self.close)
        saveBtn.clicked.connect(self.save_feature)

        grid.addWidget(featureLabel, 0, 0)
        grid.addWidget(self.featureName, 0, 1, 1, 8)
        grid.addWidget(self.flagLabel, 0, 9)
        grid.addWidget(appLabel, 1, 3)

        grid.addWidget(self.appCombo, 1, 4)

        grid.addWidget(tagLabel, 1, 0)
        grid.addWidget(self.tagCombo, 1, 1)

        grid.addWidget(self.tipLabel, 1, 6)

        grid.addWidget(self.stepCombo,2, 0)
        grid.addWidget(self.search_step, 2, 1, 1, 2)
        grid.addWidget(self.step_list, 3, 0, 20, 3)
        grid.addWidget(upBtn, 2, 3)
        grid.addWidget(downBtn, 2, 4)
        grid.addWidget(delBtn, 2, 5)
        # grid.addWidget(saveStepBtn, 2, 9)

        grid.addWidget(self.featureview, 3, 3, 20, 3)
        grid.addWidget(self.stepParamview, 3, 6, 10, 4)
        grid.addWidget(self.stepLabel, 14, 6, 1, 1)
        grid.addWidget(self.stepTip, 15, 6, 8, 4)

        grid.addWidget(saveBtn, 24, 8)
        grid.addWidget(cancelBtn, 24, 9)
        grid.setRowMinimumHeight(25, 30)

        # 设置数据展示
        try:
            self.show_steps()
        except:
            pass

        self.step_list.doubleClicked.connect(self.insert_step_to_feature)
        self.step_list.setCurrentRow(0)

        self.setLayout(grid)


        self.feature_info['module'] = ''
        self.feature_info['tags'] = ''
        try:
            self.show_feature_info(sce_name)
        except:
            pass

        self.show()

    # 往用例中添加步骤
    def insert_step_to_feature(self):
        step_txt = self.step_list.item(self.step_list.currentRow()).text()

       # 往用例列表中添加信息
        params = getter.get_step_params(step_txt)
        paramsList = []
        step_desc = ''
        for pa in params:
            p = {}
            p['name'] = pa['param']
            p['value'] = None
            print(pa['param'])
            paramsList.append(p)
            step_desc = pa['step_desc']

        stepInfo = {'name': step_txt, 'params': paramsList, 'step_desc': step_desc}

        self.feature_steps_info.append(stepInfo)
        print(self.feature_steps_info)
        self.refresh_feature_view()

    # 从用例中删除步骤
    def del_step_from_feature(self):
        cnt = self.featureview.currentRow()
        if cnt < 0:
            return
        self.feature_steps_info.pop(cnt)

        self.refresh_feature_view()

        count = self.featureview.rowCount()
        if count > -1:
            self.get_step_params()

    # 上移步骤
    def up_step_in_feature(self):
        idx = self.featureview.currentRow()

        if idx == -1:
            self.tipLabel.setText('请选中要移动的步骤')
            self.tipLabel.setPalette(self.pe_red)
            return
        self.tipLabel.setText('')
        if idx == 0:
            return
        tmp = self.feature_steps_info[idx]
        self.feature_steps_info.pop(idx)
        self.feature_steps_info.insert(idx - 1, tmp)

        # refresh featureview
        self.refresh_feature_view()
        self.get_step_params()

    # 下移步骤
    def down_step_in_feature(self):

        idx = self.featureview.currentRow()
        count = self.featureview.rowCount()
        if idx == count - 1:
            return

        tmp = self.feature_steps_info[idx]
        self.feature_steps_info.pop(idx)
        self.feature_steps_info.insert(idx + 1, tmp)

        # refresh featureview
        self.refresh_feature_view()
        self.get_step_params()

    # 获取步骤的参数信息
    def get_step_params(self):

        self.stepTip.clear()

        # 从列表中获取参数名和参数值
        idx = self.featureview.currentRow()
        if idx < 0:
            self.stepParamview.setRowCount(0)
            return

        params = self.feature_steps_info[idx]['params']

        if self.feature_steps_info[idx]['step_desc'] is not None:
            self.stepTip.setText(self.feature_steps_info[idx]['step_desc'])

        self.stepParamview.setRowCount(0)
        if len(params) == 0:
            return

        print(params)

        if len(params) > 0 and not params[0]['name']:
            return

        for i in range(len(params)):
            self.stepParamview.insertRow(i)
            self.stepParamview.setCellWidget(i, 0, QLabel(params[i]['name']))
            self.stepParamview.setItem(i, 1, QTableWidgetItem(params[i]['value']))

    # 保存步骤信息到用例
    def save_step_to_feature(self):
        idx = self.featureview.currentRow()
        count = self.stepParamview.rowCount()
        for i in range(count):

            params = self.feature_steps_info[idx]['params']
            for j in range(len(params)):
                if params[j]['name'] == self.stepParamview.cellWidget(i, 0).text():
                    params[j]['value'] = self.stepParamview.item(i, 1).text()
                    break

    # 刷新feature视图列表
    def refresh_feature_view(self):
        self.featureview.setRowCount(0)
        for i in range(len(self.feature_steps_info)):
            self.featureview.insertRow(i)
            self.featureview.setItem(i, 0, QTableWidgetItem(self.feature_steps_info[i]['name']))
        self.tipLabel.setText('')

    #     保存feature
    def save_feature(self):
        feature_name = self.featureName.text()
        if str(feature_name).strip() == '':
            self.flagLabel.setText('标题为空')
            self.flagLabel.setPalette(self.pe_red)
            return

        if self.feature_info['tags'] == '' or self.feature_info['tags'] == '--请选择--':
            self.tipLabel.setText('请选择用例类型')
            self.tipLabel.setPalette(self.pe_red)
            return

        if self.feature_info['module'] == '' or self.feature_info['module'] == '--请选择--':
            self.tipLabel.setText('请选择模块名称')
            self.tipLabel.setPalette(self.pe_red)
            return
        if len(self.feature_steps_info) == 0:
            self.tipLabel.setText('请添加步骤信息')
            self.tipLabel.setPalette(self.pe_red)
            return

        print(feature_name)
        self.feature_info['name'] = feature_name
        self.feature_info['steps'] = self.feature_steps_info
        self.feature_info['sce_type'] = self.feature_info['tags']
        getter.save_feature(self.feature_info)
        print(self.feature_info)
        self.close()

    # 添加标签到用例信息中
    def add_module_to_feature(self, item):
        self.feature_info['module'] = item

    def add_tags_to_feature(self, item):
        self.feature_info['tags'] = item

    # 校验场景信息是否完整
    def chk_sce_name(self, sce_name):

        if len(sce_name.strip()) == 0:
            self.flagLabel.setText('标题为空')
            self.flagLabel.setPalette(self.pe_red)
            return True
        feature = getter.get_feature_info(sce_name)

        if len(feature) > 0:
            self.flagLabel.setText('NO')
            self.flagLabel.setPalette(self.pe_red)
        else:
            self.flagLabel.setText('OK')
            self.flagLabel.setPalette(self.pe_green)

    # 展示步骤
    def show_steps(self):
        # 设置数据展示
        steps = getter.get_step_all()
        self.step_list.clear()
        stepListItem = []
        # 判断是所有 操作 还是验证
        step_type = self.stepCombo.currentText().strip()
        keyword = self.search_step.text().strip()

        for st in steps:
            # stepListItem.append(QListWidgetItem(st['name']))

            if keyword in st['name'] or keyword == '':
                if st['type'] == step_type:
                    stepListItem.append(QListWidgetItem(st['name']))
                if step_type == '所有':
                    stepListItem.append(QListWidgetItem(st['name']))

        for i in range(len(stepListItem)):
            self.step_list.insertItem(i, stepListItem[i])

    #展示界面元素信息
    def show_feature_info(self, sce_name=''):
        if not sce_name == '':
            feature_info = getter.get_feature_info(sce_name)
            self.feature_info['tags'] = feature_info['tags']
            self.tagCombo.setCurrentText(self.feature_info['tags'])

            self.feature_info['module'] = feature_info['module']
            self.appCombo.setCurrentText(self.feature_info['module'])

            self.feature_info['name'] = feature_info['sce_name']
            feature_step_info = getter.get_featrue_step_relationship(sce_name)
            print(len(feature_step_info))
            print(feature_step_info)
            if len(feature_step_info) > 0:
                for fs in feature_step_info:
                    step_id = fs['id']
                    step_info = getter.get_step_info_by_id(step_id)
                    step_name = step_info['name']
                    step_desc = step_info['step_desc']
                    step_idx = fs['idx']
                    params = fs['params']
                    st = {'name': step_name, 'params': params, 'step_desc': step_desc}
                    self.feature_steps_info.insert(step_idx,st)
            else:
                pass
        self.refresh_feature_view()








