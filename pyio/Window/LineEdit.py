# coding:utf-8

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtChart import *


class RangeView(QWidget):
    stop = None
    start = None

    def __init__(self, start=0, stop=0):
        super(RangeView, self).__init__()
        self.start = QSpinBox()
        self.stop = QSpinBox()
        self.start.setMaximum(1000000000.0)
        self.start.setMinimum(-1000000000.0)
        self.stop.setMaximum(100000000.0)
        self.stop.setMinimum(-100000000.0)
        self.start.setValue(start)
        self.stop.setValue(stop)

        layout = QHBoxLayout()
        layout.addWidget(self.start)
        layout.addWidget(QLabel("to"))
        layout.addWidget(self.stop)
        layout.setContentsMargins(QMargins(0, 0, 0, 0))
        self.setLayout(layout)

    def changed_value(self, func):
        self.start.valueChanged.connect(func)
        self.stop.valueChanged.connect(func)

    def get_value(self):
        return self.start.value(), self.stop.value()


class LabelOnLineEdit(QWidget):
    LineEdit = None
    label = None

    def __init__(self, label="no_label", text=""):
        super(LabelOnLineEdit, self).__init__()
        self.label = '<div align="right">'
        label += ":"
        self.label += label
        self.label += "<\div>"
        self.LineEdit = QLineEdit(text)

        layout = QHBoxLayout()

        layout.addWidget(QLabel(self.label))
        layout.addWidget(self.LineEdit)
        layout.setContentsMargins(QMargins(0, 0, 0, 0))
        self.setLayout(layout)

    def set_value(self, text: str):
        self.LineEdit.setText(text)

    def changed_value(self, func):
        self.LineEdit.returnPressed.connect(func)

    def get_value(self):
        return self.LineEdit.text()


class LabelOnSpinBox(QWidget):
    def __init__(self, label="no_label", maximum=1000, val=None):
        super(LabelOnSpinBox, self).__init__()
        self.label = '<div align="right">'
        label += ":"
        self.label += label
        self.label += "<\div>"
        self.LineEdit = QDoubleSpinBox() if type(val) == float else QSpinBox()
        self.LineEdit.setMaximum(maximum)
        self.LineEdit.setValue(val)

        layout = QHBoxLayout()
        layout.addWidget(QLabel(self.label))
        layout.addWidget(self.LineEdit)
        layout.setContentsMargins(QMargins(0, 0, 0, 0))
        self.setLayout(layout)

    def set_value(self, val: float):
        self.LineEdit.setValue(val)

    def changed_value(self, func):
        self.LineEdit.valueChanged.connect(func)

    def get_value(self):
        return self.LineEdit.value()
