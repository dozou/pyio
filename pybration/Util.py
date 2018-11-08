# -*- coding: utf-8 -*-
import datetime
import os
import sys
import json
import re
from pybration.Tools.Json import get_default_param
from pybration.DataSturucture import DataContainer
from pkg_resources import get_distribution


class System:

    def __init__(self, data: DataContainer=DataContainer()):
        self.data = data

    def load_param(self)->DataContainer:
        try:
            print("LOAD_PARAMETER:"+os.environ['HOME']+"/.pybration/param.json")
            param = open(os.environ['HOME']+"/.pybration/param.json", 'r')
            self.data.parameter = json.load(param)
            path = self._find_list(sys.path, ".*site-packages.*")[0]
            write_path = self.data.parameter['System']['plugin_folder']
            write_path = self.check_dir_str(write_path)
            self._generate_path_file(path + "/pybration_plugin.pth", write_path)

        except IOError as e:
            print("LOAD_PARAMETER:default")
            param = get_default_param()
            self.data.parameter = param
        return self.data
    
    def write_param(self):
        if not os.path.exists(os.environ['HOME']+"/.pybration"):
            os.mkdir(os.environ['HOME']+"/.pybration")
        fw = open(os.environ['HOME']+"/.pybration/param.json", 'w')
        json.dump(self.data.parameter, fw, indent=4)

    def get_work_dir(self):
        return self.data.parameter['System']['work_folder']

    def get_pulgin_dir(self):
        return self.data.parameter['System']['plugin_folder']

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

    def get_version(self):
        return get_distribution("Pybration").version

    def check_dir_str(self, dir_str: list):
        if str is type(dir_str):
            dir_str = [dir_str]

        for i,d in enumerate(dir_str):
            dir_str[i] = d.replace("//", "/")
            dir_str[i] = d.replace("~", os.environ['HOME'])
        return dir_str

    def _find_list(self, v: list, regex: str):
        r = re.compile(regex)
        v = [x for x in v if r.match(x)]
        return v

    def _generate_path_file(self, path: str, write_data: list):
        str_data = str()
        for i in write_data:
            str_data += i + "\n"

        try:
            with open(path, "r") as file:
                if str_data == file.read():
                    return
        except IOError:
            pass

        with open(path, "w") as file:
            print("Update of "+path)
            print("Please restart for load module.")
            file.write(str_data)
            exit()
