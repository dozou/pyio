# -*- coding:utf-8 -*-
from yapsy.IPlugin import IPlugin
from yapsy.PluginInfo import PluginInfo
from pybration.DataSturucture import *


class Info(PluginInfo):
    def __init__(self):
        print("call")


class Hello(IPlugin, Plugin):
    def __init__(self):
        super().__init__()
        self.parent_data = None

    def enable_button(self):
        return True



