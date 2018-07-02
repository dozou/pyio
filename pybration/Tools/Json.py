# -*- coding: utf-8 -*-
import json as js


class Json:
    def __init__(self, obj: dict=None):
        self._dict_data = obj

    def open(self, filename: str):
        fp = open(filename, "r")
        self._dict_data = js.load(fp)

    def write(self, filename: str):
        fp = open(filename, "rw")
        js.dump(self._dict_data, fp)
