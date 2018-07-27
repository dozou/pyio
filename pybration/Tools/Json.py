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


def get_default_param():
    param = {
            "System": {
                "setting_folder": "~/.pybration/",
                "plugin_folder": [],
                "work_folder": ""
            },
            "Plugins": {},
            "Device": {},
            "ExperimentInfo": {}
        }
    return param
