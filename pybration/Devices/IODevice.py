# -*- coding:utf-8 -*-

from pybration.DataSturucture import *


class IODevice:
    info = {}

    def __init__(self):
        pass

    def open_device(self):
        pass

    def close_device(self):
        pass

    def is_open(self):
        return False

    def get_serial(self):
        return ""

    def get_value(self):
        return []
