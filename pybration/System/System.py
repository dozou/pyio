# -*- coding: utf-8 -*-
import datetime
import os
import json
from pybration.DataSturucture import DataContainer


class System:

    def __init__(self, data: DataContainer=None):
        self.data = data
        pass

    def load_param(self):
        try:
            print("LOAD_PARAMETER:"+os.environ['HOME']+"/.pybration/param.json")
            param = open(os.environ['HOME']+"/.pybration/param.json", 'r')
            self.data.parameter = json.load(param)
        except IOError:
            print("LOAD_PARAMETER:default")
            param = get_default_param()
            self.data.parameter = param

    def get_data_dir(self):
        work_dir = self.data.parameter["System"]["work_folder"]
        sub_name = "/" + str(self.data.parameter['ExperimentInfo']['subject_name'])
        eid = str(self.data.parameter['ExperimentInfo']['experiment_id'])
        dir_name = "EID" + str(eid)
        work_dir = work_dir + "/" + dir_name
        work_dir = self.check_dir_str(work_dir)
        if not os.path.exists(work_dir):
            os.makedirs(work_dir)
        work_dir = work_dir + sub_name
        if not os.path.exists(work_dir):
            os.mkdir(work_dir)
        return work_dir

    def check_dir_str(self, dir_str: list):
        if str is type(dir_str):
            dir_str = [dir_str]

        for i,d in enumerate(dir_str):
            dir_str[i] = d.replace("//", "/")
            dir_str[i] = d.replace("~", os.environ['HOME'])
        return dir_str
