# -*- coding: utf-8 -*-
from pybration.DataSturucture import Plugin


class $module$(Plugin):
    def __init__(self):
        super().__init__()
        self.window = None

    def init(self, data):
        self.data = data

    def enable_button(self):
        return $button$

    def clicked(self):
        print("click!!")
