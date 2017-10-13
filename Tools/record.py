#coding:utf-8
from PyQt5.QtChart import *
from Window.DeviceWindow import *
from Window.LineEdit import *
from PyQt5.QtWidgets import *
from SignalProcessing.fft import *
import numpy as np
import pandas as pd
import threading


class RecordWindow(QWidget):
    timer = None
    device = AnalogDiscovery2()
    wave_data = None
    data_cnt = 0

    def __init__(self, parent=None, device=None):
        super(RecordWindow, self).__init__(parent)
        self.setWindowTitle('Record Manager')
        self.device = device

        self.file_name_line = LabelOnLineEdit(label="FileName",
                                              text='')
        self.timeout_line = LabelOnSpinBox(label="RecordTiming",
                                           val=50.0,
                                           maximum=10000.0)
        self.size_checkbox = QCheckBox(text='記録サイズ指定')
        self.size_checkbox.stateChanged.connect(self.update_checkbox)
        self.size_line = LabelOnSpinBox(label="記録サンプル数",
                                        val=0,
                                        maximum=50000)
        self.record_button = QPushButton("記録開始")
        self.record_button.clicked.connect(self.start_record)
        self.clear_button = QPushButton("初期化")
        self.clear_button.clicked.connect(self.clear_data)
        self.write_button = QPushButton("書き出し")
        self.write_button.clicked.connect(self.write_csv)
        self.data_cnt_text = QLabel("Samples:"+str(self.data_cnt))

        main_layout = QHBoxLayout()
        sub_layout = QVBoxLayout()
        sub_layout.addWidget(QLabel("<b>記録</b>"))
        sub_layout.addWidget(self.timeout_line)
        sub_layout.addWidget(self.size_checkbox)
        sub_layout.addWidget(self.size_line)
        sub_layout.addWidget(self.record_button)
        sub_layout.addWidget(self.clear_button)
        sub_layout.addWidget(self.write_button)
        sub_layout.addWidget(self.data_cnt_text)
        sub_layout.addWidget(self.file_name_line)
        main_layout.addLayout(sub_layout)
        self.setLayout(main_layout)
        self.timer = QTimer()
        self.timer.timeout.connect(self.rec_update)
        self.update_checkbox()
        self.check_loop = False
        self.t1 = None

    def start_record(self):
        if not self.device.is_start_ai():
            return
        self.record_button.disconnect()
        self.record_button.setText("記録停止")
        self.record_button.clicked.connect(self.stop_record)
        self.timer.setInterval(self.timeout_line.get_value())
        if self.size_checkbox.isChecked():
            size = self.size_line.get_value()
            self.wave_data = np.empty((size, self.device.get_sample_num()), float)
            print("Samples:"+str(size))
        else:
            self.wave_data = np.empty((0, self.device.get_sample_num()), float)
        # self.timer.start()
        self.check_loop = True
        self.t1 = threading.Thread(target=self.__thread_func)
        self.t1.setDaemon(True)
        self.t1.start()
        self.size_checkbox.setEnabled(False)

    def stop_record(self):
        # self.timer.stop()
        self.check_loop = False
        self.record_button.disconnect()
        self.record_button.setText("記録開始")
        self.record_button.clicked.connect(self.start_record)
        self.data_cnt = 0
        self.size_checkbox.setEnabled(True)

    def update_checkbox(self):
        if self.size_checkbox.isChecked():
            self.size_line.setEnabled(True)
        else:
            self.size_line.setEnabled(False)

    def __thread_func(self):
        while self.check_loop:
            if self.size_checkbox.isChecked() and self.size_line.get_value() <= self.data_cnt:
                break

            self.rec_update()
        self.stop_record()

    def rec_update(self):
        data = np.array([self.device.ai_data[0]])
        if self.size_checkbox.isChecked():
            self.wave_data[self.data_cnt] = data
        else:
            self.wave_data = np.append(self.wave_data, data, axis=0)
        self.data_cnt_text.setText("Samples:"+str(self.data_cnt))
        self.data_cnt += 1
        # print("data counter = %d" % self.data_cnt)

    def clear_data(self):
        self.wave_data = None
        self.data_cnt = 0

    def write_csv(self):
        wave_data = pd.DataFrame(self.wave_data)
        raw_file_name = self.file_name_line.get_value()
        wave_data.to_csv(raw_file_name+'_wave.csv')


class FFTRecordWindow(QWidget):
    record_cnt = 0
    fft_data = pd.DataFrame()
    fft_func = FFT()

    def __init__(self, parent=None):
        super(FFTRecordWindow, self).__init__(parent=parent)
        self.setMaximumSize(QSize(500, 500))
        self.setWindowTitle("Record Manager")
        self.main_layout = QHBoxLayout()

        self.control_layout = QVBoxLayout()
        self.sample_rate_line = LabelOnSpinBox(label="SampleRate",
                                               val=163840,
                                               maximum=9999999)
        self.sample_num_line = LabelOnSpinBox(label="SampleNum",
                                              val=8192,
                                              maximum=8192)

        self.record_button = QPushButton("記録開始")
        self.clear_data_button = QPushButton("クリア")
        self.write_button = QPushButton("書き出し")
        self.read_button = QPushButton("読み出し")
        self.samples_label = QLabel()

        self.record_button.clicked.connect(self.start_record)
        self.clear_data_button.clicked.connect(self.clear_data)
        self.write_button.clicked.connect(self.write_csv)
        self.record_button.clicked.connect(self.read_csv)

        self.control_layout.addWidget(QLabel("<b>記録</b>"))

        self.control_layout.addWidget(self.record_button)
        self.control_layout.addWidget(self.clear_data_button)
        self.control_layout.addWidget(self.write_button)
        self.control_layout.addWidget(self.samples_label)
        self.control_layout.addStretch()

        self.main_layout.addLayout(self.control_layout)
        self.setLayout(self.main_layout)
        self.timer = QTimer()
        self.timer.setInterval(10)
        self.timer.timeout.connect(self.record)

    def set_device(self, device):
        self.fft_func.set_device(device)

    def start_record(self):
        self.fft_data = np.empty((0, self.sample_num_line.get_value()), float)

        fft_list = pd.Series(self.fft_func.freq_list)
        self.record_button.disconnect()
        self.record_button.setText("記録停止")
        self.record_button.clicked.connect(self.stop_record)
        self.timer.start()

    def stop_record(self):
        self.timer.stop()
        self.record_button.disconnect()
        self.record_button.setText("記録開始")
        self.record_button.clicked.connect(self.start_record)

    def record(self):
        fft = self.fft_func.get()
        fft = np.array([fft])
        self.fft_data = np.append(self.fft_data, fft, axis=0)
        self.samples_label.setText('Samples:'+str(self.record_cnt))
        self.record_cnt += 1

    def write_csv(self):
        fft_data = pd.DataFrame(self.fft_data)
        fft_data.to_csv('fft.csv')

    def read_csv(self):
        print("")

    def clear_data(self):
        self.fft_data = None
        self.record_cnt = 0

if __name__ == '__main__':
    print("test")
