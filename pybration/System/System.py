# -*- coding: utf-8 -*-
import datetime
import os
from pybration.DataSturucture import DataContainer


class System:

    def __init__(self, data: DataContainer=None):
        self.data = data
        pass

    def get_data_dir(self):
        work_dir = self.data.parameter["System"]["work_folder"]
        sub_name = "/" + str(self.data.parameter['ExperimentInfo']['subject_name'])
        eid = str(self.data.parameter['ExperimentInfo']['experiment_id'])
        d = datetime.datetime.today()
        dir_name = d.strftime("%m%d")
        dir_name = dir_name + "_EID" + str(eid)
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
        if len(dir_str) == 1:
            return dir_str[0]
        return dir_str
