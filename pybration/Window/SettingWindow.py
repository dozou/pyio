# -*- coding: utf-8 -*-
from pybration.DataSturucture import DataContainer
from PyQt5.QtWidgets import QGroupBox, QVBoxLayout, QWidget, QTabWidget
from PyQt5.Qt import Qt


class SettingWindow(QTabWidget):

    def __init__(self, parent, data: DataContainer, window):
        super(SettingWindow, self).__init__(parent=parent)
        self.setWindowFlags(Qt.Dialog)
        self.setWindowTitle("設定")
        self.setContentsMargins(10, 10, 10, 10)

        for i in window:  # type:QGroupBox
            self.addTab(i, i.windowTitle())



