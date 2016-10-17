# -*- coding: utf-8 -*-
import json
import os
import subprocess

import requests
from configparser import ConfigParser

import time


class GetData:
    
    def get_request_url(self):
        cf = self.get_app_conf()
        host = str(cf.get('baseconf', 'serverIp'))
        port = str(cf.get('baseconf', 'serverPort'))

        url = 'http://' + host + ':' + port
        return url
    def get_step_all(self):
        r = requests.get(self.get_request_url() + '/atp/steps/all')
        return r.json()

    def get_step_params(self, step):
        res = requests.get(self.get_request_url() + '/atp/steps/params/' + step)
        return res.json()
    def get_feature_all(self):
        res = requests.get(self.get_request_url() + '/atp/features/all')
        return res.json()

    def save_feature(self, data):
        res = requests.post(self.get_request_url() + '/atp/feature/save', json=data)
        print(res.text)

    def get_feature_info(self, scn_name):
        res = requests.get(self.get_request_url() + '/atp/feature/info/' + scn_name)
        print(res.text)
        return res.json()
        # return res.json()

    def get_feature_info_by_id(self, feature_id):
        res = requests.get(self.get_request_url() + '/atp/feature/info/id=' + str(feature_id))
        print(res.text)
        return res.json()

    def get_featrue_step_relationship(self, scen_name):
        res = requests.get(self.get_request_url() + '/atp/feature/featureStepsRelationShip/' + scen_name)

        return res.json()
    def get_step_info_by_id(self, id):
        res = requests.get(self.get_request_url() + '/atp/steps/info/' + str(id))
        return res.json()
    def del_feature(self, feature_id):
        res = requests.get(self.get_request_url() + '/atp/feature/del/' + str(feature_id))
        return res.json()

    def del_step_by_name(self, name):
        res = requests.get(self.get_request_url() + '/atp/step/del/' + name)
        return res.json()

    def save_task_history(self, data):
        res = requests.post(self.get_request_url() + '/atp/task/save', json=data)
        # print(res.json())
        return res.json()

    def get_task_history(self):
        res = requests.get(self.get_request_url() + '/atp/task/all')
        return res.json()

    def update_task_status(self, id):
        res = requests.get(self.get_request_url() + '/atp/task/status/update/' + str(id))
        return res.json()

    def get_app_conf(self):
        # 获取当前用户目录
        curUserDir = os.path.expanduser('~')
        # 读取用户工程路径位置
        appConfigPath = os.path.join(curUserDir, '.atp.ini')
        if not os.path.exists(appConfigPath):
            raise Exception('应用配置文件不存在， 请先设置应用配置')

        cf = ConfigParser()
        cf.read(appConfigPath)
        return cf

    def save_result_to_task_his(self, data):
        res = requests.post(self.get_request_url() + '/atp/task/result/save', json=data)
        return res.json()

    def update_step_info(self, data):
        res = requests.post(self.get_request_url() + '/atp/step/info/update', json=data)
        return res.json()


    def get_step_info_by_name(self, name):
        res = requests.get(self.get_request_url() + '/atp/step/info/' + name)
        return res.json()

    # 通过任务ID获取任务历史记录
    def get_task_his_by_id(self, id):
        print(id)
        res = requests.get(self.get_request_url() + '/atp/task/' + str(id))

        print(res.json())
        return res.json()

    # 上传logcat日志到服务器
    def upload_logcat_file_to_server(self, id):
        cf = self.get_app_conf()
        projectPath = str(cf.get('baseconf', 'projectLocation'))
        atConfigPath = os.path.join(projectPath, 'support', 'config.ini')
        cf = ConfigParser()
        cf.read(atConfigPath)
        log_path = str(cf.get('baseconf', 'logPath'))
        # 进入到log目录下
        file_list = os.listdir(log_path)
        for file in file_list:
            file_path = os.path.join(log_path, file)
            if os.path.isfile(file_path):
                try:
                    f = open(file_path, 'r', encoding='utf-8')
                    for line in f:
                        time.sleep(0.001)
                        data = {'taskId': str(id), 'fileName': file, 'content': line}
                        r = requests.post(self.get_request_url() + '/atp/logcat/log', json=data)
                except:
                    pass
                finally:
                    f.close()

getter = GetData()

