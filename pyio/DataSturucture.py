# coding:utf-8
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QLayout, QWidget, QGroupBox
from pyio.Devices.DeviceManager import DeviceManager
from yapsy.IPlugin import IPlugin
from abc import ABC, abstractmethod


class DataContainer(QThread):
    def __init__(self):
        super().__init__()
        self.device = DeviceManager()
        self.parameter = {}
        self.scale = None
        print(type(self.device))
        pass

    def get_ai(self):
        ans_data = []
        for obj in self.device:
            ans_data.append([obj.ai_data[0], obj.ai_data[1]])
        return ans_data


class Plugin(ABC, IPlugin):

    def __init__(self, data: DataContainer = None):
        super(Plugin, self).__init__()
        self.data = None  # type:DataContainer

    def init(self, parent_data: DataContainer):
        pass

    def clicked(self):
        print("PUSH_BUTTON")

    def enable_button(self)->bool:
        return False

    def enable_setting_window(self)->bool:
        return False

    def get_device(self, dev_name: str):
        for dev in self.data.device:
            if dev.info['name'] == dev_name:
                return dev
        raise ValueError("Nothing "+dev_name)

    def get_dir(self):
        return ""

    def get_setting_window(self)->QGroupBox:
        default_layout = QWidget()
        return default_layout


