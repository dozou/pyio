#coding:utf-8

from Window.LineEdit import *
from Waveforms.AnalogDiscovery import *
from PyQt5.QtChart import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class AiControlView(QWidget):
    device = None
    sample_calc_1 = None
    sample_num = None
    sample_rate = None

    def __init__(self, device=None):
        super(AiControlView, self).__init__()
        self.device = device

        self.sample_calc_1 = QLabel()
        self.sample_rate = LabelOnSpinBox(label='SampleRate',
                                          val=163840,
                                          maximum=9999999)
        self.sample_rate.changed_value(self.calc_status)

        self.sample_num = LabelOnSpinBox(label='Samples',
                                         val=8192,
                                         maximum=8192)
        self.sample_num.changed_value(self.calc_status)

        update_button = QPushButton('更新')
        update_button.clicked.connect(self.update_ai)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("<b>入力設定</b>"))
        layout.addWidget(self.sample_calc_1)
        layout.addWidget(self.sample_rate)
        layout.addWidget(self.sample_num)
        layout.addWidget(update_button)
        layout.addStretch()
        layout.setContentsMargins(QMargins(0, 0, 0, 5))
        self.setLayout(layout)
        self.calc_status()

    def set_device(self, device):
        self.device = device

    def update_ai(self):
        if not self.device:
            print("デバイスが見つかりません")
            return None
        for key, device in self.device.items():
            device.setConfigAI(hzAcq=int(self.sample_rate.get_value()),
                                    nSamples=int(self.sample_num.get_value()))
            device.startAI(thread_mode=True)

    def calc_status(self):
        sampleRate = self.sample_rate.get_value()
        sampleNum = self.sample_num.get_value()
        calc1 = "SampleTime:" + str(round(1000.0*sampleNum/sampleRate, 3)) + " [msec]"
        self.sample_calc_1.setText(calc1)


class AoControlView(QWidget):
    device = None
    amp_line = None
    range_sweep = None

    def __init__(self, device=None):
        super(AoControlView, self).__init__()
        self.device = device

        self.range_sweep = RangeView(1000, 3500)
        self.range_sweep.changed_value(self.update_ao)

        self.amp_line = LabelOnSpinBox(label="Amp[V]", val=2.5, maximum=10)
        self.amp_line.changed_value(self.update_ao)

        self.update_button = QPushButton("更新")
        self.update_button.clicked.connect(self.update_ao)

        layout = QVBoxLayout()

        layout.addWidget(QLabel("<b>出力設定</b>"))
        layout.addWidget(QLabel("Sweep[Hz]"))
        layout.addWidget(self.range_sweep)
        layout.addWidget(self.amp_line)
        layout.addWidget(self.update_button)
        layout.addStretch()
        layout.setContentsMargins(QMargins(0, 0, 0, 5))
        self.setLayout(layout)

    def set_device(self, device):
        self.device = device

    def update_ao(self):
        (start, stop) = self.range_sweep.get_value()
        v = float(self.amp_line.get_value())
        for key, device in self.device.items():
            device.createSweep(startHz=start, stopHz=stop, sweepSec=0.025, outVoltage=v)
            device.startAO()


class DeviceManagerWindow(QWidget):

    def __init__(self, parent=None):
        super(DeviceManagerWindow, self).__init__(parent=parent)
        self.setWindowTitle("デバイスマネージャ")
        self.discovery_button = QPushButton("接続")
        self.discovery_button.clicked.connect(self.start_device)

        self.device_select_box = []
        device_count = get_devices()
        for i in range(device_count):
            self.device_select_box.append(QComboBox())
            for j in range(device_count):
                self.device_select_box[i].addItem(get_serial(j))
            self.device_select_box[i].addItem("update")
            self.device_select_box[i].currentIndexChanged.connect(self.update_device_list)

        self.discovery = None
        self.control_view = None
        layout = QHBoxLayout()
        sub_layout = QVBoxLayout()
        sub_layout.addWidget(QLabel("<b>AnalogDiscovery2</b>"))
        for i in range(device_count):
            sub_layout.addWidget(self.device_select_box[i])
        sub_layout.addWidget(self.discovery_button)
        sub_layout.addStretch()

        self.ao_control = AoControlView()
        self.ai_control = AiControlView()

        layout.addLayout(sub_layout)
        layout.addWidget(self.ai_control)
        layout.addWidget(self.ao_control)
        self.setLayout(layout)

    def update_device_list(self):
        devices_count = get_devices()
        for i in range(devices_count):
            if self.device_select_box[i].currentText() == 'update':
                self.device_select_box[i].clear()
                for j in range(devices_count):
                    self.device_select_box[i].addItem(get_serial(j))
                self.device_select_box[i].addItem("update")

    def set_device(self, device):
        self.discovery = device
        self.ao_control.set_device(device)
        self.ai_control.set_device(device)

    def start_device(self):
        for key, device in self.discovery.items():
            index = get_device_index(key)
            device.openDevice(get_device_index(self.device_select_box[index].currentText()))
        self.discovery_button.disconnect()
        self.discovery_button.clicked.connect(self.stop_device)
        self.discovery_button.setText("接続済み")

    def stop_device(self):
        for key, device in self.discovery.items():
            device.closeDevice()
        self.discovery_button.disconnect()
        self.discovery_button.clicked.connect(self.start_device)
        self.discovery_button.setText("接続")

    def get_device(self):
        return self.discovery

    def get_device_status(self):
        if self.discovery_button.text() == "接続済み":
            return True
        return False

