# -*- coding:utf-8 -*-
from enum import *


class Echannel(Enum):
    ch_1 = 0
    ch_2 = 1
    ch_all = 2


class IODevice:

    def __init__(self):
        self.info = {"name": "none",
                "id": 0
                }

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
