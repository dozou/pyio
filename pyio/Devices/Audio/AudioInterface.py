"""
@file AudioInterface
@brief Qtを使ったAuidioInterfaceのファイルです
@author Nobuhiro Funato
"""
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import sys

class AudioDevice:
    def __init__(self):
        self.audio_format = QAudioFormat()
        self.update_setting()


    def update_setting(self):
        self.audio_format.setSampleRate(163840)
        self.audio_format.setChannelCount(1)
        self.audio_format.setSampleSize(8)
        self.audio_format.setCodec("audio/pcm")
        self.audio_format.setByteOrder(QAudioFormat.LittleEndian)
        self.audio_format.setSampleType(QAudioFormat.UnSignedInt)

if __name__ == "__main__":
    c = C()
    b = B()
    c.show(B(b))
