import sys
import os
import time
from PyQt5 import QtWidgets
from PyQt5 import QtCore

class ThredTest(QtCore.QThread):
    add_object = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(ThredTest, self).__init__(parent)

    def stop(self):
        print("")

    def run(self):
        print("")
