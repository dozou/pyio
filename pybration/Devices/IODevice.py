# -*- coding:utf-8 -*-
from enum import *
import numpy as np


class Echannel(Enum):
    ch_1 = 0
    ch_2 = 1
    ch_all = 2


class IODevice:

    def __init__(self):
        self.info = {"name": "none",
                     "id": 0,
                     "type": "none",
                     }

    def open_device(self)->bool:
        raise Exception("open_device() require define.")

    def close_device(self)->bool:
        raise Exception("close_device() require define.")

    def is_open(self)->bool:
        return False

    def get_serial(self)->str:
        return ""

    def get_value(self)->np.ndarray:
        v = np.array([0])
        return v

    def get_shape(self):
        return np.array([0]).shape
