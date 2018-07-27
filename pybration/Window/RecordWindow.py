# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QRadioButton, QVBoxLayout
from PyQt5.QtCore import pyqtSignal, QThread
from pybration.Window.LineEdit import LabelOnSpinBox, LabelOnLineEdit
from pybration.DataSturucture import DataContainer


class Record(QThread):
    Stopped = pyqtSignal()
    ChangedIdx = pyqtSignal(int)

    def __init__(self, size: int, sleep_ms: int,data: DataContainer=None):
        super().__init__()
        self.data = data
        self.size = size
        self.th_is_alive = True
        self.sleep_ms = sleep_ms

    def run(self):
        cnt = 0 # type:int
        while cnt < self.size and self.th_is_alive:
            if self.rec(cnt):
                cnt += 1
                self.ChangedIdx.emit(cnt)
            self.msleep(self.sleep_ms)
        self.Stopped.emit()

    def rec(self, idx: int):
        print("")
        return True

    def stop(self):
        self.th_is_alive = False


class RecordWindow(QWidget):
    def __init__(self, data: DataContainer, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Record")
        self.title_label = QLabel("<h3>記録</h3>")
        self.sample_rate = LabelOnSpinBox(label='RecordTiming',
                                          val=50.0)
        self.sample_line = LabelOnSpinBox(label='サンプル数',
                                          val=0,
                                          maximum=100000)
        self.start_button = QPushButton("記録開始")
        self.init_button = QPushButton("初期化")
        self.current_samples_label = QLabel("Samples:0")

        self.write_button = QPushButton("書き出し")
        self.write_csv_check_box = QRadioButton("CSV")
        self.write_pkl_check_box = QRadioButton("PKL")
        self.write_pkl_check_box.setChecked(True)
        self.write_bson_check_box = QRadioButton("BSON")
        self.write_filename_line = LabelOnLineEdit(label="FileName")
        self.samples = 0
        self.update_layout()

    def update_layout(self):
        layout = QVBoxLayout()
        layout.addWidget(self.title_label)
        layout.addWidget(self.sample_rate)
        layout.addWidget(self.sample_line)
        layout.addWidget(self.start_button)
        layout.addWidget(self.init_button)
        layout.addWidget(self.current_samples_label)
        layout.addWidget(self.write_button)
        layout.addWidget(self.write_csv_check_box)
        layout.addWidget(self.write_pkl_check_box)
        layout.addWidget(self.write_bson_check_box)
        layout.addWidget(self.write_filename_line)
        self.setLayout(layout)

    def update_samples(self, index: int):
        self.current_samples_label.setText("Samples:"+str(index))
