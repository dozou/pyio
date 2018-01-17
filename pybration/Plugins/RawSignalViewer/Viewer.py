# -*- coding:utf-8 -*-
import numpy as np
import pandas as pd
import threading
import time
from PyQt5.QtWidgets import *
from PyQt5.QtChart import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from yapsy.IPlugin import IPlugin
from pybration.Window.LineEdit import *
from pybration.DataSturucture import *
from pybration.Window.Charts import *


class ChartWidget(QWidget):
    def __init__(self, device, parent=None):
        super().__init__(parent)
        self.qth = QThread()
        self.data = DataContainer()
        self.data.device.append(device)
        self.ch = ChartObject(data=self.data)
        self.ch.moveToThread(self.qth)
        self.qth.start()
        self.view = QChartView(self.ch.chart)
        self.view.setRenderHint(QPainter.Antialiasing)
        layout = QVBoxLayout()
        layout.addWidget(self.view)
        self.setLayout(layout)
        self.resize(500, 800)

        self.color = Qt.black
        self.device = None

    def set_title(self, title):
        self.ch.chart.setTitle(title)

    def set_data(self, device, color):
        self.color = color
        self.device = device

    def hideEvent(self, a0: QHideEvent):
        self.qth.exit()


class Viewer(QWidget):
    def __init__(self,parent=None, data:DataContainer=None):
        super().__init__(parent)
        self.device = data.device
        self.chart_widgets = []
        for i in self.device:
            self.chart_widgets.append(ChartWidget(device=i))

        layout = QVBoxLayout()
        for i, obj in enumerate(self.chart_widgets):
            obj.set_title(self.device[i].get_serial())
            layout.addWidget(obj)

        self.setLayout(layout)
        self.resize(1000, 500)


class RawSignalViewer(IPlugin, Plugin):
    def __init__(self):
        super().__init__()
        self.view = None  # type:Viewer

    def clicked(self):
        self.view = Viewer(data=self.data)
        self.view.setWindowTitle("RawSignalViewer")
        self.view.show()

    def enable_button(self):
        return True




