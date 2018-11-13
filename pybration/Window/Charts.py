import numpy as np
import pandas as pd
import threading
import time
from PyQt5.QtWidgets import *
from PyQt5.QtChart import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from pybration.DataSturucture import *


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


class ChartObject(QThread):
    def __init__(self, data:DataContainer):
        super().__init__()
        self.ncurves = 0
        self.chart = QChart()
        self.chart.legend().hide()
        self.data = data
        if not self.data.device[0].is_open():
            return
        self.color_ch1 = Qt.green
        self.color_ch2 = Qt.red
        self.color_list = [
            Qt.green,
            Qt.red,
            Qt.cyan
        ]
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
        for c, dev in zip(self.color_list,self.data.device):
            ydata = dev.get_value()
            xdata = np.linspace(0, len(ydata), len(ydata))
            self.add_data(xdata, ydata, c)

    def clear_data(self):
        self.chart.removeAllSeries()
