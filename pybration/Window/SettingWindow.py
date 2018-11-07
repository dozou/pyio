# -*- coding: utf-8 -*-
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



class SettingWindow(QWidget):

    def __init__(self, parent, data: DataContainer, window):
        super(SettingWindow, self).__init__(parent=parent)
        self.setWindowTitle("設定")
        system = System()
        # self.device_manager = DeviceManagerWindow()

        main_layout = QHBoxLayout()
        #main_layout.addWidget(self.directory_manager)
        # main_layout.addWidget(self.device_manager)

        self.setLayout(main_layout)



