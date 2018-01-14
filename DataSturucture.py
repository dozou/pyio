#coding:utf-8
from PyQt5.Qt import *


class DataContainer(QThread):
    def __init__(self):
        super().__init__()
        self.device = []
        self.parameter = {}
        self.scale = None
        pass

    def get_ai(self):
        ans_data = []
        for obj in self.device:
            ans_data.append([obj.ai_data[0], obj.ai_data[1]])
        return ans_data


class Plugin:
    def __init__(self, data:DataContainer=None):
        self.data = data  #type:DataContainer
        pass

    def set_parent_data(self, data:DataContainer):
        self.data = data