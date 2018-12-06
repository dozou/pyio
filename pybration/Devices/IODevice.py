# -*- coding:utf-8 -*-
from enum import *
import numpy as np
from abc import ABC,abstractmethod


class IODevice(ABC):

    @abstractmethod
    def __init__(self):
        self.info = {
            "name": "none",
            "id": 0,
            "type": "none",
            "ch": -1,
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

    def set_property(self):
        pass

    def set_value(self, obj):
        pass

    def get_serial(self)->str:
        return ""

    def get_1d_array(self)->np.ndarray:
        return np.array([0])

    def get_2d_array(self)->np.ndarray:
        return np.array([0])

    def get_x_scale(self):
        return np.arange(0, len(self.get_1d_array()))

    def get_value(self)->np.ndarray:
        v = np.array([0])
        return v

    def get_shape(self):
        return np.array([0]).shape
