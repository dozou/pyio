# -*- coding:utf-8 -*-
import numpy as np
import pandas as pd
import scipy.fftpack
import threading
import time
import copy
from PyQt5.QtWidgets import *
from PyQt5.QtChart import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from yapsy.IPlugin import IPlugin
from pybration.Window.LineEdit import *
from pybration.DataSturucture import *
from pybration.Window.Charts import *


class FFTContainer(DataContainer):

    def __init__(self, data:DataContainer):
        super().__init__()
        self.device = data.device
        self.ans_data = []
        self.cnt = 0
        self.is_stop = False
        self.scale = scipy.fftpack.fftfreq(data.parameter['samples'], d=1.0/data.parameter['sample_rate'])
        self.scale = self.scale[0:len(self.scale)//2]
        self.index = np.where(self.scale < 4000)[0]
        self.lpf_index = np.where(self.scale < 500)
        self.scale = self.scale[self.index]
        self.calc()

    def stop(self):
        self.is_stop = True

    def calc(self):
        ans_data = []
        for obj in self.device:
            data_ch1 = obj.ai_data[0]
            data_ch2 = obj.ai_data[1]

            data_ch1 = scipy.fftpack.fft(data_ch1)
            data_ch2 = scipy.fftpack.fft(data_ch2)

            data_ch1 = np.array([np.sqrt(c.real ** 2 + c.imag ** 2) for c in data_ch1])
            data_ch2 = np.array([np.sqrt(c.real ** 2 + c.imag ** 2) for c in data_ch2])

            data_ch1 = data_ch1[self.index]
            data_ch2 = data_ch2[self.index]

            data_ch1[self.lpf_index] = 0
            data_ch2[self.lpf_index] = 0

            ans_data.append([data_ch1, data_ch2])
        self.ans_data = ans_data

    def run(self):
        while not self.is_stop:
            self.calc()
            time.sleep(1/30)

    def get_ai(self):
        return self.ans_data


class ChartWidget(QWidget):
    def __init__(self, data:DataContainer, parent=None):
        super().__init__(parent)
        self.qth = QThread()
        self.data = FFTContainer(data=data)
        if not self.data.isRunning():
            self.data.start()
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

    def hideEvent(self, a0: QHideEvent):
        self.qth.exit()
        self.data.stop()
        self.data.wait()


class Viewer(QWidget):
    def __init__(self,parent=None, data:DataContainer=None):
        super().__init__(parent)
        self.chart_widgets = []
        for i in data.device:
            split_data = DataContainer()
            split_data.parameter = data.parameter
            split_data.device = [i]
            self.chart_widgets.append(ChartWidget(data=split_data))

        layout = QVBoxLayout()
        for i, obj in enumerate(self.chart_widgets):
            obj.set_title(data.device[i].get_serial())
            layout.addWidget(obj)

        self.setLayout(layout)
        self.resize(1000, 800)


class FFTViewer(IPlugin, Plugin):
    def __init__(self):
        super().__init__()
        self.view = None  # type:Viewer

    def clicked(self):
        self.view = Viewer(data=self.data)
        self.view.setWindowTitle("FFTViewer")
        self.view.show()
        print(self.data.parameter)

    def enable_button(self):
        return True



