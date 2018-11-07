# -*- coding: utf-8 -*-
import sys
import re
from pybration.DataSturucture import DataContainer
from PyQt5.QtWidgets import *
from pybration.Util import System


class ManageWorkDirecory(QWidget):
    def __init__(self):
        super(ManageWorkDirecory, self).__init__()
        layout = QVBoxLayout()

        change_dir_button = QPushButton("変更")

        layout.addWidget(QLabel("<b>作業ディレクトリ</b>"))
        layout.addWidget(change_dir_button)
        layout.addStretch()
        self.setLayout(layout)


def _find_list(v: list, regex: str):
    r = re.compile(regex)
    v = [x for x in v if r.match(x)]
    return v


def _generate_path_file(path: str, write_data: list):
    str_data = str()
    for i in write_data:
        str_data += i + "\n"

    with open(path, "r") as file:
        if str_data == file.read():
            return
    with open(path, "w") as file:
        print(path+"を更新")
        file.write(str_data)


class SettingWindow(QWidget):

    def __init__(self, parent, data: DataContainer, window):
        super(SettingWindow, self).__init__(parent=parent)
        self.setWindowTitle("設定")
        system = System()
        # self.device_manager = DeviceManagerWindow()
        self.directory_manager = ManageWorkDirecory()
        path = _find_list(sys.path, ".*site-packages.*")[0]
        # print(path)
        write_path = data.parameter['System']['plugin_folder']
        write_path = system.check_dir_str(write_path)
        _generate_path_file(path + "/pybration_plugin.pth", write_path)

        main_layout = QHBoxLayout()
        #main_layout.addWidget(self.directory_manager)
        # main_layout.addWidget(self.device_manager)

        self.setLayout(main_layout)



