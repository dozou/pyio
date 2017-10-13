#coding:utf-8
import sys

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from SignalProcessing.fft import *
from SignalProcessing.lpc import *
from Experiments.SupportVectorRegression import *
from Experiments.grip_strength_experiment import *
from Experiments.machine_learning import *
from MachineLearning.EstimationForContactForce import *
from Tools.record import *
from Window.SettingWindow import *
from Window.DeviceWindow import *

"""
ツールウィンドウの表示クラスです．
基本ツール＋自研究用のメソッドを追加することで自由に扱う事ができます
"""


class MainWindow(QWidget):
    face_data = ["(｀･ω･´)", "( ｀･ω)", "( 　｀･)", "(　　　　)", "(･`　 )", "(ω･` )", "(´･ω･`)"]
    device_manager = None
    setting_window = None
    force = None  # start_cfs_gui()で力覚センサの値取得関数を格納
    cfs_window = None  # 力覚センサのウィンドウクラスを格納
    plot = None  # FFTアナライザーを格納
    recoder_window = None  # 生波形レコーダを格納
    svm_window = None
    ml = None
    warning_label = None

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        layout = QVBoxLayout()
        self.setWindowTitle("PyVibrarionTools")

        self.face = QLabel()
        self.manage_daq_device = QPushButton("設定")
        self.manage_daq_device.clicked.connect(self.start_manage_window)
        self.rawdata = QPushButton("生波形ビューア")
        self.rawdata.clicked.connect(self.start_signal_view)
        self.fftana = QPushButton("FFTアナライザ")
        self.fftana.clicked.connect(self.start_fft_analyzer)
        self.lpcana = QPushButton("LPCアナライザ")
        self.lpcana.clicked.connect(self.start_lpc_analyzer)
        self.recorder = QPushButton("レコーダ")
        self.recorder.clicked.connect(self.start_recoder)
        self.cfsgui = QPushButton("力覚センサ")
        self.cfsgui.clicked.connect(self.start_cfs_gui)
        self.exp1 = QPushButton("SVMなやつ")
        self.exp1.clicked.connect(self.start_exp1)
        self.exp2 = QPushButton("機械学習")
        self.exp2.clicked.connect(self.start_exp2)
        self.exp3 = QPushButton("握力推定")
        self.exp3.clicked.connect(self.start_exp3)
        self.exit_button = QPushButton("終了")
        self.exit_button.clicked.connect(quit)

        self.warning_label = QLabel(" ")

        layout.addWidget(self.warning_label)
        layout.addWidget(self.manage_daq_device)
        layout.addWidget(self.rawdata)
        layout.addWidget(self.fftana)
        layout.addWidget(self.lpcana)
        layout.addWidget(self.recorder)
        layout.addWidget(self.cfsgui)
        layout.addWidget(self.exp1)
        layout.addWidget(self.exp2)
        layout.addWidget(self.exp3)
        layout.addWidget(self.exit_button)
        layout.addStretch()

        self.setLayout(layout)

        self.io_device = {}
        self.device_order = {}
        for i in range(get_devices()):
            self.io_device[get_serial(i)] = AnalogDiscovery2()

        for key in self.io_device.keys():
            self.device_order[key] = 0

        self.timer = QTimer()
        self.timer.setInterval(200)
        self.timer.timeout.connect(self.timeout)
        self.timer.start()
        self.face_rote = 0
        self.setting_window = SettingWindow()
        self.setting_window.device_manager.set_device(self.io_device)


    """
    ショボーンを回転させるためのメソッドです
    200[msec]間隔で更新しています
    """
    def timeout(self):
        if len(self.face_data) == self.face_rote:
            self.face_rote = 0
        self.face.setText('<div align="center">'  # Qtスバラ！！HTML指定できるんすよ！！
                          + self.face_data[self.face_rote]
                          + '</div>')
        self.face_rote += 1

    """
    デバイス管理用のツールウィンドウです
    最終的には全てのデバイスオブジェクトの管理が行われます
    """
    def start_manage_window(self):
        self.setting_window.show()


    """
    生波形表示ウィンドウの起動メソッド
    pyqtgraphを用いているため，FFTアナライザーとの併用は難しいです
    """
    def start_signal_view(self):
        if not self.setting_window.device_manager.get_device_status():
            self.set_warning("デバイスが見つからないよ")
            return False
        self.plot = RawSignalViewer(graphname='Raw Data.', xsize=1000, ysize=500, number=1)
        self.plot.set_device(self.io_device)
        self.plot.set_realtime()

    """
    FFTアナライザーの起動メソッド
    pyqtgraphを用いているため，生波形ビューアとの併用は難しいです
    """
    def start_fft_analyzer(self):
        if not self.setting_window.device_manager.get_device_status():
            self.set_warning("デバイスが見つからないよ")
            return False
        self.plot = FFTAnalyzer(graphname='FFT Analyzer', xsize=1000, ysize=500, number=1)
        self.plot.set_device(self.io_device)
        self.plot.set_realtime()

    """
    LPCアナライザーの起動メソッド
    pyqtgraphを用いているため，生波形ビューアとの併用は難しいです
    """
    def start_lpc_analyzer(self):
        if not self.setting_window.device_manager.get_device_status():
            self.set_warning("デバイスが見つからないよ")
            return False
        self.plot = LPCAnalyzer(graphname='LPC Analyzer', xsize=1000, ysize=500, number=1)
        self.plot.set_device(self.io_device)
        self.plot.set_realtime()

    """
    レコーダー
    """
    def start_recoder(self):
        if not self.setting_window.device_manager.get_device_status():
            self.set_warning("デバイスが見つからないよ")
            return False
        self.recoder_window = RecordWindow(self.parent(), self.io_device)
        self.recoder_window.show()

    """
    力覚センサのツールウィンドウ起動メソッド
    このメソッドを呼び出し後はself.force()にて力覚センサの値を取得できる様になります.
    """
    def start_cfs_gui(self):
        self.cfs_window = ContactForceMain()
        self.cfs_window.show()

    """
    以下は実験用のテストメソッドです
    ご自由にお使いください．
    """
    def start_exp1(self):
        if not self.cfs_window:  # 力覚センサのデータを使うためインスタンスチェック
            self.start_cfs_gui()
        if not self.setting_window.device_manager.get_device_status():
            self.set_warning("デバイスが見つからないよ")
            self.device_manager.show()
            return False
        self.svm_window = SvmToolWindowFFT()
        self.svm_window.set_device(self.io_device)
        self.svm_window.set_force(self.cfs_window)
        self.svm_window.show()

    def start_exp2(self):
        if not self.cfs_window:  # 力覚センサのデータを使うためインスタンスチェック
            self.start_cfs_gui()
        if not self.setting_window.device_manager.get_device_status():
            self.set_warning("デバイスが見つからないよ")
            self.device_manager.show()
            return False
        self.ml = ContactForceForSVR(parent=self.parent(),
                                     device=self.io_device,
                                     force=self.cfs_window)
        self.ml.show()

    def start_exp3(self):
        if not self.setting_window.device_manager.get_device_status():
            self.set_warning("デバイスが見つからないよ")
            self.device_manager.show()
            return False
        self.ml = GripStrengthForEnsemble(parent=self.parent(),
                                          device=self.io_device)
        self.ml.show()

    def set_warning(self, str):
        warnig_str = '<div align="center">(´･ω･`)＜ '
        warnig_str += str
        warnig_str += '</div>'
        self.warning_label.setText(warnig_str)
        self.warning_timer = QTimer()
        self.warning_timer.timeout.connect(self.clear_warning)
        self.warning_timer.start(2000)

    def clear_warning(self):
        self.warning_label.setText("")
        self.warning_timer.disconnect()
        self.warning_timer = None

    def hideEvent(self, a0: QtGui.QHideEvent):
        quit()

    def __del__(self):
        for key, device in self.io_device.items():
            device.closeDevice()

if __name__ == "__main__":
    myApp = QApplication(sys.argv)
    myWindow = MainWindow()
    myWindow.show()
    myApp.exec_()
    sys.exit(0)
