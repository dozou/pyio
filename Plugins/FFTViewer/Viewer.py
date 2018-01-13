# -*- coding:utf-8 -*-
# -*- coding:utf-8 -*-
import numpy as np
import pandas as pd
import threading
from PyQt5.QtWidgets import *
from yapsy.IPlugin import IPlugin
from Window.LineEdit import *
from DataSturucture import *


class Viewer(QWidget):
    def __init__(self, parent=None,data=None):
        super().__init__(parent)


class FFTViewer(IPlugin, Plugin):
    def __init__(self):
        super().__init__()

    def run(self):
        self.view = Viewer(data=self.data)
        self.view.show()


