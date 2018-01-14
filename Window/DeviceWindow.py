#coding:utf-8

from Window.LineEdit import *
from Devices.IODevice import *
from PyQt5.QtChart import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class AiControlView(QWidget):
    device = None
    sample_calc_1 = None
    sample_num = None
    sample_rate = None

    def __init__(self, device=None,data:DataContainer=None):
        super(AiControlView, self).__init__()
        self.device = device
        self.data = data

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
        for key, device in enumerate(self.device):
            device.set_config_ai(hzAcq=int(self.sample_rate.get_value()),
                                    nSamples=int(self.sample_num.get_value()))
            device.start_ai(thread_mode=True, channel=Echannel.ch_all)
        self.data.parameter["sample_rate"] = self.sample_rate.get_value()
        self.data.parameter["samples"] = self.sample_num.get_value()

    def calc_status(self):
        sampleRate = self.sample_rate.get_value()
        sampleNum = self.sample_num.get_value()
        calc1 = "SampleTime:" + str(round(1000.0*sampleNum/sampleRate, 3)) + " [msec]"
        self.sample_calc_1.setText(calc1)


class AoControlView(QWidget):
    device = None
    amp_line = None
    range_sweep = None

    def __init__(self, device=None, data:DataContainer=None):
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
        for key, device in enumerate(self.device):
            device.create_sweep(startHz=start, stopHz=stop, sweepSec=0.025, outVoltage=v)
            device.start_ao()


class DeviceManagerWindow(QWidget):

    def __init__(self, data:DataContainer, parent=None):
        super(DeviceManagerWindow, self).__init__(parent=parent)
        self.setWindowTitle("デバイスマネージャ")
        self.discovery_button = QPushButton("接続")
        self.discovery_button.clicked.connect(self.start_device)

        self.device_select_box = []
        device_count = get_connection_count_analog_discovery2()
        for i in range(device_count):
            self.device_select_box.append(QComboBox())
            for j in range(device_count):
                self.device_select_box[i].addItem(get_serial_analog_discovery2(j))
            self.device_select_box[i].addItem("update")
            self.device_select_box[i].currentIndexChanged.connect(self.update_device_list)

        self.device = []

        for i in range(get_connection_count_analog_discovery2()):
            self.device.append(IODevice())

        self.control_view = None
        layout = QHBoxLayout()
        sub_layout = QVBoxLayout()
        sub_layout.addWidget(QLabel("<b>AnalogDiscovery2</b>"))
        for i in range(device_count):
            sub_layout.addWidget(self.device_select_box[i])
        sub_layout.addWidget(self.discovery_button)
        sub_layout.addStretch()

        self.ao_control = AoControlView(data=data)
        self.ai_control = AiControlView(data=data)

        self.ai_control.device = self.device
        self.ao_control.device = self.device

        layout.addLayout(sub_layout)
        layout.addWidget(self.ai_control)
        layout.addWidget(self.ao_control)
        self.setLayout(layout)

        data.device = self.device

    def update_device_list(self):
        devices_count = get_connection_count_analog_discovery2()
        for i in range(devices_count):
            if self.device_select_box[i].currentText() == 'update':
                self.device_select_box[i].clear()
                for j in range(devices_count):
                    self.device_select_box[i].addItem(get_serial_analog_discovery2(j))
                self.device_select_box[i].addItem("update")

    def start_device(self):
        for index, combo_box in enumerate(self.device_select_box):
            print("OPEN_DEVICE'"+str(index)+":"+combo_box.currentText()+"'")
            self.device[index].open_device(get_index_analog_discovery2(combo_box.currentText()))
            # index = get_index_analog_discovery2(key)
            # dev.open_device(get_index_analog_discovery2(self.device_select_box[index].currentText()))
        self.discovery_button.disconnect()
        self.discovery_button.clicked.connect(self.stop_device)
        self.discovery_button.setText("接続済み")

    def stop_device(self):
        for key, dev in enumerate(self.device):
            self.device[key].close_device()
            print("CLOSE_DEVICE'"+str(key) + ":" + self.device[key].get_serial() +"'")
        self.discovery_button.disconnect()
        self.discovery_button.clicked.connect(self.start_device)
        self.discovery_button.setText("接続")

    def get_device(self):
        return self.device

    def get_device_status(self):
        if self.discovery_button.text() == "接続済み":
            return True
        return False

