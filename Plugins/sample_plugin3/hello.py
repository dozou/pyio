# -*- coding:utf-8 -*-
from yapsy.IPlugin import IPlugin


class Hello(IPlugin):
    def run(self):
        print("hello")
