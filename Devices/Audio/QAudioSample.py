"""
@file QAudioSample
@brief QAudioを使うためのサンプルです
@author Nobuhiro Funato
"""
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import sys


class SampleWidget(FigureCanvas):
    def __init__(self,width=20, height=10, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.axes.hold(False)
        super(SampleWidget, self).__init__(fig)
        self.audio_format = QAudioFormat()
        self.audio_format.setSampleRate(163840)
        self.audio_format.setChannelCount(1)
        self.audio_format.setSampleSize(8)
        self.audio_format.setCodec("audio/pcm")
        self.audio_format.setByteOrder(QAudioFormat.LittleEndian)
        self.audio_format.setSampleType(QAudioFormat.UnSignedInt)

        self.audio_input = QAudioInput(self.audio_format)
        self.audio_data = QBuffer()
        self.audio_data.setOpenMode(QIODevice.ReadWrite)
        self.audio_input.start(self.audio_data)

        self.timer = QTimer()
        self.timer.setInterval(10)
        self.timer.timeout.connect(self.update_draw)
        self.timer.start()

    def update_draw(self):
        self.audio_data.seek(0)
        data = self.audio_data.readData(8192)
        array = []
        for i in range(len(data)):
            array.append(data[i]-128)
        x = np.arange(0, len(data))
        y = np.array(array)
        self.axes.plot(x, y)
        self.draw()
        print(len(array))


if __name__ == "__main__":
    myApp = QApplication(sys.argv)
    myWindow = SampleWidget()
    myWindow.show()
    myApp.exec_()
    sys.exit(0)
