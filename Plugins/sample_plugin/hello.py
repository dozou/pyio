# -*- coding:utf-8 -*-
from yapsy.IPlugin import IPlugin
from yapsy.PluginInfo import PluginInfo
from DataSturucture import *

class Hello(IPlugin, Plugin):
    def __init__(self):
        super(Hello).__init__()
        self.parent_data = None

    def run(self):
        print("hello")



