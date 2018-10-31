# coding:utf-8
from PyQt5.QtCore import QThread
from yapsy.IPlugin import IPlugin


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


class Plugin(IPlugin):
    def __init__(self, data: DataContainer = None):
        super(Plugin, self).__init__()
        self.data = data  # type:DataContainer
        self.param = True

    def set_parent_data(self, data: DataContainer):
        self.data = data

    def clicked(self):
        print("PUSH_BUTTON")

    def enable_button(self):
        return False

    def run(self):
        pass

    def get_device(self, dev_name: str):
        for dev in self.data.device:
            if dev.info['name'] == dev_name:
                return dev
        ValueError("Nothing "+dev_name)

    def get_dir(self):
        return ""

