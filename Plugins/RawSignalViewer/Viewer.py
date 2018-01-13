# -*- coding:utf-8 -*-
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
from Window.LineEdit import *
from DataSturucture import *


def series_to_polyline(xdata, ydata):
    size = len(xdata)
    polyline = QPolygonF(size)
    pointer = polyline.data()
    dtype, tinfo = np.float, np.finfo  # integers: = np.int, np.iinfo
    pointer.setsize(2*polyline.size()*tinfo(dtype).dtype.itemsize)
    memory = np.frombuffer(pointer, dtype)
    memory[:(size-1)*2+1:2] = xdata
    memory[1:(size-1)*2+2:2] = ydata
    return polyline


class ChartObject(QObject):
    def __init__(self, device):
        super().__init__()
        self.ncurves = 0
        self.chart = QChart()
        self.chart.legend().hide()
        self.device = device
        if not self.device.is_open():
            return
        self.color_ch1 = Qt.green
        self.color_ch2 = Qt.red
        self.timer = QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_data)
        self.timer.start()

    def set_color(self,ch1, ch2):
        self.color_ch1 = ch1
        self.color_ch2 = ch2

    def add_data(self, xdata, ydata, color=None):
        curve = QLineSeries()
        pen = curve.pen()
        if color is not None:
            pen.setColor(color)
        pen.setWidthF(.1)
        curve.setPen(pen)
        curve.setUseOpenGL(True)
        curve.append(series_to_polyline(xdata, ydata))
        self.chart.addSeries(curve)
        self.chart.createDefaultAxes()
        self.ncurves += 1

    def update_data(self):
        self.clear_data()
        xdata = np.linspace(0, self.device.get_sample_num(), self.device.get_sample_num())
        ydata = self.device.ai_data[0]
        self.add_data(xdata, ydata, self.color_ch1)
        ydata = self.device.ai_data[1]
        self.add_data(xdata, ydata, self.color_ch2)

    def clear_data(self):
        self.chart.removeAllSeries()


class ChartWidget(QWidget):
    def __init__(self, device, parent=None):
        super().__init__(parent)
        self.qth = QThread()
        self.ch = ChartObject(device=device)
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

    def run(self):
        self.view = Viewer(data=self.data)
        self.view.show()




