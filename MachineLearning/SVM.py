#coding:utf-8
import sys
import math
from PyQt5.QtChart import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from sklearn.svm import *
from SignalProcessing.fft import *
import pandas as pd


class SvmToolWindow(QWidget):
    fft_func = None
    contact_force = None
    force_data = pd.DataFrame()
    fft_data = pd.DataFrame()

    def __init__(self, parent=None):
        super(SvmToolWindow, self).__init__(parent=parent)
        self.setMaximumSize(QSize(500, 500))
        self.setWindowTitle("SVM Manager")
        main_layout = QHBoxLayout()

        status_view_layout = QVBoxLayout()
        self.force_label = QLabel()
        self.sample_calc_1 = QLabel("")
        status_view_layout.addWidget(self.sample_calc_1)
        status_view_layout.addWidget(QLabel("--ContactForce--"))
        status_view_layout.addWidget(self.force_label)

        control_layout = QVBoxLayout()
        self.sample_rate_text = QLineEdit("163840")
        self.sample_num_text = QLineEdit("8192")
        self.record_button = QPushButton("記録開始")
        self.show_record_button = QPushButton("Show")
        self.sample_rate_text.textChanged.connect(self.calc_status)
        self.sample_num_text.textChanged.connect(self.calc_status)
        self.record_button.clicked.connect(self.start_record)
        self.show_record_button.clicked.connect(self.show_record)
        control_layout.addWidget(QLabel("SampleRate"))
        control_layout.addWidget(self.sample_rate_text)
        control_layout.addWidget(QLabel("SampleNum"))
        control_layout.addWidget(self.sample_num_text)
        control_layout.addWidget(self.record_button)
        control_layout.addWidget(self.show_record_button)

        main_layout.addLayout(status_view_layout)
        main_layout.addLayout(control_layout)
        self.setLayout(main_layout)
        self.timer = QTimer()
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.record)

        self.fft_func = FFT()
        self.fft_func.device.openDevice()
        self.calc_status()

    def calc_status(self):
        sampleRate = float(self.sample_rate_text.text())
        sampleNum = float(self.sample_num_text.text())
        calc1 = str(sampleNum/sampleRate) + "sec"
        self.sample_calc_1.setText(calc1)

    def set_force(self, force=None):
        self.contact_force = force

    def start_record(self):
        self.fft_func.config_ai(sampleRate=int(self.sample_rate_text.text()),
                                sampleNum=int(self.sample_num_text.text()))
        fft_list = pd.Series(self.fft_func.freq_list)
        self.fft_data = self.fft_data.append(fft_list, ignore_index=True)
        self.record_button.disconnect()
        self.record_button.setText("キャンセル")
        self.record_button.clicked.connect(self.stop_record)
        self.timer.start()

    def stop_record(self):
        self.timer.stop()
        self.record_button.disconnect()
        self.record_button.setText("計算中")

    def record(self):
        fft = self.fft_func.get()
        fft_sr = pd.Series(fft)
        self.fft_data = self.fft_data.append(fft_sr, ignore_index=True)
        z, x, y = self.contact_force()
        z = round(z, 1)
        x = round(x, 1)
        y = round(y, 1)
        force_sr = pd.Series([z, x, y])
        self.force_data = self.force_data.append(force_sr, ignore_index=True)
        force = "Z:" + str(z) + "\n"
        force += "X:" + str(x) + "\n"
        force += "Y:" + str(y) + "\n"
        self.force_label.setText(force)

    def show_record(self):
        print(self.force_data)

if __name__ == '__main__':
    print("test")
