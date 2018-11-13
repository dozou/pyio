# -*- coding:utf-8 -*-
from enum import *
import numpy as np
from abc import ABC,abstractmethod


class Echannel(Enum):
    ch_1 = 0
    ch_2 = 1
    ch_all = 2


class IODevice(ABC):

    @abstractmethod
    def __init__(self):
        self.info = {
            "name": "none",
            "id": 0,
            "type": "none",
        }

    @abstractmethod
    def open_device(self)->bool:
        raise Exception("open_device() require define.")

    @abstractmethod
    def close_device(self)->bool:
        raise Exception("close_device() require define.")

    @abstractmethod
    def is_open(self)->bool:
        return False

    def set_value(self, obj):
        pass

    def get_serial(self)->str:
        return ""

    def get_value(self)->np.ndarray:
        v = np.array([0])
        return v

    def get_shape(self):
        return np.array([0]).shape
